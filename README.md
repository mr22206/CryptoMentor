# CryptoMentor - Informations sur les Cryptomonnaies

Bienvenue sur le dépôt GitHub de **Bot Cryptomonnaies**. Ce projet est un bot Discord permettant de récupérer et afficher des informations détaillées sur les cryptomonnaies, y compris leur avatar (image) et la variation de prix, tout en facilitant l'organisation des utilisateurs dans des canaux spécifiques pour chaque cryptomonnaie.

## Table des matières
- [À propos](#à-propos)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Structure du projet](#structure-du-projet)
- [Comment installer et utiliser le projet](#comment-installer-et-utiliser-le-projet)
- [Contact](#contact)
- [Licence](#licence)

---

## À propos
Le **Bot Cryptomonnaies** est un outil pratique pour les serveurs Discord permettant de suivre les informations en temps réel sur les cryptomonnaies. Il récupère les données à partir du site *courscryptomonnaies.com* et crée des canaux personnalisés pour chaque utilisateur en fonction des rôles associés. Il permet aux utilisateurs de :
- Obtenir des informations à jour sur une cryptomonnaie spécifique.
- Consulter les variations de prix et l'avatar des cryptomonnaies.
- Organiser leur session crypto grâce à des canaux spécifiques pour chaque utilisateur et chaque cryptomonnaie.

---

## Fonctionnalités principales

### 1. **Récupération d'informations sur les cryptomonnaies**
Le bot permet de récupérer et d'afficher des informations en temps réel sur n'importe quelle cryptomonnaie supportée par le site *courscryptomonnaies.com*.
- 💡 **Illustration suggérée** : Capture d'écran de l'intégration Discord avec les informations affichées sur une cryptomonnaie (prix, variation, market cap, etc.).

### 2. **Système d'avatars et de variations de prix**
Le bot affiche l'image (avatar) de la cryptomonnaie ainsi que la variation de son prix (positive ou négative).
- 💡 **Illustration suggérée** : Capture d'écran d'une cryptomonnaie avec son avatar et sa variation de prix.

### 3. **Canaux personnalisés pour chaque utilisateur**
Lorsqu'un utilisateur obtient le rôle **Traderbalele**, le bot crée automatiquement une catégorie dédiée avec des canaux spécifiques pour chaque cryptomonnaie demandée par cet utilisateur.
- 💡 **Illustration suggérée** : Une capture d'écran de la section des canaux personnalisés pour un utilisateur avec différents canaux de cryptomonnaies.

### 4. **Commande pour obtenir des informations sur les cryptomonnaies**
Les utilisateurs peuvent taper une commande pour obtenir des informations détaillées sur la cryptomonnaie de leur choix directement dans leur canal dédié.
- 💡 **Illustration suggérée** : Exemple de l'utilisation de la commande `%info bitcoin` sur Discord.

---

## Structure du projet

### Fichier `cryptobalele.py`
- **Fonctions principales** :
  - `captureinfo()` : Récupère les informations principales d'une cryptomonnaie (market cap, volume, etc.).
  - `avatar()` : Récupère l'image et la variation de prix de la cryptomonnaie.
  
Ce fichier se charge des requêtes et du traitement des données en provenance de *courscryptomonnaies.com*.

### Fichier `sampleebalele.py`
- **Fonctions** :
  - Gestion des commandes et des événements liés aux utilisateurs (ex : ajout de rôles, création de canaux personnalisés, récupération des données des cryptomonnaies).
  - Commande `%info <crypto>` qui permet de récupérer et afficher des informations sur une cryptomonnaie.
  - Création automatique des canaux spécifiques pour chaque utilisateur et cryptomonnaie.

Ce fichier gère la majorité des interactions entre le bot et les utilisateurs de Discord, en se connectant à l'API de Discord et en utilisant Selenium pour capturer des sections du site web.

### Fichier `traderbalele.py`
- **Classe Roles** : Gère l'ajout et la suppression du rôle **Traderbalele** avec un bouton interactif sur Discord.
  
Ce fichier contient la gestion des rôles interactifs avec Discord UI.

---

## Comment installer et utiliser le projet

### Prérequis
- Python 3.x
- Librairies : `requests`, `beautifulsoup4`, `discord.py`, `selenium`, `PIL` (Pillow), `pickle`
- Navigateur Chrome (ou tout autre navigateur compatible avec Selenium)
- Un serveur Discord avec les permissions nécessaires pour le bot

### Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/crypto-bot-discord.git
   ```
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurer le bot** :
   - Remplacez `'YOUR_TOKEN_HERE'` dans `sampleebalele.py` par votre token Discord.

4. **Lancer le bot** :
   ```bash
   python sampleebalele.py
   ```

### Utilisation
- **Commandes** :
  - `%info <nom de la cryptomonnaie>` : Récupère et affiche les informations sur une cryptomonnaie.
  - `%roles` : Affiche un bouton pour obtenir ou retirer le rôle **Traderbalele**.

---

## Contact
Si vous avez des questions ou souhaitez contribuer au projet, n'hésitez pas à me contacter :
- **E-mail** : votre.email@example.com

---

## Licence
Ce projet est sous licence [MIT](LICENSE). Veuillez consulter le fichier de licence pour plus de détails.

---
