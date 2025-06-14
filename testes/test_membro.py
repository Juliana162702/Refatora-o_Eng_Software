import unittest
from datetime import date
from modelo.membro import Membro
from modelo.tarefa import Tarefa

class TestMembro(unittest.TestCase):
    """Testes para a classe Membro"""

    def setUp(self):
        """Cria um membro limpo para cada teste"""
        self.membro = Membro("João Silva", "Desenvolvedor", "joao@empresa.com")

    def test_criacao_membro(self):
        """Testa a criação correta de um membro sem tarefas atribuídas"""
        self.assertEqual(self.membro.nome, "João Silva")
        self.assertEqual(self.membro.funcao, "Desenvolvedor")
        self.assertEqual(self.membro.email, "joao@empresa.com")
        self.assertEqual(len(self.membro.tarefas_atribuidas), 0)

    def test_adicionar_tarefa(self):
        """Testa a adição de uma tarefa ao membro"""
        tarefa = Tarefa(
            titulo="Implementar login",
            descricao="Criar sistema de autenticação",
            responsavel=self.membro,
            prazo=date(2023, 12, 31),
            prioridade=3
        )
        self.assertEqual(len(self.membro.tarefas_atribuidas), 1)
        self.assertIn(tarefa, self.membro.tarefas_atribuidas)

    def test_remover_tarefa(self):
        """Testa a remoção de uma tarefa do membro"""
        tarefa = Tarefa(
            titulo="Implementar login",
            descricao="Criar sistema de autenticação",
            responsavel=self.membro,
            prazo=date(2023, 12, 31),
            prioridade=3
        )
        self.membro.remover_tarefa(tarefa)
        self.assertEqual(len(self.membro.tarefas_atribuidas), 0)

    def test_representacao_string(self):
        """Testa as representações __str__ e __repr__"""
        self.assertEqual(str(self.membro), "João Silva (Desenvolvedor) - joao@empresa.com")
        self.assertEqual(repr(self.membro), "Membro(nome='João Silva', funcao='Desenvolvedor', email='joao@empresa.com')")

if __name__ == '__main__':
    unittest.main()
