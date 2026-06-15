import tkinter as tk
from tkinter import messagebox

preco_microondas = 80
preco_frigorifico = 300
preco_aspirador = 90

preco_pc_gaming = 900
preco_headset = 35
preco_rato_gaming = 25

preco_telemovel = 200
preco_powerbank = 20
preco_carregador = 15

qtd_microondas = 0
qtd_frigorifico = 0
qtd_aspirador = 0

qtd_pc_gaming = 0
qtd_headset = 0
qtd_rato_gaming = 0

qtd_telemovel = 0
qtd_powerbank = 0
qtd_carregador = 0

username_atual = ""

ficheiro_contas = "contas.txt"


def limpar_janela():
    for coisa in root.winfo_children():
        coisa.destroy()


def ver_se_conta_existe(username):
    try:
        ficheiro = open(ficheiro_contas, "r")
        linhas = ficheiro.readlines()
        ficheiro.close()

        for linha in linhas:
            dados = linha.strip().split(";")

            if len(dados) >= 2:
                if dados[0] == username:
                    return True

    except FileNotFoundError:
        return False

    return False


def criar_conta():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Erro", "Tens de escrever username e password.")
    else:
        if ver_se_conta_existe(username):
            messagebox.showerror("Erro", "Essa conta já existe.")
        else:
            ficheiro = open(ficheiro_contas, "a")
            ficheiro.write(username + ";" + password + "\n")
            ficheiro.close()

            messagebox.showinfo("Conta criada", "Conta criada com sucesso.")


def iniciar_sessao():
    global username_atual

    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Erro", "Tens de escrever username e password.")
    else:
        try:
            ficheiro = open(ficheiro_contas, "r")
            linhas = ficheiro.readlines()
            ficheiro.close()

            encontrou = False

            for linha in linhas:
                dados = linha.strip().split(";")

                if len(dados) >= 2:
                    if dados[0] == username and dados[1] == password:
                        encontrou = True

            if encontrou == True:
                username_atual = username
                mostrar_loja()
            else:
                messagebox.showerror("Erro", "Username ou password incorretos.")

        except FileNotFoundError:
            messagebox.showerror("Erro", "Ainda não existe nenhuma conta criada.")


def atualizar_carrinho():
    total = qtd_microondas + qtd_frigorifico + qtd_aspirador
    total = total + qtd_pc_gaming + qtd_headset + qtd_rato_gaming
    total = total + qtd_telemovel + qtd_powerbank + qtd_carregador

    label_carrinho.config(text="Carrinho: " + str(total) + " produtos")

    label_qtd_microondas.config(text=str(qtd_microondas))
    label_qtd_frigorifico.config(text=str(qtd_frigorifico))
    label_qtd_aspirador.config(text=str(qtd_aspirador))

    label_qtd_pc_gaming.config(text=str(qtd_pc_gaming))
    label_qtd_headset.config(text=str(qtd_headset))
    label_qtd_rato_gaming.config(text=str(qtd_rato_gaming))

    label_qtd_telemovel.config(text=str(qtd_telemovel))
    label_qtd_powerbank.config(text=str(qtd_powerbank))
    label_qtd_carregador.config(text=str(qtd_carregador))


def adicionar_microondas():
    global qtd_microondas
    qtd_microondas = qtd_microondas + 1
    atualizar_carrinho()


def remover_microondas():
    global qtd_microondas
    if qtd_microondas > 0:
        qtd_microondas = qtd_microondas - 1
    atualizar_carrinho()


def adicionar_frigorifico():
    global qtd_frigorifico
    qtd_frigorifico = qtd_frigorifico + 1
    atualizar_carrinho()


def remover_frigorifico():
    global qtd_frigorifico
    if qtd_frigorifico > 0:
        qtd_frigorifico = qtd_frigorifico - 1
    atualizar_carrinho()


def adicionar_aspirador():
    global qtd_aspirador
    qtd_aspirador = qtd_aspirador + 1
    atualizar_carrinho()


def remover_aspirador():
    global qtd_aspirador
    if qtd_aspirador > 0:
        qtd_aspirador = qtd_aspirador - 1
    atualizar_carrinho()


def adicionar_pc_gaming():
    global qtd_pc_gaming
    qtd_pc_gaming = qtd_pc_gaming + 1
    atualizar_carrinho()


def remover_pc_gaming():
    global qtd_pc_gaming
    if qtd_pc_gaming > 0:
        qtd_pc_gaming = qtd_pc_gaming - 1
    atualizar_carrinho()


def adicionar_headset():
    global qtd_headset
    qtd_headset = qtd_headset + 1
    atualizar_carrinho()


def remover_headset():
    global qtd_headset
    if qtd_headset > 0:
        qtd_headset = qtd_headset - 1
    atualizar_carrinho()


def adicionar_rato_gaming():
    global qtd_rato_gaming
    qtd_rato_gaming = qtd_rato_gaming + 1
    atualizar_carrinho()


def remover_rato_gaming():
    global qtd_rato_gaming
    if qtd_rato_gaming > 0:
        qtd_rato_gaming = qtd_rato_gaming - 1
    atualizar_carrinho()


