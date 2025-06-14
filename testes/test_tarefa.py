import unittest
from datetime import date, timedelta
from modelo.membro import Membro
from modelo.tarefa import Tarefa

class TestTarefa(unittest.TestCase):
    """Testes para a classe Tarefa"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.membro = Membro("Maria Souza", "Designer")
        self.tarefa = Tarefa(
            titulo="Criar protótipo",
            descricao="Desenvolver protótipo de alta fidelidade",
            responsavel=self.membro,
            prazo=date.today() + timedelta(days=7),
            prioridade=2
        )
    
    def test_criacao_tarefa(self):
        """Testa a criação correta de uma tarefa"""
        self.assertEqual(self.tarefa.titulo, "Criar protótipo")
        self.assertEqual(self.tarefa.prioridade, 2)
        self.assertEqual(self.tarefa.status, Tarefa.STATUS_PENDENTE)
        self.assertEqual(len(self.membro.tarefas_atribuidas), 1)
    
    def test_concluir_tarefa(self):
        """Testa a conclusão de uma tarefa"""
        self.tarefa.concluir()
        self.assertEqual(self.tarefa.status, Tarefa.STATUS_CONCLUIDA)
    
    def test_iniciar_tarefa(self):
        """Testa o início de uma tarefa"""
        self.tarefa.iniciar()
        self.assertEqual(self.tarefa.status, Tarefa.STATUS_EM_ANDAMENTO)
    
    def test_tarefa_atrasada(self):
        """Testa a verificação de tarefa atrasada"""
        tarefa_atrasada = Tarefa(
            titulo="Tarefa atrasada",
            descricao="Teste de atraso",
            responsavel=self.membro,
            prazo=date.today() - timedelta(days=1)
        )
        self.assertTrue(tarefa_atrasada.esta_atrasada())
        self.assertFalse(self.tarefa.esta_atrasada())
    
    def test_representacao_string(self):
        """Testa as representações __str__ e __repr__"""
        self.assertIn("Criar protótipo - PENDENTE", str(self.tarefa))
        self.assertEqual(repr(self.tarefa), 
            f"Tarefa(titulo='Criar protótipo', status='pendente', responsavel='Maria Souza')")

if __name__ == '__main__':
    unittest.main()