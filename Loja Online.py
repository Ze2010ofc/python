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


def atualizar_carrinho():
    total = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato
    label_carrinho.config(text="Carrinho: " + str(total) + " produtos")


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


def pagar():
    total_produtos = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato
    total_preco = qtd_pc * preco_pc + qtd_tel * preco_tel + qtd_tv * preco_tv + qtd_fones * preco_fones + qtd_rato * preco_rato

    janela = tk.Toplevel(root)
    janela.title("Pagamento")
    janela.geometry("300x200")
    janela.configure(bg=branco)

    tk.Label(janela, text="Total de produtos: " + str(total_produtos), bg="white").place(x=50, y=60)
    tk.Label(janela, text="Preço total: " + str(total_preco) + "€", bg="white").place(x=50, y=100)


root = tk.Tk()
root.title("Loja do Zé")
root.geometry("600x600")

branco = "#ddf6f9"
root.configure(bg=branco)

tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=180, y=10)

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

root.mainloop()