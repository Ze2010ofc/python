import tkinter as tk 
from tkinter import*
from tkinter import messagebox

def adicionar():
 
    nome = input_Nome.get()
    tel = input_Telefone.get()
    end = input_Endereço.get()
    dist = input_Distrito.get()
    pais = input_País.get()
    email = input_Email.get()
 
    with open('agenda.txt', 'a') as arquivo:
        arquivo.write(nome + '\n' + tel + '\n' + end + '\n' + dist + '\n' + pais + '\n' + email + '\n')
 
    messagebox.showinfo('Agenda','Cadstro Efetuado com Sucesso!')
 
    input_Nome.delete('0', 'end')
    input_Telefone.delete('0', 'end')
    input_Endereço.delete('0', 'end')
    input_Distrito.delete('0', 'end')
    input_País.delete('0', 'end')
    input_Email.delete('0', 'end')

root = tk.Tk()

root.title("Janela 1")
root.geometry("600x600")

branco = "#ddf6f9"
root.configure(bg=branco)

label = tk.Label(root, text="Nome", fg="black", bg="white")
label.place(x=50, y=50)

label2 = tk.Label(root, text="Telefone", fg="black", bg="white")
label2.place(x=50, y=100)

label3 = tk.Label(root, text="Endereço", fg="black", bg="white")
label3.place(x=50, y=150)

label4 = tk.Label(root, text="Distrito", fg="black", bg="white")
label4.place(x=50, y=200)

label5 = tk.Label(root, text="País", fg="black", bg="white")
label5.place(x=350, y=200)

label6 = tk.Label(root, text="Email", fg="black", bg="white")
label6.place(x=50, y=250)

input_Nome = Entry(root, font='Time 10',show='*')
input_Nome.place(width=350, height=20,x=150 ,y=50)

input_Telefone = Entry(root, font='Time 10',show='*')
input_Telefone.place(width=350, height=20,x=150 ,y=100)

input_Endereço = Entry(root, font='Time 10',show='*')
input_Endereço.place(width=350, height=20,x=150 ,y=150)

input_Distrito = Entry(root, font='Time 10',show='*')
input_Distrito.place(width=100, height=20,x=150 ,y=200)

input_País = Entry(root, font='Time 10',show='*')
input_País.place(width=100, height=20,x=400 ,y=200)

input_Email = Entry(root, font='Time 10',show='*')
input_Email.place(width=350, height=20,x=150 ,y=250)

button1 = tk.Button(text="Adicionar", command=adicionar)
button1.place(width=150, height=20, x=100, y=300)

button2 = tk.Button(text="Pesquisar")
button2.place(width=150, height=20, x=300, y=300)

root.mainloop()