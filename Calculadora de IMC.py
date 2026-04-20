import tkinter as tk
from tkinter import messagebox

def calcular():
    try:
        altura = float(float_Altura.get())
        peso = float(float_Peso.get())

        if altura <= 0:
            messagebox.showwarning("Erro", "Altura inválida")
            return
        
        if peso <= 0:
            messagebox.showwarning("Erro", "Peso inválido")
            return

        imc = peso / (altura ** 2)
        label_resultado.config(text=f"{imc:.2f}")

    except ValueError:
        messagebox.showwarning("Erro", "Digite valores numéricos válidos")


root = tk.Tk()
root.title("Calculadora de IMC")
root.geometry("600x600")

branco = "#ddf6f9"
root.configure(bg=branco)

tk.Label(root, text="Calculadora de IMC", bg="white").place(x=250, y=65)
float_Altura = tk.Entry(root)
float_Altura.place(width=350, x=150, y=150)

tk.Label(root, text="Altura", bg="white").place(x=50, y=150)
float_Altura = tk.Entry(root)
float_Altura.place(width=350, x=150, y=150)

tk.Label(root, text="Peso", bg="white").place(x=50, y=250)
float_Peso = tk.Entry(root)
float_Peso.place(width=350, x=150, y=250)

tk.Label(root, text="IMC", bg="white").place(x=50, y=350)

label_resultado = tk.Label(root, text="0.00", bg="white")
label_resultado.place(width=350, x=150, y=350)

tk.Button(text="Calcular", command=calcular).place(width=150, x=225, y=450)

root.mainloop()