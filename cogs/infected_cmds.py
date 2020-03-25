from discord.ext import commands
import discord, random

config_file = {}

def check_for_channel(ctx):
    return ctx.channel in config_file["bot_channels"]

class InfectedCMDS(commands.Cog):
    global config_file

    def __init__(self, bot):
        global config_file

        self.bot = bot
        config_file = bot.config_file

    def check_for_roles(self, member):
        global config_file

        if config_file["roles"]["dead"] in member.roles:
            return False
        if config_file["roles"]["cured"] in member.roles:
            return False
        if config_file["roles"]["infected"] in member.roles:
            return False
        if config_file["roles"]["immune"] in member.roles:
            return False
        return True

    @commands.command()
    @commands.has_role(config_file["roles"]["infected"])
    @commands.check(check_for_channel)
    @commands.cooldown(1, config_file["cooldowns"]["hug"], commands.BucketType.user)
    async def hug(self, ctx):
        global config_file

        list_of_possibilities = [m for m in ctx.guild.members if self.check_for_roles(m)]
        hugged_member = random.choice(list_of_possibilities)

        if not config_file["roles"]["masked"] in ctx.author.roles:
            if config_file["chances"]["hug"] <= random.random():
                hugged_member.add_roles(config_file["roles"]["infected"])

                success_embed = discord.Embed (
                    title = "Success!", 
                    colour = discord.Colour.green(),
                    description = f"{hugged_member.mention} has been infected by {ctx.author.mention}'s' hug!"
                )
                await ctx.send(embed = success_embed)
                await config_file["log_channel"].send(embed = success_embed)

                return
        else:
            if config_file["chances"]["hug"] <= (random.random() * config_file["mask_multiplier"]):
                hugged_member.add_roles(config_file["roles"]["infected"])

                success_embed = discord.Embed (
                    title = "Success!", 
                    colour = discord.Colour.green(),
                    description = f"{hugged_member.mention} has been infected by {ctx.author.mention}'s' hug!"
                )
                await ctx.send(embed = success_embed)
                await config_file["log_channel"].send(embed = success_embed)

                return
        failed_embed = discord.Embed (
            title = "Failed...", 
            colour = discord.Colour.red(),
            description = f"{ctx.author.mention}'s' hug did not infect anyone..."
        )
        await ctx.send(embed = failed_embed)
        

    @commands.command()
    @commands.has_role(config_file["roles"]["infected"])
    @commands.check(check_for_channel)
    @commands.cooldown(1, config_file["cooldowns"]["travel"], commands.BucketType.user)
    async def travel(self, ctx):
        global config_file

        list_of_possibilities = [m for m in ctx.guild.members if self.check_for_roles(m)]
        possible_infected = []
        
        if len(list_of_possibilities) > config_file["travel_count"]:
            possible_infected = random.sample(list_of_possibilities, config_file["travel_count"])
        else:
            possible_infected = list_of_possibilities

        actual_infected = [m for m in possible_infected if config_file["chances"]["travel"] <= random.random()]

        if actual_infected == []:
            failed_embed = discord.Embed (
                title = "Failed...", 
                colour = discord.Colour.red(),
                description = f"{ctx.author.mention}'s vacation did not infect anyone..."
            )
            await ctx.send(embed = failed_embed)
        else:
            list_of_infected = ", ".join(actual_infected)
            success_embed = discord.Embed (
                title = "Success!", 
                colour = discord.Colour.green(),
                description = f"{list_of_infected} has all been infected by {ctx.author.mention}'s' vacation!"
            )
            await ctx.send(embed = success_embed)
            await config_file["log_channel"].send(embed = success_embed)


def setup(bot):
    bot.add_cog(InfectedCMDS(bot))