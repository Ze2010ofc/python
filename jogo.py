import random
import sys

D1 = str(random.randint(0, 9)) 
D2 = str(random.randint(0, 9)) 
D3 = str(random.randint(0, 9))

lista_letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

DA1 = random.choice(lista_letras)
DA2 = random.choice(lista_letras)
DA3 = random.choice(lista_letras)

N1 = random.choice([D1, DA1])
N2 = random.choice([D2, DA2])
N3 = random.choice([D3, DA3])

print(f'{N1}.')
print(f'{N2}.')
print(f'{N3}.')

print(f'Bem vindo ao advinhador de palavras pass, tens de adivinhar uma palavra pass de 3 digítos para venceres o jogo, cujo cada dígito pode ser uma letra ou número(algarismo de 0 a 9), tens 5 tentativas por digito para adivinhar.')

NV1 = input("Insere o primeiro dígito.")

NT1 = 5

while NV1 != N1 and NT1 > 0:
    NT1 -= 1
    if NT1 == 0:
        print(f'Perdeste.')
        sys.exit()
    NV1 = input("Caracter incorreto ou inválido, insere o primeiro dígito.")

if NV1 == N1:
    print(f'Acertaste, o primeiro digíto é {N1}.')

NV2 = input("Insere o segundo dígito.")

NT2 = 5 + NT1

while NV2 != N2 and NT2 > 0:
    NT2 -= 1
    if NT2 == 0:
        print(f'Perdeste.')
        sys.exit()
    NV2 = input("Caracter incorreto ou inválido, insere o segundo digíto.")

if NV2 == N2:
    print(f'Acertaste, o segundo digíto é {N2}.')

NV3 = input("Insere o terceiro dígito.")

NT3 = 5 + NT2

while NV3 != N3 and NT3 > 0:
    NT3 -= 1
    if NT3 == 0:
        print(f'Perdeste.')
        sys.exit()
    NV3 = input("Caracter incorreto ou inválido, insere o terceiro caracter?")

if NV3 == N3:
    print(f'Acertaste, o terceiro digíto é {N3}.')
    print(f'Acertaste, o código completo, {N1} {N2} {N3}, em {NT3} tentativas.')
    
    
print(f'{N1}.')
print(f'{N2}.')
print(f'{N3}.')
