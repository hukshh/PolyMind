import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from typing import List
from pinecone import Pinecone

class RAGPipeline:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if not api_key:
            print("ERROR: PINECONE_API_KEY is missing!")
        if not self.index_name:
            print("ERROR: PINECONE_INDEX_NAME is missing!")

        self.embeddings = PineconeEmbeddings(
            model="llama-text-embed-v2", 
            pinecone_api_key=api_key
        )
        # Verify if embeddings are actually working for this model
        try:
            test_embed = self.embeddings.embed_query("test")
            print(f"DEBUG: PineconeEmbeddings initialized successfully (Dim: {len(test_embed)})")
        except Exception as e:
            print(f"WARNING: PineconeEmbeddings failed for llama-text-embed-v2: {e}. Index might be Inference-only or SDK version mismatch.")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.pc = Pinecone(api_key=api_key)
        
        if self.index_name:
            try:
                self.index = self.pc.Index(self.index_name)
                # Check dimensions to help user diagnose 502/crashes
                desc = self.index.describe_index_stats()
                self.index_dimension = desc.get('dimension')
                print(f"DEBUG: Connected to Pinecone index '{self.index_name}' (Dimension: {self.index_dimension})")
                
                # llama-text-embed-v2 typically uses 1024 or 768
                if self.index_dimension not in [768, 1024]:
                    print(f"WARNING: Index dimension {self.index_dimension} might not match llama-text-embed-v2!")
            except Exception as e:
                print(f"ERROR: Could not connect to Pinecone index '{self.index_name}': {e}")
                self.index = None
                self.index_dimension = None
        else:
            self.index = None
            self.index_dimension = None

    def ingest_pdf(self, file_path: str):
        print(f"DEBUG: Starting PDF ingestion: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"DEBUG: Loaded {len(documents)} pages. Splitting...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"DEBUG: Created {len(chunks)} chunks. Adding metadata...")
        
        # Add source info to metadata
        for chunk in chunks:
            chunk.metadata["source"] = f"Page {chunk.metadata.get('page', 'unknown')}"
            chunk.metadata["source_name"] = os.path.basename(file_path)
            
        if not chunks:
            print("DEBUG: No text chunks found in PDF. Ingestion skipped.")
            return None

        print(f"DEBUG: Starting Pinecone upsert for {len(chunks)} chunks to index '{self.index_name}'...")
        try:
            vectorstore = PineconeVectorStore.from_documents(
                chunks, 
                self.embeddings, 
                index_name=self.index_name
            )
            print("DEBUG: Successfully upserted to Pinecone!")
            return vectorstore
        except Exception as e:
            print(f"CRITICAL Pinecone ERROR: {e}")
            raise e

    def ingest_url(self, url: str):
        print(f"DEBUG: Starting URL ingestion: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()
        print(f"DEBUG: Loaded URL content. Splitting...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"DEBUG: Created {len(chunks)} chunks. Adding metadata...")
        
        for chunk in chunks:
            chunk.metadata["source"] = url
            chunk.metadata["source_name"] = url
            
        print(f"DEBUG: Starting Pinecone upsert for {len(chunks)} chunks...")
        try:
            vectorstore = PineconeVectorStore.from_documents(
                chunks, 
                self.embeddings, 
                index_name=self.index_name
            )
            print("DEBUG: Successfully upserted to Pinecone!")
            return vectorstore
        except Exception as e:
            print(f"DEBUG: Pinecone ERROR: {e}")
            raise e

    def get_retriever(self):
        vectorstore = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": 5})

    def search(self, query: str):
        retriever = self.get_retriever()
        try:
            docs = retriever.invoke(query)
            return docs
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def delete_source(self, source_name: str):
        try:
            self.index.delete(filter={"source_name": source_name})
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

    def clear_all(self):
        try:
            self.index.delete(delete_all=True)
            return True
        except Exception as e:
            print(f"Clear All error: {e}")
            return False
