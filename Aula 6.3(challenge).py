qtdern= int(input("Quanta energia gastaste em kWh?"))
instalação=int(input("Diz o tipo de instalação que tens, R para residências, I para indústrias e C para comércios."))
if instalação is R:
    ordenado = ordenado+(ordenado*(15/100))
if instalação is I:
    ordenado = ordenado+(ordenado*(10/100))
else:
    ordenado = ordenado+(ordenado*(5/100))
print(f'"O teu novo ordenado é de {ordenado}€."')