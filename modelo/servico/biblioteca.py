from typing import List, Dict, Optional
from datetime import date
from modelo import (
    Projeto,
    Tarefa,
    Membro,
    ProjetoNaoEncontradoError,
    TarefaNaoEncontradaError,
    MembroNaoEncontradoError,
    ResponsavelNaoEMembroError
)

class GerenciadorProjetos:
    """Classe principal que gerencia as operações do sistema de projetos."""
    
    def __init__(self):
        self._projetos: List[Projeto] = []
        self._membros: List[Membro] = []
        self._tarefas: List[Tarefa] = []
    
    @property
    def projetos(self) -> List[Projeto]:
        """Retorna uma cópia da lista de projetos."""
        return self._projetos.copy()
    
    @property
    def membros(self) -> List[Membro]:
        """Retorna uma cópia da lista de membros."""
        return self._membros.copy()
    
    @property
    def tarefas(self) -> List[Tarefa]:
        """Retorna uma cópia da lista de tarefas."""
        return self._tarefas.copy()

    def adicionar_projeto(self, projeto: Projeto) -> None:
        """Adiciona um novo projeto ao sistema."""
        self._projetos.append(projeto)

    def cadastrar_membro(self, membro: Membro) -> None:
        """Cadastra um novo membro no sistema."""
        self._membros.append(membro)

    def buscar_projeto(self, nome_projeto: str) -> Optional[Projeto]:
        """Busca um projeto pelo nome (case insensitive)."""
        for projeto in self._projetos:
            if projeto.nome.lower() == nome_projeto.lower():
                return projeto
        return None

    def buscar_membro(self, nome_membro: str) -> Optional[Membro]:
        """Busca um membro pelo nome (case insensitive)."""
        for membro in self._membros:
            if membro.nome.lower() == nome_membro.lower():
                return membro
        return None

    def buscar_tarefa(self, titulo_tarefa: str) -> Optional[Tarefa]:
        """Busca uma tarefa pelo título (case insensitive)."""
        for tarefa in self._tarefas:
            if tarefa.titulo.lower() == titulo_tarefa.lower():
                return tarefa
        return None

    def criar_tarefa(self, nome_projeto: str, titulo: str, descricao: str, 
                    responsavel_nome: str, **kwargs) -> Tarefa:
        """
        Cria uma nova tarefa em um projeto.
        
        Args:
            nome_projeto: Nome do projeto
            titulo: Título da tarefa
            descricao: Descrição da tarefa
            responsavel_nome: Nome do membro responsável
            **kwargs: Argumentos adicionais para Tarefa (prazo, prioridade, etc.)
            
        Returns:
            Objeto Tarefa criado
            
        Raises:
            ProjetoNaoEncontradoError: Se projeto não existe
            MembroNaoEncontradoError: Se membro não existe
            ResponsavelNaoEMembroError: Se responsável não é membro do projeto
        """
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        responsavel = self.buscar_membro(responsavel_nome)
        if not responsavel:
            raise MembroNaoEncontradoError(responsavel_nome)
            
        if responsavel not in projeto.membros:
            raise ResponsavelNaoEMembroError(responsavel_nome)
            
        tarefa = Tarefa(titulo, descricao, responsavel, **kwargs)
        projeto.adicionar_tarefa(tarefa)
        self._tarefas.append(tarefa)
        
        return tarefa

    def concluir_tarefa(self, nome_projeto: str, titulo_tarefa: str) -> None:
        """
        Marca uma tarefa como concluída.
        
        Args:
            nome_projeto: Nome do projeto
            titulo_tarefa: Título da tarefa
            
        Raises:
            ProjetoNaoEncontradoError: Se projeto não existe
            TarefaNaoEncontradaError: Se tarefa não existe no projeto
        """
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        tarefa = next((t for t in projeto.tarefas 
                      if t.titulo.lower() == titulo_tarefa.lower()), None)
        
        if not tarefa:
            raise TarefaNaoEncontradaError(titulo_tarefa)
            
        tarefa.concluir()

    def adicionar_membro_projeto(self, nome_projeto: str, nome_membro: str) -> None:
        """
        Adiciona um membro existente a um projeto.
        
        Args:
            nome_projeto: Nome do projeto
            nome_membro: Nome do membro
            
        Raises:
            ProjetoNaoEncontradoError: Se projeto não existe
            MembroNaoEncontradoError: Se membro não existe
        """
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        membro = self.buscar_membro(nome_membro)
        if not membro:
            raise MembroNaoEncontradoError(nome_membro)
            
        projeto.adicionar_membro(membro)

    def relatorio_projeto(self, nome_projeto: str) -> Dict:
        """
        Gera um relatório detalhado de um projeto.
        
        Args:
            nome_projeto: Nome do projeto
            
        Returns:
            Dicionário com informações do projeto
            
        Raises:
            ProjetoNaoEncontradoError: Se projeto não existe
        """
        projeto = self.buscar_projeto(nome_projeto)
        if not projeto:
            raise ProjetoNaoEncontradoError(nome_projeto)
            
        return {
            "nome": projeto.nome,
            "descricao": projeto.descricao,
            "prazo": projeto.prazo.strftime('%d/%m/%Y') if projeto.prazo else None,
            "total_membros": len(projeto.membros),
            "total_tarefas": len(projeto.tarefas),
            "tarefas_pendentes": len([t for t in projeto.tarefas 
                                    if t.status == Tarefa.STATUS_PENDENTE]),
            "tarefas_andamento": len([t for t in projeto.tarefas 
                                    if t.status == Tarefa.STATUS_EM_ANDAMENTO]),
            "tarefas_concluidas": len([t for t in projeto.tarefas 
                                     if t.status == Tarefa.STATUS_CONCLUIDA]),
            "tarefas_atrasadas": len([t for t in projeto.tarefas 
                                    if t.esta_atrasada()])
        }

    def relatorio_membro(self, nome_membro: str) -> Dict:
        """
        Gera um relatório das atividades de um membro.
        
        Args:
            nome_membro: Nome do membro
            
        Returns:
            Dicionário com informações do membro
            
        Raises:
            MembroNaoEncontradoError: Se membro não existe
        """
        membro = self.buscar_membro(nome_membro)
        if not membro:
            raise MembroNaoEncontradoError(nome_membro)
            
        tarefas = [t for t in self._tarefas if t.responsavel == membro]
        
        return {
            "nome": membro.nome,
            "funcao": membro.funcao,
            "total_tarefas": len(tarefas),
            "tarefas_pendentes": len([t for t in tarefas 
                                     if t.status == Tarefa.STATUS_PENDENTE]),
            "tarefas_andamento": len([t for t in tarefas 
                                    if t.status == Tarefa.STATUS_EM_ANDAMENTO]),
            "tarefas_concluidas": len([t for t in tarefas 
                                     if t.status == Tarefa.STATUS_CONCLUIDA]),
            "tarefas_atrasadas": len([t for t in tarefas 
                                    if t.esta_atrasada()]),
            "projetos": [p.nome for p in self._projetos if membro in p.membros]
        }