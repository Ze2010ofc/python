euro = int(input("Diz o valor em € que desejas converter para outra moeda."))
moeda = input("Queres converter para reais(Brasil) ou bath(Tailândia)?")
reais = euro*5.32
bath = euro*31.10
if moeda == "reais":
    print(f'"{euro}€ = {reais}."')
if moeda == "bath":
    print(f'"{euro}€ = {bath}."')