import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from typing import List
from pinecone import Pinecone

class RAGPipeline:
    def __init__(self):
        self.embeddings = PineconeEmbeddings(
            model="llama-text-embed-v2", 
            pinecone_api_key=os.getenv("PINECONE_API_KEY")
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index(self.index_name)

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
