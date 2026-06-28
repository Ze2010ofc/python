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
            messagebox.showerror("Erro", "Essa conta ainda não foi criada.")


def sair():
    global qtd_microondas, qtd_frigorifico, qtd_aspirador
    global qtd_pc_gaming, qtd_headset, qtd_rato_gaming
    global qtd_telemovel, qtd_powerbank, qtd_carregador
    global username_atual

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

    mostrar_menu()


def limpar_carrinho():
    global qtd_microondas, qtd_frigorifico, qtd_aspirador
    global qtd_pc_gaming, qtd_headset, qtd_rato_gaming
    global qtd_telemovel, qtd_powerbank, qtd_carregador

    total_atual = qtd_microondas + qtd_frigorifico + qtd_aspirador
    total_atual = total_atual + qtd_pc_gaming + qtd_headset + qtd_rato_gaming
    total_atual = total_atual + qtd_telemovel + qtd_powerbank + qtd_carregador

    if total_atual == 0:
        messagebox.showerror("Erro", "O carrinho está vazio.")
    else:
        qtd_microondas = 0
        qtd_frigorifico = 0
        qtd_aspirador = 0
        qtd_pc_gaming = 0
        qtd_headset = 0
        qtd_rato_gaming = 0
        qtd_telemovel = 0
        qtd_powerbank = 0
        qtd_carregador = 0

        atualizar_carrinho()


def atualizar_carrinho():
    total = qtd_microondas + qtd_frigorifico + qtd_aspirador
    total = total + qtd_pc_gaming + qtd_headset + qtd_rato_gaming
    total = total + qtd_telemovel + qtd_powerbank + qtd_carregador

    label_carrinho.config(text="Carrinho: " + str(total) + " produtos")

    label_qtd_microondas.config(text=str(qtd_microondas))
    label_qtd_frigorifico.config(text=str(qtd_frigorifico))
    label_qtd_aspirador.config(text=str(qtd_frigorifico))
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
    elif nif.isdigit() == False:
        messagebox.showerror("Erro", "O número de contribuinte só pode ter números.")
    elif len(nif) != 9:
        messagebox.showerror("Erro", "O número de contribuinte tem de ter exatamente 9 dígitos.")
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
        janela_pagamento.geometry("350x300")
        janela_pagamento.configure(bg=fundo)

        tk.Label(janela_pagamento, text="Pagamento", bg=banner, fg=texto_claro, font=("Arial", 16)).place(x=0, y=0, width=360, height=45)

        tk.Label(janela_pagamento, text="Total de produtos: " + str(total_produtos), bg=fundo, fg=texto_preto).place(x=50, y=65)
        tk.Label(janela_pagamento, text="Preço total = " + str(total_preco) + "€", bg=fundo, fg=banner, font=("Arial", 10, "bold")).place(x=50, y=100)

        tk.Label(janela_pagamento, text="Número de contribuinte:", bg=fundo, fg=texto_preto).place(x=50, y=145)

        entry_nif = tk.Entry(janela_pagamento, relief="solid", bd=1)
        entry_nif.place(width=160, x=50, y=170)

        tk.Button(janela_pagamento, text="Confirmar", command=confirmar_pagamento, bg=btn_pagar, fg=texto_claro, relief="flat").place(width=120, x=110, y=230)


def mostrar_menu():
    global entry_username, entry_password

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=banner, fg=texto_claro, font=("Arial", 28), anchor="center").place(x=0, y=0, width=660, height=60)

    tk.Label(root, bg=painel_login).place(x=130, y=110, width=390, height=200)

    tk.Label(root, text="Username", bg=painel_login, fg=texto_preto).place(x=165, y=150)
    entry_username = tk.Entry(root, relief="solid", bd=1)
    entry_username.place(width=180, x=255, y=150)

    tk.Label(root, text="Password", bg=painel_login, fg=texto_preto).place(x=165, y=195)
    entry_password = tk.Entry(root, show="*", relief="solid", bd=1)
    entry_password.place(width=180, x=255, y=195)

    tk.Button(root, text="Iniciar sessão", command=iniciar_sessao, bg=banner, fg=texto_claro, relief="flat").place(width=130, x=175, y=260)
    tk.Button(root, text="Criar conta", command=criar_conta, bg=banner, fg=texto_claro, relief="flat").place(width=130, x=315, y=260)


