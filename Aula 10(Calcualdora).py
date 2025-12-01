x = int(input("Diz um número?"))
y = int(input("Diz um número novamente?"))
operação = input("Diz que operação desejas realizar?")

lista_operações = ['soma', 'subtração', 'multiplicação', 'divisão']

def soma(x, y):
    print(x+y)

def subtração(x, y):
    print(x-y)

def multiplicação(x, y):
    print(x*y)

def divisão(x, y):
    print(x/y)

if operação == "soma":
    soma(x, y)
elif operação == "subtração":
    subtração(x, y)
elif operação == "multiplicação":
    multiplicação(x, y)
elif operação == "divisão":
    divisão(x, y)
else:
    print("Operação inválida ou inexistente!")
