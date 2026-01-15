import os
import faiss
import pickle
import numpy as np
from django.conf import settings
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
from rank_bm25 import BM25Okapi
from ..models import InteractionLog

class RAGService:
    def __init__(self):
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.model_id = "meta-llama/Llama-3.2-3B-Instruct"
        self.client = InferenceClient(api_key=settings.HUGGINGFACE_API_KEY)
        
        self.index_path = os.path.join(settings.FAISS_INDEX_PATH, 'index.faiss')
        self.chunks_path = os.path.join(settings.FAISS_INDEX_PATH, 'chunks.txt')
        self.bm25_path = os.path.join(settings.FAISS_INDEX_PATH, 'bm25_corpus.pkl')

    def load_index_and_chunks(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.bm25_path):
            raise FileNotFoundError("Hybrid index not found. Please run ingest_kb management command.")
        
        index = faiss.read_index(self.index_path)
        with open(self.chunks_path, 'r', encoding='utf-8') as f:
            chunks = f.readlines()
            
        with open(self.bm25_path, 'rb') as f:
            tokenized_corpus = pickle.load(f)
            bm25 = BM25Okapi(tokenized_corpus)
            
        return index, chunks, bm25

    def retrieve_context(self, question, top_k=5):
        index, chunks, bm25 = self.load_index_and_chunks()
        
        # 1. Vector Search (Semantic)
        q_embedding = self.embed_model.encode([question])
        q_embedding = np.array(q_embedding).astype('float32')
        v_distances, v_indices = index.search(q_embedding, top_k * 2) # Get more for fusion
        
        # 2. BM25 Search (Keyword)
        tokenized_query = question.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)
        b_indices = np.argsort(bm25_scores)[::-1][:top_k * 2]
        
        # 3. Reciprocal Rank Fusion (RRF)
        # Score(d) = sum( 1 / (k + rank(d)) )
        rrf_scores = {}
        k = 60 # RRF constant
        
        # Add vector results to scores
        for rank, idx in enumerate(v_indices[0]):
            if idx not in rrf_scores: rrf_scores[idx] = 0
            rrf_scores[idx] += 1 / (k + rank + 1)
            
        # Add BM25 results to scores
        for rank, idx in enumerate(b_indices):
            if idx not in rrf_scores: rrf_scores[idx] = 0
            rrf_scores[idx] += 1 / (k + rank + 1)
            
        # Sort indices by fused score
        fused_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        
        relevant_chunks = []
        sources = []
        for idx in fused_indices:
            if idx < len(chunks):
                chunk = chunks[idx]
                relevant_chunks.append(chunk)
                if "[Source:" in chunk:
                    source_info = chunk.split("[Source:")[-1].split("]")[0].strip()
                    sources.append(source_info)
        
        return "\n".join(relevant_chunks), list(set(sources))

    def ask_llm(self, question, context):
        if not settings.HUGGINGFACE_API_KEY:
             return "HuggingFace API Key is missing. Please add it to your .env file.", []

        prompt = f"Use the following context to answer the question. If you don't know the answer based on the context, say you don't know. Avoid hallucinations.\n\nContext: {context}\n\nQuestion: {question}"
        
        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful science teacher. Use the provided context to answer questions accurately."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model_id,
                max_tokens=300,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error querying LLM: {str(e)}"

    def handle_query(self, question):
        context, sources = self.retrieve_context(question)
        answer = self.ask_llm(question, context)
        
        # Log to DB
        InteractionLog.objects.create(
            question=question,
            answer=answer,
            sources=sources
        )
        
        return answer, sources
