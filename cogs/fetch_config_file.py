from discord.ext import commands, tasks
import discord, aiohttp, numpy, os

class FetchConfigFile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_document.start()

    @tasks.loop(minutes=2.5)
    async def fetch_document(self):
        document_url = os.environ.get("CONFIG_URL")
        document = {}
        config_file = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(document_url) as resp:
                document = await resp.json()

        config_file["cooldowns"] = document["cooldowns"]
        config_file["chances"] = document["chances"]

        config_file["chances"]["on_mes"]["equation"] = numpy.polyfit(
            document["chances"]["on_mes"]["x"],
            document["chances"]["on_mes"]["y"],
            2
        )
        config_file["chances"]["death"]["equation"] = numpy.polyfit(
            document["chances"]["death"]["x"],
            document["chances"]["death"]["y"],
            2
        )

        config_file["travel_count"] = document["travel_count"]
        config_file["mask_multiplier"] = document["mask_multiplier"]
        config_file["infect_channels"] = document["infect_channels"]
        config_file["bot_channels"] = document["bot_channels"]

        config_file["guild"] = self.bot.get_guild(document["guild"])
        guild = config_file["guild"]

        config_file["log_channel"] = guild.get_channel(document["log_channel"])

        config_file["roles"] = {}
        config_file["roles"]["dead"] = guild.get_role(document["roles"]["dead"])
        config_file["roles"]["scientist"] = guild.get_role(document["roles"]["scientist"])
        config_file["roles"]["cured"] = guild.get_role(document["roles"]["cured"])
        config_file["roles"]["infected"] = guild.get_role(document["roles"]["infected"])
        config_file["roles"]["masked"] = guild.get_role(document["roles"]["masked"])
        config_file["roles"]["immune"] = guild.get_role(document["roles"]["immune"])
        
        self.bot.config_file = config_file

def setup(bot):
    bot.add_cog(FetchConfigFile(bot))