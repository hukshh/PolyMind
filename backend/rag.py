import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from typing import List

class RAGPipeline:
    def __init__(self):
        self.embeddings = PineconeEmbeddings(
            model="llama-text-embed-v2", 
            pinecone_api_key=os.getenv("PINECONE_API_KEY")
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    def ingest_pdf(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        # Add source info to metadata
        for chunk in chunks:
            chunk.metadata["source"] = f"Page {chunk.metadata.get('page', 'unknown')}"
            
        vectorstore = PineconeVectorStore.from_documents(
            chunks, 
            self.embeddings, 
            index_name=self.index_name
        )
        return vectorstore

    def ingest_url(self, url: str):
        loader = WebBaseLoader(url)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        for chunk in chunks:
            chunk.metadata["source"] = url
            
        vectorstore = PineconeVectorStore.from_documents(
            chunks, 
            self.embeddings, 
            index_name=self.index_name
        )
        return vectorstore

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
