from discord.ext import commands
import discord

config_file = {}

def check_for_channel(ctx):
    return ctx.channel in config_file["bot_channels"]

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
        self.bot.infected_track = {}
        await ctx.send("Let's go!")

    @commands.command()
    @commands.check(check_for_channel)
    async def stats(self, ctx):
        pop = [
            member
            for member in ctx.guild.members
            if not member.bot and not config_file["roles"]["immune"] in member.roles
        ]
        infected = [member for member in pop if config_file["roles"]["infected"] in member.roles]
        dead = [member for member in pop if config_file["roles"]["dead"] in member.roles]
        cured = [member for member in pop if config_file["roles"]["cured"] in member.roles]
        scientists = [member for member in pop if config_file["roles"]["scientists"] in member.roles]
        masked = [member for member in pop if config_file["roles"]["masked"] in member.roles]

        stats_embed = discord.Embed(title="Current Game Stats", colour=discord.Colour(0x9e6000))
        stats_embed.set_author(name="Bappo Realm Virus Bot", icon_url="https://cdn.discordapp.com/avatars/692079618831810720/f1732b553a09af1753586484a1f9828a.png?size=128")

        stats_embed.add_field(name="Total Population", value=f"{len(pop)}")
        stats_embed.add_field(name="Total Infected", value=f"{len(infected)}", inline=True)
        stats_embed.add_field(name="Total Dead", value=f"{len(dead)}", inline=True)
        stats_embed.add_field(name="Total Cured", value=f"{len(cured)}", inline=True)
        stats_embed.add_field(name="Total Scientist", value=f"{len(scientists)}", inline=True)
        stats_embed.add_field(name="Total Masked", value=f"{len(masked)}", inline=True)
        stats_embed.add_field(name="Cure Progress", value=f"{round(self.bot.cure_progress * 100, 2)}%", inline=True)

        await ctx.send(embed = stats_embed)

def setup(bot):
    bot.add_cog(ETCCMDS(bot))