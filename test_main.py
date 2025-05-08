import unittest
from main import create_site_crew, briefing_agent, html_agent
from unittest.mock import patch, MagicMock

class TestSiteGenerator(unittest.TestCase):
    def setUp(self):
        self.test_description = """Site institucional para uma empresa de tecnologia.
        Precisa ter: header com logo, menu de navegação,
        seção principal com destaque, sobre nós, serviços e contato."""

    @patch('streamlit.progress')
    @patch('streamlit.empty')
    def test_create_site_crew(self, mock_empty, mock_progress):
        # Mock dos objetos do Streamlit
        mock_progress.return_value = MagicMock()
        mock_empty.return_value = MagicMock()

        # Executa a função
        briefing, html = create_site_crew(self.test_description)

        # Verifica se os resultados não são vazios
        self.assertIsNotNone(briefing)
        self.assertIsNotNone(html)
        self.assertIsInstance(briefing, str)
        self.assertIsInstance(html, str)

    def test_briefing_agent(self):
        # Testa a configuração do agente de briefing
        self.assertEqual(briefing_agent.role, "Especialista em Briefing")
        self.assertTrue(len(briefing_agent.goal) > 0)
        self.assertTrue(len(briefing_agent.backstory) > 0)

    def test_html_agent(self):
        # Testa a configuração do agente HTML
        self.assertEqual(html_agent.role, "Desenvolvedor Frontend")
        self.assertTrue(len(html_agent.goal) > 0)
        self.assertTrue(len(html_agent.backstory) > 0)

if __name__ == '__main__':
    unittest.main()