import random
a = random.randint(1, 6)
b = random.randint(1, 6)
if a==b:
    print(f'Tiveste sorte, o dado calhou duas vezes no número {a}.')
else:
    print(f'Tiveste azar, o dado calhou em {a} e {b}.')
