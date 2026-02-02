x = int(input("quantos segundos queres que o foguete espere até ser lançado?"))
from time import sleep

for y in range(0,x):
    print(f'{x-y}')
    sleep(1)
print(f'O teu foguete foi lançado após {x} segundos.')