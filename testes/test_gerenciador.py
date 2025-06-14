import unittest
from datetime import date
from modelo.projeto import Projeto
from modelo.membro import Membro
from modelo.gerenciador import GerenciadorProjetos
from modelo.excecoes import (
    ProjetoNaoEncontradoError,
    MembroNaoEncontradoError,
    ResponsavelNaoEMembroError,
    TarefaNaoEncontradaError
)

class TestGerenciadorProjetos(unittest.TestCase):
    """Testes para a classe GerenciadorProjetos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.gerenciador = GerenciadorProjetos()
        self.projeto = Projeto(
            nome="Portal Corporativo",
            descricao="Desenvolvimento do portal",
            prazo=date(2023, 11, 30)
        )
        self.membro = Membro("Fernanda Rocha", "UX Designer", "fernanda@empresa.com")
        
        self.gerenciador.adicionar_projeto(self.projeto)
        self.gerenciador.cadastrar_membro(self.membro)
    
    def test_adicionar_projeto(self):
        """Testa a adição de um novo projeto"""
        projetos = self.gerenciador.projetos
        self.assertEqual(len(projetos), 1)
        self.assertIn(self.projeto, projetos)
    
    def test_cadastrar_membro(self):
        """Testa o cadastro de um novo membro"""
        membros = self.gerenciador.membros
        self.assertEqual(len(membros), 1)
        self.assertIn(self.membro, membros)
    
    def test_criar_tarefa_valida(self):
        """Testa a criação de uma tarefa válida"""
        self.gerenciador.adicionar_membro_projeto("Portal Corporativo", "Fernanda Rocha")
        tarefa = self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "Design Homepage",
            "Layout da página principal",
            "Fernanda Rocha",
            prioridade=1
        )
        
        self.assertEqual(tarefa.titulo, "Design Homepage")
        self.assertEqual(len(self.gerenciador.tarefas), 1)
    
    def test_criar_tarefa_com_responsavel_nao_membro(self):
        """Testa tentativa de criar tarefa com responsável não membro"""
        with self.assertRaises(ResponsavelNaoEMembroError):
            self.gerenciador.criar_tarefa(
                "Portal Corporativo",
                "Tarefa Inválida",
                "Descrição",
                "Fernanda Rocha"
            )
    
    def test_concluir_tarefa(self):
        """Testa a conclusão de uma tarefa"""
        self.gerenciador.adicionar_membro_projeto("Portal Corporativo", "Fernanda Rocha")
        self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "Tarefa para Concluir",
            "Descrição",
            "Fernanda Rocha"
        )
        
        self.gerenciador.concluir_tarefa("Portal Corporativo", "Tarefa para Concluir")
        tarefas = self.gerenciador.tarefas
        self.assertEqual(tarefas[0].status, "concluída")
    
    def test_relatorios(self):
        """Testa a geração de relatórios"""
        self.gerenciador.adicionar_membro_projeto("Portal Corporativo", "Fernanda Rocha")
        self.gerenciador.criar_tarefa(
            "Portal Corporativo",
            "Tarefa Relatório",
            "Descrição",
            "Fernanda Rocha"
        )
        
        rel_projeto = self.gerenciador.relatorio_projeto("Portal Corporativo")
        rel_membro = self.gerenciador.relatorio_membro("Fernanda Rocha")
        
        self.assertEqual(rel_projeto["total_tarefas"], 1)
        self.assertEqual(rel_membro["total_tarefas"], 1)

if __name__ == '__main__':
    unittest.main()