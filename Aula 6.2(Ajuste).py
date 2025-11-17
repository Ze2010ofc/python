ordenado= int(input("Qual o teu ordenado atual?"))
if ordenado >= 500:
    ordenado = ordenado+(ordenado*(15/100))
elif ordenado >= 1000:
    ordenado = ordenado+(ordenado*(10/100))
else:
    ordenado = ordenado+(ordenado*(5/100))
print(f'"O teu novo ordenado é de {ordenado}€."')