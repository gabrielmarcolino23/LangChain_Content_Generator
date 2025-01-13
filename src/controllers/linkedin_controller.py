from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from ..applications.post_app import LinkedInPostGenerator
from ..applications.db_app import DBApplication

app = FastAPI()
post_generator = LinkedInPostGenerator()
db_app = DBApplication()

class PostRequest(BaseModel):
    area_interesse: str
    inspiration_id: str = None

class PostResponse(BaseModel):
    topic: str
    post: str
    area_interesse: str

@app.post("/generate", response_model=PostResponse)
async def generate_post(request: PostRequest):
    try:
        # Busca inspiração se ID fornecido
        if request.inspiration_id:
            inspiration = db_app.find_similar_inspirations(request.inspiration_id, limit=1)
            post_inspiration = inspiration[0]["text"] if inspiration else None
        else:
            # Busca inspiração similar ao tema
            similar_posts = db_app.find_similar_inspirations(request.area_interesse)
            post_inspiration = similar_posts[0]["text"] if similar_posts else None
        
        # Gera post
        result = post_generator.generate_complete_post(
            request.area_interesse,
            post_inspiration
        )
        
        # Salva post gerado
        db_app.save_generated_post(result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))