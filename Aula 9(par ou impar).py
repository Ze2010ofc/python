x = int(input("Insere um número inicial."))
y = int(input("Insere um número final."))
for x in range (x, y+1):
   if x % 2 == 0:
       print(x, end=' ')

print()