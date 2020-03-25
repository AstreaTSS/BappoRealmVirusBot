from discord.ext import commands, tasks
import discord, aiohttp

class FetchConfigFile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_document.start()

    @tasks.loop(minutes=2.0)
    async def fetch_document(self):
        document_url = "None"

        async with aiohttp.ClientSession() as session:
            async with session.get(document_url) as resp:
                self.bot.config_file = await resp.json()


def setup(bot):
    bot.add_cog(FetchConfigFile(bot))