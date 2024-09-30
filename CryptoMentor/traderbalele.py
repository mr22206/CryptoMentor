from discord.ext import commands
import discord.ui
import os

# Classe pour gérer l'ajout ou la suppression du rôle Traderbalele
class Roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Bouton pour le rôle Traderbalele
    @discord.ui.button(label="Traderbalele", custom_id="Traderbalele", style=discord.ButtonStyle.secondary)
    async def button1(self, interaction, button):
        role = 1112670180988956692  # ID du rôle Traderbalele
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message("A plus Traderbalele ", ephemeral=True)
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message("Bienvenu Traderbalele !", ephemeral=True)
