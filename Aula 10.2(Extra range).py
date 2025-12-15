i = int(input("Insere um número."))
p = 0
impar = 0
while i != 0:
    if i % 2 == 0:
     p += 1
     i = int(input("Insere um número."))
    if i % 2 != 0:
     impar += 1
     i = int(input("Insere um número."))

print(f'Insere inseriste {p} números pares e {impar} números ímpares.')


