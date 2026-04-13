R = int(input("Queres introdzir os teus dados(insere qualquer número) no programa ou sair(0)?"))
if R == 0:
        print(f'Ok, tchau')
else:
    print(f'Bem vindo')
    a = input("Qual o teu nome?")
    b = int(input("Qual a tua idade?"))
    with open('dados.txt', 'w') as file:
        file.write('Chamo-me {a}.')
        file.write('Tenho {b} anos.')
    with open('dados.txt', 'r') as file:
        conteudo = arquivo.read()
        print(conteudo)

