import tkinter as tk
from tkinter import messagebox

def adicionar():
    nome = input_Nome.get()
    tel = input_Telefone.get()
    end = input_Endereco.get()
    dist = input_Distrito.get()
    pais = input_Pais.get()
    email = input_Email.get()

    if not nome:
        messagebox.showwarning("Erro", "Digite pelo menos o nome")
        return

    with open('agenda.txt', 'a') as arquivo:
        arquivo.write(f"{nome};{tel};{end};{dist};{pais};{email}\n")

    messagebox.showinfo('Lista telefónica','Cadastro efetuado com sucesso!')

    input_Nome.delete(0, 'end')
    input_Telefone.delete(0, 'end')
    input_Endereco.delete(0, 'end')
    input_Distrito.delete(0, 'end')
    input_Pais.delete(0, 'end')
    input_Email.delete(0, 'end')


def pesquisar():
    nome = input_Nome.get()

    try:
        with open('agenda.txt', 'r') as arquivo:
            linhas = arquivo.readlines()

        for linha in linhas:
            dados = linha.strip().split(";")
            if dados[0] == nome:
                messagebox.showinfo("Resultado",
                    f"Nome: {dados[0]}\nTelefone: {dados[1]}\nEndereço: {dados[2]}\nDistrito: {dados[3]}\nPaís: {dados[4]}\nEmail: {dados[5]}")
                return

        messagebox.showwarning("Aviso", "Contato não encontrado")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado")


def eliminar():
    nome = input_Nome.get()

    try:
        with open('agenda.txt', 'r') as arquivo:
            linhas = arquivo.readlines()

        with open('agenda.txt', 'w') as arquivo:
            encontrado = False
            for linha in linhas:
                dados = linha.strip().split(";")
                if dados[0] != nome:
                    arquivo.write(linha)
                else:
                    encontrado = True

        if encontrado:
            messagebox.showinfo("Sucesso", "Contato eliminado")
        else:
            messagebox.showwarning("Aviso", "Contato não encontrado")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado")


root = tk.Tk()
root.title("Lista Telefónica")
root.geometry("600x600")

branco = "#ddf6f9"
root.configure(bg=branco)

tk.Label(root, text="Nome", bg="white").place(x=50, y=50)
tk.Label(root, text="Telefone", bg="white").place(x=50, y=100)
tk.Label(root, text="Endereço", bg="white").place(x=50, y=150)
tk.Label(root, text="Distrito", bg="white").place(x=50, y=200)
tk.Label(root, text="País", bg="white").place(x=350, y=200)
tk.Label(root, text="Email", bg="white").place(x=50, y=250)

input_Nome = tk.Entry(root)
input_Nome.place(width=350, x=150, y=50)

input_Telefone = tk.Entry(root)
input_Telefone.place(width=350, x=150, y=100)

input_Endereco = tk.Entry(root)
input_Endereco.place(width=350, x=150, y=150)

input_Distrito = tk.Entry(root)
input_Distrito.place(width=100, x=150, y=200)

input_Pais = tk.Entry(root)
input_Pais.place(width=100, x=400, y=200)

input_Email = tk.Entry(root)
input_Email.place(width=350, x=150, y=250)

tk.Button(text="Adicionar", command=adicionar).place(width=150, x=50, y=300)
tk.Button(text="Pesquisar", command=pesquisar).place(width=150, x=225, y=300)
tk.Button(text="Eliminar", command=eliminar).place(width=150, x=400, y=300)

root.mainloop()