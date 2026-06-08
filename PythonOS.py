# -*- coding: utf-8 -*-
"""
PythonOS — Launcher de Aplicações
Uma única app que lança todas as outras em janelas independentes.
Inclui: Calculadora, IMC, Agenda, Jogos, Hub de Ferramentas e muito mais.
"""

import random
import sqlite3
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import re

# ═══════════════════════════════════════════════════════════════════
#  PALETAS
# ═══════════════════════════════════════════════════════════════════

OS_COR = {
    "fundo":      "#0D1117",
    "taskbar":    "#161B22",
    "card":       "#1C2128",
    "card_hover": "#22272E",
    "borda":      "#30363D",
    "azul":       "#2F81F7",
    "azul_esc":   "#1F6FEB",
    "verde":      "#3FB950",
    "amarelo":    "#D29922",
    "vermelho":   "#F85149",
    "roxo":       "#A371F7",
    "cyan":       "#39D353",
    "branco":     "#E6EDF3",
    "muted":      "#7D8590",
    "texto":      "#CDD9E5",
}

# ═══════════════════════════════════════════════════════════════════
#  UTILITÁRIOS COMUNS
# ═══════════════════════════════════════════════════════════════════

def janela_base(titulo, largura, altura, redimensionar=False):
    win = tk.Toplevel()
    win.title(titulo)
    win.geometry(f"{largura}x{altura}")
    win.resizable(redimensionar, redimensionar)
    win.configure(bg=OS_COR["fundo"])
    win.lift()
    win.focus_force()
    return win

def label_titulo(pai, texto, cor=None):
    tk.Label(pai, text=texto,
             font=("Helvetica", 16, "bold"),
             bg=OS_COR["fundo"],
             fg=cor or OS_COR["branco"]).pack(pady=(18, 2))

def label_sub(pai, texto):
    tk.Label(pai, text=texto,
             font=("Helvetica", 9),
             bg=OS_COR["fundo"],
             fg=OS_COR["muted"]).pack(pady=(0, 12))

def painel(pai, **kwargs):
    f = tk.Frame(pai, bg=OS_COR["card"],
                 highlightbackground=OS_COR["borda"],
                 highlightthickness=1, **kwargs)
    return f

def botao(pai, texto, cmd, cor=None, fg="#FFFFFF", **kwargs):
    cor = cor or OS_COR["azul"]
    return tk.Button(pai, text=texto, command=cmd,
                     bg=cor, fg=fg,
                     activebackground=cor,
                     font=("Helvetica", 9, "bold"),
                     relief="flat", cursor="hand2",
                     padx=10, pady=6, **kwargs)

def entrada(pai, var=None, largura=20, **kwargs):
    return tk.Entry(pai, textvariable=var,
                    font=("Helvetica", 11),
                    bg=OS_COR["taskbar"],
                    fg=OS_COR["branco"],
                    insertbackground=OS_COR["azul"],
                    relief="flat",
                    highlightbackground=OS_COR["borda"],
                    highlightthickness=1,
                    highlightcolor=OS_COR["azul"],
                    width=largura, **kwargs)


# ═══════════════════════════════════════════════════════════════════
#  1. CALCULADORA
# ═══════════════════════════════════════════════════════════════════

def abrir_calculadora():
    COR = {
        "fundo": "#1C1C1E", "ecra": "#2C2C2E",
        "btn_num": "#3A3A3C", "btn_op": "#FF9F0A",
        "btn_fn": "#636366", "hover_num": "#4A4A4C",
        "hover_op": "#FFB340", "hover_fn": "#7A7A7E",
        "texto": "#FFFFFF", "muted": "#8E8E93",
        "erro": "#FF453A", "sep": "#3A3A3C",
    }

    def calcular(a, op, b):
        if op == "+": return a + b
        if op == "−": return a - b
        if op == "×": return a * b
        if op == "÷":
            if b == 0: raise ZeroDivisionError
            return a / b

    def formatar(v):
        if abs(v) >= 1e15: return f"{v:.4e}"
        if v == int(v): return str(int(v))
        return f"{v:.10f}".rstrip("0").rstrip(".")

    win = tk.Toplevel()
    win.title("Calculadora")
    win.geometry("320x540")
    win.resizable(False, False)
    win.configure(bg=COR["fundo"])
    win.lift(); win.focus_force()

    s_display = ["0"]
    s_acum    = [None]
    s_op      = [None]
    s_novo    = [False]

    lbl_hist = tk.Label(win, text="", anchor="e",
             font=("Helvetica", 11), bg=COR["ecra"],
             fg=COR["muted"], padx=16, pady=2)
    lbl_hist.pack(fill="x")

    lbl_ecra = tk.Label(win, text="0", anchor="e",
             font=("Helvetica", 52, "bold"),
             bg=COR["ecra"], fg=COR["texto"],
             padx=16, pady=8)
    lbl_ecra.pack(fill="x")
    tk.Frame(win, bg=COR["sep"], height=1).pack(fill="x")

    grade = tk.Frame(win, bg=COR["fundo"])
    grade.pack(fill="both", expand=True, padx=8, pady=8)
    for c in range(4): grade.columnconfigure(c, weight=1, uniform="c")
    for r in range(5): grade.rowconfigure(r, weight=1, uniform="r")

    layout = [
        ("AC","fn",0,0,1),("+/−","fn",0,1,1),("%","fn",0,2,1),("÷","op",0,3,1),
        ("7","num",1,0,1),("8","num",1,1,1),("9","num",1,2,1),("×","op",1,3,1),
        ("4","num",2,0,1),("5","num",2,1,1),("6","num",2,2,1),("−","op",2,3,1),
        ("1","num",3,0,1),("2","num",3,1,1),("3","num",3,2,1),("+","op",3,3,1),
        ("0","num",4,0,2),(",","num",4,2,1),("=","op",4,3,1),
    ]
    cores = {
        "num": (COR["btn_num"], COR["hover_num"]),
        "op":  (COR["btn_op"],  COR["hover_op"]),
        "fn":  (COR["btn_fn"],  COR["hover_fn"]),
    }

    def atualizar_ecra():
        txt = s_display[0].replace(".", ",")
        tam = 52
        if len(txt) > 9:  tam = 36
        if len(txt) > 13: tam = 26
        lbl_ecra.config(text=txt, font=("Helvetica", tam, "bold"), fg=COR["texto"])

    def erro_calc(msg):
        lbl_ecra.config(text=msg, fg=COR["erro"], font=("Helvetica", 28, "bold"))
        s_display[0]="0"; s_acum[0]=None; s_op[0]=None; s_novo[0]=False
        lbl_hist.config(text="")
        win.after(1800, atualizar_ecra)

    def clicar(t):
        if t in "0123456789":
            if s_novo[0] or s_display[0]=="0":
                s_display[0]=t; s_novo[0]=False
            else:
                if len(s_display[0].replace("-","").replace(",","")) < 12:
                    s_display[0]+=t
            atualizar_ecra()
        elif t==",":
            if s_novo[0]: s_display[0]="0,"; s_novo[0]=False
            elif "," not in s_display[0]: s_display[0]+=","
            atualizar_ecra()
        elif t in ("+","−","×","÷"):
            try: atual = float(s_display[0].replace(",","."))
            except: return
            if s_acum[0] is not None and not s_novo[0]:
                try: res = calcular(s_acum[0], s_op[0], atual)
                except ZeroDivisionError: erro_calc("Divisão por zero"); return
                s_acum[0]=res; s_display[0]=formatar(res)
            else: s_acum[0]=atual
            s_op[0]=t; s_novo[0]=True
            lbl_hist.config(text=f"{formatar(s_acum[0])} {t}")
            atualizar_ecra()
        elif t=="=":
            if s_op[0] is None or s_acum[0] is None: return
            try:
                b=float(s_display[0].replace(",",".")); res=calcular(s_acum[0],s_op[0],b)
            except ZeroDivisionError: erro_calc("Divisão por zero"); return
            expr=f"{formatar(s_acum[0])} {s_op[0]} {formatar(b)} ="
            lbl_hist.config(text=expr)
            s_display[0]=formatar(res); s_acum[0]=None; s_op[0]=None; s_novo[0]=True
            atualizar_ecra()
        elif t=="AC":
            s_display[0]="0"; s_acum[0]=None; s_op[0]=None; s_novo[0]=False
            lbl_hist.config(text=""); atualizar_ecra()
        elif t=="+/−":
            try:
                v=float(s_display[0].replace(",",".")); s_display[0]=formatar(-v); atualizar_ecra()
            except: pass
        elif t=="%":
            try:
                v=float(s_display[0].replace(",",".")); s_display[0]=formatar(v/100); atualizar_ecra()
            except: pass
        elif t=="DEL":
            if s_novo[0]: return
            s_display[0] = "0" if len(s_display[0])<=1 else s_display[0][:-1]
            atualizar_ecra()

    for (lbl, tipo, row, col, span) in layout:
        bg, hover = cores[tipo]
        wr = tk.Frame(grade, bg=COR["fundo"], padx=3, pady=3)
        wr.grid(row=row, column=col, columnspan=span, sticky="nsew")
        anchor = "w" if (lbl=="0" and span==2) else "center"
        padx_ = 20 if (lbl=="0" and span==2) else 0
        b = tk.Label(wr, text=lbl, font=("Helvetica",20,"bold"),
                     bg=bg, fg=COR["texto"], anchor=anchor, padx=padx_,
                     cursor="hand2", highlightbackground=COR["fundo"],
                     highlightthickness=2, relief="flat")
        b.pack(fill="both", expand=True)
        b.bind("<Enter>",    lambda e, w=b, c=hover: w.config(bg=c))
        b.bind("<Leave>",    lambda e, w=b, c=bg:    w.config(bg=c))
        b.bind("<Button-1>", lambda e, t=lbl: clicar(t))
        wr.bind("<Button-1>",lambda e, t=lbl: clicar(t))

    win.bind("<Return>",    lambda e: clicar("="))
    win.bind("<KP_Enter>",  lambda e: clicar("="))
    win.bind("<BackSpace>", lambda e: clicar("DEL"))
    win.bind("<Escape>",    lambda e: clicar("AC"))
    win.bind("<plus>",      lambda e: clicar("+"))
    win.bind("<minus>",     lambda e: clicar("−"))
    win.bind("<asterisk>",  lambda e: clicar("×"))
    win.bind("<slash>",     lambda e: clicar("÷"))
    win.bind("<period>",    lambda e: clicar(","))
    win.bind("<comma>",     lambda e: clicar(","))
    win.bind("<KeyPress>",
             lambda e: clicar(e.char) if e.char in "0123456789" else None)


# ═══════════════════════════════════════════════════════════════════
#  2. CALCULADORA DE IMC
# ═══════════════════════════════════════════════════════════════════

def abrir_imc():
    CLASSIF = [
        (0,    18.5, "Abaixo do peso",    "#3B82F6", "#1E3A5F"),
        (18.5, 25.0, "Peso normal",       "#4ADE80", "#14532D"),
        (25.0, 30.0, "Excesso de peso",   "#FACC15", "#3D2E00"),
        (30.0, 35.0, "Obesidade grau I",  "#FB923C", "#431407"),
        (35.0, 40.0, "Obesidade grau II", "#F87171", "#450A0A"),
        (40.0, 999,  "Obesidade grau III","#C084FC", "#3B0764"),
    ]

    def classificar(imc):
        for mn, mx, lbl, cor, bg in CLASSIF:
            if mn <= imc < mx: return lbl, cor, bg
        return "—", OS_COR["muted"], OS_COR["card"]

    win = janela_base("Calculadora de IMC", 420, 560)
    label_titulo(win, "Calculadora de IMC", OS_COR["azul"])
    label_sub(win, "Índice de Massa Corporal — classificação OMS")

    form = painel(win)
    form.pack(padx=28, fill="x")

    def campo(pai, lbl, ph, row):
        tk.Label(pai, text=lbl, font=("Helvetica",9,"bold"),
                 bg=OS_COR["card"], fg=OS_COR["muted"]).grid(
                     row=row*2, column=0, sticky="w", padx=14, pady=(10,0))
        e = entrada(pai, largura=24)
        e.insert(0, ph); e.config(fg=OS_COR["muted"])
        e.grid(row=row*2+1, column=0, sticky="ew", padx=14, pady=(2,0), ipady=4)
        e.bind("<FocusIn>",  lambda ev, en=e, p=ph: (en.delete(0,"end"), en.config(fg=OS_COR["branco"])) if en.get()==p else None)
        e.bind("<FocusOut>", lambda ev, en=e, p=ph: (en.insert(0,p), en.config(fg=OS_COR["muted"])) if not en.get().strip() else None)
        return e

    form.columnconfigure(0, weight=1)
    e_peso   = campo(form, "Peso (kg)", "ex: 70.5", 0)
    tk.Frame(form, bg=OS_COR["borda"], height=1).grid(row=2, column=0, sticky="ew", padx=14)
    e_altura = campo(form, "Altura (m)", "ex: 1.75", 1)

    res_frame = painel(win)
    res_frame.pack(padx=28, pady=(10,0), fill="x")
    res_frame.columnconfigure(0, weight=1)

    lbl_imc    = tk.Label(res_frame, text="—", font=("Helvetica",38,"bold"),
                          bg=OS_COR["card"], fg=OS_COR["branco"])
    lbl_imc.grid(row=0, column=0, sticky="w", padx=16, pady=(12,0))
    lbl_cls    = tk.Label(res_frame, text="", font=("Helvetica",12,"bold"),
                          bg=OS_COR["card"], fg=OS_COR["muted"])
    lbl_cls.grid(row=1, column=0, sticky="w", padx=16)
    canvas_bar = tk.Canvas(res_frame, height=12, bg=OS_COR["taskbar"],
                           highlightthickness=0)
    canvas_bar.grid(row=2, column=0, sticky="ew", padx=16, pady=(6,4))
    lbl_ideal  = tk.Label(res_frame, text="", font=("Helvetica",9),
                          bg=OS_COR["card"], fg=OS_COR["muted"])
    lbl_ideal.grid(row=3, column=0, sticky="w", padx=16, pady=(0,12))

    def desenhar_barra(imc, cor):
        canvas_bar.update_idletasks()
        w = canvas_bar.winfo_width()
        canvas_bar.delete("all")
        cores_seg = ["#3B82F6","#4ADE80","#FACC15","#FB923C","#F87171"]
        sw = w // 5
        for i, c in enumerate(cores_seg):
            canvas_bar.create_rectangle(i*sw, 0, (i+1)*sw-2, 12, fill=c, outline="")
        prop = max(0, min(1, (imc-10)/35))
        x = int(prop * w)
        canvas_bar.create_polygon(x, 0, x-5, 12, x+5, 12,
                                  fill="white", outline=OS_COR["fundo"], width=1)

    def calcular():
        ps = e_peso.get().strip(); hs = e_altura.get().strip()
        for v, ph in [(ps,"ex: 70.5"),(hs,"ex: 1.75")]:
            if v == ph or not v:
                messagebox.showwarning("Atenção", "Preenche peso e altura.", parent=win); return
        try:
            p = float(ps.replace(",",".")); h = float(hs.replace(",","."))
        except ValueError:
            messagebox.showwarning("Atenção", "Valores numéricos inválidos.", parent=win); return
        if not (1 < p < 500): messagebox.showwarning("Atenção","Peso inválido.",parent=win); return
        if not (0.5 < h < 3): messagebox.showwarning("Atenção","Altura inválida.",parent=win); return
        imc = p / (h**2)
        lbl_, cor, bg = classificar(imc)
        res_frame.config(bg=bg, highlightbackground=cor)
        for w_ in res_frame.winfo_children():
            try: w_.config(bg=bg)
            except: pass
        lbl_imc.config(text=f"{imc:.1f}", fg=cor)
        lbl_cls.config(text=lbl_, fg=cor)
        desenhar_barra(imc, cor)
        pmin, pmax = 18.5*h**2, 25*h**2
        lbl_ideal.config(text=f"Peso ideal: {pmin:.1f} – {pmax:.1f} kg")

    botao(win, "Calcular IMC", calcular, OS_COR["azul"]).pack(
        padx=28, pady=(12,0), fill="x", ipady=4)

    # Tabela referência
    tk.Label(win, text="REFERÊNCIA OMS", font=("Helvetica",7),
             bg=OS_COR["fundo"], fg=OS_COR["muted"]).pack(anchor="w", padx=28, pady=(12,3))
    ft = painel(win)
    ft.pack(padx=28, fill="x")
    for mn, mx, lbl_, cor, bg in CLASSIF:
        intv = f"{mn}–{mx}" if mx < 999 else f"≥{mn}"
        fr = tk.Frame(ft, bg=bg); fr.pack(fill="x")
        tk.Label(fr, text=intv, font=("Helvetica",8,"bold"),
                 bg=bg, fg=cor, width=10, anchor="w").pack(side="left", padx=10, pady=2)
        tk.Label(fr, text=lbl_, font=("Helvetica",8),
                 bg=bg, fg=cor).pack(side="left")

    win.bind("<Return>",   lambda e: calcular())
    win.bind("<KP_Enter>", lambda e: calcular())


# ═══════════════════════════════════════════════════════════════════
#  3. AGENDA DE CONTACTOS
# ═══════════════════════════════════════════════════════════════════

