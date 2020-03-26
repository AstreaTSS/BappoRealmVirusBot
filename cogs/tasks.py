from discord.ext import commands, tasks
import discord, random

config_file = {}

class Tasks(commands.Cog):
    global config_file

    def __init__(self, bot):
        global config_file

        self.bot = bot
        config_file = bot.config_file

        self.win_condition.start()
        self.infect_death.start()

    @tasks.loop(seconds=10.0)
    async def win_condition(self):
        global config_file

        if self.bot.started:
            guild = config_file["guild"]

            pop = [
                member for member in guild.members
                if not member.bot and not config_file["roles"]["immune"] in member.roles
            ]

            infected = [member for member in pop if config_file["roles"]["infected"] in member.roles]
            dead = [member for member in pop if config_file["roles"]["dead"] in member.roles]
            cured = [member for member in pop if config_file["roles"]["cured"] in member.roles]

            if len(dead) == len(pop):
                infect_win_embed = discord.Embed (
                    title = "The infected and dead win!", 
                    colour = discord.Colour.red(),
                    description = "Everyone has been infected and has died!"
                )
                await config_file["log_channel"].send(embed = infect_win_embed)
                self.bot.started = False
            elif (len(dead) + len(cured)) == len(pop):
                cured_win_embed = discord.Embed (
                    title = "The cured and the curers win!", 
                    colour = discord.Colour.blue(),
                    description = "Everyone has been cured!"
                )
                await config_file["log_channel"].send(embed = cured_win_embed)
                self.bot.started = False
            elif (len(infected) == 0) and (len(dead) + len(cured)) != len(pop):
                no_infected_embed = discord.Embed (
                    title = "The curers and uninfected win!", 
                    colour = discord.Colour.dark_blue(),
                    description = "There are no infected people left!"
                )
                await config_file["log_channel"].send(embed = no_infected_embed)
                self.bot.started = False

    @tasks.loop(minutes=1.0)
    async def infect_death(self):
        global config_file

        if self.bot.started:
            guild = config_file["guild"]

            infected = [
                member for member in guild.members
                if not member.bot and not config_file["roles"]["infected"] in member.roles
            ]

            for member in infected:
                if not member in self.bot.infected_track.keys():
                    self.bot.infected_track[member] = 1
                else:
                    if self.bot.infected_track[member] < config_file["chances"]["death"]["limit"]:
                        self.bot.infected_track[member] += 1

                    if self.bot.infected_track[member] >= config_file["chances"]["death"]["start"]:
                        x_value = self.bot.infected_track[member]
                        a = (x_value ** 2) * config_file["chances"]["death"]["equation"][0]
                        b = x_value * config_file["chances"]["death"]["equation"][1]
                        c = self.bot.config_file["chances"]["death"]["equation"][2]
                        prob = a + b + c

                        if prob <= random.random():
                            member.add_roles(self.bot.config_file["roles"]["dead"])
                            member.remove_roles(self.bot.config_file["roles"]["infected"])
                            infect_embed = discord.Embed (
                                title = "Oh no...", 
                                colour = discord.Colour.darker_grey(),
                                description = f"{member.mention} has died!"
                            )

                            await self.bot.config_file["log_channel"].send(embed = infect_embed)

def setup(bot):
    bot.add_cog(Tasks(bot))