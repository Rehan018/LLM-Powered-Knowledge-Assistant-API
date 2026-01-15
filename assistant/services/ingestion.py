"""
Knowledge Base Ingestion Service.

This service handles the heavy lifting of preparing our data aka the "ETL" process.

It basically does three things:
1. Extract: It reads the raw PDF files from our data folder.
2. Transform: It cleans up the text and chops it into smaller pieces called "chunks". This is crucial because our AI model has a limit on how much text it can read at once. It then turns these chunks into mathematical vectors (embeddings).
3. Load: Finally, it saves these vectors into a FAISS index (for fast searching) and a BM25 index (for keyword matching).

We usually run this once when we add new documents, so the main API can stay fast and lightweight.
"""

import os
import PyPDF2
import faiss
import pickle
import numpy as np
from django.conf import settings
from sentence_transformers import SentenceTransformer
from ..models import KnowledgeDocument

class IngestionService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def parse_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + f"\n[Source: {os.path.basename(file_path)} - Page {page_num + 1}]\n"
        return text

    def chunk_text(self, text):
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i:i + self.chunk_size])
        return chunks

    def process_knowledge_base(self):
        all_chunks = []
        
        # Ensure index directory exists
        if not os.path.exists(settings.FAISS_INDEX_PATH):
            os.makedirs(settings.FAISS_INDEX_PATH)

        pdf_files = [f for f in os.listdir(settings.KNOWLEDGE_BASE_PATH) if f.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            file_path = os.path.join(settings.KNOWLEDGE_BASE_PATH, pdf_file)
            print(f"Processing {pdf_file}...")
            
            text = self.parse_pdf(file_path)
            chunks = self.chunk_text(text)
            all_chunks.extend(chunks)
            
            # Track document in DB
            KnowledgeDocument.objects.get_or_create(
                file_name=pdf_file,
                file_path=file_path,
                defaults={'is_processed': True}
            )

        if not all_chunks:
            return "No text found in PDFs."

        # Generate Embeddings
        embeddings = self.model.encode(all_chunks)
        embeddings = np.array(embeddings).astype('float32')

        # Initialize FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # Save index and chunks (meta)
        faiss.write_index(index, os.path.join(settings.FAISS_INDEX_PATH, 'index.faiss'))
        
        # Save tokenized chunks for BM25
        tokenized_corpus = [doc.lower().split() for doc in all_chunks]
        with open(os.path.join(settings.FAISS_INDEX_PATH, 'bm25_corpus.pkl'), 'wb') as f:
            pickle.dump(tokenized_corpus, f)

        with open(os.path.join(settings.FAISS_INDEX_PATH, 'chunks.txt'), 'w', encoding='utf-8') as f:
            for chunk in all_chunks:
                f.write(chunk.replace('\n', ' ') + '\n')

        return f"Processed {len(pdf_files)} files into {len(all_chunks)} chunks with Hybrid Indexing."
