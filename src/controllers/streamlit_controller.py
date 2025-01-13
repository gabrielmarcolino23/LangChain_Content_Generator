import streamlit as st
from ..applications.post_app import LinkedInPostGenerator
from ..applications.db_app import DBApplication

class StreamlitController:
    def __init__(self):
        self.post_generator = LinkedInPostGenerator()
        self.db_app = DBApplication()
    
    def render_post_generator(self):
        st.title("Gerador de Posts para LinkedIn")
        
        # Input da área de interesse
        area_interesse = st.text_input("Área de Interesse", "tecnologia")
        
        # Opção de usar inspiração específica
        use_specific_inspiration = st.checkbox("Usar inspiração específica")
        
        if use_specific_inspiration:
            inspiration_id = st.text_input("ID da Inspiração")
            inspiration = self.db_app.find_similar_inspirations(inspiration_id, limit=1)
            post_inspiration = inspiration[0]["text"] if inspiration else None
        else:
            # Busca inspirações similares
            similar_posts = self.db_app.find_similar_inspirations(area_interesse)
            post_inspiration = similar_posts[0]["text"] if similar_posts else None
        
        if st.button("Gerar Post"):
            with st.spinner("Gerando post..."):
                result = self.post_generator.generate_complete_post(
                    area_interesse,
                    post_inspiration
                )
                
                # Salva o post gerado
                post_id = self.db_app.save_generated_post(result)
                
                # Exibe resultado
                st.subheader("Post Gerado")
                st.write(f"Tópico: {result['topic']}")
                st.text_area("Conteúdo", result["post"], height=300)
                st.success(f"Post gerado e salvo com ID: {post_id}")
        
        # Exibe posts recentes
        st.subheader("Posts Recentes")
        recent_posts = self.db_app.get_generated_posts(limit=5)
        for post in recent_posts:
            with st.expander(f"Post: {post['topic']}"):
                st.write(post["content"])
                st.write(f"Área: {post['area_interesse']}")
                st.write(f"Data: {post['created_at']}")
