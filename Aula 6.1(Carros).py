marca = input("Diz uma marca de carros?")
if marca in('Ford Chevrolet Tesla Dodge Range Rover Jeep'):
    print(f'"{marca} é Americana."')
elif marca in('Toyota Honda Susuki Xiaomi'):
    print(f'"{marca} é Asiática."')
elif marca in('BMW Peugeot Mini Dacia Mercedes Audi'):
    print(f'"{marca} é Europeia."')
elif marca in('Innoson Kantanka Kiira'):
    print(f'{marca} é Africana."')
else:
    print(f'"A tua marca não está presente na nossa base de dados."')