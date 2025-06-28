from dataclasses import dataclass, asdict
from validar_entrada import pega_numero_negativo, pega_string
import pandas as pd
lista_tarefas = []
colunas = ["Código", "Tarefa", "Concluída"]
codigo = 1

@dataclass
class Tarefa:
    codigo: int
    descricao: str
    concluida: bool = False

def adicionar_tarefa(descricao: str):
    global codigo
    tarefa = Tarefa(codigo, descricao)
    lista_tarefas.append(tarefa)
    codigo += 1
    print("Tarefa adicionada com sucesso.")

def visualizar_tarefas():
    if not lista_tarefas:
        print("A lista está vazia.")
        return
    print("\n--- Lista de Tarefas ---")
    for tarefa in lista_tarefas:
        status = "Concluída" if tarefa.concluida else "Pendente"
        print(f"[{tarefa.codigo}] {tarefa.descricao} - {status}")

def marcar_concluida(cod: int):
    for tarefa in lista_tarefas:
        if tarefa.codigo == cod:
            tarefa.concluida = True
            print("Tarefa marcada como concluída.")
            return
    print("Código não encontrado.")

def excluir_tarefa(cod: int):
    global lista_tarefas
    for tarefa in lista_tarefas:
        if tarefa.codigo == cod:
            lista_tarefas.remove(tarefa)
            print("Tarefa excluída com sucesso.")
            return
    print("Código não encontrado.")

def criar_json():
    lista_dict = [asdict(tarefa) for tarefa in lista_tarefas]
    df = pd.DataFrame(lista_dict)
    df.to_json("lista_tarefas.json", orient="records", indent=4, force_ascii=False)

def main():
    while True:
        opcao = pega_numero_negativo('''
1 - Adicionar tarefa
2 - Visualizar tarefas
3 - Marcar como concluída
4 - Excluir tarefa
5 - Sair
Digite aqui -->: ''')

        match opcao:
            case 1:
                descricao = pega_string("Digite a tarefa: ").strip().title()
                while not descricao:
                    descricao = pega_string("Digite a tarefa: ").strip().title()
                adicionar_tarefa(descricao)
            case 2:
                visualizar_tarefas()
            case 3:
                cod = pega_numero_negativo("Digite o código da tarefa a concluir: ")
                marcar_concluida(cod)
            case 4:
                cod = pega_numero_negativo("Digite o código da tarefa a excluir: ")
                excluir_tarefa(cod)
            case 5:
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
    criar_json()
