import unittest
from datetime import date
from modelo.projeto import Projeto
from modelo.membro import Membro
from modelo.tarefa import Tarefa

class TestProjeto(unittest.TestCase):
    def setUp(self):
        self.projeto = Projeto(
            nome="Sistema de Vendas",
            descricao="Desenvolvimento do novo sistema de vendas",
            prazo=date(2023, 12, 31)  # Prazo no passado para testar atraso
        )

    def test_criacao_projeto(self):
        """Testa a criação correta de um projeto"""
        self.assertEqual(self.projeto.nome, "Sistema de Vendas")
        self.assertEqual(self.projeto.descricao, "Desenvolvimento do novo sistema de vendas")
        self.assertEqual(len(self.projeto.membros), 0)
        self.assertEqual(len(self.projeto.tarefas), 0)

    def test_adicionar_membro(self):
        """Testa a adição de um membro ao projeto"""
        membro = Membro("Ana", "Gerente")
        self.projeto.adicionar_membro(membro)
        self.assertEqual(len(self.projeto.membros), 1)
        self.assertIn(membro, self.projeto.membros)

    def test_adicionar_tarefa(self):
        """Testa a adição de uma tarefa ao projeto"""
        membro = Membro("Carlos", "Dev")
        self.projeto.adicionar_membro(membro)
        tarefa = Tarefa(
            titulo="Criar banco de dados",
            descricao="Montar estrutura inicial",
            responsavel=membro,
            prazo=date(2024, 12, 31),
            prioridade=2
        )
        self.projeto.adicionar_tarefa(tarefa)
        self.assertEqual(len(self.projeto.tarefas), 1)
        self.assertIn(tarefa, self.projeto.tarefas)

    def test_relatorio_projeto(self):
        """Testa o método de geração de relatório do projeto"""
        membro = Membro("João", "Tester")
        self.projeto.adicionar_membro(membro)
        tarefa = self.projeto.criar_tarefa(
            titulo="Testar login",
            descricao="Testes unitários",
            responsavel=membro,
            prazo=date(2023, 12, 15),
            prioridade=3
        )
        relatorio = self.projeto.relatorio_projeto()
        self.assertEqual(relatorio["total_membros"], 1)
        self.assertEqual(relatorio["total_tarefas"], 1)
        self.assertEqual(relatorio["tarefas_pendentes"], 1)

    def test_representacao_string(self):
        """Testa a representação __str__ de Projeto"""
        resultado = str(self.projeto)
        self.assertIn("Projeto: Sistema de Vendas", resultado)
        self.assertIn("Descrição: Desenvolvimento do novo sistema de vendas", resultado)
        self.assertIn("Prazo: 31/12/2023", resultado)
        self.assertIn("Membros: 0", resultado)
        self.assertIn("Tarefas: 0", resultado)

