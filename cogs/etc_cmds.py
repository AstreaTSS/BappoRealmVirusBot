from discord.ext import commands
import discord

config_file = {}

class ETCCMDS(commands.Cog):
    global config_file

    def __init__(self, bot):
        global config_file
        
        self.bot = bot
        config_file = bot.config_file

    @commands.command()
    @commands.is_owner()
    async def start_game(self, ctx):
        self.bot.started = True
        await ctx.send("Let's go!")

def setup(bot):
    bot.add_cog(ETCCMDS(bot))