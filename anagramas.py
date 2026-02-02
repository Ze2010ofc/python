import random

D1 = random.randint(1, 9)
D2 = random.randint(1, 9)
D3 = random.randint(1, 9)

lista_letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]

DA1 = random.choice(lista_letras)
DA2 = random.choice(lista_letras)
DA3 = random.choice(lista_letras)

S1 = random.randint(0, 3)
if S1 == 1:
       N1 = D1
else:
    N1 = DA1

S2 = random.randint(0, 3)
if S2 == 1:
       N2 = D2
else:
    N2 = DA2

S3 = random.randint(0, 3)
if S3 == 1:
       N3 = D3
else:
    N3 = DA3

print(f'Bem vindo ao advinhador de palavras pass, tens de adivinhar uma palavra pass de 3 digítos para venceres o jogo, cujo cada dígito pode ser uma letra ou número(algarismo de 0 a 9), tens 5 tentativas por digito para adivinhar.')

NV1 = input("Insere o primeiro caracter?")

NT1 = 5

Pontos = NT1*100

print(N1, N2, N3)

while NV1 != N1 and NT1 >0:
    NT1 -= 1
    if NT1 == 0:
        print(f'Perdeste.')
        break
    NV1 = input("Caracter incorreto ou inválido, insere o primeiro caracter?")

if NV1 == N1:
    print(f'Acertaste, o primeiro digíto é {N1}.')

NV2 = input("Insere o segundo caracter?")

NT2 = 5+NT1

Pontos = NT2*100


while NV2 != N2 and NT2 >0:
    NT2 -= 1
    if NT2 == 0:
        print(f'Perdeste.')
        break
    NV2 = input("Caracter incorreto ou inválido, insere o segundo digíto?")

if NV2 == N2:
    print(f'Acertaste, o segundo digíto é {N2}.')

NV3 = input("Insere o terceiro caracter?")

NT3 = 5 + NT2

Pontos = NT3*100


while NV3 != N3 and NT3 >0:
    NT3 -= 1
    if NT3 == 0:
        print(f'Perdeste.')
        break
    NV3 = input("Caracter incorreto ou inválido, insere o terceiro caracter?")

if NV3 == N3:
    print(f'Acertaste, o terceiro digíto é {N3}.')
    print(f'Acertaste, o código completo, {N1} {N2} {N3}, em {NT3} tentativas.')






