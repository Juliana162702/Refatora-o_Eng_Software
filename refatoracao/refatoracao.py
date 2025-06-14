from typing import List, Dict, Optional
from datetime import date
from .membro import Membro
from .projeto import Projeto
from .tarefa import Tarefa
from .excecoes import (
    ProjetoNaoEncontradoError,
    MembroNaoEncontradoError,
    TarefaNaoEncontradaError,
    ResponsavelNaoEMembroError
)

class GerenciadorProjetos:
    """Classe principal que gerencia todos os projetos, membros e tarefas."""
    
    def __init__(self):
        self._projetos: List[Projeto] = []
        self._membros: List[Membro] = []
        self._tarefas: List[Tarefa] = []
    
    @property
    def projetos(self) -> List[Projeto]:
        """Retorna uma cópia da lista de projetos"""
        return self._projetos.copy()
    
    @property
    def membros(self) -> List[Membro]:
        """Retorna uma cópia da lista de membros"""
        return self._membros.copy()
    
    @property
    def tarefas(self) -> List[Tarefa]:
        """Retorna uma cópia da lista de tarefas"""
        return self._tarefas.copy()

    def adicionar_projeto(self, projeto: Projeto) -> None:
        """Adiciona um novo projeto ao sistema"""
        if projeto in self._projetos:
            raise ValueError(f"Projeto '{projeto.nome}' já existe")
        self._projetos.append(projeto)

    def cadastrar_membro(self, membro: Membro) -> None:
        """Cadastra um novo membro no sistema"""
        if any(m.nome.lower() == membro.nome.lower() for m in self._membros):
            raise ValueError(f"Membro '{membro.nome}' já cadastrado")
        self._membros.append(membro)

    def buscar_projeto(self, nome_projeto: str) -> Optional[Projeto]:
        """Busca um projeto pelo nome (case insensitive)"""
        for projeto in self._projetos:
            if projeto.nome.lower() == nome_projeto.lower():
                return projeto
        return None

    def buscar_membro(self, nome_membro: str) -> Optional[Membro]:
        """Busca um membro pelo nome (case insensitive)"""
        for membro in self._membros:
            if membro.nome.lower() == nome_membro.lower():
                return membro
        return None

    def buscar_tarefa(self, titulo_tarefa: str) -> Optional[Tarefa]:
        """Busca uma tarefa pelo título (case insensitive)"""
        for tarefa in self._tarefas:
            if tarefa.titulo.lower() == titulo_tarefa.lower():
                return tarefa
        return None

    def adicionar_membro_projeto(self, nome_projeto: str, nome_membro: str) -> None:
        """Adiciona um membro existente a um projeto"""
        projeto = self.buscar_projeto(nome_projeto)
        membro = self.buscar_membro(nome_membro)
        
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
        if not membro:
            raise MembroNaoEncontradoError(nome_membro)
            
        projeto.adicionar_membro(membro)

    def criar_tarefa(self, nome_projeto: str, titulo: str, descricao: str,
                    responsavel_nome: str, prazo: Optional[date] = None,
                    prioridade: int = 1) -> Tarefa:
        """Cria e atribui uma nova tarefa em um projeto"""
        projeto = self.buscar_projeto(nome_projeto)
        responsavel = self.buscar_membro(responsavel_nome)
        
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
        if not responsavel:
            raise MembroNaoEncontradoError(responsavel_nome)
        if responsavel not in projeto.membros:
            raise ResponsavelNaoEMembroError(responsavel_nome)
            
        tarefa = Tarefa(titulo, descricao, responsavel, prazo, prioridade)
        projeto.tarefas.append(tarefa)
        self._tarefas.append(tarefa)
        responsavel.adicionar_tarefa(tarefa)
        
        return tarefa

    def concluir_tarefa(self, nome_projeto: str, titulo_tarefa: str) -> None:
        """Marca uma tarefa como concluída"""
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        tarefa = next((t for t in projeto.tarefas 
                      if t.titulo.lower() == titulo_tarefa.lower()), None)
        if not tarefa:
            raise TarefaNaoEncontradaError(titulo_tarefa)
            
        tarefa.concluir()

    def relatorio_projeto(self, nome_projeto: str) -> Dict:
        """Gera um relatório completo de um projeto"""
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        return {
            "nome": projeto.nome,
            "descricao": projeto.descricao,
            "prazo": projeto.prazo_final.strftime('%d/%m/%Y') if projeto.prazo_final else None,
            "dias_atraso": projeto.calcular_atraso(),
            "total_membros": len(projeto.membros),
            "total_tarefas": len(projeto.tarefas),
            "tarefas_pendentes": sum(1 for t in projeto.tarefas if t.status == Tarefa.STATUS_PENDENTE),
            "tarefas_andamento": sum(1 for t in projeto.tarefas if t.status == Tarefa.STATUS_EM_ANDAMENTO),
            "tarefas_concluidas": sum(1 for t in projeto.tarefas if t.status == Tarefa.STATUS_CONCLUIDA),
            "tarefas_atrasadas": sum(1 for t in projeto.tarefas if t.esta_atrasada())
        }

    def relatorio_membro(self, nome_membro: str) -> Dict:
        """Gera um relatório das atividades de um membro"""
        membro = self.buscar_membro(nome_membro)
        if not membro:
            raise MembroNaoEncontradoError(nome_membro)
            
        tarefas = [t for t in self._tarefas if t.responsavel == membro]
        
        return {
            "nome": membro.nome,
            "funcao": membro.funcao,
            "email": membro.email,
            "total_tarefas": len(tarefas),
            "tarefas_pendentes": sum(1 for t in tarefas if t.status == Tarefa.STATUS_PENDENTE),
            "tarefas_andamento": sum(1 for t in tarefas if t.status == Tarefa.STATUS_EM_ANDAMENTO),
            "tarefas_concluidas": sum(1 for t in tarefas if t.status == Tarefa.STATUS_CONCLUIDA),
            "tarefas_atrasadas": sum(1 for t in tarefas if t.esta_atrasada()),
            "projetos": [p.nome for p in self._projetos if membro in p.membros]
        }