# Importation des modules nécessaires
import socket
import select
import sys
import os
from _thread import *
from cryptography.fernet import Fernet

# Charger la clé de chiffrement
def load_key():
    key_file_path = "secret.key"
    # Si le fichier secrets.key n'existe pas
    if not os.path.exists(key_file_path):
        # Générer une nouvelle clé et la sauvegarder dans le fichier
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
    # Sinon
    else:
        # Charger la clé existante à partir du fichier existant
        with open(key_file_path, "rb") as key_file:
            key = key_file.read()

    return key

# Charger la clé et créer une instance Fernet pour le chiffrement
key = load_key()
cipher_suite = Fernet(key)

# Créer un socket serveur (socket.SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vérification des arguments de la ligne de commande (l'adresse IP et port)
if len(sys.argv) != 3:
    print("Utilisation correcte : script, adresse IP, numéro de port")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Liasion du socket serveur à l'adresse IP et au port
server.bind((IP_address, Port))
server.listen(100)

# Liste des clients connectés
list_of_clients = []

# Fonction qui gère les communications avec un client spécifique
def clientthread(conn, addr):
    # Envoyer un message de bienvenue au client
    welcome_message = "Bienvenue dans ce salon de discussion !"
    encrypted_welcome_message = cipher_suite.encrypt(welcome_message.encode())
    conn.send(encrypted_welcome_message)

    while True:
        try:
            # Recevoir et déchiffrer le message du client
            encrypted_message = conn.recv(2048)
            message = cipher_suite.decrypt(encrypted_message).decode()
            if message:
                # Afficher le message et l'adresse du client
                print("<" + addr[0] + "> " + message)

                # Chiffrer et diffuser le message aux autres clients
                message_to_send = "<" + addr[0] + "> " + message
                encrypted_message_to_send = cipher_suite.encrypt(message_to_send.encode())
                broadcast(encrypted_message_to_send, conn)
            else:
                # Supprimer le client de la liste s'il n'envoie pas de message
                remove(conn)

        except:
            continue

# Fonction pour diffuser un message à tous les clients sauf l'expéditeur
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

# Fonction pour supprimer un client de la liste des clients
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

# Boucle principale du serveur pour accepter les connexions entrantes
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connecté")
    start_new_thread(clientthread, (conn, addr))

# Fermeture des connexions
conn.close()
server.close()