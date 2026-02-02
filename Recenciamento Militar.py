nascimento = int(input("Qual o ano em que nasceste?"))
from datetime import date
hoje = date.today().year
idade = hoje-nascimento
if idade < 18:
    print(f'"Não tens de te apresentar ans forças armadas."')
elif idade > 21:
    print(f'"Não tens de te apresentar ans forças armadas."')
else:
    print(f'"Tens de te apresentar ans forças armadas."')