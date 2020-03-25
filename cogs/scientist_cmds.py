from discord.ext import commands
import discord, random

config_file = {}

def check_for_channel(ctx):
    return ctx.channel.id in config_file["bot_channels"]

class ScientistCMDS(commands.Cog):
    global config_file

    def __init__(self, bot):
        global config_file

        self.bot = bot
        config_file = bot.config_file

    def check_for_roles(self, member):
        global config_file

        if config_file["roles"]["infected"] in member.roles:
            if not config_file["roles"]["dead"] in member.roles:
                return True

        return False

    @commands.command()
    @commands.has_role(config_file["roles"]["scientist"])
    @commands.check(check_for_channel)
    @commands.cooldown(1, config_file["cooldowns"]["work"], commands.BucketType.user)
    async def work(self, ctx):
        global config_file

        if self.bot.cure_progress != 1:
            cure_add = random.uniform(config_file["chances"]["work"]["min"], config_file["chances"]["work"]["max"])

            if config_file["roles"]["infected"] in ctx.author.roles:
                cure_add = round(cure_add / config_file["chances"]["work"]["infect_divide"], 2)

            self.bot.cure_progress = 1 if self.bot.cure_progress + cure_add >= 1 else self.bot.cure_progress + cure_add

            if self.bot.cure_progress < 1:
                cure_embed = discord.Embed (
                    title = "Cure Progress", 
                    colour = discord.Colour.blue(),
                    description = f"The cure is at {self.bot.cure_progress * 100}%"
                )
                await ctx.send(embed = cure_embed)
                await config_file["log_channel"].send(embed = cure_embed)
            else:
                final_cure_embed = discord.Embed (
                    title = "Cure Progress", 
                    colour = discord.Colour.green(),
                    description = f"The cure is at {self.bot.cure_progress * 100}%! Scientists can now use the `v!cure` command!"
                )
                await ctx.send(embed = final_cure_embed)
                await config_file["log_channel"].send(embed = final_cure_embed)
        else:
            await ctx.send("You already have completed the cure! Use `v!cure` to cure people!")

    @commands.command()
    @commands.has_role(config_file["roles"]["scientist"])
    @commands.check(check_for_channel)
    @commands.cooldown(1, config_file["cooldowns"]["cure"], commands.BucketType.user)
    async def cure(self, ctx):
        global config_file

        if self.bot.cure_progress == 1:
            list_of_possibilities = [m for m in ctx.guild.members if self.check_for_roles(m)]

            if list_of_possibilities != []:
                possible_cured = random.choice(list_of_possibilities)

                if config_file["chances"]["cure"] <= random.random():
                    possible_cured.add_roles(config_file["roles"]["cured"])
                    possible_cured.remove_roles(config_file["roles"]["infected"])

                    cured_embed = discord.Embed (
                        title = "Cured!", 
                        colour = discord.Colour.green(),
                        description = f"{ctx.author.mention} has healed {ctx.possible_cured.mention}! They no long can be infected."
                    )
                    await ctx.send(embed = cured_embed)
                    await config_file["log_channel"].send(embed = cured_embed)
                else:
                    failed_cure_embed = discord.Embed (
                        title = "Failed...", 
                        colour = discord.Colour.red(),
                        description = f"{ctx.author.mention} has failed to heal {ctx.possible_cured.mention}."
                    )
                    await ctx.send(embed = failed_cure_embed)
                    await config_file["log_channel"].send(embed = failed_cure_embed)
            else:
                await ctx.send("Everyone has been cured or has died!")
        else:
            await ctx.send("You haven't fully developed the cure yet!")


def setup(bot):
    bot.add_cog(ScientistCMDS(bot))