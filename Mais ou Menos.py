import random
a = random.randint(1, 100)
b = int(input("Diz um número?"))
c = 0
while b != a:
    if a < b:
        print(f'"Esse número é maior que o meu número."')
    elif a > b:
        print(f'"Esse número é menor que o meu número."')
    b = int(input("Diz um número?"))
    c +=1
if a == b:
    c += 1
    print(f'"Acertaste o número."')
    print(f'"Acertaste ao fim de {c} tentativas."')

