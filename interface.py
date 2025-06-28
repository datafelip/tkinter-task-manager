import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass, asdict
import pandas as pd
import os

# -------------------- Dados --------------------
@dataclass
class Tarefa:
    codigo: int
    descricao: str
    concluida: bool = False

lista_tarefas = []
codigo = 1
json_path = "lista_tarefas.json"

# -------------------- Funções --------------------
def carregar_tarefas():
    global codigo
    if os.path.exists(json_path):
        df = pd.read_json(json_path)
        for _, row in df.iterrows():
            tarefa = Tarefa(int(row['codigo']), row['descricao'], bool(row['concluida']))
            lista_tarefas.append(tarefa)
        if lista_tarefas:
            codigo = max(t.codigo for t in lista_tarefas) + 1

def adicionar_tarefa():
    global codigo
    descricao = entrada.get().strip()
    if not descricao:
        messagebox.showwarning("Aviso", "Digite uma tarefa válida.")
        return

    tarefa = Tarefa(codigo, descricao)
    lista_tarefas.append(tarefa)
    codigo += 1
    atualizar_lista()
    entrada.delete(0, tk.END)

def atualizar_lista():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "=== PENDENTES ===")
    for tarefa in lista_tarefas:
        if not tarefa.concluida:
            listbox.insert(tk.END, f"{tarefa.codigo} - {tarefa.descricao}")
    listbox.insert(tk.END, "")
    listbox.insert(tk.END, "=== CONCLUÍDAS ===")
    for tarefa in lista_tarefas:
        if tarefa.concluida:
            listbox.insert(tk.END, f"{tarefa.codigo} - {tarefa.descricao}")

def obter_indice_real():
    selecao = listbox.curselection()
    if not selecao or selecao[0] in (0, listbox.size()-1) or "===" in listbox.get(selecao):
        return None
    texto = listbox.get(selecao[0])
    try:
        cod = int(texto.split("-")[0].strip())
        for i, tarefa in enumerate(lista_tarefas):
            if tarefa.codigo == cod:
                return i
    except:
        return None
    return None

def marcar_concluida():
    idx = obter_indice_real()
    if idx is not None:
        lista_tarefas[idx].concluida = True
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Selecione uma tarefa válida.")

def excluir_tarefa():
    idx = obter_indice_real()
    if idx is not None:
        del lista_tarefas[idx]
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Selecione uma tarefa válida.")

def salvar_json():
    dados = [asdict(t) for t in lista_tarefas]
    df = pd.DataFrame(dados)
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)
    messagebox.showinfo("Salvo", "Tarefas salvas em JSON com sucesso.")

def exportar_excel():
    dados = [asdict(t) for t in lista_tarefas]
    df = pd.DataFrame(dados)
    df.to_excel("lista_tarefas.xlsx", index=False)
    messagebox.showinfo("Exportado", "Tarefas exportadas para Excel com sucesso.")

# -------------------- Interface --------------------
root = tk.Tk()
root.title("Lista de Tarefas")
root.geometry("450x500")

entrada = tk.Entry(root, width=40)
entrada.pack(pady=10)

btn_adicionar = tk.Button(root, text="Adicionar Tarefa", width=20, command=adicionar_tarefa)
btn_adicionar.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

btn_concluir = tk.Button(root, text="Marcar como Concluída", width=20, command=marcar_concluida)
btn_concluir.pack(pady=5)

btn_excluir = tk.Button(root, text="Excluir Tarefa", width=20, command=excluir_tarefa)
btn_excluir.pack(pady=5)

btn_salvar = tk.Button(root, text="Salvar em JSON", width=20, command=salvar_json)
btn_salvar.pack(pady=5)

btn_exportar = tk.Button(root, text="Exportar para Excel", width=20, command=exportar_excel)
btn_exportar.pack(pady=10)


carregar_tarefas()
atualizar_lista()

root.mainloop()
