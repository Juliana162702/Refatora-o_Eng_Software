from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.tarefa import Tarefa  # Só para type checking

class Membro:
    def __init__(self, nome: str, funcao: str, email: str = ""):
        self.nome = nome
        self.funcao = funcao
        self.email = email
        self.tarefas_atribuidas: List['Tarefa'] = []  # Usando string type hint

    def adicionar_tarefa(self, tarefa: 'Tarefa') -> None:
        """Método que será chamado pela Tarefa posteriormente"""
        if tarefa not in self.tarefas_atribuidas:
            self.tarefas_atribuidas.append(tarefa)

    def remover_tarefa(self, tarefa: 'Tarefa') -> None:
        if tarefa in self.tarefas_atribuidas:
            self.tarefas_atribuidas.remove(tarefa)

    def __str__(self) -> str:
        return f"{self.nome} ({self.funcao})" + (f" - {self.email}" if self.email else "")

    def __repr__(self) -> str:
        return f"Membro(nome='{self.nome}', funcao='{self.funcao}', email='{self.email}')"