#abrir o arquivo em modo apepend
with open('exemplo.txt', 'a') as arquivo:
    #defenir conteudo
    conteudo = arquivo.read()
    print(conteudo)