def mostrar_loja():
    global label_qtd_microondas, label_qtd_frigorifico, label_qtd_aspirador
    global label_qtd_pc_gaming, label_qtd_headset, label_qtd_rato_gaming
    global label_qtd_telemovel, label_qtd_powerbank, label_qtd_carregador
    global label_carrinho

    limpar_janela()

    tk.Label(root, text="Loja do Zé", bg=banner, fg=texto_claro, font=("Arial", 28), anchor="center").place(x=0, y=0, width=660, height=60)

    tk.Label(root, text="Conta: " + username_atual, bg=fundo, fg=cinzento_medio).place(x=50, y=68)

    tk.Button(root, text="Sair", command=sair, bg=btn_remover, fg=texto_claro, relief="flat").place(width=60, height=25, x=560, y=68)

    tk.Label(root, text="Produto", bg=fundo, fg=cinzento_escuro, font=("Arial", 9, "bold")).place(x=50, y=95)
    tk.Label(root, text="Preço", bg=fundo, fg=cinzento_escuro, font=("Arial", 9, "bold")).place(x=200, y=95)
    tk.Label(root, text="No carrinho", bg=fundo, fg=cinzento_escuro, font=("Arial", 9, "bold")).place(x=490, y=95)

    tk.Frame(root, bg=separador).place(x=30, y=113, width=600, height=1)

    tk.Label(root, text="Eletrodomésticos", bg=fundo, fg=banner, font=("Arial", 11, "bold")).place(x=50, y=120)

    tk.Label(root, bg=fundo).place(x=30, y=140, width=600, height=25)
    tk.Label(root, text="Microondas", bg=fundo, fg=texto_preto).place(x=50, y=143)
    tk.Label(root, text="Preço = " + str(preco_microondas) + "€", bg=fundo, fg=banner).place(x=200, y=143)
    tk.Button(root, text="Adicionar", command=adicionar_microondas, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=141)
    tk.Button(root, text="Remover", command=remover_microondas, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=141)
    label_qtd_microondas = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_microondas.place(x=490, y=143)
    tk.Frame(root, bg=separador).place(x=30, y=165, width=600, height=1)

    tk.Label(root, bg=zebra).place(x=30, y=166, width=600, height=25)
    tk.Label(root, text="Frigorífico", bg=zebra, fg=texto_preto).place(x=50, y=169)
    tk.Label(root, text="Preço = " + str(preco_frigorifico) + "€", bg=zebra, fg=banner).place(x=200, y=169)
    tk.Button(root, text="Adicionar", command=adicionar_frigorifico, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=167)
    tk.Button(root, text="Remover", command=remover_frigorifico, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=167)
    label_qtd_frigorifico = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_frigorifico.place(x=490, y=169)
    tk.Frame(root, bg=separador).place(x=30, y=191, width=600, height=1)

    tk.Label(root, bg=fundo).place(x=30, y=192, width=600, height=25)
    tk.Label(root, text="Aspirador", bg=fundo, fg=texto_preto).place(x=50, y=195)
    tk.Label(root, text="Preço = " + str(preco_aspirador) + "€", bg=fundo, fg=banner).place(x=200, y=195)
    tk.Button(root, text="Adicionar", command=adicionar_aspirador, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=193)
    tk.Button(root, text="Remover", command=remover_aspirador, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=193)
    label_qtd_aspirador = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_aspirador.place(x=490, y=195)
    tk.Frame(root, bg=separador).place(x=30, y=217, width=600, height=1)

    tk.Label(root, text="Gaming", bg=fundo, fg=banner, font=("Arial", 11, "bold")).place(x=50, y=224)

    tk.Label(root, bg=zebra).place(x=30, y=244, width=600, height=25)
    tk.Label(root, text="PC Gaming", bg=zebra, fg=texto_preto).place(x=50, y=247)
    tk.Label(root, text="Preço = " + str(preco_pc_gaming) + "€", bg=zebra, fg=banner).place(x=200, y=247)
    tk.Button(root, text="Adicionar", command=adicionar_pc_gaming, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=245)
    tk.Button(root, text="Remover", command=remover_pc_gaming, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=245)
    label_qtd_pc_gaming = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_pc_gaming.place(x=490, y=247)
    tk.Frame(root, bg=separador).place(x=30, y=269, width=600, height=1)

    tk.Label(root, bg=fundo).place(x=30, y=270, width=600, height=25)
    tk.Label(root, text="Headset", bg=fundo, fg=texto_preto).place(x=50, y=273)
    tk.Label(root, text="Preço = " + str(preco_headset) + "€", bg=fundo, fg=banner).place(x=200, y=273)
    tk.Button(root, text="Adicionar", command=adicionar_headset, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=271)
    tk.Button(root, text="Remover", command=remover_headset, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=271)
    label_qtd_headset = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_headset.place(x=490, y=273)
    tk.Frame(root, bg=separador).place(x=30, y=295, width=600, height=1)

    tk.Label(root, bg=zebra).place(x=30, y=296, width=600, height=25)
    tk.Label(root, text="Rato Gaming", bg=zebra, fg=texto_preto).place(x=50, y=299)
    tk.Label(root, text="Preço = " + str(preco_rato_gaming) + "€", bg=zebra, fg=banner).place(x=200, y=299)
    tk.Button(root, text="Adicionar", command=adicionar_rato_gaming, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=297)
    tk.Button(root, text="Remover", command=remover_rato_gaming, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=297)
    label_qtd_rato_gaming = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_rato_gaming.place(x=490, y=299)
    tk.Frame(root, bg=separador).place(x=30, y=321, width=600, height=1)

    tk.Label(root, text="Telemóveis", bg=fundo, fg=banner, font=("Arial", 11, "bold")).place(x=50, y=328)

    tk.Label(root, bg=fundo).place(x=30, y=348, width=600, height=25)
    tk.Label(root, text="Telemóvel", bg=fundo, fg=texto_preto).place(x=50, y=351)
    tk.Label(root, text="Preço = " + str(preco_telemovel) + "€", bg=fundo, fg=banner).place(x=200, y=351)
    tk.Button(root, text="Adicionar", command=adicionar_telemovel, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=349)
    tk.Button(root, text="Remover", command=remover_telemovel, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=349)
    label_qtd_telemovel = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_telemovel.place(x=490, y=351)
    tk.Frame(root, bg=separador).place(x=30, y=373, width=600, height=1)

    tk.Label(root, bg=zebra).place(x=30, y=374, width=600, height=25)
    tk.Label(root, text="Powerbank", bg=zebra, fg=texto_preto).place(x=50, y=377)
    tk.Label(root, text="Preço = " + str(preco_powerbank) + "€", bg=zebra, fg=banner).place(x=200, y=377)
    tk.Button(root, text="Adicionar", command=adicionar_powerbank, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=375)
    tk.Button(root, text="Remover", command=remover_powerbank, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=375)
    label_qtd_powerbank = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_powerbank.place(x=490, y=377)
    tk.Frame(root, bg=separador).place(x=30, y=399, width=600, height=1)

    tk.Label(root, bg=fundo).place(x=30, y=400, width=600, height=25)
    tk.Label(root, text="Carregador", bg=fundo, fg=texto_preto).place(x=50, y=403)
    tk.Label(root, text="Preço = " + str(preco_carregador) + "€", bg=fundo, fg=banner).place(x=200, y=403)
    tk.Button(root, text="Adicionar", command=adicionar_carregador, bg=banner, fg=texto_claro, relief="flat").place(width=80, x=300, y=401)
    tk.Button(root, text="Remover", command=remover_carregador, bg=btn_remover, fg=texto_claro, relief="flat").place(width=80, x=390, y=401)
    label_qtd_carregador = tk.Label(root, text="0", bg=cinzento_claro, fg=texto_preto, width=3)
    label_qtd_carregador.place(x=490, y=403)
    tk.Frame(root, bg=separador).place(x=30, y=425, width=600, height=1)

    tk.Frame(root, bg=separador).place(x=30, y=450, width=600, height=2)

    label_carrinho = tk.Label(root, text="Carrinho: 0 produtos", bg=fundo, fg=texto_preto, font=("Arial", 9, "bold"))
    label_carrinho.place(x=50, y=465)

    tk.Button(root, text="Limpar carrinho", command=limpar_carrinho, bg=btn_remover, fg=texto_claro, relief="flat").place(width=130, height=35, x=50, y=490)
    tk.Button(root, text="Proceder ao pagamento", command=pagar, bg=btn_pagar, fg=texto_claro, relief="flat").place(width=200, height=35, x=390, y=490)

    atualizar_carrinho()


root = tk.Tk()
root.title("Loja do Zé")
root.geometry("650x545")

fundo = "#ffffff"
banner = "#cc0000"
texto_claro = "#ffffff"
texto_preto = "#1a1a1a"
cinzento_escuro = "#444444"
cinzento_medio = "#666666"
cinzento_claro = "#e8e8e8"
painel_login = "#f2f2f2"
zebra = "#f7f7f7"
separador = "#e0e0e0"
btn_remover = "#333333"
btn_pagar = "#ff6600"

root.configure(bg=fundo)

mostrar_menu()

root.mainloop()
