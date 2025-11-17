nascimento = int(input("Qual o ano em que nasceste?"))
from datetime import date
hoje = date.today().year
idade = hoje-nascimento
if idade <= 9:
    print(f'"A tua categoria é mirim."')
elif idade <= 14:
    print(f'"A tua categoria é infantil."')
elif idade <= 19:
    print(f'"A tua categoria é junior."')
elif idade <= 25:
    print(f'"A tua categoria é sénior."')
else:
    print(f'"A tua categoria é master."')