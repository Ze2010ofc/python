import random

x = ["Pedra", "Papel", "Tesoura"]

a = random.choice(x)

b = int(input("Diz o teu ataque(1=Pedra, 2=Papel, 3=Tesoura)."))
print(a)



if b==1:
    c="Pedra"
elif b==2:
    c="Papel"
elif b==3:
    c="Tesoura"


if a==c:
    print("Empate")
elif a=="Papel" and c=="Pedra":
    print("Perdeste")
elif a=="Pedra" and c=="Tesoura":
    print("Perdeste")
elif a=="Tesoura" and c=="Papel":
    print("Perdeste")
elif c=="Papel" and a=="Pedra":
    print("Ganhaste")
elif c=="Pedra" and a=="Tesoura":
    print("Ganhaste")
elif c=="Tesoura" and a=="Papel":
    print("Ganhaste")
else:
    print("Nenhuma opção")
