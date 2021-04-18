
import os

print(os.listdir())

file = input('enter file name:')

def xml_transfer(file:str):
    data = None

    with open(file, encoding = 'cp866') as f:
        data = f.read()

    with open(f'{file}_prsd.xml', 'wb') as f:
        f.write(data.encode('utf-8'))
    return 'Success'

xml_transfer(file)
