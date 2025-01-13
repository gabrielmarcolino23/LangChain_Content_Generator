from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from typing import List, Dict
import json

class StyleAnalyzer:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key)
        
        self.style_analysis_template = """
        Analise cuidadosamente o seguinte post do LinkedIn e extraia os elementos de estilo e tom de voz:

        POST DE REFERÊNCIA:
        {post}

        Por favor, analise e extraia:
        1. Estrutura do post (como o conteúdo está organizado)
        2. Tom de voz (formal, informal, motivacional, educativo, etc)
        3. Padrões de linguagem (uso de emojis, hashtags, formatação)
        4. Elementos de engajamento (perguntas, calls-to-action, etc)
        5. Comprimento médio dos parágrafos
        6. Técnicas de storytelling utilizadas

        Retorne a análise em formato JSON com estes elementos.
        """
        
        self.style_analysis_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.style_analysis_template)
        )
    
    def analyze_post_style(self, post: str) -> Dict:
        """Analisa o estilo de um post"""
        result = self.style_analysis_chain.invoke({"post": post})
        return json.loads(result['text'])
    
    def analyze_multiple_posts(self, posts: List[str]) -> Dict:
        """Analisa múltiplos posts e retorna um estilo consolidado"""
        analyses = [self.analyze_post_style(post) for post in posts]
        return self._consolidate_analyses(analyses)
    
    def _consolidate_analyses(self, analyses: List[Dict]) -> Dict:
        """Consolida múltiplas análises em um estilo único"""
        return {
            "estrutura_comum": self._find_common_structure(analyses),
            "tom_predominante": self._find_predominant_tone(analyses),
            "padroes_linguagem": self._aggregate_language_patterns(analyses),
            "elementos_engajamento": self._aggregate_engagement_elements(analyses)
        }
    
    def _find_common_structure(self, analyses: List[Dict]) -> str:
        # Implementar lógica para encontrar estrutura comum
        return analyses[0].get("estrutura", "")
    
    def _find_predominant_tone(self, analyses: List[Dict]) -> str:
        # Implementar lógica para encontrar tom predominante
        return analyses[0].get("tom_de_voz", "")
    
    def _aggregate_language_patterns(self, analyses: List[Dict]) -> List[str]:
        # Implementar lógica para agregar padrões de linguagem
        return analyses[0].get("padroes_linguagem", [])
    
    def _aggregate_engagement_elements(self, analyses: List[Dict]) -> List[str]:
        # Implementar lógica para agregar elementos de engajamento
        return analyses[0].get("elementos_engajamento", [])