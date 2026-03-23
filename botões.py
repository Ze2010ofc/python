import tkinter as tk  
 
 

    root2 = tk.Toplevel(root)  
    root2.title("Janela 2")
   
    root.configure(bg=roxo)
    lb2 = tk.Label(root2, text="Escreve algo:")
    lb2.place(x=50, y=20)
 
    entry2 = tk.Entry(root2)
    entry2.place(x=50, y=50, width=200)
 
    button2 = tk.Button(root2, text="Clica denovo!", command=abrir_root3)
    button2.place(x=100, y=100)
 
 
def abrir_root3():
    root3 = tk.Toplevel(root)
    root3.title("Janela 3")
    root3.geometry("300x200")
   
    lb3 = tk.Label(root3, text="Escreve outra coisa:")
    lb3.place(x=50, y=20)
 
    entry3 = tk.Entry(root3)
    entry3.place(x=50, y=50, width=200)
 
    button3 = tk.Button(root3, text="Não cliques!")
    button3.place(x=100, y=100)
 
root = tk.Tk()
root.title("Janela 1")
root.geometry("300x200")
 
roxo = '#dd00ff'
root.configure(bg=roxo)
 
lb1 = tk.Label(root, text="Escreve algo:")
lb1.place(x=50, y=20)
 
entry1 = tk.Entry(root)
entry1.place(x=50, y=50, width=200)
 
button1 = tk.Button(root, text="Clica!", command=abrir_root2)
button1.place(x=100, y=100)
 
root.mainloop()