from datetime import date, timedelta
import unittest
from modelo.gerenciador import GerenciadorProjetos
from modelo.projeto import Projeto
from modelo.membro import Membro

class TestIntegracaoGerenciador(unittest.TestCase):
    """Testes de integração do sistema completo"""
    
    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.gerenciador = GerenciadorProjetos()
        
        # Cria membros
        self.dev = Membro("Carlos Silva", "Desenvolvedor", "carlos@empresa.com")
        self.designer = Membro("Ana Costa", "Designer", "ana@empresa.com")
        self.gerente = Membro("Maria Santos", "Gerente de Projeto", "maria@empresa.com")
        
        # Cadastra membros
        self.gerenciador.cadastrar_membro(self.dev)
        self.gerenciador.cadastrar_membro(self.designer)
        self.gerenciador.cadastrar_membro(self.gerente)
        
        # Cria projeto
        self.projeto = Projeto(
            "Portal Corporativo",
            "Desenvolvimento do novo portal da empresa",
            date.today() + timedelta(days=30)
        )    
        
        # Adiciona projeto ao gerenciador
        self.gerenciador.adicionar_projeto(self.projeto)
        
        # Adiciona membros ao projeto
        self.gerenciador.adicionar_membro_projeto("Portal Corporativo", "Carlos Silva")
        self.gerenciador.adicionar_membro_projeto("Portal Corporativo", "Ana Costa")
    
    def test_fluxo_completo_projeto(self):
        """Testa um fluxo completo de gerenciamento de projeto"""
        # Cria tarefas
        tarefa_dev = self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "API de Autenticação",
            "Desenvolver endpoints de autenticação JWT",
            "Carlos Silva",
            prazo=date.today() + timedelta(days=15),
            prioridade=3
        )
        
        tarefa_design = self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "Design Homepage",
            "Criar layout moderno para a página inicial",
            "Ana Costa",
            prazo=date.today() + timedelta(days=7),
            prioridade=2
        )
        
        # Verifica estado inicial
        relatorio = self.gerenciador.relatorio_projeto("Portal Corporativo")
        self.assertEqual(relatorio["total_tarefas"], 2)
        self.assertEqual(relatorio["tarefas_pendentes"], 2)
        
        # Conclui uma tarefa
        self.gerenciador.concluir_tarefa("Portal Corporativo", "Design Homepage")
        
        # Verifica estado após conclusão
        relatorio = self.gerenciador.relatorio_projeto("Portal Corporativo")
        self.assertEqual(relatorio["tarefas_pendentes"], 1)
        self.assertEqual(relatorio["tarefas_concluidas"], 1)
        
        # Verifica relatório do membro
        relatorio_ana = self.gerenciador.relatorio_membro("Ana Costa")
        self.assertEqual(relatorio_ana["tarefas_concluidas"], 1)
        self.assertEqual(relatorio_ana["total_tarefas"], 1)
    
    def test_tarefa_atrasada(self):
        """Testa o fluxo de tarefa atrasada"""
        # Cria tarefa com prazo no passado
        tarefa_atrasada = self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "Configurar Servidor",
            "Configurar ambiente de produção",
            "Carlos Silva",
            prazo=date.today() - timedelta(days=1),
            prioridade=4
        )
        
        # Verifica se está marcada como atrasada
        relatorio = self.gerenciador.relatorio_projeto("Portal Corporativo")
        self.assertEqual(relatorio["tarefas_atrasadas"], 1)
        
        # Verifica no relatório do membro
        relatorio_carlos = self.gerenciador.relatorio_membro("Carlos Silva")
        self.assertEqual(relatorio_carlos["tarefas_atrasadas"], 1)
    
    def test_adicionar_responsavel_nao_membro(self):
        """Testa tentativa de atribuir tarefa a não membro"""
        with self.assertRaises(Exception) as context:
            self.gerenciador.criar_tarefa(
                "Portal Corporativo",
                "Tarefa Inválida",
                "Não deveria ser criada",
                "Maria Santos"  # Maria não foi adicionada ao projeto
            )
        
        self.assertIn("Responsável 'Maria Santos' não é membro do projeto", str(context.exception))

if __name__ == '__main__':
    unittest.main()