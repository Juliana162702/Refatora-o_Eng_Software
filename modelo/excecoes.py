class ProjetoError(Exception):
    """Classe base para erros do sistema de gerenciamento de projetos."""
    pass


class ProjetoNaoEncontradoError(ProjetoError):
    def __init__(self, nome_projeto: str):
        super().__init__(f"Projeto '{nome_projeto}' não encontrado")
        self.nome_projeto = nome_projeto


class TarefaNaoEncontradaError(ProjetoError):
    def __init__(self, titulo_tarefa: str):
        super().__init__(f"Tarefa '{titulo_tarefa}' não encontrada")
        self.titulo_tarefa = titulo_tarefa


class TarefaJaConcluidaError(ProjetoError):
    def __init__(self, titulo_tarefa: str):
        super().__init__(f"Tarefa '{titulo_tarefa}' já está concluída")
        self.titulo_tarefa = titulo_tarefa


class MembroNaoEncontradoError(ProjetoError):
    def __init__(self, nome_membro: str):
        super().__init__(f"Membro '{nome_membro}' não encontrado no projeto")
        self.nome_membro = nome_membro


class MembroJaExistenteError(ProjetoError):
    def __init__(self, nome_membro: str):
        super().__init__(f"Membro '{nome_membro}' já está no projeto")
        self.nome_membro = nome_membro


class ResponsavelNaoEMembroError(ProjetoError):
    def __init__(self, nome_responsavel: str):
        super().__init__(
            f"Responsável '{nome_responsavel}' não é membro do projeto. "
            "Adicione-o como membro primeiro."
        )
        self.nome_responsavel = nome_responsavel


class OperacaoTarefaError(ProjetoError):
    """Erro durante operação com tarefa (criação/conclusão/atribuição)"""
    pass


__all__ = [
    'ProjetoError',
    'ProjetoNaoEncontradoError',
    'TarefaNaoEncontradaError',
    'TarefaJaConcluidaError',
    'MembroNaoEncontradoError',
    'MembroJaExistenteError',
    'ResponsavelNaoEMembroError',
    'OperacaoTarefaError'
]