#á parte, apenas para criar automaticamente o ficheiro
with open('agenda.txt', 'w') as fileagenda:
    fileagenda.write('Sharkcoders')

with open('agenda.txt', 'r', encoding='utf-8') as ficheiro:
    for linha in ficheiro:
        if 'Sharkcoders' in linha:
            print(linha.rstrip())