def adicionar_telemovel():
    global qtd_telemovel
    qtd_telemovel = qtd_telemovel + 1
    atualizar_carrinho()


def remover_telemovel():
    global qtd_telemovel
    if qtd_telemovel > 0:
        qtd_telemovel = qtd_telemovel - 1
    atualizar_carrinho()


def adicionar_powerbank():
    global qtd_powerbank
    qtd_powerbank = qtd_powerbank + 1
    atualizar_carrinho()


def remover_powerbank():
    global qtd_powerbank
    if qtd_powerbank > 0:
        qtd_powerbank = qtd_powerbank - 1
    atualizar_carrinho()


def adicionar_carregador():
    global qtd_carregador
    qtd_carregador = qtd_carregador + 1
    atualizar_carrinho()


def remover_carregador():
    global qtd_carregador
    if qtd_carregador > 0:
        qtd_carregador = qtd_carregador - 1
    atualizar_carrinho()


def confirmar_pagamento():
    nif = entry_nif.get()

    if nif == "":
        messagebox.showerror("Erro", "Tens de colocar o número de contribuinte.")
    else:
        messagebox.showinfo("Pagamento", "Pagamento confirmado.\nNúmero de contribuinte: " + nif)
        janela_pagamento.destroy()


def pagar():
    global entry_nif, janela_pagamento

    total_produtos = qtd_microondas + qtd_frigorifico + qtd_aspirador
    total_produtos = total_produtos + qtd_pc_gaming + qtd_headset + qtd_rato_gaming
    total_produtos = total_produtos + qtd_telemovel + qtd_powerbank + qtd_carregador

    total_preco = qtd_microondas * preco_microondas
    total_preco = total_preco + qtd_frigorifico * preco_frigorifico
    total_preco = total_preco + qtd_aspirador * preco_aspirador
    total_preco = total_preco + qtd_pc_gaming * preco_pc_gaming
    total_preco = total_preco + qtd_headset * preco_headset
    total_preco = total_preco + qtd_rato_gaming * preco_rato_gaming
    total_preco = total_preco + qtd_telemovel * preco_telemovel
    total_preco = total_preco + qtd_powerbank * preco_powerbank
    total_preco = total_preco + qtd_carregador * preco_carregador

    if total_produtos == 0:
        messagebox.showerror("Erro", "O carrinho está vazio.")
    else:
        janela_pagamento = tk.Toplevel(root)
        janela_pagamento.title("Pagamento")
        janela_pagamento.geometry("350x270")
        janela_pagamento.configure(bg=branco)

        tk.Label(janela_pagamento, text="Total de produtos: " + str(total_produtos), bg="white").place(x=50, y=50)
        tk.Label(janela_pagamento, text="Preço total = " + str(total_preco) + "€", bg="white").place(x=50, y=90)

        tk.Label(janela_pagamento, text="Número de contribuinte:", bg="white").place(x=50, y=130)

        entry_nif = tk.Entry(janela_pagamento)
        entry_nif.place(width=160, x=50, y=160)

        tk.Button(janela_pagamento, text="Confirmar", command=confirmar_pagamento).place(width=120, x=110, y=210)


def mostrar_menu():
    global entry_username, entry_password

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=210, y=50)

    tk.Label(root, text="Username", bg="white").place(x=180, y=150)
    entry_username = tk.Entry(root)
    entry_username.place(width=180, x=290, y=150)

    tk.Label(root, text="Password", bg="white").place(x=180, y=200)
    entry_password = tk.Entry(root, show="*")
    entry_password.place(width=180, x=290, y=200)

    tk.Button(root, text="Iniciar sessão", command=iniciar_sessao).place(width=130, x=190, y=270)
    tk.Button(root, text="Criar conta", command=criar_conta).place(width=130, x=340, y=270)


