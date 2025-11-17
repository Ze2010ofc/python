vcasa = int(input("Qual o valor total em € da sua casa?"))
slm = int(input("Qual o seu salário mensal em €?"))
time = int(input("Em quantos anos você deseja pagar a sua casa?"))
sl30 = slm*30
prest = (vcasa/time/12)
if prest< sl30:
    print(f'"A prestação mensal de {prest}€ é superior a 30% do seu salário."')
else:
    print(f'"A prestação mensal de {prest}€ é inferior a 30% do seu salário."')