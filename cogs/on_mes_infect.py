from discord.ext import commands
import discord, random

class OnMesInfect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_for_roles(self, member):
        if self.bot.config_file["roles"]["dead"] in member.roles:
            return False
        if self.bot.config_file["roles"]["cured"] in member.roles:
            return False
        if self.bot.config_file["roles"]["infected"] in member.roles:
            return False
        if self.bot.config_file["roles"]["immune"] in member.roles:
            return False
        return True

    @commands.Cog.listener()
    async def on_message(self, mes):
        if mes.guild == None:
            return
        if self.check_for_roles(mes.author) or self.bot.started == False:
            return
        elif mes.channel.id in self.bot.config_file["infect_channels"]:
            authors = [
                m.author
                async for m in mes.channel.history(limit=40)
                if not m.author.bot and isinstance(m.author, discord.Member)
            ]
            authors = list(set(authors[0:9]))

            infected = [member for member in authors if self.bot.config_file["roles"]["infected"] in member.roles]

            if infected != []:
                masked = [member for member in infected 
                if self.bot.config_file["roles"]["masked"] in member.roles]

                x_value = (len(infected) - len(masked)) + ((len(masked) * 0.65))

                a = (x_value ** 2) * self.bot.config_file["chances"]["on_mes"]["equation"][0]
                b = x_value * self.bot.config_file["chances"]["on_mes"]["equation"][1]
                c = self.bot.config_file["chances"]["on_mes"]["equation"][2]
                prob = a + b + c

                if prob <= random.random():
                    mes.author.add_roles(self.bot.config_file["roles"]["infected"])

                    infect_embed = discord.Embed (
                        title = "Uh oh...", 
                        colour = discord.Colour.red(),
                        description = f"{mes.author.mention} has been infected!"
                    )
                    await mes.channel.send(embed = infect_embed)
                    await self.bot.config_file["log_channel"].send(embed = infect_embed)

def setup(bot):
    bot.add_cog(OnMesInfect(bot))
