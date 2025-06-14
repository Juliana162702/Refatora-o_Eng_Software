from typing import List, Dict, Optional
from datetime import date
from .membro import Membro
from .tarefa import Tarefa

class Projeto:
    
    def __init__(self, nome: str, descricao: str, prazo: Optional[date] = None):
        self.nome = nome
        self.descricao = descricao
        self.prazo = prazo
        self.data_criacao = date.today()
        self._membros: List[Membro] = []
        self._tarefas: List[Tarefa] = []

    @property
    def membros(self) -> List[Membro]:
        """Retorna uma cópia da lista de membros"""
        return self._membros.copy()

    @property
    def tarefas(self) -> List[Tarefa]:
        """Retorna uma cópia da lista de tarefas"""
        return self._tarefas.copy()

    def adicionar_membro(self, membro: Membro) -> None:
        """Adiciona um membro ao projeto"""
        if membro in self._membros:
            raise ValueError(f"Membro {membro.nome} já está no projeto")
        self._membros.append(membro)

    def adicionar_tarefa(self, tarefa: Tarefa) -> None:
        """Adiciona uma tarefa existente ao projeto"""
        if tarefa in self._tarefas:
            raise ValueError(f"Tarefa '{tarefa.titulo}' já existe no projeto")
        self._tarefas.append(tarefa)

    def criar_tarefa(self, titulo: str, descricao: str, responsavel: Membro, 
                    **kwargs) -> Tarefa:
        """Cria e adiciona uma nova tarefa ao projeto"""
        if responsavel not in self._membros:
            raise ValueError(f"Responsável {responsavel.nome} não é membro do projeto")
        
        tarefa = Tarefa(titulo, descricao, responsavel, **kwargs)
        self.adicionar_tarefa(tarefa)
        return tarefa

    def calcular_atraso(self) -> int:
        """Calcula dias de atraso do projeto (se aplicável)"""
        if self.prazo and date.today() > self.prazo:
            return (date.today() - self.prazo).days
        return 0

    def relatorio_projeto(self) -> Dict:
        """Gera um relatório completo do projeto"""
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "prazo": self.prazo.strftime('%d/%m/%Y') if self.prazo else None,
            "dias_atraso": self.calcular_atraso(),
            "total_membros": len(self._membros),
            "total_tarefas": len(self._tarefas),
            "tarefas_pendentes": sum(1 for t in self._tarefas 
                                   if t.status == Tarefa.STATUS_PENDENTE),
            "tarefas_andamento": sum(1 for t in self._tarefas 
                                   if t.status == Tarefa.STATUS_EM_ANDAMENTO),
            "tarefas_concluidas": sum(1 for t in self._tarefas 
                                    if t.status == Tarefa.STATUS_CONCLUIDA),
            "tarefas_atrasadas": sum(1 for t in self._tarefas 
                                   if getattr(t, 'esta_atrasada', lambda: False)())
        }

    def __str__(self) -> str:
        atraso = f" (Atraso: {self.calcular_atraso()} dias)" if self.calcular_atraso() > 0 else ""
        return (f"Projeto: {self.nome}\n"
                f"Descrição: {self.descricao}\n"
                f"Prazo: {self.prazo.strftime('%d/%m/%Y') if self.prazo else 'Sem prazo'}{atraso}\n"
                f"Membros: {len(self._membros)}\n"
                f"Tarefas: {len(self._tarefas)}")

    def __repr__(self) -> str:
        return f"Projeto(nome='{self.nome}', prazo={self.prazo}, membros={len(self._membros)})"