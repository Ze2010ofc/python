import tkinter as tk
from tkinter import messagebox

preco_pc = 2000
preco_tel = 900
preco_tv = 1000
preco_fones = 20
preco_rato = 50

qtd_pc = 0
qtd_tel = 0
qtd_tv = 0
qtd_fones = 0
qtd_rato = 0

users = []
passwords = []

carrinho_pc = []
carrinho_tel = []
carrinho_tv = []
carrinho_fones = []
carrinho_rato = []

utilizador_atual = ""
posicao_user = -1


def limpar_janela():
    for widget in root.winfo_children():
        widget.destroy()


def procurar_user(nome):
    i = 0
    while i < len(users):
        if users[i] == nome:
            return i
        i = i + 1
    return -1


def gravar_carrinho():
    if posicao_user >= 0:
        carrinho_pc[posicao_user] = qtd_pc
        carrinho_tel[posicao_user] = qtd_tel
        carrinho_tv[posicao_user] = qtd_tv
        carrinho_fones[posicao_user] = qtd_fones
        carrinho_rato[posicao_user] = qtd_rato


def atualizar_quantidades():
    label_qtd_pc.config(text=str(qtd_pc))
    label_qtd_tel.config(text=str(qtd_tel))
    label_qtd_tv.config(text=str(qtd_tv))
    label_qtd_fones.config(text=str(qtd_fones))
    label_qtd_rato.config(text=str(qtd_rato))


def atualizar_carrinho():
    total = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato
    label_carrinho.config(text="Carrinho: " + str(total) + " produtos")
    gravar_carrinho()


def criar_conta():
    nome = entry_user.get()
    password = entry_password.get()

    if nome == "" or password == "":
        messagebox.showerror("Erro", "Tens de escrever user e password.")
    else:
        pos = procurar_user(nome)

        if pos != -1:
            messagebox.showerror("Erro", "Esse user já existe.")
        else:
            users.append(nome)
            passwords.append(password)

            carrinho_pc.append(0)
            carrinho_tel.append(0)
            carrinho_tv.append(0)
            carrinho_fones.append(0)
            carrinho_rato.append(0)

            messagebox.showinfo("Conta criada", "Conta criada com sucesso.")


def iniciar_sessao():
    global qtd_pc, qtd_tel, qtd_tv, qtd_fones, qtd_rato
    global utilizador_atual, posicao_user

    nome = entry_user.get()
    password = entry_password.get()

    pos = procurar_user(nome)

    if pos == -1:
        messagebox.showerror("Erro", "User não existe.")
    else:
        if passwords[pos] == password:
            utilizador_atual = nome
            posicao_user = pos

            qtd_pc = carrinho_pc[pos]
            qtd_tel = carrinho_tel[pos]
            qtd_tv = carrinho_tv[pos]
            qtd_fones = carrinho_fones[pos]
            qtd_rato = carrinho_rato[pos]

            mostrar_loja()
        else:
            messagebox.showerror("Erro", "Password errada.")


def sair_conta():
    global utilizador_atual, posicao_user
    global qtd_pc, qtd_tel, qtd_tv, qtd_fones, qtd_rato

    gravar_carrinho()

    utilizador_atual = ""
    posicao_user = -1

    qtd_pc = 0
    qtd_tel = 0
    qtd_tv = 0
    qtd_fones = 0
    qtd_rato = 0

    mostrar_menu()


def adicionar_pc():
    global qtd_pc
    qtd_pc = qtd_pc + 1
    label_qtd_pc.config(text=str(qtd_pc))
    atualizar_carrinho()


def remover_pc():
    global qtd_pc
    if qtd_pc > 0:
        qtd_pc = qtd_pc - 1
    label_qtd_pc.config(text=str(qtd_pc))
    atualizar_carrinho()


def adicionar_tel():
    global qtd_tel
    qtd_tel = qtd_tel + 1
    label_qtd_tel.config(text=str(qtd_tel))
    atualizar_carrinho()


def remover_tel():
    global qtd_tel
    if qtd_tel > 0:
        qtd_tel = qtd_tel - 1
    label_qtd_tel.config(text=str(qtd_tel))
    atualizar_carrinho()


def adicionar_tv():
    global qtd_tv
    qtd_tv = qtd_tv + 1
    label_qtd_tv.config(text=str(qtd_tv))
    atualizar_carrinho()


def remover_tv():
    global qtd_tv
    if qtd_tv > 0:
        qtd_tv = qtd_tv - 1
    label_qtd_tv.config(text=str(qtd_tv))
    atualizar_carrinho()


def adicionar_fones():
    global qtd_fones
    qtd_fones = qtd_fones + 1
    label_qtd_fones.config(text=str(qtd_fones))
    atualizar_carrinho()


def remover_fones():
    global qtd_fones
    if qtd_fones > 0:
        qtd_fones = qtd_fones - 1
    label_qtd_fones.config(text=str(qtd_fones))
    atualizar_carrinho()


def adicionar_rato():
    global qtd_rato
    qtd_rato = qtd_rato + 1
    label_qtd_rato.config(text=str(qtd_rato))
    atualizar_carrinho()


