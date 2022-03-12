
from OGE import OGE

def connect():
    with open("/home/pi/Documents/OGE-API-ESIREM/password.txt", 'r') as fichier:
    	password = fichier.read()
    api = OGE("bm400609", password)
    api.connexion()
    api.getNombreNote()

if __name__ == '__main__':
    connect()
