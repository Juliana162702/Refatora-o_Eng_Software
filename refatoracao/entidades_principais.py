class Membro:
    def __init__(self, nome, funcao):
        self.nome = nome
        self.funcao = funcao

    def __str__(self):
        return f"{self.nome} ({self.funcao})"


class Tarefa:
    def __init__(self, titulo, descricao, responsavel):
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel = responsavel
        self.status = "pendente"

    def concluir(self):
        self.status = "concluída"

    def __str__(self):
        return f"{self.titulo} - {self.status} - Responsável: {self.responsavel}"


class Projeto:
    def __init__(self, nome, prazo, descricao):
        self.nome = nome
        self.prazo = prazo
        self.descricao = descricao
        self.tarefas = []
        self.membros = []

    def adicionar_tarefa(self, titulo, descricao, responsavel):
        tarefa = Tarefa(titulo, descricao, responsavel)
        self.tarefas.append(tarefa)

    def adicionar_membro(self, nome, funcao):
        self.membros.append(Membro(nome, funcao))

    def listar_tarefas(self):
        for tarefa in self.tarefas:
            print(tarefa)

    def concluir_tarefa(self, titulo):
        for tarefa in self.tarefas:
            if tarefa.titulo == titulo:
                tarefa.concluir()
                print(f"Tarefa {titulo} concluída")
                return
        print(f"Tarefa {titulo} não encontrada")

    def relatorio_projeto(self):
        print(f"Projeto: {self.nome}")
        print(f"Prazo: {self.prazo}")
        print(f"Descrição: {self.descricao}")
        print("Membros:")
        for membro in self.membros:
            print(f" - {membro}")
        print("Tarefas:")
        self.listar_tarefas()