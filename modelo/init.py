# Exportação das classes principais
from .gerenciador import GerenciadorProjetos
from .membro import Membro
from .projeto import Projeto
from .tarefa import Tarefa

# Exportação das exceções (adicione esses imports se ainda não existirem)
from .excecoes import (
    ProjetoError,
    ProjetoNaoEncontradoError,
    TarefaNaoEncontradaError,
    MembroNaoEncontradoError,
    ResponsavelNaoEMembroError
)

# Lista única de tudo o que deve ser exportado
__all__ = [
    'GerenciadorProjetos',
    'Membro',
    'Projeto',
    'Tarefa',
    'ProjetoError',
    'ProjetoNaoEncontradoError', 
    'TarefaNaoEncontradaError',
    'MembroNaoEncontradoError',
    'ResponsavelNaoEMembroError'
]