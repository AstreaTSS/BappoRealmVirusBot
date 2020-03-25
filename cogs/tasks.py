from discord.ext import commands
import discord

config_file = {}

class Tasks(commands.Cog):
    global config_file

    def __init__(self, bot):
        global config_file

        self.bot = bot
        config_file = bot.config_file

def setup(bot):
    bot.add_cog(Tasks(bot))