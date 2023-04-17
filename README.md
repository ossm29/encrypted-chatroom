# encrypted-chatroom
![output](https://user-images.githubusercontent.com/77997318/232584858-eec7e12a-221f-419c-9ea8-6586f31a39db.gif)

## Chatroom sécurisée avec chiffrement de bout en bout

Implémentation d'une chatroom sécurisée avec chiffrement de bout en bout utilisant le protocole TCP. Les messages échangés entre les clients et le serveur sont chiffrés (AES) à l'aide de la bibliothèque python `cryptography`.
Les clients peuvent envoyer et recevoir des messages chiffrés en temps réel, assurant une communication sécurisée et privée.

## Fonctionnalités

- Chiffrement de bout en bout des messages avec la bibliothèque `cryptography`
- Utilisation du protocole TCP pour une communication fiable entre le serveur et les clients
- Gestion des multiples clients avec des threads
- Envoi de messages à tous les clients connectés, à l'exception de l'expéditeur

## Fonctionnement

### Chiffrement

Le chiffrement utilisé dans ce projet est Fernet, qui est une implémentation de chiffrement symétrique basée sur la norme AES (Advanced Encryption Standard) avec un mode d'opération CBC (Cipher Block Chaining) et une taille de clé de 128 bits. Fernet fait partie de la bibliothèque Python`cryptography` .

### Génération de la clé

Le serveur génère une clé de chiffrement lors de son démarrage s'il n'existe pas déjà de fichier `secret.key`. Cette clé est ensuite stockée dans le fichier `secret.key`. Les clients doivent utiliser cette clé pour chiffrer et déchiffrer les messages. La clé doit être partagée manuellement avec les clients avant qu'ils ne se connectent au serveur.

### Utilisation de la clé

Les clients chargent la clé de chiffrement à partir du fichier `secret.key` lorsqu'ils démarrent. La clé est utilisée pour chiffrer les messages avant de les envoyer au serveur, et pour déchiffrer les messages reçus du serveur.

### Communication

Le serveur accepte les connexions des clients et gère la communication entre eux. Lorsqu'un client envoie un message, il est d'abord chiffré avec la clé de chiffrement, puis envoyé au serveur. Le serveur reçoit le message chiffré et le retransmet à tous les autres clients connectés. Les clients déchiffrent ensuite le message avec la clé de chiffrement et l'affichent.


## Utilisation

1. Clonez le dépôt :
`git clone https://github.com/votre_nom_utilisateur/votre_chatroom.git`


2. Installez les dépendances :
`pip install cryptography`

3. Exécutez le serveur :
`python server.py <adresse_ip> <numéro_de_port>`
<adresse_ip> : ip de la machine qui éxécute le serveur
<numéro_de_port> : numéro de port non utilisé et non réservé dans la plage 1024-65535.

4. Exécutez le/les clients :
`python client.py <adresse_ip> <numéro_de_port>`
Il est possible d'éxécuter jusqu'à 100 clients simultanément.
Vous pouvez modifier la capacité d'écoute du serveur en modifiant le paramètre du fichier server.py ligne 43 : `server.listen(100)`


## Configuration

Le serveur et le client utilisent le même fichier `secret.key` pour le chiffrement et le déchiffrement des messages. Ce fichier doit être présent sur la machine qui exécute le serveur et sur chaque machine client.

Le fichier `secret.key` est généré automatiquement par le serveur s'il n'est pas déjà présent. Copiez ce fichier sur les machines clientes pour permettre le déchiffrement des messages.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.
