from __future__ import annotations
from datetime import date
from typing import Optional

from refatoracao.entidades_principais import Membro

class Tarefa:
    STATUS_PENDENTE = "pendente"
    STATUS_EM_ANDAMENTO = "em_andamento"
    STATUS_CONCLUIDA = "concluída"
    
    def __init__(self, titulo: str, descricao: str, responsavel: 'Membro', 
                 prazo: Optional[date] = None, prioridade: int = 1):
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel = responsavel  # Type hint como string
        self.prazo = prazo
        self.prioridade = min(max(1, prioridade), 5)
        self.status = self.STATUS_PENDENTE
        self.data_criacao = date.today()
        
        # Adia a atribuição até que o membro esteja totalmente inicializado
        responsavel.adicionar_tarefa(self)

    def iniciar(self) -> None:
        """Marca a tarefa como em andamento."""
        self.status = self.STATUS_EM_ANDAMENTO

    def concluir(self) -> None:
        """Marca a tarefa como concluída."""
        self.status = self.STATUS_CONCLUIDA

    def esta_atrasada(self) -> bool:
        """Verifica se a tarefa está atrasada."""
        return (self.prazo is not None and 
                self.prazo < date.today() and 
                self.status != self.STATUS_CONCLUIDA)

    def __str__(self) -> str:
        status_str = f"{self.status.upper()}"
        if self.esta_atrasada():
            status_str += " (ATRASADA)"
        return (f"{self.titulo} - {status_str}\n"
                f"Responsável: {self.responsavel.nome}\n"
                f"Prazo: {self.prazo.strftime('%d/%m/%Y') if self.prazo else 'Sem prazo'}\n"
                f"Prioridade: {'★' * self.prioridade}")

    def __repr__(self) -> str:
        return (f"Tarefa(titulo='{self.titulo}', status='{self.status}', "
                f"responsavel='{self.responsavel.nome}')")