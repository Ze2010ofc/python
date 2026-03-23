#Jogo do Galo

import tkinter as tk 

root = tk.Tk()
#root.title("Janela 1")
root.geometry("500x500")


    
def verifica_vencedor():
    combinações = {[0, 1, 2], [2, 5, 8], [3, 4, 5], [6, 7, 8], [0, 3, 6], [0, 4, 8], [2, 4, 6], [1, 4, 7]}
    for comb in combinações:
        if board
    

branco = "#ffffff"
root.configure(bg=branco)

button1 = tk.Button(root)
button1.place(x=50, y=50)

button2 = tk.Button(root)
button2.place(x=150, y=50)

button3 = tk.Button(root)
button3.place(x=250, y=50)

button4 = tk.Button(root)
button4.place(x=50, y=150)

button5 = tk.Button(root)
button5.place(x=150, y=150)

button6 = tk.Button(root)
button6.place(x=250, y=150)

button7 = tk.Button(root)
button7.place(x=50, y=250)

button8 = tk.Button(root)
button8.place(x=150, y=250)

button9 = tk.Button(root)
button9.place(x=250, y=250)

root.mainloop()