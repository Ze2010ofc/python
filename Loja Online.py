import tkinter as tk
from tkinter import messagebox

preco_pc = 1450
preco_tel = 900
preco_tv = 1000
preco_fones = 20
preco_rato = 50
preco_ = 50
preco_teclado = 45
preco_relogio = 30
preco_tapete = 15
preco_carregador = 5
preco_powerbank = 10

qtd_pc = 0
qtd_tel = 0
qtd_tv = 0
qtd_fones = 0
qtd_rato = 0
qtd_teclado = 0
qtd_relogio = 0
qtd_tapete = 0
qtd_carregador = 0
qtd_powerbank = 0


def atualizar_carrinho():
    total = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato + qtd_teclado + qtd_relogio + qtd_tapete + qtd_carregador + qtd_powerbank
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


def adicionar_teclado():
    global qtd_teclado
    qtd_teclado = qtd_teclado + 1
    label_qtd_teclado.config(text=str(qtd_teclado))
    atualizar_carrinho()


def remover_teclado():
    global qtd_teclado
    if qtd_teclado > 0:
        qtd_teclado = qtd_teclado - 1
    label_qtd_teclado.config(text=str(qtd_teclado))
    atualizar_carrinho()


def adicionar_relogio():
    global qtd_relogio
    qtd_relogio = qtd_relogio + 1
    label_qtd_relogio.config(text=str(qtd_relogio))
    atualizar_carrinho()


def remover_relogio():
    global qtd_relogio
    if qtd_relogio > 0:
        qtd_relogio = qtd_relogio - 1
    label_qtd_relogio.config(text=str(qtd_relogio))
    atualizar_carrinho()


def adicionar_tapete():
    global qtd_tapete
    qtd_tapete = qtd_tapete + 1
    label_qtd_tapete.config(text=str(qtd_tapete))
    atualizar_carrinho()


def remover_tapete():
    global qtd_tapete
    if qtd_tapete > 0:
        qtd_tapete = qtd_tapete - 1
    label_qtd_tapete.config(text=str(qtd_tapete))
    atualizar_carrinho()


def adicionar_carregador():
    global qtd_carregador
    qtd_carregador = qtd_carregador + 1
    label_qtd_carregador.config(text=str(qtd_carregador))
    atualizar_carrinho()


def remover_carregador():
    global qtd_carregador
    if qtd_carregador > 0:
        qtd_carregador = qtd_carregador - 1
    label_qtd_carregador.config(text=str(qtd_carregador))
    atualizar_carrinho()


def adicionar_powerbank():
    global qtd_powerbank
    qtd_powerbank = qtd_powerbank + 1
    label_qtd_powerbank.config(text=str(qtd_powerbank))
    atualizar_carrinho()


def remover_powerbank():
    global qtd_powerbank
    if qtd_powerbank > 0:
        qtd_powerbank = qtd_powerbank - 1
    label_qtd_powerbank.config(text=str(qtd_powerbank))
    atualizar_carrinho()


def pagar():
    total_produtos = qtd_pc + qtd_tel + qtd_tv + qtd_fones + qtd_rato + qtd_teclado + qtd_relogio + qtd_tapete + qtd_carregador + qtd_powerbank
    total_preco = qtd_pc * preco_pc + qtd_tel * preco_tel + qtd_tv * preco_tv + qtd_fones * preco_fones + qtd_rato * preco_rato + qtd_teclado * preco_teclado + qtd_relogio * preco_relogio + qtd_tapete * preco_tapete + qtd_carregador * preco_carregador + qtd_powerbank * preco_powerbank

    janela = tk.Toplevel(root)
    janela.title("Pagamento")
    janela.geometry("300x200")
    janela.configure(bg=branco)

    tk.Label(janela, text="Total de produtos: " + str(total_produtos), bg="white").place(x=50, y=30)
    tk.Label(janela, text="Preço total: " + str(total_preco) + "€", bg="white").place(x=50, y=70)
    tk.Button(janela, text="Fechar", command=janela.destroy).place(width=100, x=100, y=120)


root = tk.Tk()
root.title("Loja do Zé")
root.geometry("600x620")

branco = "#ddf6f9"
root.configure(bg=branco)

tk.Label(root, text="Loja do Zé", bg=branco, font=("Arial", 28)).place(x=180, y=10)