def mostrar_loja():
    global label_qtd_microondas, label_qtd_frigorifico, label_qtd_aspirador
    global label_qtd_pc_gaming, label_qtd_headset, label_qtd_rato_gaming
    global label_qtd_telemovel, label_qtd_powerbank, label_qtd_carregador
    global label_carrinho

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=210, y=10)
    tk.Label(root, text="Conta: " + username_atual, bg="white").place(x=50, y=55)

    tk.Label(root, text="Produto", bg="white").place(x=50, y=85)
    tk.Label(root, text="Preço", bg="white").place(x=200, y=85)
    tk.Label(root, text="No carrinho", bg="white").place(x=520, y=85)

    tk.Label(root, text="Eletrodomésticos", bg=branco, font=("Arial", 14)).place(x=50, y=120)

    tk.Label(root, text="Microondas", bg="white").place(x=50, y=155)
    tk.Label(root, text="Preço = " + str(preco_microondas) + "€", bg="white").place(x=200, y=155)
    tk.Button(root, text="Adicionar", command=adicionar_microondas).place(width=80, x=300, y=155)
    tk.Button(root, text="Remover", command=remover_microondas).place(width=80, x=400, y=155)
    label_qtd_microondas = tk.Label(root, text="0", bg="white")
    label_qtd_microondas.place(x=555, y=155)

    tk.Label(root, text="Frigorífico", bg="white").place(x=50, y=190)
    tk.Label(root, text="Preço = " + str(preco_frigorifico) + "€", bg="white").place(x=200, y=190)
    tk.Button(root, text="Adicionar", command=adicionar_frigorifico).place(width=80, x=300, y=190)
    tk.Button(root, text="Remover", command=remover_frigorifico).place(width=80, x=400, y=190)
    label_qtd_frigorifico = tk.Label(root, text="0", bg="white")
    label_qtd_frigorifico.place(x=555, y=190)

    tk.Label(root, text="Aspirador", bg="white").place(x=50, y=225)
    tk.Label(root, text="Preço = " + str(preco_aspirador) + "€", bg="white").place(x=200, y=225)
    tk.Button(root, text="Adicionar", command=adicionar_aspirador).place(width=80, x=300, y=225)
    tk.Button(root, text="Remover", command=remover_aspirador).place(width=80, x=400, y=225)
    label_qtd_aspirador = tk.Label(root, text="0", bg="white")
    label_qtd_aspirador.place(x=555, y=225)

    tk.Label(root, text="Gaming", bg=branco, font=("Arial", 14)).place(x=50, y=270)

    tk.Label(root, text="PC Gaming", bg="white").place(x=50, y=305)
    tk.Label(root, text="Preço = " + str(preco_pc_gaming) + "€", bg="white").place(x=200, y=305)
    tk.Button(root, text="Adicionar", command=adicionar_pc_gaming).place(width=80, x=300, y=305)
    tk.Button(root, text="Remover", command=remover_pc_gaming).place(width=80, x=400, y=305)
    label_qtd_pc_gaming = tk.Label(root, text="0", bg="white")
    label_qtd_pc_gaming.place(x=555, y=305)

    tk.Label(root, text="Headset", bg="white").place(x=50, y=340)
    tk.Label(root, text="Preço = " + str(preco_headset) + "€", bg="white").place(x=200, y=340)
    tk.Button(root, text="Adicionar", command=adicionar_headset).place(width=80, x=300, y=340)
    tk.Button(root, text="Remover", command=remover_headset).place(width=80, x=400, y=340)
    label_qtd_headset = tk.Label(root, text="0", bg="white")
    label_qtd_headset.place(x=555, y=340)

    tk.Label(root, text="Rato Gaming", bg="white").place(x=50, y=375)
    tk.Label(root, text="Preço = " + str(preco_rato_gaming) + "€", bg="white").place(x=200, y=375)
    tk.Button(root, text="Adicionar", command=adicionar_rato_gaming).place(width=80, x=300, y=375)
    tk.Button(root, text="Remover", command=remover_rato_gaming).place(width=80, x=400, y=375)
    label_qtd_rato_gaming = tk.Label(root, text="0", bg="white")
    label_qtd_rato_gaming.place(x=555, y=375)

    tk.Label(root, text="Telemóveis", bg=branco, font=("Arial", 14)).place(x=50, y=420)

    tk.Label(root, text="Telemóvel", bg="white").place(x=50, y=455)
    tk.Label(root, text="Preço = " + str(preco_telemovel) + "€", bg="white").place(x=200, y=455)
    tk.Button(root, text="Adicionar", command=adicionar_telemovel).place(width=80, x=300, y=455)
    tk.Button(root, text="Remover", command=remover_telemovel).place(width=80, x=400, y=455)
    label_qtd_telemovel = tk.Label(root, text="0", bg="white")
    label_qtd_telemovel.place(x=555, y=455)

    tk.Label(root, text="Powerbank", bg="white").place(x=50, y=490)
    tk.Label(root, text="Preço = " + str(preco_powerbank) + "€", bg="white").place(x=200, y=490)
    tk.Button(root, text="Adicionar", command=adicionar_powerbank).place(width=80, x=300, y=490)
    tk.Button(root, text="Remover", command=remover_powerbank).place(width=80, x=400, y=490)
    label_qtd_powerbank = tk.Label(root, text="0", bg="white")
    label_qtd_powerbank.place(x=555, y=490)

    tk.Label(root, text="Carregador", bg="white").place(x=50, y=525)
    tk.Label(root, text="Preço = " + str(preco_carregador) + "€", bg="white").place(x=200, y=525)
    tk.Button(root, text="Adicionar", command=adicionar_carregador).place(width=80, x=300, y=525)
    tk.Button(root, text="Remover", command=remover_carregador).place(width=80, x=400, y=525)
    label_qtd_carregador = tk.Label(root, text="0", bg="white")
    label_qtd_carregador.place(x=555, y=525)

    label_carrinho = tk.Label(root, text="Carrinho: 0 produtos", bg="white")
    label_carrinho.place(x=50, y=590)

    tk.Button(root, text="Proceder ao pagamento", command=pagar).place(width=180, x=220, y=585)

    atualizar_carrinho()


root = tk.Tk()
root.title("Loja do Zé")
root.geometry("650x680")

branco = "#ff0000"
root.configure(bg=branco)

mostrar_menu()

root.mainloop()
