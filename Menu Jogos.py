lista_users = ["Bernardo", "Zé", "Rodrigo", "Afonso", "Lívia"]

def Inserir_Password():
    PSS = input("Diz a tua palavra pass?")
    if PSS == "Shark":
        print(f'"Bem vindo/a,{User}."')
    while PSS != "Shark":
        PSS = input(f'Password incorreta, insere novamente.')



def Inserir_User():
    User = input("Diz o teu nome de utilizador?")
    if User in lista_users:
        Inserir_Password()
    while User not in lista_users:
        PSS = input(f'Username mal escrito ou inexistente, insere novamente.')



Inserir_User()