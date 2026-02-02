import random

lista_numeros = []

def sorteio():
    soma = 0
    while soma < 10:
        lista_numeros.append(random.randint(1, 20))
        soma += 1
    print(f"Os 10 valores sorteados foram:", lista_numeros)

def soma_pares(lista_numeros):
    soma_numeros_pares = 0
    for n in lista_numeros:
            if n % 2 == 0:
                soma_numeros_pares += n
    print(f"A soma dos valores sorteados na lista {lista_numeros} é {soma_numeros_pares}.")

numeros = sorteio()
soma_pares(lista_numeros)





