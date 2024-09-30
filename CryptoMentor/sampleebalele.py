import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import re
import logging
from PIL import Image
from selenium import webdriver
from io import BytesIO
import datetime
import time
import pickle

# Initialisation du bot Discord avec les permissions nécessaires
logging.basicConfig(level=logging.DEBUG)
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='%', intents=intents)

# Sauvegarde des canaux liés aux cryptomonnaies dans un fichier pickle
def save_crypto_channels():
    serialized_channels = {}
    for user_id, channels in crypto_channels.items():
        serialized_channels[user_id] = {}
        for crypto, channel in channels.items():
            serialized_channels[user_id][crypto] = {
                'name': channel.name,
                'id': channel.id
            }
    with open('crypto_channels.pkl', 'wb') as file:
        pickle.dump(serialized_channels, file)

# Chargement des canaux liés aux cryptomonnaies depuis un fichier pickle
def load_crypto_channels():
    global crypto_channels
    try:
        with open('crypto_channels.pkl', 'rb') as file:
            serialized_channels = pickle.load(file)
            crypto_channels = {}
            for user_id, channels in serialized_channels.items():
                crypto_channels[user_id] = {}
                for crypto, channel_info in channels.items():
                    channel = discord.utils.get(bot.get_all_channels(), id=channel_info['id'])
                    if channel is not None:
                        crypto_channels[user_id][crypto] = channel
    except FileNotFoundError:
        crypto_channels = {}

# Événement déclenché quand le bot est prêt
@bot.event
async def on_ready():
    load_crypto_channels()
    print(f'{bot.user.name} est en ligne !')

# Commande de test pour vérifier le bon fonctionnement du bot
@bot.command()
async def samplee(ctx):
    await ctx.send("La commande test fonctionne correctement !")

# Commande pour afficher les rôles disponibles
@bot.command()
async def roles(ctx):
    embed = discord.Embed(title="Obtenir ta session Traderbalele", description="Appuyez pour ajouter/supprimer Traderbalele")
    await ctx.send(embed=embed, view=Roles())

# Gestion des événements lors de la mise à jour des membres
@bot.event
async def on_member_update(before, after):
    guild = after.guild
    role_id = 1112670180988956692  # ID du rôle à vérifier
    target_category_id = 1107227636742246410  # ID de la catégorie de destination

    if role_id in [role.id for role in after.roles]:
        category_name = f"{after.id}"  # Nom de la catégorie basé sur l'ID de l'utilisateur
        new_role_name = f"{after.name} ({after.id})"  # Nom du nouveau rôle

        # Création de la catégorie et des permissions
        category = discord.utils.get(guild.categories, name=category_name)
        new_role = discord.utils.get(guild.roles, name=new_role_name)

        if category is None:
            category = await guild.create_category(category_name)
            info_channel = await category.create_text_channel("info")

            embed_info_perso = discord.Embed(title=f"Bienvenue dans ta session !", 
                                             description="Envoie dans ce channel la commande `%info bitcoin` pour obtenir les informations sur la cryptomonnaie.", 
                                             color=0x00ff00)
            await info_channel.send(embed=embed_info_perso)

            await category.set_permissions(guild.default_role, read_messages=False)
            await category.set_permissions(after, read_messages=True)

            target_category = discord.utils.get(guild.categories, id=target_category_id)
            await category.edit(position=target_category.position + 1)

        if new_role is None:
            new_role = await guild.create_role(name=new_role_name)
            await after.add_roles(new_role)

# Commande pour récupérer les informations d'une cryptomonnaie
@bot.command()
async def info(ctx, crypto):
    user_id = ctx.channel.category.name.split("#")[-1]
    user = bot.get_user(int(user_id))
    
    # Création du canal de discussion pour la cryptomonnaie demandée
    if user_id in crypto_channels and crypto in crypto_channels[user_id]:
        crypto_channel = crypto_channels[user_id][crypto]
    else:
        crypto_channel_name = f"{crypto} ({user_id})"
        crypto_channel = await ctx.channel.category.create_text_channel(crypto_channel_name)
        if user_id not in crypto_channels:
            crypto_channels[user_id] = {}
        crypto_channels[user_id][crypto] = crypto_channel

    maintenant = datetime.datetime.now()
    
    # Configuration du navigateur pour capturer les informations du site web
    driver_path = "/usr/bin"
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(driver_path, options=options)
    width = 800
    height = 900
    driver.set_window_size(width, height)
    driver.get(f'https://courscryptomonnaies.com/{crypto}/')
    
    # Capture d'écran de la section souhaitée
    div_element = driver.find_element('css selector', '.jsx-23578178.simple-card')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'})", div_element)
    screenshot = div_element.screenshot_as_png
    driver.quit()

    # Requête pour récupérer des informations sur la cryptomonnaie
    url = f"https://courscryptomonnaies.com/{crypto}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        div = soup.find("div", class_="jsx-2063552482 card-text")
        if div:
            div_element = div.find("div", class_="jsx-2063552482 price-value")
            if div_element:
                span = div_element.find("span")
                if span:
                    price = span.text.strip()

                    # Affichage des informations récupérées
                    liste_info = captureinfo(crypto)
                    cap = liste_info[0]
                    vol = liste_info[1]
                    circ = liste_info[2]
                    maxx = liste_info[3]
                    var = "Variation positive : " + avatar(crypto)[0] if float(avatar(crypto)[0][:-1:]) > 0 else "Variation négative : " + avatar(crypto)[0]

                    embed = discord.Embed(title=f"Prix de la cryptomonnaie {crypto}", 
                                          description=f"Le prix actuel de {crypto} est {price}.", 
                                          color=0x00ff00)
                    author = discord.Member
                    author.name = crypto
                    author.avatar_url = avatar(crypto)[1]

                    embed.set_author(name=author.name, icon_url=author.avatar_url)
                    
                    # Création de l'image à partir de la capture d'écran
                    image_bytes = BytesIO(screenshot)
                    image = Image.open(image_bytes)
                    image_stream = BytesIO()
                    image.save(image_stream, format='PNG')
                    image_stream.seek(0)

                    file = discord.File(image_stream, filename="image.png")
                    embed.set_image(url="attachment://image.png")
                    embed.set_thumbnail(url=author.avatar_url)
                    embed.set_footer(text="Informations supplémentaires sur la cryptomonnaie")

                    embed.add_field(name="Date et heure", value=maintenant.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
                    embed.add_field(name="Variation", value=var, inline=False)
                    embed.add_field(name="Market cap", value=cap, inline=False)
                    embed.add_field(name="Volume (24h)", value=vol, inline=False)
                    embed.add_field(name="En circulation", value=circ, inline=False)
                    embed.add_field(name="Liquidité max.", value=maxx, inline=False)
                    embed.add_field(name="Source", value=url, inline=False)
                    
                    await crypto_channel.send(embed=embed, file=file)
                    save_crypto_channels()  # Sauvegarde des canaux mis à jour

        else:
            await crypto_channel.send("Impossible de trouver le prix de la cryptomonnaie !")
    else:
        await crypto_channel.send("Erreur lors de la requête à la page.")

# Lancement du bot (REMPLACER 'YOUR_TOKEN_HERE' PAR LE TOKEN DU BOT)
bot.run('YOUR_TOKEN_HERE')
