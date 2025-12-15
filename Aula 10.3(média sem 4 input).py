n = int(input("Insere uma nota."))

soma = 0

for x in range(1,5):
    soma += n

m = soma % 4

print(f'A média é {m}.')