tk.Label(root, text="Produto", bg="white").place(x=50, y=65)
tk.Label(root, text="No carrinho", bg="white").place(x=480, y=65)

tk.Label(root, text="PC Gamer", bg="white").place(x=50, y=100)
tk.Button(root, text="Adicionar", command=adicionar_pc).place(width=80, x=200, y=100)
tk.Button(root, text="Remover", command=remover_pc).place(width=80, x=300, y=100)
label_qtd_pc = tk.Label(root, text="0", bg="white")
label_qtd_pc.place(x=500, y=100)

tk.Label(root, text="Telemóvel", bg="white").place(x=50, y=140)
tk.Button(root, text="Adicionar", command=adicionar_tel).place(width=80, x=200, y=140)
tk.Button(root, text="Remover", command=remover_tel).place(width=80, x=300, y=140)
label_qtd_tel = tk.Label(root, text="0", bg="white")
label_qtd_tel.place(x=500, y=140)

tk.Label(root, text="TV", bg="white").place(x=50, y=180)
tk.Button(root, text="Adicionar", command=adicionar_tv).place(width=80, x=200, y=180)
tk.Button(root, text="Remover", command=remover_tv).place(width=80, x=300, y=180)
label_qtd_tv = tk.Label(root, text="0", bg="white")
label_qtd_tv.place(x=500, y=180)

tk.Label(root, text="Fones", bg="white").place(x=50, y=220)
tk.Button(root, text="Adicionar", command=adicionar_fones).place(width=80, x=200, y=220)
tk.Button(root, text="Remover", command=remover_fones).place(width=80, x=300, y=220)
label_qtd_fones = tk.Label(root, text="0", bg="white")
label_qtd_fones.place(x=500, y=220)

tk.Label(root, text="Rato", bg="white").place(x=50, y=260)
tk.Button(root, text="Adicionar", command=adicionar_rato).place(width=80, x=200, y=260)
tk.Button(root, text="Remover", command=remover_rato).place(width=80, x=300, y=260)
label_qtd_rato = tk.Label(root, text="0", bg="white")
label_qtd_rato.place(x=500, y=260)

tk.Label(root, text="Teclado", bg="white").place(x=50, y=300)
tk.Button(root, text="Adicionar", command=adicionar_teclado).place(width=80, x=200, y=300)
tk.Button(root, text="Remover", command=remover_teclado).place(width=80, x=300, y=300)
label_qtd_teclado = tk.Label(root, text="0", bg="white")
label_qtd_teclado.place(x=500, y=300)

tk.Label(root, text="Relógio", bg="white").place(x=50, y=340)
tk.Button(root, text="Adicionar", command=adicionar_relogio).place(width=80, x=200, y=340)
tk.Button(root, text="Remover", command=remover_relogio).place(width=80, x=300, y=340)
label_qtd_relogio = tk.Label(root, text="0", bg="white")
label_qtd_relogio.place(x=500, y=340)

tk.Label(root, text="Tapete", bg="white").place(x=50, y=380)
tk.Button(root, text="Adicionar", command=adicionar_tapete).place(width=80, x=200, y=380)
tk.Button(root, text="Remover", command=remover_tapete).place(width=80, x=300, y=380)
label_qtd_tapete = tk.Label(root, text="0", bg="white")
label_qtd_tapete.place(x=500, y=380)

tk.Label(root, text="Carregador", bg="white").place(x=50, y=420)
tk.Button(root, text="Adicionar", command=adicionar_carregador).place(width=80, x=200, y=420)
tk.Button(root, text="Remover", command=remover_carregador).place(width=80, x=300, y=420)
label_qtd_carregador = tk.Label(root, text="0", bg="white")
label_qtd_carregador.place(x=500, y=420)

tk.Label(root, text="Powerbank", bg="white").place(x=50, y=460)
tk.Button(root, text="Adicionar", command=adicionar_powerbank).place(width=80, x=200, y=460)
tk.Button(root, text="Remover", command=remover_powerbank).place(width=80, x=300, y=460)
label_qtd_powerbank = tk.Label(root, text="0", bg="white")
label_qtd_powerbank.place(x=500, y=460)

label_carrinho = tk.Label(root, text="Carrinho: 0 produtos", bg="white")
label_carrinho.place(x=50, y=510)

tk.Button(root, text="Pagar", command=pagar).place(width=150, x=225, y=550)

root.mainloop()