def remover_rato():
    global qtd_rato
    if qtd_rato > 0:
        qtd_rato = qtd_rato - 1
    label_qtd_rato.config(text=str(qtd_rato))
    atualizar_carrinho()


def apagar_carrinho():
    global qtd_pc, qtd_tel, qtd_tv, qtd_fones, qtd_rato

    qtd_pc = 0
    qtd_tel = 0
    qtd_tv = 0
    qtd_fones = 0
    qtd_rato = 0

    atualizar_quantidades()
    atualizar_carrinho()

    messagebox.showinfo("Carrinho", "Carrinho apagado.")


def pagar():
    total_produtos = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato
    total_preco = qtd_pc * preco_pc + qtd_tel * preco_tel + qtd_tv * preco_tv + qtd_fones * preco_fones + qtd_rato * preco_rato

    janela = tk.Toplevel(root)
    janela.title("Pagamento")
    janela.geometry("300x200")
    janela.configure(bg=branco)

    tk.Label(janela, text="Total de produtos: " + str(total_produtos), bg="white").place(x=50, y=60)
    tk.Label(janela, text="Preço total: " + str(total_preco) + "€", bg="white").place(x=50, y=100)


def mostrar_menu():
    global entry_user, entry_password

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=180, y=50)

    tk.Label(root, text="User", bg="white").place(x=170, y=150)
    entry_user = tk.Entry(root)
    entry_user.place(x=280, y=150)

    tk.Label(root, text="Password", bg="white").place(x=170, y=200)
    entry_password = tk.Entry(root, show="*")
    entry_password.place(x=280, y=200)

    tk.Button(root, text="Iniciar sessão", command=iniciar_sessao).place(width=150, x=225, y=270)
    tk.Button(root, text="Criar conta", command=criar_conta).place(width=180, x=210, y=320)



def mostrar_loja():
    global label_qtd_pc, label_qtd_tel, label_qtd_tv, label_qtd_fones, label_qtd_rato
    global label_carrinho

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=180, y=10)
    tk.Label(root, text="Utilizador: " + utilizador_atual, bg="white").place(x=50, y=35)

    tk.Label(root, text="Produto", bg="white").place(x=50, y=70)
    tk.Label(root, text="No carrinho", bg="white").place(x=480, y=70)

    tk.Label(root, text="PC Gamer", bg="white").place(x=50, y=110)
    tk.Button(root, text="Adicionar", command=adicionar_pc).place(width=80, x=200, y=110)
    tk.Button(root, text="Remover", command=remover_pc).place(width=80, x=300, y=110)
    label_qtd_pc = tk.Label(root, text="0", bg="white")
    label_qtd_pc.place(x=500, y=110)

    tk.Label(root, text="Telemóvel", bg="white").place(x=50, y=160)
    tk.Button(root, text="Adicionar", command=adicionar_tel).place(width=80, x=200, y=160)
    tk.Button(root, text="Remover", command=remover_tel).place(width=80, x=300, y=160)
    label_qtd_tel = tk.Label(root, text="0", bg="white")
    label_qtd_tel.place(x=500, y=160)

    tk.Label(root, text="TV", bg="white").place(x=50, y=210)
    tk.Button(root, text="Adicionar", command=adicionar_tv).place(width=80, x=200, y=210)
    tk.Button(root, text="Remover", command=remover_tv).place(width=80, x=300, y=210)
    label_qtd_tv = tk.Label(root, text="0", bg="white")
    label_qtd_tv.place(x=500, y=210)

    tk.Label(root, text="Fones", bg="white").place(x=50, y=260)
    tk.Button(root, text="Adicionar", command=adicionar_fones).place(width=80, x=200, y=260)
    tk.Button(root, text="Remover", command=remover_fones).place(width=80, x=300, y=260)
    label_qtd_fones = tk.Label(root, text="0", bg="white")
    label_qtd_fones.place(x=500, y=260)

    tk.Label(root, text="Rato", bg="white").place(x=50, y=310)
    tk.Button(root, text="Adicionar", command=adicionar_rato).place(width=80, x=200, y=310)
    tk.Button(root, text="Remover", command=remover_rato).place(width=80, x=300, y=310)
    label_qtd_rato = tk.Label(root, text="0", bg="white")
    label_qtd_rato.place(x=500, y=310)

    label_carrinho = tk.Label(root, text="Carrinho: 0 produtos", bg="white")
    label_carrinho.place(x=50, y=380)

    tk.Button(root, text="Pagar", command=pagar).place(width=150, x=225, y=430)
    tk.Button(root, text="Apagar carrinho", command=apagar_carrinho).place(width=150, x=225, y=470)
    tk.Button(root, text="Sair da conta", command=sair_conta).place(width=150, x=225, y=510)

    atualizar_quantidades()
    atualizar_carrinho()


root = tk.Tk()
root.title("Loja do Zé")
root.geometry("600x600")

branco = "#ddf6f9"
root.configure(bg=branco)

mostrar_menu()

root.mainloop()
