import unittest
from modelo.excecoes import (
    ProjetoError,
    ProjetoNaoEncontradoError,
    TarefaNaoEncontradaError,
    MembroNaoEncontradoError,
    ResponsavelNaoEMembroError
)

class TestExcecoes(unittest.TestCase):
    """Testes para as classes de exceção"""
    
    def test_projeto_nao_encontrado(self):
        """Testa a exceção ProjetoNaoEncontradoError"""
        with self.assertRaises(ProjetoNaoEncontradoError) as context:
            raise ProjetoNaoEncontradoError("Projeto Inexistente")
        
        self.assertEqual(str(context.exception), "Projeto 'Projeto Inexistente' não encontrado")
        self.assertEqual(context.exception.nome_projeto, "Projeto Inexistente")
        self.assertIsInstance(context.exception, ProjetoError)
    
    def test_tarefa_nao_encontrada(self):
        """Testa a exceção TarefaNaoEncontradaError"""
        with self.assertRaises(TarefaNaoEncontradaError) as context:
            raise TarefaNaoEncontradaError("Tarefa Fantasma")
        
        self.assertEqual(str(context.exception), "Tarefa 'Tarefa Fantasma' não encontrada")
        self.assertEqual(context.exception.titulo_tarefa, "Tarefa Fantasma")
        self.assertIsInstance(context.exception, ProjetoError)
    
    def test_membro_nao_encontrado(self):
        """Testa a exceção MembroNaoEncontradoError"""
        with self.assertRaises(MembroNaoEncontradoError) as context:
            raise MembroNaoEncontradoError("Membro Inexistente")
        
        self.assertEqual(str(context.exception), "Membro 'Membro Inexistente' não encontrado no projeto")
        self.assertEqual(context.exception.nome_membro, "Membro Inexistente")
        self.assertIsInstance(context.exception, ProjetoError)
    
    def test_responsavel_nao_membro(self):
        """Testa a exceção ResponsavelNaoEMembroError"""
        with self.assertRaises(ResponsavelNaoEMembroError) as context:
            raise ResponsavelNaoEMembroError("Fulano")
        
        self.assertIn("Fulano", str(context.exception))
        self.assertEqual(context.exception.nome_responsavel, "Fulano")
        self.assertIsInstance(context.exception, ProjetoError)

if __name__ == '__main__':
    unittest.main()