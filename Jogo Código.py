import random

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numero1 = random.randint(1, 9)
numero2 = random.randint(1, 9)
numero3 = random.randint(1, 9)
letra1 = random.choice(letras)
letra2 = random.choice(letras)
letra3 = random.choice(letras)

r1 = random.randint(0, 3)
if r1 == 1:
    N1 = numero1
else:
    N1 = letra1

r2 = random.randint(0, 3)
if r2 == 1:
    N2 = numero2
else:
    N2 = letra2

r3 = random.randint(0, 3)
if r3 == 1:
    N3 = numero3
else:
    N3 = letra3

print("Escolhe o nível de dificuldade: 1 - Fácil, 2 - Médio, 3 - Difícil")
nivel = input("Nível (1/2/3): ")
if nivel == "1":
    base_tentativas = 7
elif nivel == "3":
    base_tentativas = 4
else:
    base_tentativas = 5

print(f"Tens de adivinhar um código de 3 dígitos. Cada dígito pode ser letra ou número. Começas com {base_tentativas} tentativas para o primeiro dígito.")

tentativas1 = base_tentativas
acertou1 = False
while tentativas1 > 0:
    print(f"Primeiro dígito - tentativas restantes: {tentativas1}")
    print("Ajudas: 1-Revelar (2 tentativas), 2-Letra ou número (1 tentativa), 3-Sem ajuda")
    escolha = input("Escolhe ajuda (1/2/3): ")
    if escolha == "1":
        if tentativas1 >= 2:
            tentativas1 = tentativas1 - 2
            print(f"A ajuda revelou: {N1}")
            acertou1 = True
            break
        else:
            print("Não tens tentativas suficientes para revelar o carácter.")
    elif escolha == "2":
        if tentativas1 >= 1:
            tentativas1 = tentativas1 - 1
            if N1 in "0123456789":
                print("A ajuda diz que é um número")
            else:
                print("A ajuda diz que é uma letra")
        else:
            print("Não tens tentativas suficientes para esta ajuda.")
    else:
        tentativa = input("Insere o primeiro caracter: ")
        if len(tentativa) != 1:
            print("Insere apenas um caracter.")
            continue
        if tentativa == N1:
            print(f"Acertaste, o primeiro dígito é {N1}.")
            acertou1 = True
            break
        else:
            tentativas1 = tentativas1 - 1
            if tentativas1 == 0:
                print("Perdeste.")
                exit()
            print("Caracter incorreto ou inválido.")

tentativas2 = 5 + tentativas1
print(f"Começas o segundo dígito com {tentativas2} tentativas (5 + {tentativas1} restantes do primeiro).")

acertou2 = False
while tentativas2 > 0:
    print(f"Segundo dígito - tentativas restantes: {tentativas2}")
    print("Ajudas: 1-Revelar (2 tentativas), 2-Letra ou número (1 tentativa), 3-Par/ímpar (1 tentativa, só se for número), 4-Sem ajuda")
    escolha = input("Escolhe ajuda (1/2/3/4): ")
    if escolha == "1":
        if tentativas2 >= 2:
            tentativas2 = tentativas2 - 2
            print(f"A ajuda revelou: {N2}")
            acertou2 = True
            break
        else:
            print("Não tens tentativas suficientes para revelar o carácter.")
    elif escolha == "2":
        if tentativas2 >= 1:
            tentativas2 = tentativas2 - 1
            if N2 in "0123456789":
                print("A ajuda diz que é um número")
            else:
                print("A ajuda diz que é uma letra")
        else:
            print("Não tens tentativas suficientes para esta ajuda.")
    elif escolha == "3":
        if N2 in "0123456789":
            if tentativas2 >= 1:
                tentativas2 = tentativas2 - 1
                if int(N2) % 2 == 0:
                    print("A ajuda diz que o número é par")
                else:
                    print("A ajuda diz que o número é ímpar")
            else:
                print("Não tens tentativas suficientes para esta ajuda.")
        else:
            print("Esta ajuda só se aplica se o carácter for um número.")
    else:
        tentativa = input("Insere o segundo caracter: ")
        if len(tentativa) != 1:
            print("Insere apenas um caracter.")
            continue
        if tentativa == N2:
            print(f"Acertaste, o segundo dígito é {N2}.")
            acertou2 = True
            break
        else:
            tentativas2 = tentativas2 - 1
            if tentativas2 == 0:
                print("Perdeste.")
                exit()
            print("Caracter incorreto ou inválido.")

tentativas3 = 5 + tentativas2
print(f"Começas o terceiro dígito com {tentativas3} tentativas (5 + {tentativas2} restantes do segundo).")

acertou3 = False
while tentativas3 > 0:
    print(f"Terceiro dígito - tentativas restantes: {tentativas3}")
    print("Ajudas: 1-Revelar (2 tentativas), 2-Letra ou número (1 tentativa), 3-Par/ímpar (1 tentativa, só se for número), 4-Sem ajuda")
    escolha = input("Escolhe ajuda (1/2/3/4): ")
    if escolha == "1":
        if tentativas3 >= 2:
            tentativas3 = tentativas3 - 2
            print(f"A ajuda revelou: {N3}")
            acertou3 = True
            break
        else:
            print("Não tens tentativas suficientes para revelar o carácter.")
    elif escolha == "2":
        if tentativas3 >= 1:
            tentativas3 = tentativas3 - 1
            if N3 in "0123456789":
                print("A ajuda diz que é um número")
            else:
                print("A ajuda diz que é uma letra")
        else:
            print("Não tens tentativas suficientes para esta ajuda.")
    elif escolha == "3":
        if N3 in "0123456789":
            if tentativas3 >= 1:
                tentativas3 = tentativas3 - 1
                if int(N3) % 2 == 0:
                    print("A ajuda diz que o número é par")
                else:
                    print("A ajuda diz que o número é ímpar")
            else:
                print("Não tens tentativas suficientes para esta ajuda.")
        else:
            print("Esta ajuda só se aplica se o carácter for um número.")
    else:
        tentativa = input("Insere o terceiro caracter: ")
        if len(tentativa) != 1:
            print("Insere apenas um caracter.")
            continue
        if tentativa == N3:
            print(f"Acertaste, o terceiro dígito é {N3}.")
            acertou3 = True
            break
        else:
            tentativas3 = tentativas3 - 1
            if tentativas3 == 0:
                print("Perdeste.")
                exit()
            print("Caracter incorreto ou inválido.")

print(f"Adivinhaste o código completo: {N1} {N2} {N3}")
pontuacao = tentativas3 * 100
print(f"Pontuação final: {pontuacao}")