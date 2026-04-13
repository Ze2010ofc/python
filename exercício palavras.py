P = input("Qual a palavra que queres procurar?")  

with open('agenda.txt', 'w') as filea:
    filea.write('Sharkcoders, Faro, Portugal')

with open('agenda.txt', 'r', encoding='utf-8') as file:
    for linha in file:
        if P in linha:
            print(linha.rstrip())
            print(f'A palavra {P} está no ficheiro.')
        else:
            print(f'A palavra {P} não está no ficheiro.')
