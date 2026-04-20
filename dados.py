R = int(input("Queres introduzir os teus dados (insere qualquer número) ou sair (0)? "))
if R == 0:
   print('Ok, tchau')
else:
   print('Bem vindo')
   a = input("Qual o teu nome? ")
   b = int(input("Qual a tua idade? "))
   with open('dados.txt', 'w') as file:
       file.write(f'Chamo-me {a}.')
       file.write(f'Tenho {b} anos.')
   with open('dados.txt', 'r') as file:
       conteudo = file.read()
       print(conteudo)

