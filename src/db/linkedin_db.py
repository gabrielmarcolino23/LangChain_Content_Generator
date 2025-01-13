from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Dict
from ..config import Config

Base = declarative_base()

class GeneratedPost(Base):
    __tablename__ = 'generated_posts'
    
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    content = Column(String)
    area_interesse = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class GeneratedDB:
    def __init__(self):
        self.engine = create_engine(Config.POSTGRES_URI)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_post(self, post_data: Dict) -> int:
        """Salva um post gerado no banco de dados"""
        session = self.Session()
        
        post = GeneratedPost(
            topic=post_data["topic"],
            content=post_data["post"],
            area_interesse=post_data["area_interesse"],
            metadata=post_data.get("metadata", {})
        )
        
        session.add(post)
        session.commit()
        post_id = post.id
        session.close()
        
        return post_id
    
    def get_posts(self, limit: int = 10) -> List[Dict]:
        """Recupera posts gerados do banco de dados"""
        session = self.Session()
        posts = session.query(GeneratedPost).order_by(
            GeneratedPost.created_at.desc()
        ).limit(limit).all()
        
        results = [{
            "id": post.id,
            "topic": post.topic,
            "content": post.content,
            "area_interesse": post.area_interesse,
            "metadata": post.metadata,
            "created_at": post.created_at.isoformat()
        } for post in posts]
        
        session.close()
        return results