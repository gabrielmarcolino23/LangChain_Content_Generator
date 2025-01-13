from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TAVI_API_KEY = os.getenv('TAVI_API_KEY')
    POSTGRES_URL = os.getenv('POSTGRES_URL')
    QDRANT_HOST = os.getenv('QDRANT_HOST',"localhost")
    QDRANT_PORT = os.getenv('QDRANT_PORT',6333)

