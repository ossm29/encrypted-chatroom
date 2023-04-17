# Importation des modules nécessaires
import socket
import select
import sys
from cryptography.fernet import Fernet

# Charger la clé de chiffrement
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# Charger la clé et créer une instance Fernet pour le chiffrement
key = load_key()
cipher_suite = Fernet(key)

# Créer un socket client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vérifier les arguments de la ligne de commande pour l'adresse IP et le port
if len(sys.argv) != 3:
    print("Utilisation correcte : script, adresse IP, numéro de port")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Se connecter au serveur avec l'adresse IP et le port passés en paramètre
server.connect((IP_address, Port))

# Boucle principale du client
while True:
    # Liste des sockets à surveiller (stdin et serveur)
    sockets_list = [sys.stdin, server]

    # Utiliser select pour vérifier les sockets prêts à être lus
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            # Si le socket du serveur est prêt à être lu, recevoir le message chiffré
            encrypted_message = socks.recv(2048)

            # Déchiffrer et afficher le message
            message = cipher_suite.decrypt(encrypted_message).decode()
            print(message)
        else:
            # Si l'entrée standard est prête à être lue, lire le message de l'utilisateur
            message = sys.stdin.readline()

            # Chiffrer le message et l'envoyer au serveur
            encrypted_message = cipher_suite.encrypt(message.encode())
            server.send(encrypted_message)

            # Afficher le message envoyé chez l'expéditeur avec le préfixe <MOI>
            sys.stdout.write("<MOI>")
            sys.stdout.write(message)
            sys.stdout.flush()

# Fermeture socket client
server.close()