def abrir_agenda():
    DB = Path("agenda.db")

    def init_db():
        with sqlite3.connect(DB) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS contactos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL, telefone TEXT DEFAULT '',
                endereco TEXT DEFAULT '', distrito TEXT DEFAULT '',
                pais TEXT DEFAULT '', email TEXT DEFAULT '')""")

    def get(q, p=()): 
        with sqlite3.connect(DB) as c: return c.execute(q,p).fetchall()

    def run(q, p=()):
        with sqlite3.connect(DB) as c: c.execute(q,p)

    init_db()
    CAMPOS = ["nome","telefone","endereco","distrito","pais","email"]
    LABELS = ["Nome *","Telefone","Endereço","Distrito","País","Email"]

    win = janela_base("Agenda de Contactos", 860, 600, True)
    win.configure(bg="#F8FAFC")

    style = ttk.Style(win)
    style.theme_use("clam")
    style.configure("Treeview", background="white", foreground="#1E293B",
                    rowheight=26, fieldbackground="white", font=("Segoe UI",10))
    style.configure("Treeview.Heading", background="#E2E8F0",
                    foreground="#1E293B", font=("Segoe UI",10,"bold"))
    style.map("Treeview", background=[("selected","#DBEAFE")])

    tk.Label(win, text="📒  Agenda de Contactos",
             font=("Segoe UI",15,"bold"), bg="#F8FAFC",
             fg="#2563EB").pack(pady=(14,4))

    main_ = tk.Frame(win, bg="#F8FAFC")
    main_.pack(fill="both", expand=True, padx=16, pady=6)
    main_.columnconfigure(1, weight=1); main_.rowconfigure(0, weight=1)

    # Formulário
    ff = tk.LabelFrame(main_, text=" Dados ", font=("Segoe UI",9,"bold"),
                       bg="#F8FAFC", fg="#1E293B", bd=1, relief="groove",
                       padx=12, pady=8)
    ff.grid(row=0, column=0, sticky="ns", padx=(0,12))

    entries = {}
    sel_id  = [None]

    for i, (c, l) in enumerate(zip(CAMPOS, LABELS)):
        tk.Label(ff, text=l, font=("Segoe UI",8), bg="#F8FAFC",
                 fg="#64748B", anchor="w").grid(row=i*2, column=0, sticky="w", pady=(5,0))
        e = tk.Entry(ff, font=("Segoe UI",10), width=24, relief="flat",
                     bg="white", fg="#1E293B",
                     highlightbackground="#E2E8F0", highlightthickness=1)
        e.grid(row=i*2+1, column=0, sticky="ew", pady=(0,1))
        entries[c] = e

    entries["nome"].bind("<KeyRelease>", lambda ev: filtrar())

    def obter():
        return {c: entries[c].get().strip() for c in CAMPOS}

    def limpar():
        for e in entries.values(): e.delete(0,"end")
        sel_id[0] = None; atualizar()

    def adicionar():
        d = obter()
        if not d["nome"]: messagebox.showwarning("Erro","Nome obrigatório.",parent=win); return
        run("INSERT INTO contactos(nome,telefone,endereco,distrito,pais,email) VALUES(?,?,?,?,?,?)",
            tuple(d[c] for c in CAMPOS))
        limpar()

    def editar():
        if not sel_id[0]: messagebox.showwarning("Aviso","Selecciona um contacto.",parent=win); return
        d = obter()
        if not d["nome"]: messagebox.showwarning("Erro","Nome obrigatório.",parent=win); return
        run("UPDATE contactos SET nome=?,telefone=?,endereco=?,distrito=?,pais=?,email=? WHERE id=?",
            (*[d[c] for c in CAMPOS], sel_id[0]))
        limpar()

    def eliminar():
        if not sel_id[0]: messagebox.showwarning("Aviso","Selecciona um contacto.",parent=win); return
        nome_ = entries["nome"].get()
        if not messagebox.askyesno("Confirmar",f"Eliminar '{nome_}'?",parent=win): return
        run("DELETE FROM contactos WHERE id=?", (sel_id[0],)); limpar()

    bframe = tk.Frame(ff, bg="#F8FAFC")
    bframe.grid(row=len(CAMPOS)*2+1, column=0, pady=(12,0), sticky="ew")
    for txt, cmd, cor in [("➕ Adicionar",adicionar,"#16A34A"),
                           ("✏️  Editar",editar,"#2563EB"),
                           ("🗑️  Eliminar",eliminar,"#DC2626"),
                           ("🔄 Limpar",limpar,"#6B7280")]:
        tk.Button(bframe, text=txt, command=cmd, bg=cor, fg="white",
                  font=("Segoe UI",8,"bold"), relief="flat", cursor="hand2",
                  padx=6, pady=4).pack(fill="x", pady=1)

    # Lista
    lf = tk.LabelFrame(main_, text=" Contactos ", font=("Segoe UI",9,"bold"),
                       bg="#F8FAFC", fg="#1E293B", bd=1, relief="groove")
    lf.grid(row=0, column=1, sticky="nsew")
    lf.columnconfigure(0, weight=1); lf.rowconfigure(2, weight=1)

    pesq_var = tk.StringVar()
    pesq_var.trace_add("write", lambda *_: filtrar())
    pe = tk.Entry(lf, textvariable=pesq_var, font=("Segoe UI",10),
                  relief="flat", bg="white", fg="#1E293B",
                  highlightbackground="#E2E8F0", highlightthickness=1)
    pe.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=(8,2), ipady=3)
    tk.Label(lf, text="🔍 pesquisa em todos os campos",
             font=("Segoe UI",7), bg="#F8FAFC", fg="#94A3B8"
             ).grid(row=1, column=0, sticky="w", padx=10, pady=(0,4))

    colunas = ("id","nome","telefone","endereco","distrito","pais","email")
    tabela = ttk.Treeview(lf, columns=colunas, show="headings", selectmode="browse")
    tabela.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0,8))
    sb = ttk.Scrollbar(lf, orient="vertical", command=tabela.yview)
    sb.grid(row=2, column=1, sticky="ns")
    tabela.configure(yscrollcommand=sb.set)

    for col, w in zip(colunas, [30,130,100,130,75,60,155]):
        tabela.column(col, width=w)
        tabela.heading(col, text=col.capitalize())

    lbl_total = tk.Label(win, text="", font=("Segoe UI",8),
                         bg="#F8FAFC", fg="#94A3B8")
    lbl_total.pack(anchor="w", padx=16, pady=(0,6))

    def atualizar(rows=None):
        for i in tabela.get_children(): tabela.delete(i)
        if rows is None:
            q = pesq_var.get().strip()
            if q:
                p = f"%{q}%"
                rows = get("SELECT * FROM contactos WHERE "
                           "LOWER(nome) LIKE LOWER(?) OR LOWER(telefone) LIKE LOWER(?) "
                           "OR LOWER(email) LIKE LOWER(?) OR LOWER(endereco) LIKE LOWER(?) "
                           "OR LOWER(distrito) LIKE LOWER(?) OR LOWER(pais) LIKE LOWER(?) "
                           "ORDER BY LOWER(nome)",
                           (p,p,p,p,p,p))
            else:
                rows = get("SELECT * FROM contactos ORDER BY LOWER(nome)")
        for r in rows: tabela.insert("","end",values=r)
        lbl_total.config(text=f"{len(rows)} contacto(s)")

    def filtrar(): atualizar()

    def ao_selecionar(ev):
        sel = tabela.selection()
        if not sel: return
        vals = tabela.item(sel[0])["values"]
        sel_id[0] = vals[0]
        for c, v in zip(CAMPOS, vals[1:]):
            entries[c].delete(0,"end")
            entries[c].insert(0, v if v else "")

    tabela.bind("<<TreeviewSelect>>", ao_selecionar)
    atualizar()


# ═══════════════════════════════════════════════════════════════════
#  4. JOGO DO GALO
# ═══════════════════════════════════════════════════════════════════

def abrir_galo():
    COMBS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def verif(board):
        for a,b,c in COMBS:
            if board[a] and board[a]==board[b]==board[c]: return board[a],(a,b,c)
        if all(board): return "empate", None
        return None, None

    win = janela_base("Jogo do Galo", 400, 520)
    win.configure(bg="#F8FAFC")

    board = [""] * 9; turno = ["X"]; activo = [True]
    pts = {"X":0,"O":0}

    tk.Label(win, text="JOGO DO GALO", font=("Helvetica",16,"bold"),
             bg="#F8FAFC", fg="#1E293B").pack(pady=(16,4))

    pl = tk.Frame(win, bg="#F1F5F9", highlightbackground="#E2E8F0",
                  highlightthickness=1)
    pl.pack(padx=40, fill="x", pady=(0,10))
    px = tk.Frame(pl, bg="#F1F5F9"); px.pack(side="left", expand=True, pady=6)
    tk.Label(px, text="Jogador X", font=("Helvetica",8), bg="#F1F5F9",
             fg="#94A3B8").pack()
    lbl_x = tk.Label(px, text="0", font=("Helvetica",20,"bold"),
                     bg="#F1F5F9", fg="#2563EB"); lbl_x.pack()
    tk.Frame(pl, bg="#E2E8F0", width=1).pack(side="left", fill="y", pady=4)
    po = tk.Frame(pl, bg="#F1F5F9"); po.pack(side="right", expand=True, pady=6)
    tk.Label(po, text="Jogador O", font=("Helvetica",8), bg="#F1F5F9",
             fg="#94A3B8").pack()
    lbl_o = tk.Label(po, text="0", font=("Helvetica",20,"bold"),
                     bg="#F1F5F9", fg="#DC2626"); lbl_o.pack()

    lbl_est = tk.Label(win, text="", font=("Helvetica",11,"bold"),
                       bg="#F8FAFC", fg="#1E293B"); lbl_est.pack(pady=(0,8))

    gr = tk.Frame(win, bg="#1E293B", padx=3, pady=3); gr.pack()
    btns = []

    def atualizar_est():
        cor = "#2563EB" if turno[0]=="X" else "#DC2626"
        lbl_est.config(text=f"Vez do Jogador  {turno[0]}", fg=cor)

    def jogada(i):
        if not activo[0] or board[i]: return
        board[i] = turno[0]
        cor = "#2563EB" if turno[0]=="X" else "#DC2626"
        btns[i].config(text=turno[0], fg=cor, state="disabled",
                       disabledforeground=cor)
        res, tripla = verif(board)
        if res in ("X","O"):
            pts[res] += 1
            lbl_x.config(text=str(pts["X"])); lbl_o.config(text=str(pts["O"]))
            for idx in tripla:
                btns[idx].config(bg="#DCFCE7", highlightbackground="#16A34A",
                                 highlightthickness=2)
            activo[0] = False
            lbl_est.config(text=f"🏆 Jogador {res} venceu!",
                           fg="#2563EB" if res=="X" else "#DC2626")
        elif res == "empate":
            activo[0] = False
            for b in btns: b.config(bg="#FEF9C3")
            lbl_est.config(text="🤝 Empate!", fg="#94A3B8")
        else:
            turno[0] = "O" if turno[0]=="X" else "X"
            atualizar_est()

    for i in range(9):
        r, c_ = divmod(i, 3)
        b = tk.Button(gr, text="", font=("Helvetica",32,"bold"),
                      width=3, height=1, bg="white", fg="#1E293B",
                      activebackground="#F1F5F9", relief="flat", cursor="hand2",
                      command=lambda idx=i: jogada(idx))
        b.grid(row=r, column=c_, padx=3, pady=3, ipadx=8, ipady=8)
        btns.append(b)

    def nova():
        for i in range(9): board[i] = ""
        turno[0] = "X"; activo[0] = True
        for b in btns:
            b.config(text="", state="normal", bg="white", highlightthickness=0)
        atualizar_est()

    def reset():
        pts["X"]=0; pts["O"]=0
        lbl_x.config(text="0"); lbl_o.config(text="0"); nova()

    ctrl = tk.Frame(win, bg="#F8FAFC"); ctrl.pack(pady=(12,0))
    botao(ctrl, "🔄 Nova Partida", nova, "#1E293B").pack(side="left", padx=5)
    botao(ctrl, "🗑 Resetar Pontos", reset, "#F1F5F9", "#1E293B").pack(side="left", padx=5)
    atualizar_est()


# ═══════════════════════════════════════════════════════════════════
#  5. SNAKE
# ═══════════════════════════════════════════════════════════════════

def abrir_snake():
    CELL=20; COLS=20; ROWS=20; DELAY=150

    win = janela_base("Snake", COLS*CELL, ROWS*CELL+80)

    cobra=[(10,10),(9,10),(8,10)]; dir_=[(1,0)]; dir_prox=[(1,0)]
    fruta=[( 0,0)]; pontos=[0]; record=[0]; activo=[False]; job=[None]

    top = tk.Frame(win, bg="#1E293B",
                   highlightbackground="#334155", highlightthickness=1)
    top.pack(fill="x")
    tk.Label(top, text="SNAKE", font=("Helvetica",11,"bold"),
             bg="#1E293B", fg="#4ADE80").pack(side="left", padx=14, pady=6)
    fr_pts = tk.Frame(top, bg="#1E293B"); fr_pts.pack(side="right", padx=12, pady=3)
    tk.Label(fr_pts, text="PONTOS", font=("Helvetica",6), bg="#1E293B", fg="#64748B").pack()
    lbl_pts = tk.Label(fr_pts, text="0", font=("Helvetica",14,"bold"),
                       bg="#1E293B", fg="#FACC15"); lbl_pts.pack()
    fr_rec = tk.Frame(top, bg="#1E293B"); fr_rec.pack(side="right", padx=12, pady=3)
    tk.Label(fr_rec, text="RECORDE", font=("Helvetica",6), bg="#1E293B", fg="#64748B").pack()
    lbl_rec = tk.Label(fr_rec, text="0", font=("Helvetica",14,"bold"),
                       bg="#1E293B", fg="#F1F5F9"); lbl_rec.pack()

    cv = tk.Canvas(win, width=COLS*CELL, height=ROWS*CELL,
                   bg="#0F172A", highlightthickness=0)
    cv.pack()

    bot_ = tk.Frame(win, bg="#1E293B",
                    highlightbackground="#334155", highlightthickness=1)
    bot_.pack(fill="x")
    tk.Label(bot_, text="Setas para mover  •  Enter para começar  •  P para pausar",
             font=("Helvetica",7), bg="#1E293B", fg="#64748B").pack(pady=5)

    def grade():
        for c in range(0, COLS*CELL, CELL):
            cv.create_line(c, 0, c, ROWS*CELL, fill="#1E293B", width=1)
        for l in range(0, ROWS*CELL, CELL):
            cv.create_line(0, l, COLS*CELL, l, fill="#1E293B", width=1)

    def colocar_fruta():
        livres = [(c,l) for c in range(COLS) for l in range(ROWS) if (c,l) not in cobra]
        if livres: fruta[0] = random.choice(livres)

    def desenhar():
        cv.delete("all"); grade()
        fc, fl = fruta[0]
        cv.create_oval(fc*CELL+2, fl*CELL+2, fc*CELL+CELL-4, fl*CELL+CELL-4,
                       fill="#F87171", outline="")
        for i, (c,l) in enumerate(cobra):
            cor = "#4ADE80" if i==0 else "#16A34A"
            cv.create_rectangle(c*CELL+1, l*CELL+1, c*CELL+CELL-2, l*CELL+CELL-2,
                                 fill=cor, outline="")

    def loop():
        if not activo[0]: return
        dir_[0] = dir_prox[0]
        dc, dl = dir_[0]; cc, cl = cobra[0]
        nova = (cc+dc, cl+dl)
        if not (0<=nova[0]<COLS and 0<=nova[1]<ROWS) or nova in cobra:
            fim(); return
        cobra.insert(0, nova)
        if nova == fruta[0]:
            pontos[0] += 10; lbl_pts.config(text=str(pontos[0])); colocar_fruta()
        else:
            cobra.pop()
        desenhar()
        job[0] = win.after(DELAY, loop)

    def iniciar():
        if job[0]: win.after_cancel(job[0])
        cobra.clear()
        cm=COLS//2; lm=ROWS//2
        cobra.extend([(cm,lm),(cm-1,lm),(cm-2,lm)])
        dir_[0]=(1,0); dir_prox[0]=(1,0)
        pontos[0]=0; activo[0]=True
        lbl_pts.config(text="0"); colocar_fruta(); loop()

    def mudar(dc, dl):
        if (dc,dl) != (-dir_[0][0], -dir_[0][1]):
            dir_prox[0] = (dc,dl)

    def pausar():
        if not activo[0]: return
        if job[0]:
            win.after_cancel(job[0]); job[0]=None
            cv.create_text(COLS*CELL//2, ROWS*CELL//2, text="⏸ PAUSA",
                           font=("Helvetica",18,"bold"), fill="#FACC15", tags="pausa")
        else:
            cv.delete("pausa"); loop()

    def fim():
        activo[0]=False
        if job[0]: win.after_cancel(job[0]); job[0]=None
        if pontos[0] > record[0]:
            record[0]=pontos[0]; lbl_rec.config(text=str(record[0]))
        cx=COLS*CELL//2; cy=ROWS*CELL//2
        cv.create_rectangle(cx-110,cy-44,cx+110,cy+44,
                            fill="#0F172A", outline="#334155", width=2)
        cv.create_text(cx, cy-16, text="💀 FIM DE JOGO",
                       font=("Helvetica",14,"bold"), fill="#F87171")
        cv.create_text(cx, cy+8, text=f"Pontuação: {pontos[0]}",
                       font=("Helvetica",11), fill="#F1F5F9")
        cv.create_text(cx, cy+28, text="Enter para jogar de novo",
                       font=("Helvetica",9), fill="#64748B")

    # Ecrã inicial
    cv.delete("all"); grade()
    cx=COLS*CELL//2; cy=ROWS*CELL//2
    cv.create_text(cx, cy-16, text="🐍 SNAKE",
                   font=("Helvetica",20,"bold"), fill="#4ADE80")
    cv.create_text(cx, cy+16, text="Pressiona Enter para começar",
                   font=("Helvetica",10), fill="#64748B")

    win.bind("<Up>",     lambda e: mudar(0,-1))
    win.bind("<Down>",   lambda e: mudar(0, 1))
    win.bind("<Left>",   lambda e: mudar(-1,0))
    win.bind("<Right>",  lambda e: mudar(1, 0))
    win.bind("<Return>",   lambda e: iniciar())
    win.bind("<KP_Enter>", lambda e: iniciar())
    win.bind("<p>",      lambda e: pausar())
    win.bind("<P>",      lambda e: pausar())


# ═══════════════════════════════════════════════════════════════════
#  6. FORCA
# ═══════════════════════════════════════════════════════════════════

def abrir_forca():
    PALAVRAS = [
        "PYTHON","TKINTER","COMPUTADOR","TECLADO","MONITOR",
        "PROGRAMACAO","ALGORITMO","VARIAVEL","FUNCAO","CLASSE",
        "INTERNET","SOFTWARE","HARDWARE","JANELA","BOTAO",
        "PORTUGAL","FUTEBOL","MUSICA","ELEFANTE","GIRAFA",
        "DINOSSAURO","BORBOLETA","CARACOL","LISBOA","ALGARVE",
    ]
    BONECO = [
        ("create_oval", [155,40,195,80], {"outline":"#F1F5F9","width":3}),
        ("create_line", [175,80,175,140],{"fill":"#F1F5F9","width":3}),
        ("create_line", [175,95,145,125],{"fill":"#F1F5F9","width":3}),
        ("create_line", [175,95,205,125],{"fill":"#F1F5F9","width":3}),
        ("create_line", [175,140,145,175],{"fill":"#F1F5F9","width":3}),
        ("create_line", [175,140,205,175],{"fill":"#F1F5F9","width":3}),
    ]

    win = janela_base("Forca", 480, 580)

    palavra=[""]; adiv=[set()]; erros=[0]; activo=[True]
    vit=[0]; der=[0]

    tk.Label(win, text="FORCA", font=("Helvetica",14,"bold"),
             bg=OS_COR["fundo"], fg=OS_COR["branco"]).pack(pady=(14,2))

    pl = painel(win); pl.pack(padx=30, fill="x", pady=(0,8))
    lv = tk.Label(pl, text="0", font=("Helvetica",18,"bold"),
                  bg=OS_COR["card"], fg=OS_COR["verde"])
    ld = tk.Label(pl, text="0", font=("Helvetica",18,"bold"),
                  bg=OS_COR["card"], fg=OS_COR["vermelho"])
    for i, (lb, txt) in enumerate([(lv,"Vitórias"),(ld,"Derrotas")]):
        col = tk.Frame(pl, bg=OS_COR["card"]); col.pack(side="left", expand=True, pady=6)
        tk.Label(col, text=txt, font=("Helvetica",8),
                 bg=OS_COR["card"], fg=OS_COR["muted"]).pack()
        lb.pack(in_=col); lb.lift()
        if i == 0:
            tk.Frame(pl, bg=OS_COR["borda"], width=1).pack(side="left", fill="y", pady=4)

    meio = tk.Frame(win, bg=OS_COR["fundo"]); meio.pack(padx=16, fill="x")

    cv = tk.Canvas(meio, width=220, height=200,
                   bg=OS_COR["card"], highlightthickness=0)
    cv.pack(side="left")

    def estrutura():
        cv.create_line(20,190,200,190,fill="#475569",width=3)
        cv.create_line(60,190,60,15,fill="#475569",width=3)
        cv.create_line(60,15,175,15,fill="#475569",width=3)
        cv.create_line(175,15,175,40,fill="#475569",width=3)

    dir_ = tk.Frame(meio, bg=OS_COR["fundo"]); dir_.pack(side="left", padx=(14,0))
    tk.Label(dir_, text="ERRADAS", font=("Helvetica",7),
             bg=OS_COR["fundo"], fg=OS_COR["muted"]).pack(anchor="w")
    lbl_err_lets = tk.Label(dir_, text="", font=("Helvetica",12,"bold"),
                            wraplength=200, justify="left",
                            bg=OS_COR["fundo"], fg=OS_COR["vermelho"])
    lbl_err_lets.pack(anchor="w")
    tk.Label(dir_, text="ERROS", font=("Helvetica",7),
             bg=OS_COR["fundo"], fg=OS_COR["muted"]).pack(anchor="w", pady=(10,0))
    lbl_erros = tk.Label(dir_, text="0/6", font=("Helvetica",14,"bold"),
                         bg=OS_COR["fundo"], fg=OS_COR["amarelo"])
    lbl_erros.pack(anchor="w")

    lbl_palavra = tk.Label(win, text="", font=("Helvetica",22,"bold"),
                           bg=OS_COR["fundo"], fg=OS_COR["branco"])
    lbl_palavra.pack(pady=(10,2))
    lbl_msg = tk.Label(win, text="", font=("Helvetica",11,"bold"),
                       bg=OS_COR["fundo"], fg=OS_COR["branco"])
    lbl_msg.pack()

    teclado = tk.Frame(win, bg=OS_COR["fundo"]); teclado.pack(pady=(8,0))
    btns_l = {}
    for i, l in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        r_, c_ = divmod(i, 9)
        b = tk.Button(teclado, text=l, font=("Helvetica",9,"bold"),
                      width=2, height=1, bg=OS_COR["card"],
                      fg=OS_COR["branco"], relief="flat", cursor="hand2",
                      command=lambda lt=l: tentar(lt))
        b.grid(row=r_, column=c_, padx=2, pady=2)
        btns_l[l] = b

    botao(win, "🔄 Nova Palavra", lambda: novo(), OS_COR["card"],
          OS_COR["verde"]).pack(pady=(8,0))

    def atualizar_palavra():
        ex = "  ".join(l if l in adiv[0] else "_" for l in palavra[0])
        lbl_palavra.config(text=ex)

    def novo():
        palavra[0] = random.choice(PALAVRAS)
        adiv[0] = set(); erros[0] = 0; activo[0] = True
        cv.delete("boneco"); estrutura()
        lbl_err_lets.config(text="")
        lbl_erros.config(text="0/6", fg=OS_COR["amarelo"])
        lbl_msg.config(text="")
        lbl_palavra.config(fg=OS_COR["branco"])
        for b in btns_l.values():
            b.config(state="normal", bg=OS_COR["card"], fg=OS_COR["branco"])
        atualizar_palavra()

    def tentar(l):
        if not activo[0] or l in adiv[0]: return
        adiv[0].add(l)
        if l in palavra[0]:
            btns_l[l].config(bg="#14532D", fg=OS_COR["verde"], state="disabled")
        else:
            erros[0] += 1
            btns_l[l].config(bg="#7F1D1D", fg=OS_COR["vermelho"], state="disabled")
            m, args, kw = BONECO[erros[0]-1]
            getattr(cv, m)(*args, tags="boneco", **kw)
            erradas = sorted(x for x in adiv[0] if x not in palavra[0])
            lbl_err_lets.config(text="  ".join(erradas))
            cor = OS_COR["vermelho"] if erros[0]>=4 else OS_COR["amarelo"]
            lbl_erros.config(text=f"{erros[0]}/6", fg=cor)
        atualizar_palavra()
        if all(l in adiv[0] for l in palavra[0]):
            activo[0]=False; vit[0]+=1; lv.config(text=str(vit[0]))
            lbl_msg.config(text=f"🏆 Acertaste! Era '{palavra[0]}'", fg=OS_COR["verde"])
            for b in btns_l.values(): b.config(state="disabled")
        elif erros[0] >= 6:
            activo[0]=False; der[0]+=1; ld.config(text=str(der[0]))
            lbl_palavra.config(text="  ".join(palavra[0]), fg=OS_COR["vermelho"])
            lbl_msg.config(text=f"💀 Era '{palavra[0]}'!", fg=OS_COR["vermelho"])
            for b in btns_l.values(): b.config(state="disabled")

    win.bind("<KeyPress>", lambda e: tentar(e.char.upper()) if e.char.upper() in btns_l else None)
    novo()


# ═══════════════════════════════════════════════════════════════════
#  7. PEDRA PAPEL TESOURA
# ═══════════════════════════════════════════════════════════════════

def abrir_ppt():
    OPCOES=["Pedra","Papel","Tesoura"]
    EMOJI={"Pedra":"🪨","Papel":"📄","Tesoura":"✂️"}
    VENCE={"Pedra":"Tesoura","Papel":"Pedra","Tesoura":"Papel"}
    BTN_COR={"Pedra":"#1E3A5F","Papel":"#14532D","Tesoura":"#4C1D95"}

    win = janela_base("Pedra, Papel ou Tesoura", 400, 520)
    pontos={"vitoria":0,"derrota":0,"empate":0}

    label_titulo(win, "PEDRA  PAPEL  TESOURA")
    label_sub(win, "Escolhe a tua jogada")

    pl = painel(win); pl.pack(padx=30, fill="x", pady=(0,12))
    lbls={}
    for i,(lbl,chave,cor) in enumerate([("Vitórias","vitoria",OS_COR["verde"]),
                                         ("Empates","empate",OS_COR["amarelo"]),
                                         ("Derrotas","derrota",OS_COR["vermelho"])]):
        col=tk.Frame(pl,bg=OS_COR["card"]); col.pack(side="left",expand=True,pady=8)
        tk.Label(col,text=lbl,font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
        lb=tk.Label(col,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=cor); lb.pack()
        lbls[chave]=lb
        if i<2: tk.Frame(pl,bg=OS_COR["borda"],width=1).pack(side="left",fill="y",pady=5)

    arena = painel(win); arena.pack(padx=30, fill="x", pady=(0,12))
    fr_la = tk.Frame(arena, bg=OS_COR["card"]); fr_la.pack(fill="x", padx=14, pady=10)
    lado_pc = tk.Frame(fr_la,bg=OS_COR["card"]); lado_pc.pack(side="left",expand=True)
    tk.Label(lado_pc,text="COMPUTADOR",font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
    lbl_epc=tk.Label(lado_pc,text="❓",font=("Helvetica",40),bg=OS_COR["card"]); lbl_epc.pack()
    lbl_npc=tk.Label(lado_pc,text="???",font=("Helvetica",10,"bold"),bg=OS_COR["card"],fg=OS_COR["muted"]); lbl_npc.pack()
    tk.Label(fr_la,text="VS",font=("Helvetica",14,"bold"),bg=OS_COR["card"],fg=OS_COR["muted"]).pack(side="left",expand=True)
    lado_j=tk.Frame(fr_la,bg=OS_COR["card"]); lado_j.pack(side="right",expand=True)
    tk.Label(lado_j,text="TU",font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
    lbl_ej=tk.Label(lado_j,text="❓",font=("Helvetica",40),bg=OS_COR["card"]); lbl_ej.pack()
    lbl_nj=tk.Label(lado_j,text="???",font=("Helvetica",10,"bold"),bg=OS_COR["card"],fg=OS_COR["muted"]); lbl_nj.pack()
    lbl_res=tk.Label(arena,text="",font=("Helvetica",13,"bold"),bg=OS_COR["card"],fg=OS_COR["branco"])
    lbl_res.pack(pady=(0,10))

    tk.Label(win,text="A TUA JOGADA",font=("Helvetica",7),bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(pady=(0,6))
    fb=tk.Frame(win,bg=OS_COR["fundo"]); fb.pack()

    def jogar(j):
        pc=random.choice(OPCOES)
        res = "empate" if j==pc else ("vitoria" if VENCE[j]==pc else "derrota")
        lbl_epc.config(text=EMOJI[pc]); lbl_npc.config(text=pc,fg=OS_COR["branco"])
        lbl_ej.config(text=EMOJI[j]);   lbl_nj.config(text=j, fg=OS_COR["branco"])
        cor=OS_COR["verde"] if res=="vitoria" else OS_COR["vermelho"] if res=="derrota" else OS_COR["amarelo"]
        msgs={"vitoria":"🏆 Ganhaste!","derrota":"💀 Perdeste!","empate":"🤝 Empate!"}
        lbl_res.config(text=msgs[res], fg=cor)
        pontos[res]+=1
        for k,l in lbls.items(): l.config(text=str(pontos[k]))

    def reiniciar():
        for k in pontos: pontos[k]=0
        for l in lbls.values(): l.config(text="0")
        lbl_epc.config(text="❓"); lbl_npc.config(text="???",fg=OS_COR["muted"])
        lbl_ej.config(text="❓");  lbl_nj.config(text="???",fg=OS_COR["muted"])
        lbl_res.config(text="")

    for op in OPCOES:
        tk.Button(fb, text=f"{EMOJI[op]}\n{op}", font=("Helvetica",11,"bold"),
                  width=6, height=3, bg=BTN_COR[op], fg=OS_COR["branco"],
                  relief="flat", cursor="hand2",
                  command=lambda o=op: jogar(o)).pack(side="left", padx=8)

    botao(win,"🔄 Reiniciar",reiniciar,OS_COR["card"],OS_COR["muted"]).pack(pady=(14,0))


# ═══════════════════════════════════════════════════════════════════
#  8. ADIVINHAR O NÚMERO
# ═══════════════════════════════════════════════════════════════════

def abrir_numero():
    MAX=7
    win = janela_base("Adivinhar o Número", 380, 500)
    label_titulo(win, "ADIVINHAR O NÚMERO", OS_COR["azul"])
    label_sub(win, "Número entre 1 e 100  •  7 tentativas")

    pl=painel(win); pl.pack(padx=30,fill="x",pady=(0,12))
    lv=tk.Label(pl,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=OS_COR["verde"])
    ld=tk.Label(pl,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=OS_COR["vermelho"])
    for i,(lbl,lb) in enumerate([("Vitórias",lv),("Derrotas",ld)]):
        col=tk.Frame(pl,bg=OS_COR["card"]); col.pack(side="left",expand=True,pady=8)
        tk.Label(col,text=lbl,font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
        lb.pack(in_=col); lb.lift()
        if i==0:
            tk.Frame(pl,bg=OS_COR["borda"],width=1).pack(side="left",fill="y",pady=5)

    lbl_tent=tk.Label(win,text="",font=("Helvetica",10),bg=OS_COR["fundo"],fg=OS_COR["amarelo"]); lbl_tent.pack()
    lbl_dica=tk.Label(win,text="",font=("Helvetica",26),bg=OS_COR["fundo"],fg=OS_COR["branco"]); lbl_dica.pack(pady=6)
    lbl_msg=tk.Label(win,text="",font=("Helvetica",12,"bold"),bg=OS_COR["fundo"],fg=OS_COR["branco"]); lbl_msg.pack()

    fi=tk.Frame(win,bg=OS_COR["fundo"]); fi.pack(pady=14)
    var=tk.StringVar()
    e=entrada(fi,var,largura=7); e.pack(side="left",padx=(0,8),ipady=5)
    
    numero=[0]; tent=[0]; activo=[True]; vit_n=[0]; der_n=[0]
    hist_f=tk.Frame(win,bg=OS_COR["fundo"]); hist_f.pack()

    def novo():
        numero[0]=random.randint(1,100); tent[0]=0; activo[0]=True
        var.set(""); lbl_dica.config(text="🤔",fg=OS_COR["branco"])
        lbl_msg.config(text="Qual é o número?",fg=OS_COR["branco"])
        lbl_tent.config(text=f"{MAX} tentativas restantes")
        for w in hist_f.winfo_children(): w.destroy()
        e.config(state="normal"); e.focus_set()

    def tentar():
        if not activo[0]: return
        try:
            ch=int(var.get().strip())
            if not(1<=ch<=100): raise ValueError
        except:
            lbl_msg.config(text="Introduz um número entre 1 e 100",fg=OS_COR["amarelo"]); return
        var.set(""); tent[0]+=1; rest=MAX-tent[0]
        ln=tk.Frame(hist_f,bg=OS_COR["fundo"]); ln.pack()
        if ch==numero[0]:
            activo[0]=False; vit_n[0]+=1; lv.config(text=str(vit_n[0]))
            lbl_dica.config(text="🏆"); lbl_tent.config(text="")
            lbl_msg.config(text=f"Acertaste em {tent[0]} tentativa(s)!",fg=OS_COR["verde"])
            e.config(state="disabled")
            tk.Label(ln,text=f"✔ {ch}",font=("Helvetica",8,"bold"),bg=OS_COR["fundo"],fg=OS_COR["verde"]).pack()
        elif ch<numero[0]:
            lbl_dica.config(text="⬆️ Mais alto",fg=OS_COR["azul"])
            lbl_msg.config(text=f"{ch} é muito baixo",fg=OS_COR["azul"])
            tk.Label(ln,text=f"↑ {ch} — baixo",font=("Helvetica",8),bg=OS_COR["fundo"],fg=OS_COR["azul"]).pack()
        else:
            lbl_dica.config(text="⬇️ Mais baixo",fg=OS_COR["vermelho"])
            lbl_msg.config(text=f"{ch} é muito alto",fg=OS_COR["vermelho"])
            tk.Label(ln,text=f"↓ {ch} — alto",font=("Helvetica",8),bg=OS_COR["fundo"],fg=OS_COR["vermelho"]).pack()
        if ch!=numero[0]:
            if rest==0:
                activo[0]=False; der_n[0]+=1; ld.config(text=str(der_n[0]))
                lbl_dica.config(text="💀"); lbl_tent.config(text="")
                lbl_msg.config(text=f"Era o {numero[0]}! Sem tentativas.",fg=OS_COR["vermelho"])
                e.config(state="disabled")
            else:
                lbl_tent.config(text=f"{rest} tentativa(s) restante(s)")

    botao(fi,"OK",tentar,OS_COR["azul"]).pack(side="left")
    botao(win,"🔄 Novo Jogo",novo,OS_COR["card"],OS_COR["azul"]).pack(pady=(10,0))
    win.bind("<Return>",   lambda e_: tentar())
    win.bind("<KP_Enter>", lambda e_: tentar())
    novo()


# ═══════════════════════════════════════════════════════════════════
#  9. CARA OU COROA
# ═══════════════════════════════════════════════════════════════════

def abrir_coc():
    win = janela_base("Cara ou Coroa", 360, 460)
    label_titulo(win, "CARA OU COROA", "#F59E0B")
    label_sub(win, "Escolhe e lança a moeda")

    pl=painel(win); pl.pack(padx=30,fill="x",pady=(0,12))
    stats={"Cara":0,"Coroa":0}; vit=[0]; der=[0]; streak=[0]; max_s=[0]; total=[0]
    lv=tk.Label(pl,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=OS_COR["verde"])
    ld=tk.Label(pl,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=OS_COR["vermelho"])
    ls=tk.Label(pl,text="0",font=("Helvetica",20,"bold"),bg=OS_COR["card"],fg=OS_COR["amarelo"])
    for i,(lbl,lb) in enumerate([("Vitórias",lv),("Streak",ls),("Derrotas",ld)]):
        col=tk.Frame(pl,bg=OS_COR["card"]); col.pack(side="left",expand=True,pady=8)
        tk.Label(col,text=lbl,font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
        lb.pack(in_=col); lb.lift()
        if i<2:
            tk.Frame(pl,bg=OS_COR["borda"],width=1).pack(side="left",fill="y",pady=5)

    lbl_m=tk.Label(win,text="🪙",font=("Helvetica",56),bg=OS_COR["fundo"]); lbl_m.pack(pady=6)
    lbl_r=tk.Label(win,text="",font=("Helvetica",13,"bold"),bg=OS_COR["fundo"],fg=OS_COR["branco"]); lbl_r.pack()
    lbl_s=tk.Label(win,text="",font=("Helvetica",8),bg=OS_COR["fundo"],fg=OS_COR["muted"]); lbl_s.pack(pady=(3,12))

    tk.Label(win,text="A TUA ESCOLHA",font=("Helvetica",7),bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(pady=(0,5))
    fb=tk.Frame(win,bg=OS_COR["fundo"]); fb.pack()

    def lancar(esc):
        res=random.choice(["Cara","Coroa"]); total[0]+=1; stats[res]+=1
        lbl_m.config(text="😊" if res=="Cara" else "👑")
        if esc==res:
            vit[0]+=1; streak[0]+=1; max_s[0]=max(max_s[0],streak[0])
            lbl_r.config(text=f"✔ {res}! Acertaste!",fg=OS_COR["verde"])
        else:
            der[0]+=1; streak[0]=0
            lbl_r.config(text=f"✘ {res}! Erraste!",fg=OS_COR["vermelho"])
        lv.config(text=str(vit[0])); ld.config(text=str(der[0])); ls.config(text=str(streak[0]))
        pct=round(vit[0]/total[0]*100) if total[0] else 0
        lbl_s.config(text=f"Caras:{stats['Cara']}  Coroas:{stats['Coroa']}  "
                          f"Acerto:{pct}%  Melhor streak:{max_s[0]}")

    def reiniciar():
        for k in stats: stats[k]=0
        vit[0]=der[0]=streak[0]=max_s[0]=total[0]=0
        for l in [lv,ld,ls]: l.config(text="0")
        lbl_m.config(text="🪙"); lbl_r.config(text=""); lbl_s.config(text="")

    for op,em in [("Cara","😊"),("Coroa","👑")]:
        tk.Button(fb,text=f"{em}\n{op}",font=("Helvetica",11,"bold"),
                  width=7,height=2,bg=OS_COR["card"],fg=OS_COR["branco"],
                  relief="flat",cursor="hand2",
                  command=lambda o=op: lancar(o)).pack(side="left",padx=10)

    botao(win,"🔄 Reiniciar",reiniciar,OS_COR["card"],OS_COR["muted"]).pack(pady=(14,0))


# ═══════════════════════════════════════════════════════════════════
#  10. ADIVINHADOR DE CÓDIGOS
# ═══════════════════════════════════════════════════════════════════

def abrir_codigos():
    MAX_T=5; NUM_P=3; MAX_PTS=1500

    def gerar():
        letras=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return [str(random.randint(0,9)) if random.random()<0.3
                else random.choice(letras) for _ in range(NUM_P)]

    win = janela_base("Adivinhador de Códigos", 460, 580)
    label_titulo(win, "ADIVINHADOR DE CÓDIGOS", "#22D3EE")
    label_sub(win, "Descobre o código de 3 caracteres  •  5 tentativas por posição")

    fc=tk.Frame(win,bg=OS_COR["fundo"]); fc.pack(pady=(0,16))
    caixas=[]
    for _ in range(NUM_P):
        l=tk.Label(fc,text="?",font=("Consolas",30,"bold"),width=3,height=1,
                   bg=OS_COR["card"],fg=OS_COR["muted"],
                   highlightbackground=OS_COR["borda"],highlightthickness=2)
        l.pack(side="left",padx=7); caixas.append(l)

    pp=painel(win); pp.pack(padx=28,fill="x")
    tk.Label(pp,text="POSIÇÃO ACTUAL",font=("Consolas",8),
             bg=OS_COR["card"],fg=OS_COR["muted"]).pack(pady=(10,0))
    lbl_pos=tk.Label(pp,text="",font=("Consolas",10,"bold"),
                     bg=OS_COR["card"],fg="#22D3EE"); lbl_pos.pack()
    fb_=tk.Frame(pp,bg=OS_COR["card"]); fb_.pack(pady=6)
    bolinhas=[]
    for _ in range(MAX_T):
        b=tk.Label(fb_,text="●",font=("Consolas",16),
                   bg=OS_COR["card"],fg=OS_COR["verde"]); b.pack(side="left",padx=3)
        bolinhas.append(b)

    fi_=tk.Frame(pp,bg=OS_COR["card"]); fi_.pack(pady=(2,0))
    var=tk.StringVar()

    def limitar(*_):
        v=var.get().upper()
        if len(v)>1: var.set(v[-1])
        elif v!=var.get(): var.set(v)

    var.trace_add("write",limitar)
    e=tk.Entry(fi_,textvariable=var,font=("Consolas",26,"bold"),width=3,
               justify="center",bg=OS_COR["fundo"],fg=OS_COR["branco"],
               insertbackground="#22D3EE",relief="flat",
               highlightbackground=OS_COR["borda"],highlightthickness=2,
               highlightcolor="#22D3EE"); e.pack(side="left",padx=(0,8))
    
    codigo=[]; pos=[0]; tent=[0]; pontos=[0]; activo=[True]
    hist_f=tk.Frame(win,bg=OS_COR["fundo"])

    lbl_fb=tk.Label(pp,text="",font=("Consolas",9),
                    bg=OS_COR["card"],fg=OS_COR["amarelo"]); lbl_fb.pack(pady=(7,12))

    hist_f.pack(padx=28,fill="x",pady=(10,0))
    pf=tk.Frame(win,bg=OS_COR["fundo"]); pf.pack(padx=28,pady=(10,0),fill="x")
    tk.Label(pf,text="PONTUAÇÃO",font=("Consolas",7),bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(anchor="w")
    lbl_pts_c=tk.Label(pf,text="0 / 1500",font=("Consolas",12,"bold"),
                       bg=OS_COR["fundo"],fg=OS_COR["branco"]); lbl_pts_c.pack(anchor="w")
    cv_bar=tk.Canvas(pf,height=8,bg=OS_COR["card"],highlightthickness=0)
    cv_bar.pack(fill="x",pady=(3,0))

    def desenhar_bar(p):
        cv_bar.update_idletasks(); w=cv_bar.winfo_width()
        cv_bar.delete("all"); prop=p/MAX_PTS
        fill=int(prop*w)
        cor=OS_COR["verde"] if prop>=0.8 else OS_COR["amarelo"] if prop>=0.5 else OS_COR["vermelho"]
        if fill>0: cv_bar.create_rectangle(0,0,fill,8,fill=cor,outline="")

    def atualizar_ui():
        nomes=["primeiro","segundo","terceiro"]
        if pos[0]<NUM_P:
            lbl_pos.config(text=f"Posição {pos[0]+1} — {nomes[pos[0]]} caracter")
        for i,b in enumerate(bolinhas):
            b.config(fg=OS_COR["verde"] if i<tent[0] else OS_COR["muted"])
        lbl_pts_c.config(text=f"{pontos[0]} / {MAX_PTS}")
        desenhar_bar(pontos[0])

    def novo():
        codigo.clear(); codigo.extend(gerar())
        pos[0]=0; tent[0]=MAX_T; pontos[0]=0; activo[0]=True
        for c in caixas:
            c.config(text="?",fg=OS_COR["muted"],bg=OS_COR["card"],
                     highlightbackground=OS_COR["borda"])
        for w in hist_f.winfo_children(): w.destroy()
        var.set(""); e.config(state="normal"); e.focus_set()
        lbl_fb.config(text=""); atualizar_ui(); desenhar_bar(0)

    def tentar():
        if not activo[0]: return
        entrada_v=var.get().strip().upper(); var.set("")
        if not(len(entrada_v)==1 and entrada_v in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
            lbl_fb.config(text="⚠ Introduz 1 letra ou 1 número",fg=OS_COR["amarelo"]); return
        correto=codigo[pos[0]].upper()
        ln=tk.Frame(hist_f,bg=OS_COR["fundo"]); ln.pack(fill="x",pady=1)
        if entrada_v==correto:
            pts=calcular_p(MAX_T-tent[0]+1); pontos[0]+=pts
            lbl_fb.config(text=f"✔ Correto! +{pts} pts",fg=OS_COR["verde"])
            caixas[pos[0]].config(text=correto,fg=OS_COR["verde"],
                                  bg="#14532D",highlightbackground=OS_COR["verde"])
            tk.Label(ln,text=f"✔ Pos.{pos[0]+1}: {entrada_v} — acertou",
                     font=("Consolas",8),bg=OS_COR["fundo"],fg=OS_COR["verde"]).pack(anchor="w")
            pos[0]+=1; tent[0]=MAX_T
        else:
            tent[0]-=1
            tk.Label(ln,text=f"✘ Pos.{pos[0]+1}: {entrada_v} — errou",
                     font=("Consolas",8),bg=OS_COR["fundo"],fg=OS_COR["vermelho"]).pack(anchor="w")
            if tent[0]==0:
                lbl_fb.config(text=f"✘ Era '{correto}'. Sem tentativas!",fg=OS_COR["vermelho"])
                caixas[pos[0]].config(text=correto,fg=OS_COR["vermelho"],
                                      bg="#7F1D1D",highlightbackground=OS_COR["vermelho"])
                pos[0]+=1; tent[0]=MAX_T
            else:
                lbl_fb.config(text=f"✘ Errado — {tent[0]} tentativa(s)",fg=OS_COR["amarelo"])
        atualizar_ui()
        if pos[0]>=NUM_P:
            win.after(350, fim)

    def calcular_p(usadas): return (MAX_T-usadas+1)*100

    def fim():
        activo[0]=False; e.config(state="disabled")
        ganhou=all(c.cget("bg")=="#14532D" for c in caixas)
        pct=round(pontos[0]/MAX_PTS*100)
        cor=OS_COR["verde"] if pct>=80 else OS_COR["amarelo"] if pct>=50 else OS_COR["vermelho"]
        msg=f"🏆 Parabéns! {pontos[0]} pts ({pct}%)" if ganhou else f"💀 Fim — {pontos[0]} pts ({pct}%)"
        lbl_fb.config(text=msg,fg=cor); lbl_pos.config(text="Jogo terminado",fg=OS_COR["muted"])

    tk.Button(fi_,text="OK",font=("Consolas",12,"bold"),
              bg="#22D3EE",fg=OS_COR["fundo"],relief="flat",cursor="hand2",
              width=4,pady=5,command=tentar).pack(side="left")
    botao(win,"🔄 Novo Jogo",novo,OS_COR["card"],"#22D3EE").pack(pady=(10,0))
    win.bind("<Return>",   lambda ev: tentar())
    win.bind("<KP_Enter>", lambda ev: tentar())
    novo()


# ═══════════════════════════════════════════════════════════════════
#  LAUNCHER PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
# -*- coding: utf-8 -*-
# BLOCO DE NOTAS
def abrir_notas():
    import tkinter as tk
    from tkinter import filedialog, font as tkfont
    win = janela_base("Bloco de Notas", 600, 500, True)
    toolbar = tk.Frame(win, bg=OS_COR["taskbar"], pady=4)
    toolbar.pack(fill="x")
    txt = tk.Text(win, font=("Consolas", 11), bg="#0D1117", fg=OS_COR["branco"],
                  insertbackground=OS_COR["azul"], relief="flat",
                  padx=12, pady=8, wrap="word",
                  highlightthickness=0, undo=True)
    txt.pack(fill="both", expand=True)
    sb = tk.Scrollbar(win, command=txt.yview); sb.pack(side="right", fill="y")
    txt.configure(yscrollcommand=sb.set)
    caminho = [None]
    lbl_info = tk.Label(win, text="Novo ficheiro", font=("Helvetica",8),
                        bg=OS_COR["taskbar"], fg=OS_COR["muted"])
    lbl_info.pack(fill="x", side="bottom", padx=8)
    def novo():
        txt.delete("1.0","end"); caminho[0]=None; lbl_info.config(text="Novo ficheiro")
    def abrir():
        p = filedialog.askopenfilename(filetypes=[("Texto","*.txt"),("Todos","*.*")])
        if not p: return
        with open(p,"r",encoding="utf-8",errors="replace") as f: conteudo=f.read()
        txt.delete("1.0","end"); txt.insert("1.0",conteudo)
        caminho[0]=p; lbl_info.config(text=p)
    def guardar():
        if caminho[0]:
            with open(caminho[0],"w",encoding="utf-8") as f: f.write(txt.get("1.0","end-1c"))
            lbl_info.config(text=f"Guardado: {caminho[0]}")
        else: guardar_como()
    def guardar_como():
        p = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Texto","*.txt"),("Todos","*.*")])
        if not p: return
        with open(p,"w",encoding="utf-8") as f: f.write(txt.get("1.0","end-1c"))
        caminho[0]=p; lbl_info.config(text=f"Guardado: {p}")
    for txt_b, cmd in [("📄 Novo",novo),("📂 Abrir",abrir),("💾 Guardar",guardar),("💾 Guardar como",guardar_como)]:
        tk.Button(toolbar,text=txt_b,command=cmd,bg=OS_COR["card"],fg=OS_COR["branco"],
                  font=("Helvetica",9),relief="flat",cursor="hand2",padx=8,pady=3
                  ).pack(side="left",padx=3)
    win.bind("<Control-s>", lambda e: guardar())
    win.bind("<Control-o>", lambda e: abrir())
    win.bind("<Control-n>", lambda e: novo())


# GESTOR DE PASSWORDS
def abrir_passwords():
    import tkinter as tk
    from tkinter import ttk
    import sqlite3, hashlib
    DB_P = "passwords.db"
    def init():
        with sqlite3.connect(DB_P) as c:
            c.execute("CREATE TABLE IF NOT EXISTS entradas(id INTEGER PRIMARY KEY AUTOINCREMENT, servico TEXT, utilizador TEXT, password TEXT)")
    def get_all(filtro=""):
        with sqlite3.connect(DB_P) as c:
            if filtro: return c.execute("SELECT * FROM entradas WHERE LOWER(servico) LIKE LOWER(?)",(f"%{filtro}%",)).fetchall()
            return c.execute("SELECT * FROM entradas ORDER BY servico").fetchall()
    def add(s,u,p):
        with sqlite3.connect(DB_P) as c: c.execute("INSERT INTO entradas(servico,utilizador,password) VALUES(?,?,?)",(s,u,p))
    def delete(id_):
        with sqlite3.connect(DB_P) as c: c.execute("DELETE FROM entradas WHERE id=?",(id_,))
    init()
    win = janela_base("Gestor de Passwords", 560, 520)
    label_titulo(win,"Gestor de Passwords","#F87171")
    label_sub(win,"As passwords são guardadas localmente")
    pnl = painel(win); pnl.pack(padx=24,fill="x",pady=(0,10))
    pnl.columnconfigure(1,weight=1)
    vars_ = {}
    for i,(lbl,key,show) in enumerate([("Serviço","s",""),("Utilizador","u",""),("Password","p","*")]):
        tk.Label(pnl,text=lbl,font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]
                 ).grid(row=i,column=0,sticky="w",padx=10,pady=4)
        v=tk.StringVar(); vars_[key]=v
        e=entrada(pnl,v,largura=28,show=show); e.grid(row=i,column=1,sticky="ew",padx=10,pady=4,ipady=3)
    show_p = [False]
    def toggle():
        entries_list = [w for w in pnl.winfo_children() if isinstance(w,tk.Entry)]
        pw_entry = entries_list[-1] if entries_list else None
        if pw_entry:
            show_p[0] = not show_p[0]
            pw_entry.config(show="" if show_p[0] else "*")
    botao(pnl,"👁",toggle,OS_COR["card"],OS_COR["muted"]).grid(row=2,column=2,padx=4,pady=4)
    pesq_v = tk.StringVar(); pesq_v.trace_add("write",lambda *_: refresh())
    pe = entrada(win,pesq_v); pe.pack(padx=24,fill="x",pady=(0,6),ipady=3)
    tk.Label(win,text="🔍 pesquisar serviço",font=("Helvetica",7),
             bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(anchor="w",padx=26)
    style=ttk.Style(win); style.theme_use("clam")
    style.configure("PW.Treeview",background=OS_COR["card"],foreground=OS_COR["branco"],
                    rowheight=24,fieldbackground=OS_COR["card"],font=("Consolas",9))
    style.configure("PW.Treeview.Heading",background=OS_COR["taskbar"],
                    foreground=OS_COR["muted"],font=("Helvetica",9,"bold"))
    cols=("id","Serviço","Utilizador","Password")
    tab=ttk.Treeview(win,columns=cols,show="headings",selectmode="browse",style="PW.Treeview")
    for col,w in zip(cols,[30,160,160,160]):
        tab.column(col,width=w); tab.heading(col,text=col)
    tab.pack(padx=24,fill="both",expand=True,pady=6)
    sel_id=[None]
    def refresh():
        for i in tab.get_children(): tab.delete(i)
        for r in get_all(pesq_v.get().strip()):
            tab.insert("","end",values=(r[0],r[1],r[2],"••••••••"))
    def ao_sel(ev):
        s=tab.selection()
        if not s: return
        vals=tab.item(s[0])["values"]; sel_id[0]=vals[0]
        vars_["s"].set(vals[1]); vars_["u"].set(vals[2])
    tab.bind("<<TreeviewSelect>>",ao_sel)
    def revelar():
        s=tab.selection()
        if not s: return
        id_=tab.item(s[0])["values"][0]
        with sqlite3.connect(DB_P) as c:
            row=c.execute("SELECT password FROM entradas WHERE id=?",(id_,)).fetchone()
        if row: tab.item(s[0],values=(id_,tab.item(s[0])["values"][1],tab.item(s[0])["values"][2],row[0]))
    def adicionar():
        s=vars_["s"].get().strip(); u=vars_["u"].get().strip(); p=vars_["p"].get()
        if not s or not p: return
        add(s,u,p); refresh()
        for v in vars_.values(): v.set("")
    def eliminar():
        if not sel_id[0]: return
        delete(sel_id[0]); sel_id[0]=None; refresh()
    bf=tk.Frame(win,bg=OS_COR["fundo"]); bf.pack(pady=(0,8))
    botao(bf,"➕ Adicionar",adicionar,"#16A34A").pack(side="left",padx=5)
    botao(bf,"👁 Revelar",revelar,OS_COR["card"],OS_COR["muted"]).pack(side="left",padx=5)
    botao(bf,"🗑 Eliminar",eliminar,"#DC2626").pack(side="left",padx=5)
    refresh()


# ORÇAMENTO PESSOAL
def abrir_orcamento():
    import tkinter as tk
    from tkinter import ttk
    import sqlite3
    DB_O="orcamento.db"
    def init():
        with sqlite3.connect(DB_O) as c:
            c.execute("CREATE TABLE IF NOT EXISTS mov(id INTEGER PRIMARY KEY AUTOINCREMENT,desc TEXT,valor REAL,tipo TEXT)")
    def get_all():
        with sqlite3.connect(DB_O) as c: return c.execute("SELECT * FROM mov ORDER BY id DESC").fetchall()
    def add(d,v,t):
        with sqlite3.connect(DB_O) as c: c.execute("INSERT INTO mov(desc,valor,tipo) VALUES(?,?,?)",(d,v,t))
    def delete(i):
        with sqlite3.connect(DB_O) as c: c.execute("DELETE FROM mov WHERE id=?",(i,))
    init()
    win=janela_base("Orçamento Pessoal",520,560)
    label_titulo(win,"Orçamento Pessoal","#4ADE80")
    label_sub(win,"Receitas e despesas pessoais")
    sum_f=painel(win); sum_f.pack(padx=24,fill="x",pady=(0,12))
    lbl_rec=tk.Label(sum_f,text="€0.00",font=("Helvetica",18,"bold"),bg=OS_COR["card"],fg="#4ADE80")
    lbl_des=tk.Label(sum_f,text="€0.00",font=("Helvetica",18,"bold"),bg=OS_COR["card"],fg="#F87171")
    lbl_sal=tk.Label(sum_f,text="€0.00",font=("Helvetica",18,"bold"),bg=OS_COR["card"],fg="#FACC15")
    for i,(lbl,lb) in enumerate([("Receitas",lbl_rec),("Saldo",lbl_sal),("Despesas",lbl_des)]):
        col=tk.Frame(sum_f,bg=OS_COR["card"]); col.pack(side="left",expand=True,pady=8)
        tk.Label(col,text=lbl,font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
        lb.pack(in_=col); lb.lift()
        if i<2:
            tk.Frame(sum_f,bg=OS_COR["borda"],width=1).pack(side="left",fill="y",pady=5)
    fp=painel(win); fp.pack(padx=24,fill="x",pady=(0,8))
    fp.columnconfigure(1,weight=1)
    vd=tk.StringVar(); vv=tk.StringVar(); vt=tk.StringVar(value="receita")
    tk.Label(fp,text="Descrição",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=0,column=0,sticky="w",padx=10,pady=4)
    entrada(fp,vd,largura=22).grid(row=0,column=1,sticky="ew",padx=10,pady=4,ipady=3)
    tk.Label(fp,text="Valor (€)",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=1,column=0,sticky="w",padx=10,pady=4)
    entrada(fp,vv,largura=12).grid(row=1,column=1,sticky="w",padx=10,pady=4,ipady=3)
    rf=tk.Frame(fp,bg=OS_COR["card"]); rf.grid(row=2,column=0,columnspan=2,padx=10,pady=4)
    for val,txt,cor in [("receita","💚 Receita","#4ADE80"),("despesa","❤️ Despesa","#F87171")]:
        tk.Radiobutton(rf,text=txt,variable=vt,value=val,bg=OS_COR["card"],fg=cor,
                       selectcolor=OS_COR["card"],activebackground=OS_COR["card"],
                       font=("Helvetica",10,"bold")).pack(side="left",padx=12)
    style=ttk.Style(win); style.theme_use("clam")
    style.configure("ORC.Treeview",background=OS_COR["card"],foreground=OS_COR["branco"],
                    rowheight=24,fieldbackground=OS_COR["card"],font=("Helvetica",9))
    style.configure("ORC.Treeview.Heading",background=OS_COR["taskbar"],foreground=OS_COR["muted"])
    cols=("id","Descrição","Valor","Tipo")
    tab=ttk.Treeview(win,columns=cols,show="headings",selectmode="browse",style="ORC.Treeview")
    for col,w in zip(cols,[30,220,100,100]):
        tab.column(col,width=w); tab.heading(col,text=col)
    tab.pack(padx=24,fill="both",expand=True,pady=4)
    sel_id=[None]
    def refresh():
        for i in tab.get_children(): tab.delete(i)
        rows=get_all(); rec=sum(r[2] for r in rows if r[3]=="receita")
        des=sum(r[2] for r in rows if r[3]=="despesa")
        lbl_rec.config(text=f"€{rec:.2f}"); lbl_des.config(text=f"€{des:.2f}")
        sal=rec-des; cor="#4ADE80" if sal>=0 else "#F87171"
        lbl_sal.config(text=f"€{sal:.2f}",fg=cor)
        for r in rows:
            fg="#4ADE80" if r[3]=="receita" else "#F87171"
            tab.insert("","end",values=(r[0],r[1],f"€{r[2]:.2f}",r[3]),tags=(r[3],))
        tab.tag_configure("receita",foreground="#4ADE80")
        tab.tag_configure("despesa",foreground="#F87171")
    def ao_sel(ev):
        s=tab.selection()
        if s: sel_id[0]=tab.item(s[0])["values"][0]
    tab.bind("<<TreeviewSelect>>",ao_sel)
    def adicionar():
        d=vd.get().strip()
        try: v=float(vv.get().replace(",","."))
        except: return
        if not d or v<=0: return
        add(d,v,vt.get()); vd.set(""); vv.set(""); refresh()
    def eliminar():
        if not sel_id[0]: return
        delete(sel_id[0]); sel_id[0]=None; refresh()
    bf=tk.Frame(win,bg=OS_COR["fundo"]); bf.pack(pady=(0,8))
    botao(bf,"➕ Adicionar",adicionar,"#16A34A").pack(side="left",padx=5)
    botao(bf,"🗑 Eliminar",eliminar,"#DC2626").pack(side="left",padx=5)
    refresh()


# CONVERSOR UNIVERSAL
def abrir_conversor():
    import tkinter as tk
    CATEGORIAS = {
        "Comprimento": [
            ("Metro","m",1),("Quilómetro","km",1000),("Centímetro","cm",0.01),
            ("Milímetro","mm",0.001),("Milha","mi",1609.34),("Pé","ft",0.3048),("Polegada","in",0.0254),
        ],
        "Peso": [
            ("Quilograma","kg",1),("Grama","g",0.001),("Libra","lb",0.453592),
            ("Onça","oz",0.0283495),("Tonelada","t",1000),
        ],
        "Temperatura": [("Celsius","°C",None),("Fahrenheit","°F",None),("Kelvin","K",None)],
        "Velocidade": [
            ("m/s","m/s",1),("km/h","km/h",1/3.6),("mph","mph",0.44704),("nó","kt",0.514444),
        ],
        "Área": [
            ("m²","m²",1),("km²","km²",1e6),("cm²","cm²",0.0001),
            ("Hectare","ha",10000),("Acre","ac",4046.86),
        ],
        "Volume": [
            ("Litro","L",1),("Mililitro","mL",0.001),("m³","m³",1000),
            ("Galão (US)","gal",3.78541),("Pint","pt",0.473176),
        ],
        "Dados": [
            ("Byte","B",1),("Kilobyte","KB",1024),("Megabyte","MB",1048576),
            ("Gigabyte","GB",1073741824),("Terabyte","TB",1099511627776),
        ],
    }
    win=janela_base("Conversor Universal",400,340)
    label_titulo(win,"Conversor Universal","#A78BFA")
    label_sub(win,"Converte entre diferentes unidades")
    cat_v=tk.StringVar(value=list(CATEGORIAS.keys())[0])
    de_v=tk.StringVar(); para_v=tk.StringVar()
    val_v=tk.StringVar(); res_v=tk.StringVar(value="—")
    fp=painel(win); fp.pack(padx=24,fill="x",pady=(0,10)); fp.columnconfigure(1,weight=1)
    tk.Label(fp,text="Categoria",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=0,column=0,sticky="w",padx=10,pady=5)
    cat_box=tk.OptionMenu(fp,cat_v,*CATEGORIAS.keys()); cat_box.config(bg=OS_COR["card"],fg=OS_COR["branco"],relief="flat",highlightthickness=0,font=("Helvetica",9)); cat_box.grid(row=0,column=1,sticky="ew",padx=10,pady=5)
    def atualizar_unidades(*_):
        cat=cat_v.get(); uns=[u[0] for u in CATEGORIAS[cat]]
        de_v.set(uns[0]); para_v.set(uns[1] if len(uns)>1 else uns[0])
        for menu,var in [(de_menu,de_v),(para_menu,para_v)]:
            menu["menu"].delete(0,"end")
            for u in uns: menu["menu"].add_command(label=u,command=tk._setit(var,u))
    tk.Label(fp,text="De",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=1,column=0,sticky="w",padx=10,pady=5)
    de_menu=tk.OptionMenu(fp,de_v,"—"); de_menu.config(bg=OS_COR["card"],fg=OS_COR["branco"],relief="flat",highlightthickness=0,font=("Helvetica",9)); de_menu.grid(row=1,column=1,sticky="ew",padx=10)
    tk.Label(fp,text="Para",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=2,column=0,sticky="w",padx=10,pady=5)
    para_menu=tk.OptionMenu(fp,para_v,"—"); para_menu.config(bg=OS_COR["card"],fg=OS_COR["branco"],relief="flat",highlightthickness=0,font=("Helvetica",9)); para_menu.grid(row=2,column=1,sticky="ew",padx=10)
    tk.Label(fp,text="Valor",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=3,column=0,sticky="w",padx=10,pady=5)
    entrada(fp,val_v,largura=16).grid(row=3,column=1,sticky="w",padx=10,pady=5,ipady=4)
    cat_v.trace_add("write",atualizar_unidades)
    atualizar_unidades()
    lbl_res=tk.Label(win,text="—",font=("Helvetica",20,"bold"),bg=OS_COR["fundo"],fg="#A78BFA"); lbl_res.pack(pady=8)
    def converter():
        cat=cat_v.get()
        try: val=float(val_v.get().replace(",","."))
        except: lbl_res.config(text="Valor inválido",fg=OS_COR["vermelho"]); return
        uns=CATEGORIAS[cat]; de_n=de_v.get(); para_n=para_v.get()
        de_u=next((u for u in uns if u[0]==de_n),None)
        para_u=next((u for u in uns if u[0]==para_n),None)
        if not de_u or not para_u: return
        if cat=="Temperatura":
            nomes=[u[1] for u in uns]
            de_s=de_u[1]; para_s=para_u[1]
            if de_s=="°C":
                c=val
            elif de_s=="°F":
                c=(val-32)*5/9
            else:
                c=val-273.15
            if para_s=="°C": res=c
            elif para_s=="°F": res=c*9/5+32
            else: res=c+273.15
        else:
            res=val*de_u[2]/para_u[2]
        txt=f"{res:.6f}".rstrip("0").rstrip(".")
        lbl_res.config(text=f"{val} {de_u[1]} = {txt} {para_u[1]}",fg="#A78BFA")
    botao(win,"Converter",converter,"#7C3AED").pack(pady=(0,8))
    win.bind("<Return>",lambda e: converter())


# GERADOR DE PASSWORDS
def abrir_gerador():
    import tkinter as tk, string, secrets
    win=janela_base("Gerador de Passwords",380,360)
    label_titulo(win,"Gerador de Passwords","#F59E0B")
    label_sub(win,"Gera passwords seguras e aleatórias")
    fp=painel(win); fp.pack(padx=24,fill="x",pady=(0,12)); fp.columnconfigure(1,weight=1)
    comp_v=tk.IntVar(value=16)
    checks={"Maiúsculas":tk.BooleanVar(value=True),"Minúsculas":tk.BooleanVar(value=True),"Números":tk.BooleanVar(value=True),"Símbolos":tk.BooleanVar(value=False)}
    tk.Label(fp,text="Comprimento",font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=0,column=0,sticky="w",padx=10,pady=6)
    sf=tk.Frame(fp,bg=OS_COR["card"]); sf.grid(row=0,column=1,sticky="w",padx=10,pady=6)
    sl=tk.Scale(sf,from_=4,to=64,orient="horizontal",variable=comp_v,bg=OS_COR["card"],fg=OS_COR["branco"],highlightthickness=0,troughcolor=OS_COR["taskbar"],length=160); sl.pack(side="left")
    tk.Label(sf,textvariable=comp_v,font=("Helvetica",10,"bold"),bg=OS_COR["card"],fg=OS_COR["azul"]).pack(side="left",padx=6)
    for i,(lbl,var) in enumerate(checks.items()):
        tk.Checkbutton(fp,text=lbl,variable=var,bg=OS_COR["card"],fg=OS_COR["branco"],
                       selectcolor=OS_COR["taskbar"],activebackground=OS_COR["card"],
                       font=("Helvetica",9)).grid(row=i+1,column=0,columnspan=2,sticky="w",padx=10,pady=2)
    lbl_pw=tk.Label(win,text="",font=("Consolas",12,"bold"),bg=OS_COR["fundo"],
                    fg="#F59E0B",wraplength=320); lbl_pw.pack(pady=(8,4))
    lbl_f=tk.Label(win,text="",font=("Helvetica",8),bg=OS_COR["fundo"],fg=OS_COR["muted"]); lbl_f.pack()
    def gerar():
        chars=""
        if checks["Maiúsculas"].get(): chars+=string.ascii_uppercase
        if checks["Minúsculas"].get(): chars+=string.ascii_lowercase
        if checks["Números"].get(): chars+=string.digits
        if checks["Símbolos"].get(): chars+=string.punctuation
        if not chars: lbl_pw.config(text="Selecciona pelo menos uma opção"); return
        pw="".join(secrets.choice(chars) for _ in range(comp_v.get()))
        lbl_pw.config(text=pw)
        import math
        entropia=len(pw)*math.log2(len(chars))
        nivel="Fraca" if entropia<40 else "Razoável" if entropia<60 else "Forte" if entropia<80 else "Muito forte"
        lbl_f.config(text=f"Entropia: {entropia:.0f} bits  •  {nivel}")
    def copiar():
        pw=lbl_pw.cget("text")
        if pw and pw!="Selecciona pelo menos uma opção":
            win.clipboard_clear(); win.clipboard_append(pw)
            lbl_f.config(text="Copiado para a área de transferência!")
    bf=tk.Frame(win,bg=OS_COR["fundo"]); bf.pack(pady=(6,0))
    botao(bf,"🎲 Gerar",gerar,"#D97706").pack(side="left",padx=5)
    botao(bf,"📋 Copiar",copiar,OS_COR["card"],OS_COR["muted"]).pack(side="left",padx=5)
    gerar()


# CRONÓMETRO + TEMPORIZADOR
def abrir_cronometro():
    import tkinter as tk, time
    win=janela_base("Cronómetro + Temporizador",360,440)
    nb=tk.Frame(win,bg=OS_COR["taskbar"]); nb.pack(fill="x")
    modo=tk.StringVar(value="crono")
    for m,t in [("crono","⏱ Cronómetro"),("timer","⏳ Temporizador")]:
        tk.Radiobutton(nb,text=t,variable=modo,value=m,bg=OS_COR["taskbar"],fg=OS_COR["branco"],
                       selectcolor=OS_COR["azul"],activebackground=OS_COR["taskbar"],
                       font=("Helvetica",10,"bold"),indicatoron=False,
                       relief="flat",padx=14,pady=8).pack(side="left")
    lbl_main=tk.Label(win,text="00:00.0",font=("Consolas",52,"bold"),
                      bg=OS_COR["fundo"],fg=OS_COR["branco"]); lbl_main.pack(pady=(20,4))
    lbl_sub=tk.Label(win,text="",font=("Helvetica",9),bg=OS_COR["fundo"],fg=OS_COR["muted"]); lbl_sub.pack()
    running=[False]; start_t=[0]; elapsed=[0]; job=[None]
    timer_h=tk.StringVar(value="0"); timer_m=tk.StringVar(value="5"); timer_s_v=tk.StringVar(value="0")
    timer_total=[300]; timer_left=[300]
    tf=tk.Frame(win,bg=OS_COR["fundo"]); tf.pack(pady=6)
    for v,lbl in [(timer_h,"h"),(timer_m,"m"),(timer_s_v,"s")]:
        entrada(tf,v,largura=4).pack(side="left",padx=2,ipady=4)
        tk.Label(tf,text=lbl,font=("Helvetica",10),bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(side="left")
    voltas_f=tk.Frame(win,bg=OS_COR["fundo"]); voltas_f.pack(pady=2,fill="x",padx=24)
    voltas=[]
    def fmt_c(s): return f"{int(s//60):02d}:{s%60:05.2f}" if s<3600 else f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{s%60:05.2f}"
    def fmt_t(s): return f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{int(s%60):02d}"
    def tick_crono():
        if not running[0]: return
        elapsed[0]=time.time()-start_t[0]
        lbl_main.config(text=fmt_c(elapsed[0]))
        job[0]=win.after(100,tick_crono)
    def tick_timer():
        if not running[0]: return
        timer_left[0]=timer_total[0]-(time.time()-start_t[0])
        if timer_left[0]<=0:
            timer_left[0]=0; running[0]=False
            lbl_main.config(text="00:00:00",fg="#F87171")
            lbl_sub.config(text="⏰ Tempo esgotado!")
            return
        lbl_main.config(text=fmt_t(timer_left[0]),fg=OS_COR["branco"])
        job[0]=win.after(100,tick_timer)
    def iniciar():
        if running[0]: return
        if modo.get()=="crono":
            start_t[0]=time.time()-elapsed[0]; running[0]=True; tick_crono()
        else:
            try: t=int(timer_h.get())*3600+int(timer_m.get())*60+int(timer_s_v.get())
            except: return
            if t<=0: return
            timer_total[0]=t; timer_left[0]=t
            start_t[0]=time.time(); running[0]=True; tick_timer()
    def parar():
        running[0]=False
        if job[0]: win.after_cancel(job[0])
    def reset():
        parar(); elapsed[0]=0; timer_left[0]=timer_total[0]
        lbl_main.config(text="00:00.0" if modo.get()=="crono" else fmt_t(timer_total[0]),fg=OS_COR["branco"])
        lbl_sub.config(text="")
        for w in voltas_f.winfo_children(): w.destroy()
        voltas.clear()
    def volta():
        if modo.get()!="crono" or not running[0]: return
        t=fmt_c(elapsed[0]); n=len(voltas)+1
        voltas.append(t)
        tk.Label(voltas_f,text=f"Volta {n}: {t}",font=("Consolas",9),
                 bg=OS_COR["fundo"],fg=OS_COR["muted"]).pack(anchor="w")
    bf=tk.Frame(win,bg=OS_COR["fundo"]); bf.pack(pady=(8,0))
    botao(bf,"▶ Iniciar",iniciar,OS_COR["verde"]).pack(side="left",padx=4)
    botao(bf,"⏸ Parar",parar,OS_COR["amarelo"],OS_COR["fundo"]).pack(side="left",padx=4)
    botao(bf,"🔄 Reset",reset,OS_COR["card"]).pack(side="left",padx=4)
    botao(bf,"🏁 Volta",volta,OS_COR["azul"]).pack(side="left",padx=4)


# CALCULADORA CIENTÍFICA
def abrir_cient():
    import tkinter as tk, math
    win=janela_base("Calculadora Científica",380,520)
    COR2={"fundo":"#1C1C1E","ecra":"#2C2C2E","num":"#3A3A3C","op":"#FF9F0A","fn":"#636366","sci":"#2563EB","txt":"#FFF","mut":"#8E8E93","err":"#FF453A","sep":"#3A3A3C"}
    lbl_hist=tk.Label(win,text="",anchor="e",font=("Helvetica",9),bg=COR2["ecra"],fg=COR2["mut"],padx=12,pady=1); lbl_hist.pack(fill="x")
    lbl_ecra=tk.Label(win,text="0",anchor="e",font=("Helvetica",40,"bold"),bg=COR2["ecra"],fg=COR2["txt"],padx=12,pady=6); lbl_ecra.pack(fill="x")
    tk.Frame(win,bg=COR2["sep"],height=1).pack(fill="x")
    grade=tk.Frame(win,bg=COR2["fundo"]); grade.pack(fill="both",expand=True,padx=6,pady=6)
    for c in range(5): grade.columnconfigure(c,weight=1,uniform="c")
    for r in range(7): grade.rowconfigure(r,weight=1,uniform="r")
    disp=["0"]; acum=[None]; opr=[None]; novo=[False]
    def fmt(v):
        if v==int(v) and abs(v)<1e12: return str(int(v))
        return f"{v:.8f}".rstrip("0").rstrip(".")
    def upd():
        txt=disp[0].replace(".",","); tam=40 if len(txt)<10 else 28 if len(txt)<14 else 20
        lbl_ecra.config(text=txt,font=("Helvetica",tam,"bold"),fg=COR2["txt"])
    def err(msg): lbl_ecra.config(text=msg,fg=COR2["err"],font=("Helvetica",22,"bold")); disp[0]="0"; acum[0]=None; opr[0]=None; novo[0]=False; win.after(1800,upd)
    def calc(a,op,b):
        if op=="+": return a+b
        if op=="−": return a-b
        if op=="×": return a*b
        if op=="÷":
            if b==0: raise ZeroDivisionError
            return a/b
    def clicar(t):
        if t in "0123456789":
            if novo[0] or disp[0]=="0": disp[0]=t; novo[0]=False
            elif len(disp[0].replace("-","").replace(",",""))<12: disp[0]+=t
            upd()
        elif t==",":
            if novo[0]: disp[0]="0,"; novo[0]=False
            elif "," not in disp[0]: disp[0]+=","
            upd()
        elif t in ("+","−","×","÷"):
            try: cur=float(disp[0].replace(",","."))
            except: return
            if acum[0] is not None and not novo[0]:
                try: res=calc(acum[0],opr[0],cur)
                except ZeroDivisionError: err("Div/0"); return
                acum[0]=res; disp[0]=fmt(res)
            else: acum[0]=cur
            opr[0]=t; novo[0]=True; lbl_hist.config(text=f"{fmt(acum[0])} {t}"); upd()
        elif t=="=":
            if opr[0] is None or acum[0] is None: return
            try:
                b=float(disp[0].replace(",",".")); res=calc(acum[0],opr[0],b)
            except ZeroDivisionError: err("Div/0"); return
            lbl_hist.config(text=f"{fmt(acum[0])} {opr[0]} {fmt(b)} =")
            disp[0]=fmt(res); acum[0]=None; opr[0]=None; novo[0]=True; upd()
        elif t=="AC": disp[0]="0"; acum[0]=None; opr[0]=None; novo[0]=False; lbl_hist.config(text=""); upd()
        elif t=="DEL":
            if novo[0]: return
            disp[0]="0" if len(disp[0])<=1 else disp[0][:-1]; upd()
        elif t=="+/−":
            try: v=float(disp[0].replace(",",".")); disp[0]=fmt(-v); upd()
            except: pass
        elif t=="%":
            try: v=float(disp[0].replace(",",".")); disp[0]=fmt(v/100); upd()
            except: pass
        else:
            try:
                v=float(disp[0].replace(",","."))
                funcs={"sin":math.sin,"cos":math.cos,"tan":math.tan,"√":math.sqrt,"log":math.log10,"ln":math.log,"x²":lambda x:x**2,"x³":lambda x:x**3,"1/x":lambda x:1/x,"π":lambda _:math.pi,"e":lambda _:math.e,"!":lambda x:math.factorial(int(round(x))),"abs":abs}
                if t in funcs: res=funcs[t](v if t not in ("π","e") else 0); disp[0]=fmt(res); novo[0]=True; upd()
            except Exception as ex: err("Erro")
    layout=[
        ("sin","sci"),("cos","sci"),("tan","sci"),("log","sci"),("ln","sci"),
        ("√","sci"),("x²","sci"),("x³","sci"),("1/x","sci"),("!","sci"),
        ("π","sci"),("e","sci"),("AC","fn"),("+/−","fn"),("%","fn"),
        ("7","num"),("8","num"),("9","num"),("÷","op"),("DEL","fn"),
        ("4","num"),("5","num"),("6","num"),("×","op"),None,
        ("1","num"),("2","num"),("3","num"),("−","op"),None,
        ("0","num"),(",","num"),("=","op"),("+","op"),None,
    ]
    cores={"num":(COR2["num"],"#4A4A4C"),"op":(COR2["op"],"#FFB340"),"fn":(COR2["fn"],"#7A7A7E"),"sci":(COR2["sci"],"#3B82F6")}
    for i,item in enumerate(layout):
        r,c=divmod(i,5)
        if item is None: continue
        txt_,tipo=item; bg,hv=cores[tipo]
        wr=tk.Frame(grade,bg=COR2["fundo"],padx=2,pady=2); wr.grid(row=r,column=c,sticky="nsew")
        b=tk.Label(wr,text=txt_,font=("Helvetica",13,"bold"),bg=bg,fg=COR2["txt"],anchor="center",cursor="hand2",highlightbackground=COR2["fundo"],highlightthickness=1,relief="flat"); b.pack(fill="both",expand=True)
        b.bind("<Enter>",lambda e,w=b,c_=hv:w.config(bg=c_))
        b.bind("<Leave>",lambda e,w=b,c_=bg:w.config(bg=c_))
        b.bind("<Button-1>",lambda e,t=txt_:clicar(t))
        wr.bind("<Button-1>",lambda e,t=txt_:clicar(t))
    win.bind("<Return>",lambda e:clicar("="))
    win.bind("<BackSpace>",lambda e:clicar("DEL"))
    win.bind("<Escape>",lambda e:clicar("AC"))
    win.bind("<KeyPress>",lambda e:clicar(e.char) if e.char in "0123456789" else None)


# SIMULADOR DE EMPRÉSTIMO
def abrir_emprestimo():
    import tkinter as tk
    win=janela_base("Simulador de Empréstimo",420,440)
    label_titulo(win,"Simulador de Empréstimo","#38BDF8")
    label_sub(win,"Calcula prestações e juros totais")
    fp=painel(win); fp.pack(padx=24,fill="x",pady=(0,10)); fp.columnconfigure(1,weight=1)
    campos=[("Capital (€)","cap"),("Taxa anual (%)","taxa"),("Prazo (anos)","anos")]
    vars_={k:tk.StringVar() for _,k in campos}
    for i,(lbl,k) in enumerate(campos):
        tk.Label(fp,text=lbl,font=("Helvetica",9),bg=OS_COR["card"],fg=OS_COR["muted"]).grid(row=i,column=0,sticky="w",padx=12,pady=6)
        entrada(fp,vars_[k],largura=16).grid(row=i,column=1,sticky="w",padx=12,pady=6,ipady=4)
    res_f=painel(win); res_f.pack(padx=24,fill="x",pady=(0,10))
    lbls_res={}
    for i,(k,lbl,cor) in enumerate([("prest","Prestação mensal","#FACC15"),("total","Total a pagar","#F87171"),("juros","Total de juros","#FB923C")]):
        col=tk.Frame(res_f,bg=OS_COR["card"]); col.pack(side="left",expand=True,pady=10)
        tk.Label(col,text=lbl,font=("Helvetica",7),bg=OS_COR["card"],fg=OS_COR["muted"]).pack()
        l=tk.Label(col,text="—",font=("Helvetica",15,"bold"),bg=OS_COR["card"],fg=cor); l.pack()
        lbls_res[k]=l
        if i<2: tk.Frame(res_f,bg=OS_COR["borda"],width=1).pack(side="left",fill="y",pady=6)
    cv=tk.Canvas(win,height=120,bg=OS_COR["card"],highlightthickness=0); cv.pack(padx=24,fill="x")
    def calcular():
        try:
            cap=float(vars_["cap"].get().replace(",",".")); taxa=float(vars_["taxa"].get().replace(",","."))/ 100/12; anos=int(vars_["anos"].get()); n=anos*12
        except: return
        if cap<=0 or taxa<0 or anos<=0: return
        if taxa==0: prest=cap/n
        else: prest=cap*(taxa*(1+taxa)**n)/((1+taxa)**n-1)
        total=prest*n; juros=total-cap
        lbls_res["prest"].config(text=f"€{prest:.2f}")
        lbls_res["total"].config(text=f"€{total:.2f}")
        lbls_res["juros"].config(text=f"€{juros:.2f}")
        cv.update_idletasks(); w=cv.winfo_width(); h=120
        cv.delete("all")
        cap_w=int(cap/total*w); jur_w=w-cap_w
        cv.create_rectangle(0,20,cap_w,70,fill="#38BDF8",outline="")
        cv.create_rectangle(cap_w,20,w,70,fill="#F87171",outline="")
        cv.create_text(cap_w//2,45,text=f"Capital\n{cap/total*100:.0f}%",fill="white",font=("Helvetica",8,"bold"))
        cv.create_text(cap_w+jur_w//2,45,text=f"Juros\n{juros/total*100:.0f}%",fill="white",font=("Helvetica",8,"bold"))
        meses=list(range(n+1)); saldo=[cap]
        for _ in range(n): saldo.append(max(0,saldo[-1]*(1+taxa)-prest))
        pw=w/(n+1)
        for i in range(n): 
            x1=i*pw; x2=(i+1)*pw; y1=80+int((1-saldo[i]/cap)*35); y2=80+int((1-saldo[i+1]/cap)*35) if i<n-1 else 115
            cv.create_rectangle(x1,y1,x2,115,fill="#38BDF8",outline="")
    botao(win,"Calcular",calcular,OS_COR["azul"]).pack(pady=(0,8))
    win.bind("<Return>",lambda e:calcular())


# JOGO DA MEMÓRIA
def abrir_memoria():
    import tkinter as tk, random
    EMOJIS=["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🦁","🐯","🐸","🐵","🦋","🐝","🌸","⭐"]
    win=janela_base("Jogo da Memória",480,560)
    win.configure(bg="#0F172A")
    label_titulo(win,"JOGO DA MEMÓRIA","#22D3EE")
    sf=tk.Frame(win,bg="#0F172A"); sf.pack(pady=(0,8))
    lbl_mv=tk.Label(sf,text="Movimentos: 0",font=("Helvetica",10),bg="#0F172A",fg=OS_COR["muted"]); lbl_mv.pack(side="left",padx=10)
    lbl_par=tk.Label(sf,text="Pares: 0/16",font=("Helvetica",10),bg="#0F172A",fg=OS_COR["muted"]); lbl_par.pack(side="left",padx=10)
    grade=tk.Frame(win,bg="#0F172A"); grade.pack(pady=4)
    cartas=[]; viradas=[]; pares=[0]; movs=[0]; bloqueado=[False]
    def novo():
        for w in grade.winfo_children(): w.destroy()
        cartas.clear(); viradas.clear(); pares[0]=0; movs[0]=0; bloqueado[0]=False
        emojis=random.sample(EMOJIS,16); emojis=emojis+emojis; random.shuffle(emojis)
        lbl_mv.config(text="Movimentos: 0"); lbl_par.config(text="Pares: 0/16")
        for i,em in enumerate(emojis):
            r,c=divmod(i,8)
            btn=tk.Label(grade,text="",width=4,height=2,font=("Helvetica",20),
                         bg="#1E293B",cursor="hand2",relief="flat",
                         highlightbackground="#334155",highlightthickness=1)
            btn.grid(row=r,column=c,padx=3,pady=3)
            btn.bind("<Button-1>",lambda e,idx=i,b=btn,em_=em:virar(idx,b,em_))
            cartas.append({"btn":btn,"emoji":em,"virada":False,"par":False})
    def virar(idx,btn,em):
        if bloqueado[0] or cartas[idx]["par"] or cartas[idx]["virada"]: return
        cartas[idx]["virada"]=True; btn.config(text=em,bg="#1E3A5F")
        viradas.append(idx)
        if len(viradas)==2:
            movs[0]+=1; lbl_mv.config(text=f"Movimentos: {movs[0]}")
            bloqueado[0]=True
            if cartas[viradas[0]]["emoji"]==cartas[viradas[1]]["emoji"]:
                for i in viradas:
                    cartas[i]["par"]=True; cartas[i]["btn"].config(bg="#14532D")
                pares[0]+=1; lbl_par.config(text=f"Pares: {pares[0]}/16")
                viradas.clear(); bloqueado[0]=False
                if pares[0]==16: lbl_par.config(text=f"🏆 Completo em {movs[0]} movimentos!",fg=OS_COR["verde"])
            else:
                def esconder():
                    for i in viradas:
                        cartas[i]["virada"]=False; cartas[i]["btn"].config(text="",bg="#1E293B")
                    viradas.clear(); bloqueado[0]=False
                win.after(800,esconder)
    botao(win,"🔄 Novo Jogo",novo,"#22D3EE","#0F172A").pack(pady=(6,0))
    novo()


# -*- coding: utf-8 -*-

# CAÇA AO TESOURO
def abrir_caca():
    import tkinter as tk, random
    GRID=10; CELL=44
    win=janela_base("Caça ao Tesouro",GRID*CELL+40,GRID*CELL+140)
    win.configure(bg="#0F172A")
    label_titulo(win,"CAÇA AO TESOURO","#F59E0B")
    sf=tk.Frame(win,bg="#0F172A"); sf.pack()
    lbl_t=tk.Label(sf,text="Tentativas: 0",font=("Helvetica",9),bg="#0F172A",fg=OS_COR["muted"]); lbl_t.pack(side="left",padx=8)
    lbl_m=tk.Label(sf,text="",font=("Helvetica",10,"bold"),bg="#0F172A",fg=OS_COR["amarelo"]); lbl_m.pack(side="left",padx=8)
    cv=tk.Canvas(win,width=GRID*CELL,height=GRID*CELL,bg="#1E293B",highlightthickness=0); cv.pack(pady=8)
    tesouro=[None]; tentativas=[0]; encontrado=[False]; grid_state=[[0]*GRID for _ in range(GRID)]
    def novo():
        tesouro[0]=(random.randint(0,GRID-1),random.randint(0,GRID-1))
        tentativas[0]=0; encontrado[0]=False
        for i in range(GRID):
            for j in range(GRID): grid_state[i][j]=0
        lbl_t.config(text="Tentativas: 0"); lbl_m.config(text="Clica num quadrado!")
        desenhar()
    def desenhar():
        cv.delete("all")
        for r in range(GRID):
            for c in range(GRID):
                x1=c*CELL; y1=r*CELL; x2=x1+CELL-2; y2=y1+CELL-2
                s=grid_state[r][c]
                if s==0: cor="#1E3A5F"
                elif s==1: cor="#075985"
                elif s==2: cor="#0c4a6e"
                elif s==3: cor="#0369a1"
                elif s==4: cor="#F59E0B"
                else: cor="#14532D"
                cv.create_rectangle(x1,y1,x2,y2,fill=cor,outline="#0F172A",width=1)
                if s>0 and s<4:
                    hints=["🔥","🌡","❄"][s-1] if s<=3 else ""
                    cv.create_text(x1+CELL//2,y1+CELL//2,text=hints,font=("Helvetica",16))
                elif s==4: cv.create_text(x1+CELL//2,y1+CELL//2,text="💎",font=("Helvetica",18))
    def clique(ev):
        if encontrado[0]: return
        c=ev.x//CELL; r=ev.y//CELL
        if not(0<=r<GRID and 0<=c<GRID): return
        tentativas[0]+=1; lbl_t.config(text=f"Tentativas: {tentativas[0]}")
        tr,tc=tesouro[0]
        dist=abs(r-tr)+abs(c-tc)
        if dist==0: grid_state[r][c]=4; encontrado[0]=True; lbl_m.config(text=f"🏆 Encontrado em {tentativas[0]} tentativas!",fg=OS_COR["verde"])
        elif dist<=2: grid_state[r][c]=1; lbl_m.config(text="🔥 Muito quente!",fg="#F87171")
        elif dist<=4: grid_state[r][c]=2; lbl_m.config(text="🌡 Quente!",fg="#FB923C")
        elif dist<=6: grid_state[r][c]=3; lbl_m.config(text="❄ Frio!",fg="#38BDF8")
        else: grid_state[r][c]=3; lbl_m.config(text="🧊 Muito frio!",fg="#7DD3FC")
        desenhar()
    cv.bind("<Button-1>",clique)
    botao(win,"🔄 Novo Jogo",novo,"#D97706").pack(pady=(0,6))
    novo()


# FLAPPY BIRD
def abrir_flappy():
    import tkinter as tk, random
    W=400; H=500; G=0.5; JUMP=-9; PIPE_W=60; GAP=140; PIPE_SPEED=3
    win=janela_base("Flappy Bird",W,H)
    cv=tk.Canvas(win,width=W,height=H,bg="#87CEEB",highlightthickness=0); cv.pack()
    by=[H//2]; bv=[0]; pipes=[]; score=[0]; activo=[False]; job=[None]
    def draw_all():
        cv.delete("all")
        # Fundo
        cv.create_rectangle(0,H*0.7,W,H,fill="#90EE90",outline="")
        # Tubos
        for p in pipes:
            cv.create_rectangle(p["x"],0,p["x"]+PIPE_W,p["top"],fill="#228B22",outline="#155d1b",width=2)
            cv.create_rectangle(p["x"]-4,p["top"]-20,p["x"]+PIPE_W+4,p["top"],fill="#2d9e2d",outline="")
            cv.create_rectangle(p["x"],p["top"]+GAP,p["x"]+PIPE_W,H,fill="#228B22",outline="#155d1b",width=2)
            cv.create_rectangle(p["x"]-4,p["top"]+GAP,p["x"]+PIPE_W+4,p["top"]+GAP+20,fill="#2d9e2d",outline="")
        # Pássaro
        cv.create_oval(W//4-18,by[0]-14,W//4+18,by[0]+14,fill="#FFD700",outline="#FFA500",width=2)
        cv.create_oval(W//4+4,by[0]-8,W//4+18,by[0]+4,fill="white",outline="")
        cv.create_oval(W//4+8,by[0]-5,W//4+14,by[0]+1,fill="black",outline="")
        cv.create_polygon(W//4+14,by[0]-4,W//4+24,by[0],W//4+14,by[0]+4,fill="#FF8C00")
        # Score
        cv.create_text(W//2,40,text=str(score[0]),font=("Helvetica",32,"bold"),fill="white")
        if not activo[0]:
            cv.create_rectangle(W//2-120,H//2-50,W//2+120,H//2+60,fill="#000000",stipple="gray50",outline="")
            msg="Pressiona ESPAÇO para começar" if score[0]==0 else f"Fim! Pontuação: {score[0]}\nESPAÇO para jogar de novo"
            cv.create_text(W//2,H//2,text=msg,font=("Helvetica",14,"bold"),fill="white",justify="center")
    def jump(ev=None):
        if not activo[0]: iniciar(); return
        bv[0]=JUMP
    def iniciar():
        by[0]=H//2; bv[0]=0; pipes.clear(); score[0]=0; activo[0]=True
        if job[0]: win.after_cancel(job[0])
        loop()
    def loop():
        if not activo[0]: return
        bv[0]+=G; by[0]+=bv[0]
        if by[0]>H-14 or by[0]<14: fim(); return
        if not pipes or pipes[-1]["x"]<W-200:
            top=random.randint(60,H-GAP-60); pipes.append({"x":W,"top":top,"scored":False})
        for p in pipes:
            p["x"]-=PIPE_SPEED
            if not p["scored"] and p["x"]+PIPE_W<W//4-18:
                p["scored"]=True; score[0]+=1
            if W//4+18>p["x"] and W//4-18<p["x"]+PIPE_W:
                if by[0]-14<p["top"] or by[0]+14>p["top"]+GAP: fim(); return
        pipes[:]=[ p for p in pipes if p["x"]>-PIPE_W]
        draw_all(); job[0]=win.after(20,loop)
    def fim(): activo[0]=False; draw_all()
    win.bind("<space>",jump); win.bind("<Up>",jump); win.bind("<Return>",jump)
    draw_all()


# SPACE SHOOTER
def abrir_space():
    import tkinter as tk, random
    W=420; H=520; SHIP_SPEED=5
    win=janela_base("Space Shooter",W,H)
    cv=tk.Canvas(win,width=W,height=H,bg="#0D1117",highlightthickness=0); cv.pack()
    sx=[W//2]; sy=[H-60]; bullets=[]; enemies=[]; score=[0]; lives=[3]; activo=[False]; job=[None]
    keys={"left":False,"right":False,"space":False}
    last_shot=[0]
    def stars():
        for _ in range(60): cv.create_oval(random.randint(0,W),random.randint(0,H),2,2,fill="white",tags="star")
    def draw():
        cv.delete("all")
        # Fundo estrelado
        for _ in range(60):
            x=random.randint(0,W); y=random.randint(0,H)
            cv.create_oval(x,y,x+1,y+1,fill="white")
        # Nave
        cv.create_polygon(sx[0],sy[0]-20,sx[0]-15,sy[0]+15,sx[0]+15,sy[0]+15,fill="#38BDF8",outline="#7DD3FC",width=1)
        cv.create_polygon(sx[0]-8,sy[0]+8,sx[0]-16,sy[0]+20,sx[0],sy[0]+10,fill="#FB923C")
        cv.create_polygon(sx[0]+8,sy[0]+8,sx[0]+16,sy[0]+20,sx[0],sy[0]+10,fill="#FB923C")
        # Balas
        for b in bullets:
            cv.create_rectangle(b[0]-2,b[1]-8,b[0]+2,b[1]+8,fill="#FACC15",outline="")
        # Inimigos
        for e in enemies:
            cv.create_polygon(e[0],e[1]+15,e[0]-15,e[1]-10,e[0]+15,e[1]-10,fill="#F87171",outline="#FCA5A5",width=1)
            cv.create_oval(e[0]-5,e[1]-6,e[0]+5,e[1]+4,fill="#0D1117")
        # HUD
        cv.create_text(16,16,text=f"Score: {score[0]}",font=("Helvetica",12,"bold"),fill="white",anchor="w")
        cv.create_text(W-16,16,text="❤ "*lives[0],font=("Helvetica",12),fill="#F87171",anchor="e")
        if not activo[0]:
            cv.create_rectangle(W//2-130,H//2-50,W//2+130,H//2+60,fill="#000000",stipple="gray50",outline="")
            msg="ENTER para começar" if score[0]==0 else f"Game Over!\nScore: {score[0]}\nENTER para jogar de novo"
            cv.create_text(W//2,H//2,text=msg,font=("Helvetica",14,"bold"),fill="white",justify="center")
    import time
    def loop():
        if not activo[0]: return
        if keys["left"] and sx[0]>20: sx[0]-=SHIP_SPEED
        if keys["right"] and sx[0]<W-20: sx[0]+=SHIP_SPEED
        if keys["space"]:
            now=time.time()
            if now-last_shot[0]>0.25: bullets.append([sx[0],sy[0]-22]); last_shot[0]=now
        for b in bullets: b[1]-=8
        bullets[:]=[b for b in bullets if b[1]>0]
        if random.random()<0.025: enemies.append([random.randint(20,W-20),0])
        for e in enemies: e[1]+=2+score[0]//10
        # Colisão bala-inimigo
        to_rem_b=set(); to_rem_e=set()
        for bi,b in enumerate(bullets):
            for ei,e in enumerate(enemies):
                if abs(b[0]-e[0])<18 and abs(b[1]-e[1])<18:
                    to_rem_b.add(bi); to_rem_e.add(ei); score[0]+=10
        bullets[:]=[b for i,b in enumerate(bullets) if i not in to_rem_b]
        enemies[:]=[e for i,e in enumerate(enemies) if i not in to_rem_e]
        # Inimigos chegam ao fundo
        mortos=[e for e in enemies if e[1]>H-30]
        if mortos:
            enemies[:]=[e for e in enemies if e[1]<=H-30]
            lives[0]-=1
            if lives[0]<=0: activo[0]=False; draw(); return
        draw(); job[0]=win.after(30,loop)
    def iniciar(ev=None):
        if activo[0]: return
        sx[0]=W//2; bullets.clear(); enemies.clear(); score[0]=0; lives[0]=3; activo[0]=True; loop()
    win.bind("<Left>",    lambda e: keys.update({"left":True}))
    win.bind("<Right>",   lambda e: keys.update({"right":True}))
    win.bind("<KeyRelease-Left>", lambda e: keys.update({"left":False}))
    win.bind("<KeyRelease-Right>",lambda e: keys.update({"right":False}))
    win.bind("<space>",   lambda e: keys.update({"space":True}))
    win.bind("<KeyRelease-space>",lambda e: keys.update({"space":False}))
    win.bind("<Return>",  iniciar)
    win.focus_set(); draw()


# SIMON SAYS
def abrir_simon():
    import tkinter as tk, random, time
    CORES_S=["#F87171","#4ADE80","#FACC15","#60A5FA"]
    NOMES=["Vermelho","Verde","Amarelo","Azul"]
    win=janela_base("Simon Says",380,440)
    win.configure(bg="#0F172A")
    label_titulo(win,"SIMON SAYS","#A78BFA")
    lbl_nivel=tk.Label(win,text="Nível: 0",font=("Helvetica",10),bg="#0F172A",fg=OS_COR["muted"]); lbl_nivel.pack()
    lbl_msg=tk.Label(win,text="Pressiona Iniciar",font=("Helvetica",11,"bold"),bg="#0F172A",fg=OS_COR["branco"]); lbl_msg.pack(pady=4)
    grade=tk.Frame(win,bg="#0F172A"); grade.pack(pady=8)
    btns=[]; sequencia=[]; idx=[0]; a_jogar=[False]; record=[0]
    lbl_rec=tk.Label(win,text="Recorde: 0",font=("Helvetica",9),bg="#0F172A",fg=OS_COR["muted"]); lbl_rec.pack()
    def iluminar(i,delay=0):
        def on(): btns[i].config(bg=CORES_S[i])
        def off(): btns[i].config(bg=dim(i))
        win.after(delay,on); win.after(delay+400,off)
    def dim(i): return CORES_S[i]+"66" if len(CORES_S[i])==7 else "#333"
    DIM=["#7F2E2E","#1F6630","#7A6210","#1E3A6E"]
    def iluminar2(i,delay=0):
        def on(): btns[i].config(bg=CORES_S[i])
        def off(): btns[i].config(bg=DIM[i])
        win.after(delay,on); win.after(delay+350,off)
    def mostrar_seq():
        a_jogar[0]=False; lbl_msg.config(text="Observa...",fg=OS_COR["amarelo"])
        for j,c in enumerate(sequencia):
            iluminar2(c,j*600)
        win.after(len(sequencia)*600+200,lambda:(lbl_msg.config(text="A tua vez!",fg=OS_COR["verde"]),a_jogar.__setitem__(0,True),idx.__setitem__(0,0)))
    def clicar(i):
        if not a_jogar[0]: return
        iluminar2(i)
        if sequencia[idx[0]]==i:
            idx[0]+=1
            if idx[0]==len(sequencia):
                a_jogar[0]=False; lbl_nivel.config(text=f"Nível: {len(sequencia)}")
                if len(sequencia)>record[0]: record[0]=len(sequencia); lbl_rec.config(text=f"Recorde: {record[0]}")
                sequencia.append(random.randint(0,3))
                win.after(800,mostrar_seq)
        else:
            a_jogar[0]=False; lbl_msg.config(text=f"❌ Errado! Chegaste ao nível {len(sequencia)-1}",fg=OS_COR["vermelho"])
    for i in range(4):
        r,c=divmod(i,2)
        b=tk.Label(grade,width=8,height=4,bg=DIM[i],cursor="hand2",relief="flat",
                   highlightbackground="#0F172A",highlightthickness=3)
        b.grid(row=r,column=c,padx=6,pady=6)
        b.bind("<Button-1>",lambda e,i_=i:clicar(i_))
        btns.append(b)
    def iniciar():
        sequencia.clear(); sequencia.append(random.randint(0,3))
        idx[0]=0; lbl_nivel.config(text="Nível: 1"); mostrar_seq()
    botao(win,"▶ Iniciar",iniciar,"#7C3AED").pack(pady=(8,0))
    # fix: pass iniciar as command


# BLACKJACK
def abrir_blackjack():
    import tkinter as tk, random
    NAIPES=["♠","♥","♦","♣"]; VALORES=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    def novo_baralho():
        b=[(v,n) for v in VALORES for n in NAIPES]; random.shuffle(b); return b
    def valor_mao(mao):
        s=0; ases=0
        for v,_ in mao:
            if v in ("J","Q","K"): s+=10
            elif v=="A": s+=11; ases+=1
            else: s+=int(v)
        while s>21 and ases: s-=10; ases-=1
        return s
    def fmt_carta(c): return f"{c[0]}{c[1]}"
    def cor_carta(c): return "#F87171" if c[1] in ("♥","♦") else OS_COR["branco"]
    win=janela_base("Blackjack",480,500); win.configure(bg="#0B4A2A")
    tk.Label(win,text="BLACKJACK",font=("Helvetica",18,"bold"),bg="#0B4A2A",fg="#FFD700").pack(pady=(14,2))
    fichas=[1000]; baralho=[novo_baralho()]; mao_j=[]; mao_d=[]; aposta=[0]
    lbl_fichas=tk.Label(win,text="Fichas: €1000",font=("Helvetica",11,"bold"),bg="#0B4A2A",fg="#FFD700"); lbl_fichas.pack()
    lbl_msg=tk.Label(win,text="Faz uma aposta!",font=("Helvetica",11),bg="#0B4A2A",fg="white"); lbl_msg.pack(pady=2)
    # Dealer
    tk.Label(win,text="DEALER",font=("Helvetica",8),bg="#0B4A2A",fg="#94A3B8").pack()
    frame_d=tk.Frame(win,bg="#0B4A2A"); frame_d.pack(pady=2)
    lbl_val_d=tk.Label(win,text="",font=("Helvetica",9),bg="#0B4A2A",fg="#94A3B8"); lbl_val_d.pack()
    # Jogador
    tk.Label(win,text="TU",font=("Helvetica",8),bg="#0B4A2A",fg="#94A3B8").pack(pady=(8,0))
    frame_j=tk.Frame(win,bg="#0B4A2A"); frame_j.pack(pady=2)
    lbl_val_j=tk.Label(win,text="",font=("Helvetica",9),bg="#0B4A2A",fg="#94A3B8"); lbl_val_j.pack()
    # Aposta
    ap_f=tk.Frame(win,bg="#0B4A2A"); ap_f.pack(pady=6)
    ap_v=tk.StringVar(value="50")
    tk.Label(ap_f,text="Aposta: €",font=("Helvetica",10),bg="#0B4A2A",fg="white").pack(side="left")
    tk.Entry(ap_f,textvariable=ap_v,width=6,font=("Helvetica",10),bg="#0B4A2A",fg="white",insertbackground="white",relief="flat",highlightbackground="#FFD700",highlightthickness=1).pack(side="left",padx=4)
    btn_f=tk.Frame(win,bg="#0B4A2A"); btn_f.pack(pady=4)
    def desenhar_maos(revelar_dealer=False):
        for w in frame_d.winfo_children(): w.destroy()
        for w in frame_j.winfo_children(): w.destroy()
        for i,(v,n) in enumerate(mao_d):
            mostrar = i>0 or revelar_dealer
            txt=f"{v}{n}" if mostrar else "🂠"
            c=cor_carta((v,n)) if mostrar else "#94A3B8"
            f=tk.Frame(frame_d,bg="#fff" if mostrar else "#1E3A5F",padx=6,pady=4,relief="raised",bd=1); f.pack(side="left",padx=3)
            tk.Label(f,text=txt,font=("Helvetica",16,"bold"),bg=f.cget("bg"),fg=c).pack()
        for v,n in mao_j:
            f=tk.Frame(frame_j,bg="white",padx=6,pady=4,relief="raised",bd=1); f.pack(side="left",padx=3)
            tk.Label(f,text=f"{v}{n}",font=("Helvetica",16,"bold"),bg="white",fg=cor_carta((v,n))).pack()
        vj=valor_mao(mao_j); lbl_val_j.config(text=f"Valor: {vj}" if vj else "")
        vd=valor_mao(mao_d) if revelar_dealer else "?"
        lbl_val_d.config(text=f"Valor: {vd}")
    def comprar(): return baralho[0].pop() if baralho[0] else (baralho.__setitem__(0,novo_baralho()),baralho[0].pop())[1]
    def nova_ronda():
        try: ap=int(ap_v.get())
        except: ap=50
        if ap<=0 or ap>fichas[0]: lbl_msg.config(text="Aposta inválida!"); return
        aposta[0]=ap; mao_j.clear(); mao_d.clear()
        mao_j.extend([comprar(),comprar()]); mao_d.extend([comprar(),comprar()])
        for b in btn_f.winfo_children(): b.destroy()
        botao(btn_f,"🃏 Pedir",pedir,"#16A34A").pack(side="left",padx=4)
        botao(btn_f,"✋ Parar",parar,OS_COR["azul"]).pack(side="left",padx=4)
        desenhar_maos(); lbl_msg.config(text=f"Aposta: €{ap} — Pede ou para?")
        if valor_mao(mao_j)==21: parar()
    def pedir():
        mao_j.append(comprar()); desenhar_maos()
        if valor_mao(mao_j)>21: fim("bust")
    def parar():
        while valor_mao(mao_d)<17: mao_d.append(comprar())
        desenhar_maos(True); fim("normal")
    def fim(tipo):
        for b in btn_f.winfo_children(): b.destroy()
        vj=valor_mao(mao_j); vd=valor_mao(mao_d)
        if tipo=="bust" or (tipo=="normal" and vd>=vj and vd<=21 and vd!=vj):
            fichas[0]-=aposta[0]; lbl_msg.config(text=f"❌ Perdeste €{aposta[0]}!",fg="#F87171")
        elif vj>21: fichas[0]-=aposta[0]; lbl_msg.config(text=f"❌ Ultrapassaste 21! -€{aposta[0]}",fg="#F87171")
        elif vd>21 or vj>vd: fichas[0]+=aposta[0]; lbl_msg.config(text=f"✅ Ganhaste €{aposta[0]}!",fg="#4ADE80")
        else: lbl_msg.config(text="🤝 Empate!",fg="#FACC15")
        lbl_fichas.config(text=f"Fichas: €{fichas[0]}")
        botao(btn_f,"🔄 Nova Ronda",nova_ronda,"#D97706").pack(pady=4)
        if fichas[0]<=0: lbl_msg.config(text="💸 Sem fichas! Jogo terminado.",fg="#F87171")
        desenhar_maos(True)
    botao(btn_f,"▶ Iniciar",nova_ronda,"#D97706").pack(pady=4)


# CORRIDA DE REFLEXOS
def abrir_reflexos():
    import tkinter as tk, random, time
    win=janela_base("Corrida de Reflexos",400,440); win.configure(bg="#0F172A")
    label_titulo(win,"CORRIDA DE REFLEXOS","#4ADE80")
    label_sub(win,"Clica no alvo assim que aparecer!")
    lbl_record=tk.Label(win,text="Recorde: —",font=("Helvetica",9),bg="#0F172A",fg=OS_COR["muted"]); lbl_record.pack()
    cv=tk.Canvas(win,width=360,height=220,bg="#1E293B",highlightthickness=0); cv.pack(pady=8)
    tempos=[]; record=[None]; estado=["espera"]; t_apareceu=[0]; job=[None]
    lbl_res=tk.Label(win,text="",font=("Helvetica",13,"bold"),bg="#0F172A",fg=OS_COR["branco"]); lbl_res.pack()
    lbl_avg=tk.Label(win,text="",font=("Helvetica",9),bg="#0F172A",fg=OS_COR["muted"]); lbl_avg.pack()
    def mostrar_alvo():
        cv.delete("all")
        x=random.randint(30,330); y=random.randint(30,190)
        r=random.randint(20,40); cor=random.choice(["#F87171","#FACC15","#4ADE80","#60A5FA","#A78BFA"])
        cv.create_oval(x-r,y-r,x+r,y+r,fill=cor,outline="white",width=2,tags="alvo")
        cv.create_text(x,y,text="🎯",font=("Helvetica",int(r*0.8)),tags="alvo")
        estado[0]="aguarda"; t_apareceu[0]=time.time()
    def clique(ev):
        if estado[0]=="espera": return
        if estado[0]=="aguarda":
            items=cv.find_withtag("alvo")
            hit=any(cv.find_closest(ev.x,ev.y)[0]==i for i in items)
            if not hit: 
                # clique fora — penalidade
                tempo=800; tempos.append(tempo)
                lbl_res.config(text="❌ Clicaste fora! +800ms",fg="#F87171")
            else:
                tempo=round((time.time()-t_apareceu[0])*1000)
                tempos.append(tempo)
                cor="#4ADE80" if tempo<250 else "#FACC15" if tempo<500 else "#F87171"
                lbl_res.config(text=f"⚡ {tempo} ms!",fg=cor)
                if record[0] is None or tempo<record[0]:
                    record[0]=tempo; lbl_record.config(text=f"Recorde: {tempo} ms")
            if len(tempos)>0:
                avg=sum(tempos)/len(tempos)
                lbl_avg.config(text=f"Tentativas: {len(tempos)}  •  Média: {avg:.0f} ms")
            cv.delete("all"); estado[0]="espera"
            if len(tempos)<10: proxima()
            else:
                avg=sum(tempos)/len(tempos)
                cv.create_text(180,110,text=f"Fim!\nMédia: {avg:.0f}ms\nRecorde: {record[0]}ms",
                               font=("Helvetica",16,"bold"),fill="white",justify="center")
                estado[0]="fim"
    def proxima():
        delay=random.randint(1000,3000)
        cv.delete("all")
        cv.create_text(180,110,text="Prepara-te...",font=("Helvetica",14),fill="#64748B")
        job[0]=win.after(delay,mostrar_alvo)
    def iniciar():
        tempos.clear(); record[0]=None
        lbl_res.config(text=""); lbl_avg.config(text=""); lbl_record.config(text="Recorde: —")
        estado[0]="espera"; proxima()
    cv.bind("<Button-1>",clique)
    botao(win,"▶ Iniciar",iniciar,OS_COR["verde"]).pack(pady=(0,8))



# ═══════════════════════════════════════════════════════════════════
#  LAUNCHER PRINCIPAL — PythonOS
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
#  DADOS DAS APPS
# ═══════════════════════════════════════════════════════════════════

CATEGORIAS_APPS = {
    "🛠  Ferramentas": [
        ("Calculadora",        "🔢", "Operações matemáticas estilo iOS",          abrir_calculadora,  "#FF9F0A"),
        ("Calc. Científica",   "🧮", "Sin, cos, raiz, log e muito mais",           abrir_cient,        "#FB923C"),
        ("IMC",                "⚕️",  "Índice de Massa Corporal OMS",              abrir_imc,          "#3B82F6"),
        ("Conversor Universal","📐", "Comprimento, peso, temperatura e mais",      abrir_conversor,    "#A78BFA"),
        ("Simulador Empréstimo","🏦","Prestações, juros e amortização",            abrir_emprestimo,   "#38BDF8"),
        ("Orçamento Pessoal",  "💰", "Receitas e despesas com saldo",              abrir_orcamento,    "#4ADE80"),
        ("Cronómetro / Timer", "⏱",  "Cronómetro com voltas e temporizador",      abrir_cronometro,   "#FACC15"),
    ],
    "📁  Produtividade": [
        ("Bloco de Notas",     "📝", "Editor de texto com abrir/guardar",          abrir_notas,        "#64748B"),
        ("Agenda",             "📒", "Contactos com SQLite e pesquisa",            abrir_agenda,       "#4ADE80"),
        ("Gestor de Passwords","🔑", "Guarda passwords localmente",               abrir_passwords,    "#F87171"),
        ("Gerador de Passwords","🎲","Passwords seguras com entropia",             abrir_gerador,      "#F59E0B"),
    ],
    "♟  Jogos de Tabuleiro": [
        ("Jogo do Galo",       "❌", "Tic-Tac-Toe para 2 jogadores",              abrir_galo,         "#F87171"),
        ("Blackjack",          "🃏", "21 com baralho e fichas virtuais",           abrir_blackjack,    "#D97706"),
        ("Jogo da Memória",    "🧩", "Encontra os pares de emojis",               abrir_memoria,      "#22D3EE"),
        ("Simon Says",         "🔴", "Repete a sequência de cores",               abrir_simon,        "#A78BFA"),
    ],
    "🧠  Jogos de Adivinha": [
        ("Adivinhar o Número", "🎯", "1 a 100 com dicas e histórico",             abrir_numero,       "#38BDF8"),
        ("Adiv. de Códigos",   "🔐", "Descobre o código de 3 caracteres",         abrir_codigos,      "#22D3EE"),
        ("Caça ao Tesouro",    "💎", "Encontra o tesouro na grelha",              abrir_caca,         "#F59E0B"),
        ("Forca",              "💀", "Adivinhar palavras com teclado",            abrir_forca,        "#A78BFA"),
        ("Pedra Papel Tesoura","✂️",  "Vs o computador com estatísticas",         abrir_ppt,          "#FB923C"),
        ("Cara ou Coroa",      "🪙", "Moeda com streak e taxa de acerto",          abrir_coc,          "#FACC15"),
    ],
    "🎮  Jogos de Acção": [
        ("Snake",              "🐍", "Cobra clássica com recorde",                abrir_snake,        "#4ADE80"),
        ("Flappy Bird",        "🐦", "Voa entre os tubos!",                       abrir_flappy,       "#FACC15"),
        ("Space Shooter",      "🚀", "Destrói os inimigos com a nave",            abrir_space,        "#F87171"),
        ("Corrida de Reflexos","⚡",  "Testa os teus reflexos em 10 tentativas",  abrir_reflexos,     "#4ADE80"),
    ],
}

TODAS_APPS = [app for apps in CATEGORIAS_APPS.values() for app in apps]

# ═══════════════════════════════════════════════════════════════════
#  PythonOS — LAUNCHER COM SIDEBAR
# ═══════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk
import datetime

class PythonOS:
    SIDEBAR_W = 200

    def __init__(self, root):
        self.root = root
        self.root.title("PythonOS")
        self.root.geometry("1100x680")
        self.root.minsize(900, 560)
        self.root.configure(bg=OS_COR["fundo"])
        self._cat_atual = None   # None = mostrar tudo
        self._pesq_term = ""
        self._construir()

    # ── Layout principal ───────────────────────────────────────────

    def _construir(self):
        # ── Taskbar no topo ────────────────────────────────────────
        self._taskbar()

        # ── Corpo (sidebar + conteúdo) ─────────────────────────────
        body = tk.Frame(self.root, bg=OS_COR["fundo"])
        body.pack(fill="both", expand=True)

        # IMPORTANTE: criar o painel de conteúdo ANTES da sidebar
        # para que _inner exista quando _sel_cat for chamada
        self._content_frame = tk.Frame(body, bg=OS_COR["fundo"])

        self._sidebar(body)

        # Separador vertical
        tk.Frame(body, bg=OS_COR["borda"], width=1).pack(
            side="left", fill="y")

        self._content_frame.pack(side="left", fill="both", expand=True)
        self._painel_conteudo()

    # ── Taskbar ────────────────────────────────────────────────────

    def _taskbar(self):
        bar = tk.Frame(self.root, bg=OS_COR["taskbar"],
                       highlightbackground=OS_COR["borda"],
                       highlightthickness=1, height=52)
        bar.pack(fill="x"); bar.pack_propagate(False)

        # Logo
        tk.Label(bar, text="  ⬡  PythonOS",
                 font=("Helvetica", 14, "bold"),
                 bg=OS_COR["taskbar"], fg=OS_COR["azul"]
                 ).pack(side="left", padx=(12, 4), pady=10)

        # Relógio + data
        self._lbl_clock = tk.Label(bar, text="",
                 font=("Helvetica", 11, "bold"),
                 bg=OS_COR["taskbar"], fg=OS_COR["branco"])
        self._lbl_clock.pack(side="right", padx=(0, 20))
        self._lbl_date = tk.Label(bar, text="",
                 font=("Helvetica", 9),
                 bg=OS_COR["taskbar"], fg=OS_COR["muted"])
        self._lbl_date.pack(side="right", padx=(0, 8))

        # Contador de apps
        total = len(TODAS_APPS)
        tk.Label(bar, text=f"{total} apps  •  {len(CATEGORIAS_APPS)} categorias",
                 font=("Helvetica", 9),
                 bg=OS_COR["taskbar"], fg=OS_COR["muted"]
                 ).pack(side="right", padx=20)

        tk.Frame(self.root, bg=OS_COR["borda"], height=1).pack(fill="x")
        self._atualizar_relogio()

    def _atualizar_relogio(self):
        now = datetime.datetime.now()
        self._lbl_clock.config(text=now.strftime("%H:%M:%S"))
        dias = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
        meses = ["Jan","Fev","Mar","Abr","Mai","Jun",
                 "Jul","Ago","Set","Out","Nov","Dez"]
        dia_sem = dias[now.weekday()]
        self._lbl_date.config(
            text=f"{dia_sem}, {now.day} {meses[now.month-1]} {now.year}")
        self.root.after(1000, self._atualizar_relogio)

    # ── Sidebar ────────────────────────────────────────────────────

    def _sidebar(self, pai):
        sb = tk.Frame(pai, bg=OS_COR["taskbar"],
                      width=self.SIDEBAR_W)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Pesquisa
        pesq_wrap = tk.Frame(sb, bg=OS_COR["taskbar"], pady=10, padx=10)
        pesq_wrap.pack(fill="x")
        tk.Label(pesq_wrap, text="🔍",
                 font=("Helvetica", 11), bg=OS_COR["taskbar"],
                 fg=OS_COR["muted"]).pack(side="left", padx=(0, 4))
        self._pesq_var = tk.StringVar()
        self._pesq_var.trace_add("write", lambda *_: self._ao_pesquisar())
        pesq_e = tk.Entry(pesq_wrap, textvariable=self._pesq_var,
                          font=("Helvetica", 10),
                          bg=OS_COR["card"], fg=OS_COR["branco"],
                          insertbackground=OS_COR["azul"],
                          relief="flat",
                          highlightbackground=OS_COR["borda"],
                          highlightthickness=1)
        pesq_e.pack(fill="x", ipady=4)

        tk.Frame(sb, bg=OS_COR["borda"], height=1).pack(fill="x",
                                                        padx=10, pady=2)

        # Botão "Todas"
        self._btn_todas = self._sidebar_btn(
            sb, "🏠  Todas as apps", None)

        # Botões por categoria
        self._btns_cat = {}
        for cat in CATEGORIAS_APPS:
            n = len(CATEGORIAS_APPS[cat])
            btn = self._sidebar_btn(sb, f"{cat}  ({n})", cat)
            self._btns_cat[cat] = btn

        tk.Frame(sb, bg=OS_COR["borda"], height=1).pack(fill="x",
                                                        padx=10, pady=8)

        # Stats no fundo
        stats_f = tk.Frame(sb, bg=OS_COR["taskbar"])
        stats_f.pack(fill="x", side="bottom", padx=12, pady=10)
        tk.Label(stats_f, text=f"{len(TODAS_APPS)} aplicações instaladas",
                 font=("Helvetica", 8), bg=OS_COR["taskbar"],
                 fg=OS_COR["muted"], wraplength=160,
                 justify="left").pack(anchor="w")

        self._sel_cat(None)  # seleccionar "Todas" por defeito

    def _sidebar_btn(self, pai, texto, cat):
        is_todas = (cat is None)
        f = tk.Frame(pai, bg=OS_COR["taskbar"])
        f.pack(fill="x", padx=6, pady=1)

        # faixa colorida à esquerda quando seleccionado
        faixa = tk.Frame(f, bg=OS_COR["taskbar"], width=3)
        faixa.pack(side="left", fill="y")

        btn = tk.Label(f, text=texto,
                       font=("Helvetica", 9, "bold" if is_todas else "normal"),
                       bg=OS_COR["taskbar"], fg=OS_COR["branco"],
                       anchor="w", cursor="hand2",
                       padx=10, pady=7)
        btn.pack(side="left", fill="x", expand=True)

        def clique(ev=None):
            self._sel_cat(cat)

        btn.bind("<Button-1>", clique)
        f.bind("<Button-1>", clique)

        def enter(ev, w=f, b=btn):
            w.config(bg=OS_COR["card_hover"])
            b.config(bg=OS_COR["card_hover"])

        def leave(ev, w=f, b=btn, c=cat):
            sel = self._cat_atual
            bg = OS_COR["card"] if sel == c else OS_COR["taskbar"]
            w.config(bg=bg); b.config(bg=bg)

        btn.bind("<Enter>", enter); btn.bind("<Leave>", leave)
        f.bind("<Enter>", enter);   f.bind("<Leave>", leave)

        # guardar referência para mudar estilo ao seleccionar
        btn._frame_ref = f
        btn._faixa_ref = faixa
        btn._cat_ref   = cat
        return btn

    def _sel_cat(self, cat):
        self._cat_atual = cat
        self._pesq_var.set("")  # limpa pesquisa ao trocar categoria

        # Reset visual de todos os botões
        todos_btns = [self._btn_todas] + list(self._btns_cat.values())
        for b in todos_btns:
            is_sel = (b._cat_ref == cat)
            bg = OS_COR["card"] if is_sel else OS_COR["taskbar"]
            b.config(bg=bg); b._frame_ref.config(bg=bg)
            b._faixa_ref.config(bg=OS_COR["azul"] if is_sel else OS_COR["taskbar"])

        self._renderizar_conteudo()

    def _ao_pesquisar(self):
        if not hasattr(self, "_inner"):
            return
        self._pesq_term = self._pesq_var.get().strip().lower()
        # ao pesquisar, des-seleccionar categoria
        if self._pesq_term:
            self._cat_atual = None
            todos_btns = [self._btn_todas] + list(self._btns_cat.values())
            for b in todos_btns:
                b.config(bg=OS_COR["taskbar"])
                b._frame_ref.config(bg=OS_COR["taskbar"])
                b._faixa_ref.config(bg=OS_COR["taskbar"])
        self._renderizar_conteudo()

    # ── Painel de conteúdo ─────────────────────────────────────────

    def _painel_conteudo(self):
        # Header
        header = tk.Frame(self._content_frame, bg=OS_COR["fundo"])
        header.pack(fill="x", padx=20, pady=(14, 6))
        self._lbl_titulo = tk.Label(header, text="Todas as apps",
                 font=("Helvetica", 18, "bold"),
                 bg=OS_COR["fundo"], fg=OS_COR["branco"])
        self._lbl_titulo.pack(side="left")
        self._lbl_subtitulo = tk.Label(header, text="",
                 font=("Helvetica", 9),
                 bg=OS_COR["fundo"], fg=OS_COR["muted"])
        self._lbl_subtitulo.pack(side="left", padx=(10, 0), anchor="s",
                                 pady=(0, 3))

        # Canvas scrollável
        canvas_w = tk.Canvas(self._content_frame,
                             bg=OS_COR["fundo"], highlightthickness=0)
        sb_v = ttk.Scrollbar(self._content_frame, orient="vertical",
                             command=canvas_w.yview)
        canvas_w.configure(yscrollcommand=sb_v.set)
        sb_v.pack(side="right", fill="y", padx=(0, 4))
        canvas_w.pack(fill="both", expand=True, padx=(12, 0))

        self._inner = tk.Frame(canvas_w, bg=OS_COR["fundo"])
        self._win_id = canvas_w.create_window(
            (0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>",
            lambda e: canvas_w.configure(
                scrollregion=canvas_w.bbox("all")))

        def _ao_redimensionar(e):
            canvas_w.itemconfig(self._win_id, width=e.width)
            # nº de colunas que cabem (carta ~172px de largura)
            novo_cols = max(1, (e.width - 12) // 172)
            if novo_cols != getattr(self, "_cols", 0):
                self._cols = novo_cols
                self._renderizar_conteudo()
        canvas_w.bind("<Configure>", _ao_redimensionar)

        def _scroll(delta):
            canvas_w.yview_scroll(-1 * (delta // 120 if delta else 0), "units")
        canvas_w.bind("<MouseWheel>", lambda e: _scroll(e.delta))
        # roda do rato em Linux/X11
        canvas_w.bind("<Button-4>", lambda e: canvas_w.yview_scroll(-1, "units"))
        canvas_w.bind("<Button-5>", lambda e: canvas_w.yview_scroll(1, "units"))
        self._canvas_w = canvas_w
        self._cols = 4
        self._renderizar_conteudo()

    # ── Renderização ───────────────────────────────────────────────

    def _renderizar_conteudo(self):
        if not hasattr(self, "_inner"):
            return
        for w in self._inner.winfo_children():
            w.destroy()

        termo = self._pesq_term

        if termo:
            # Pesquisa global
            filtradas = [(n, e, d, f, c)
                         for n, e, d, f, c in TODAS_APPS
                         if termo in n.lower() or termo in d.lower()]
            self._lbl_titulo.config(text=f"Resultados para  \"{self._pesq_var.get()}\"")
            self._lbl_subtitulo.config(text=f"{len(filtradas)} encontrada(s)")
            if filtradas:
                self._grelha(self._inner, filtradas)
            else:
                tk.Label(self._inner, text="Nenhuma app encontrada.",
                         font=("Helvetica", 12),
                         bg=OS_COR["fundo"], fg=OS_COR["muted"]
                         ).pack(pady=40)
            return

        if self._cat_atual is None:
            # Todas — mostrar por categoria
            self._lbl_titulo.config(text="Todas as apps")
            self._lbl_subtitulo.config(
                text=f"{len(TODAS_APPS)} apps  •  "
                     f"{len(CATEGORIAS_APPS)} categorias")
            for cat, apps in CATEGORIAS_APPS.items():
                self._secao(self._inner, cat, apps)
        else:
            # Categoria específica
            apps = CATEGORIAS_APPS[self._cat_atual]
            self._lbl_titulo.config(text=self._cat_atual)
            self._lbl_subtitulo.config(text=f"{len(apps)} app(s)")
            self._grelha(self._inner, apps)

        tk.Frame(self._inner, bg=OS_COR["fundo"], height=20).pack()

    def _secao(self, pai, titulo, apps):
        # Cabeçalho da secção com linha
        hf = tk.Frame(pai, bg=OS_COR["fundo"])
        hf.pack(fill="x", padx=8, pady=(16, 6))
        tk.Label(hf, text=titulo,
                 font=("Helvetica", 12, "bold"),
                 bg=OS_COR["fundo"], fg=OS_COR["muted"]
                 ).pack(side="left")
        tk.Frame(hf, bg=OS_COR["borda"], height=1
                 ).pack(side="left", fill="x", expand=True, padx=(10, 8),
                        pady=6)
        n = len(apps)
        tk.Label(hf, text=f"{n} app{'s' if n!=1 else ''}",
                 font=("Helvetica", 8),
                 bg=OS_COR["fundo"], fg=OS_COR["muted"]
                 ).pack(side="right", padx=8)
        self._grelha(pai, apps)

    def _grelha(self, pai, apps):
        gf = tk.Frame(pai, bg=OS_COR["fundo"])
        gf.pack(fill="x", padx=6)
        cols = max(1, getattr(self, "_cols", 4))
        for c in range(cols):
            gf.columnconfigure(c, weight=1)
        for idx, (nome, emoji, desc, func, acento) in enumerate(apps):
            r, c = divmod(idx, cols)
            self._card(gf, nome, emoji, desc, func, acento, r, c)

    def _card(self, row, nome, emoji, desc, func, acento, r=0, c=0):
        card = tk.Frame(row, bg=OS_COR["card"],
                        highlightbackground=OS_COR["borda"],
                        highlightthickness=1, cursor="hand2",
                        width=162, height=182)
        card.grid(row=r, column=c, padx=5, pady=5)
        card.grid_propagate(False)

        # Faixa de cor no topo
        faixa = tk.Frame(card, bg=acento, height=3)
        faixa.pack(fill="x")

        tk.Label(card, text=emoji, font=("Helvetica", 28),
                 bg=OS_COR["card"]).pack(pady=(10, 2))

        tk.Label(card, text=nome,
                 font=("Helvetica", 9, "bold"),
                 bg=OS_COR["card"], fg=OS_COR["branco"],
                 justify="center", wraplength=148).pack()

        tk.Label(card, text=desc,
                 font=("Helvetica", 7),
                 bg=OS_COR["card"], fg=OS_COR["muted"],
                 justify="center", wraplength=146).pack(pady=(2, 6))

        btn = tk.Button(card, text="Abrir",
                        font=("Helvetica", 8, "bold"),
                        bg=acento, fg="white",
                        activebackground=acento,
                        relief="flat", cursor="hand2",
                        padx=14, pady=4, command=func)
        btn.pack(side="bottom", pady=(0, 12))

        # Widgets cujo fundo NÃO deve mudar no hover (mantêm cor de acento)
        fixos = {str(faixa), str(btn)}

        def enter(e, c=card):
            c.config(bg=OS_COR["card_hover"],
                     highlightbackground=acento)
            for w in c.winfo_children():
                if str(w) in fixos:
                    continue
                try: w.config(bg=OS_COR["card_hover"])
                except tk.TclError: pass

        def leave(e, c=card):
            c.config(bg=OS_COR["card"],
                     highlightbackground=OS_COR["borda"])
            for w in c.winfo_children():
                if str(w) in fixos:
                    continue
                try: w.config(bg=OS_COR["card"])
                except tk.TclError: pass

        card.bind("<Enter>", enter)
        card.bind("<Leave>", leave)
        card.bind("<Button-1>", lambda e: func())
        for w in card.winfo_children():
            if str(w) in fixos:
                continue
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)


if __name__ == "__main__":
    root = tk.Tk()
    PythonOS(root)
    root.mainloop()
