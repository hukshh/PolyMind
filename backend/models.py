from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    response = Column(String)
    response_time = Column(Float)  # in seconds
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    source_type = Column(String)  # 'pdf' or 'url'
