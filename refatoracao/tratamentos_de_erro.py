class GerenciadorProjetosError(Exception):
    """Classe base para erros do sistema de gerenciamento de projetos"""
    pass


class ProjetoNaoEncontradoError(GerenciadorProjetosError):
    def __init__(self, nome_projeto: str):
        super().__init__(f"Projeto '{nome_projeto}' não encontrado")
        self.nome_projeto = nome_projeto


class MembroNaoEncontradoError(GerenciadorProjetosError):
    def __init__(self, nome_membro: str):
        super().__init__(f"Membro '{nome_membro}' não encontrado")
        self.nome_membro = nome_membro


class TarefaNaoEncontradaError(GerenciadorProjetosError):
    def __init__(self, titulo_tarefa: str):
        super().__init__(f"Tarefa '{titulo_tarefa}' não encontrada")
        self.titulo_tarefa = titulo_tarefa


class ResponsavelNaoEMembroError(GerenciadorProjetosError):
    def __init__(self, nome_responsavel: str):
        super().__init__(
            f"Responsável '{nome_responsavel}' não é membro do projeto. "
            "Adicione-o como membro primeiro."
        )
        self.nome_responsavel = nome_responsavel


class TarefaJaConcluidaError(GerenciadorProjetosError):
    def __init__(self, titulo_tarefa: str):
        super().__init__(f"Tarefa '{titulo_tarefa}' já está concluída")
        self.titulo_tarefa = titulo_tarefa


class ProjetoExistenteError(GerenciadorProjetosError):
    def __init__(self, nome_projeto: str):
        super().__init__(f"Projeto '{nome_projeto}' já existe no sistema")
        self.nome_projeto = nome_projeto


class MembroExistenteError(GerenciadorProjetosError):
    def __init__(self, nome_membro: str):
        super().__init__(f"Membro '{nome_membro}' já está cadastrado")
        self.nome_membro = nome_membro


class TarefaAtrasadaError(GerenciadorProjetosError):
    def __init__(self, titulo_tarefa: str, dias_atraso: int):
        super().__init__(
            f"Tarefa '{titulo_tarefa}' está atrasada em {dias_atraso} dias"
        )
        self.titulo_tarefa = titulo_tarefa
        self.dias_atraso = dias_atraso


class PrioridadeInvalidaError(GerenciadorProjetosError):
    def __init__(self, prioridade: int):
        super().__init__(
            f"Prioridade {prioridade} é inválida. Deve ser entre 1 e 5"
        )
        self.prioridade = prioridade


__all__ = [
    'GerenciadorProjetosError',
    'ProjetoNaoEncontradoError',
    'MembroNaoEncontradoError',
    'TarefaNaoEncontradaError',
    'ResponsavelNaoEMembroError',
    'TarefaJaConcluidaError',
    'ProjetoExistenteError',
    'MembroExistenteError',
    'TarefaAtrasadaError',
    'PrioridadeInvalidaError'
]