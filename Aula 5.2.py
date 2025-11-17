a = int(input("Qual a tua primeira nota?"))
b = int(input("Qual a tua segunda nota?"))
media =((a+b)/2)
if media>= 60:
    print(f'"Passaste de ano com média de {media}."')
else :
    print(f'"Reprovaste com média de {media}."')
