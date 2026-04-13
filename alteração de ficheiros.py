#abrir o arquivo em modo apepend
with open('exemplo.txt', 'a') as arquivo:
    #adicionar uma nova linha ao final do arquivo
    arquivo.write('\nlinha 4')