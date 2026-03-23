import tkinter as tk 
 
root = tk.Tk()
root.title("Janela 1")
root.geometry("1000x1000")

def change_verde():
    verde = "#00ff62"
    root.configure(bg=verde)
    label.config(text="Verde", fg="black", bg="green")

def change_vermelho():
    vermelho = "#ff0000"
    root.configure(bg=vermelho)
    label.config(text="Vermelho", fg="black", bg="red")
    
def change_azul():
    azul = "#3300ff"
    root.configure(bg=azul)
    label.config(text="Azul", fg="black", bg="blue")

def change_amarelo():
    amarelo = "#ffff00"
    root.configure(bg=amarelo)
    label.config(text="Amarelo", fg="black", bg="yellow")

branco = "#ffffff"
root.configure(bg=branco)

button1 = tk.Button(text="verde", command=change_verde)
button1.place(x=250, y=250)

button2 = tk.Button(text="vermelho", command=change_vermelho)
button2.place(x=250, y=500)

button3 = tk.Button(text="azul", command=change_azul)
button3.place(x=500, y=250)

button4 = tk.Button(text="amarelo", command=change_amarelo)
button4.place(x=750, y=500)

label = tk.Label(root, text=".", fg="white", bg="white")
label.place(x=400, y=400)

root.mainloop()