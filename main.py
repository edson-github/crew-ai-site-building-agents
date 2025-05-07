from crewai import Agent, Task, Crew
import streamlit as st
from typing import Tuple

# Definição dos agentes
briefing_agent = Agent(
    name="BriefingAgent",
    role="Especialista em Briefing",
    goal="Criar briefings de projetos web detalhados",
    backstory="Sou um especialista em análise de requisitos e criação de briefings para projetos web, com vasta experiência em transformar ideias em documentos estruturados."
)

html_agent = Agent(
    name="HTMLAgent",
    role="Desenvolvedor Frontend",
    goal="Criar estruturas HTML com base em briefings",
    backstory="Sou um desenvolvedor frontend especializado em criar estruturas HTML semânticas e bem organizadas, seguindo as melhores práticas de desenvolvimento web."
)

def create_site_crew(project_description: str) -> Tuple[str, str]:
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Tarefa 1: Gerar Briefing
    status_text.text("Gerando briefing...")
    briefing_task = Task(
        description=f"""
        Analise a seguinte descrição de projeto e crie um briefing detalhado:
        {project_description}
        
        O briefing deve incluir:
        1. Objetivos do projeto
        2. Público-alvo
        3. Funcionalidades principais
        4. Requisitos técnicos
        5. Estrutura de navegação
        """,
        agent=briefing_agent,
        expected_output="Um briefing detalhado do projeto contendo objetivos, público-alvo, funcionalidades e requisitos técnicos"
    )
    progress_bar.progress(33)

    # Tarefa 2: Gerar HTML
    status_text.text("Gerando estrutura HTML...")
    html_task = Task(
        description="""
        Com base no briefing gerado, crie uma estrutura HTML completa e semântica com design profissional.
        
        Requisitos:
        1. Use HTML5 semântico e CSS moderno
        2. Inclua comentários explicativos
        3. Estruture o código de forma organizada
        4. Adicione estilos CSS inline usando variáveis:
           - Defina variáveis CSS no :root:
             --primary-color: #0056b3
             --secondary-color: #28a745
             --accent-color: #ffcc00
             --text-color: #333
             --bg-light: #f8f9fa

        5. Estilização profissional:
           - Fonte: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
           - Header com gradiente: linear-gradient(135deg, var(--primary-color), #003366)
           - Layout responsivo com max-width: 1200px
           - Cards com sombras e hover effects
           - Botões com gradientes e animações
           - Formulários estilizados com transições
           - Grid system para serviços
           - Espaçamento consistente (8px grid)

        6. Animações e interações:
           - Fade-in nas seções usando keyframes
           - Transições suaves (0.3s ease)
           - Efeitos hover com transform
           - Micro-interações em elementos clicáveis
           - Animação de pulse em botões
           
        7. Responsividade:
           - Media queries para mobile
           - Layout flexível
           - Tipografia responsiva
           - Navegação adaptativa

        8. Elementos visuais:
           - Gradientes em títulos
           - Sombras sutis em cards
           - Bordas arredondadas
           - Efeitos de elevação
           - Feedback visual em interações

        Importante: Todo o CSS deve ser incluído na tag <style> do documento.
        """,
        agent=html_agent,
        expected_output="Código HTML semântico e bem estruturado com design profissional",
        context=[briefing_task]
    )
    progress_bar.progress(66)

    crew = Crew(
        agents=[briefing_agent, html_agent],
        tasks=[briefing_task, html_task],
        verbose=True
    )

    try:
        crew.kickoff()
        progress_bar.progress(100)
        status_text.text("Processo concluído!")
        
        # Extrai os resultados das tarefas
        briefing_output = briefing_task.output.raw
        html_output = html_task.output.raw
        
        return briefing_output, html_output
    except Exception as e:
        st.error(f"Erro ao gerar o site: {str(e)}")
        return "", ""

# Interface Streamlit
st.set_page_config(page_title="Gerador de Sites com CrewAI", layout="wide")
st.title("🧠 Gerador de Sites com Agentes de IA (CrewAI)")

st.markdown("""
### Como funciona?
1. Descreva seu projeto de site abaixo
2. Os agentes de IA irão:
   - Gerar um briefing detalhado
   - Criar a estrutura HTML inicial
""")

projeto_descricao = st.text_area(
    "Descrição do Projeto",
    """Site institucional para uma empresa de tecnologia.
    Precisa ter: header com logo, menu de navegação,
    seção principal com destaque, sobre nós, serviços e contato.""",
    height=150
)

if st.button("Gerar Site"):
    with st.spinner("Executando agentes e gerando resultados..."):
        briefing, html = create_site_crew(projeto_descricao)
        
        if briefing and html:
            tab1, tab2, tab3 = st.tabs(["📋 Briefing", "💻 Código HTML", "👀 Visualizar Site"])
            
            with tab1:
                st.subheader("Briefing Gerado")
                st.markdown(briefing)
            
            with tab2:
                st.subheader("Código HTML Gerado")
                st.code(html, language="html")
                
                st.download_button(
                    label="⬇️ Download HTML",
                    data=html,
                    file_name="site.html",
                    mime="text/html"
                )
            
            with tab3:
                st.subheader("Prévia do Site")
                # Adiciona CSS para melhorar a visualização no Streamlit
                st.markdown("""
                    <style>
                        iframe {
                            width: 100%;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        }
                    </style>
                """, unsafe_allow_html=True)
                st.components.v1.html(html, height=800, scrolling=True)