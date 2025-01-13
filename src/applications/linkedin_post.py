from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from typing import List, Dict
import json
from ..config import Config

class LinkedInPostGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=Config.OPENAI_API_KEY)
        self.search_tool = TavilySearchResults(tavily_api_key=Config.TAVILY_API_KEY)
        self.output_parser = StrOutputParser()
        
        # Template para busca de temas atuais
        self.topic_template = """
        Baseado nas seguintes informações de pesquisa, identifique um tópico relevante 
        para um post do LinkedIn focado em {area_interesse}.
        
        Informações da pesquisa:
        {search_results}
        
        Retorne apenas o tópico identificado em uma frase curta.
        """
        
        # Template para geração do post
        self.post_template = """
        Crie um post para LinkedIn sobre o seguinte tópico: {topic}
        
        Use como inspiração a seguinte estrutura de post bem sucedido:
        {post_inspiration}
        
        O post deve:
        - Ter um gancho inicial forte
        - Incluir dados ou exemplos relevantes
        - Ter uma call-to-action clara
        - Usar emojis apropriadamente
        - Ter hashtags relevantes
        - Ter no máximo 1300 caracteres
        
        Post:
        """
        
        self.topic_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.topic_template),
            output_parser=self.output_parser
        )
        
        self.post_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.post_template),
            output_parser=self.output_parser
        )

    def search_current_topics(self, area_interesse: str) -> List[Dict]:
        """Busca tópicos atuais usando Tavily"""
        search_query = f"últimas notícias trends {area_interesse} 2024"
        results = self.search_tool.invoke({"query": search_query})
        return results
    
    def generate_topic(self, area_interesse: str) -> str:
        """Gera um tópico baseado nas pesquisas atuais"""
        search_results = self.search_current_topics(area_interesse)
        topic = self.topic_chain.invoke({
            "area_interesse": area_interesse,
            "search_results": json.dumps(search_results, ensure_ascii=False)
        })
        return topic.strip()
    
    def generate_post(self, topic: str, post_inspiration: str) -> str:
        """Gera um post do LinkedIn baseado no tópico e inspiração"""
        post = self.post_chain.invoke({
            "topic": topic,
            "post_inspiration": post_inspiration
        })
        return post.strip()
    
    def generate_complete_post(self, area_interesse: str, post_inspiration: str) -> Dict:
        """Pipeline completo de geração de post"""
        topic = self.generate_topic(area_interesse)
        post = self.generate_post(topic, post_inspiration)
        
        return {
            "topic": topic,
            "post": post,
            "area_interesse": area_interesse
        }