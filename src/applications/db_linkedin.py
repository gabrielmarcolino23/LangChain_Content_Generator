from typing import List, Dict
from ..db.linkedin_inspiration_db import InspirationDB
from ..db.linkedin_db import GeneratedDB

class DBApplication:
    def __init__(self):
        self.inspiration_db = InspirationDB()
        self.generated_db = GeneratedDB()
    
    def save_inspiration(self, post: str, metadata: Dict) -> str:
        """Salva um post de inspiração no banco vetorial"""
        return self.inspiration_db.add_post(post, metadata)
    
    def find_similar_inspirations(self, topic: str, limit: int = 3) -> List[Dict]:
        """Busca posts de inspiração similares"""
        return self.inspiration_db.search_similar(topic, limit)
    
    def save_generated_post(self, post: Dict) -> int:
        """Salva um post gerado no banco relacional"""
        return self.generated_db.save_post(post)
    
    def get_generated_posts(self, limit: int = 10) -> List[Dict]:
        """Recupera posts gerados"""
        return self.generated_db.get_posts(limit)