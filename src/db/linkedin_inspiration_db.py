from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Optional
from ..config import Config
from ..utils.style_analyzer import StyleAnalyzer

class InspirationDB:
    def __init__(self):
        self.collection_name = "linkedin_inspirations"
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.style_analyzer = StyleAnalyzer(openai_api_key=Config.OPENAI_API_KEY)
        self.client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
        
        # Cria collection se não existir
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "content": VectorParams(size=1536, distance=Distance.COSINE),
                    "style": VectorParams(size=1536, distance=Distance.COSINE)
                }
            )
    
    def _get_style_embedding(self, style_analysis: Dict) -> List[float]:
        """Gera embedding para o estilo do post"""
        style_text = f"""
        Estrutura: {style_analysis['estrutura_comum']}
        Tom: {style_analysis['tom_predominante']}
        Padrões: {style_analysis['padroes_linguagem']}
        Engajamento: {style_analysis['elementos_engajamento']}
        """
        return self.embeddings.embed_query(style_text)

    async def add_post(self, post: str, metadata: Dict = None) -> str:
        """Adiciona um post de inspiração ao banco vetorial"""
        # Análise de estilo
        style_analysis = self.style_analyzer.analyze_post_style(post)
        
        # Gera embeddings
        content_vector = self.embeddings.embed_query(post)
        style_vector = self._get_style_embedding(style_analysis)
        
        # Prepara payload
        payload = {
            "text": post,
            "style_analysis": style_analysis
        }
        if metadata:
            payload.update(metadata)
        
        # Gera ID único
        point_id = str(self.client.count(collection_name=self.collection_name).count + 1)
        
        # Insere no Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector={
                        "content": content_vector,
                        "style": style_vector
                    },
                    payload=payload
                )
            ]
        )
        
        return point_id

    async def search_by_style(self, style_description: str, limit: int = 3) -> List[Dict]:
        """Busca posts com estilo similar"""
        style_vector = self.embeddings.embed_query(style_description)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=("style", style_vector),
            limit=limit
        )
        
        return [r.payload for r in results]

    async def get_random_style_inspirations(self, limit: int = 3) -> List[Dict]:
        """Retorna posts aleatórios para inspiração de estilo"""
        results = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )[0]
        
        return [point.payload for point in results]

    async def batch_add_posts(self, posts: List[Dict[str, str]]) -> List[str]:
        """Adiciona múltiplos posts em batch"""
        points = []
        point_ids = []
        
        for idx, post_data in enumerate(posts):
            post = post_data["text"]
            metadata = post_data.get("metadata", {})
            
            style_analysis = self.style_analyzer.analyze_post_style(post)
            content_vector = self.embeddings.embed_query(post)
            style_vector = self._get_style_embedding(style_analysis)
            
            point_id = str(self.client.count(collection_name=self.collection_name).count + idx + 1)
            point_ids.append(point_id)
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector={
                        "content": content_vector,
                        "style": style_vector
                    },
                    payload={
                        "text": post,
                        "style_analysis": style_analysis,
                        **metadata
                    }
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return point_ids