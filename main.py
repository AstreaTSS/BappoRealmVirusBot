import discord, os, asyncio, math
from discord.ext import commands

bot = commands.Bot(command_prefix='v!', fetch_offline_members=True)

bot.remove_command("help")

@bot.event
async def on_ready():

    bot.config_file = None
    bot.load_extension("cogs.fetch_config_file")

    while bot.config_file == None:
        do_nothing = True

    cogs_list = ["cogs.infected_cmds", "cogs.etc_cmds", "cogs.tasks"
    "cogs.on_mes_infect", "cogs.scientist_cmds"]

    for cog in cogs_list:
        bot.load_extension(cog)

    bot.cure_progress = 0
    bot.started = False

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------\n')

    activity = discord.Activity(name = 'over infected people', type = discord.ActivityType.watching)
    await bot.change_presence(activity = activity)
    
@bot.check
async def global_block(ctx):
    if ctx.guild is None:
        return False
    elif bot.started == False:
        if ctx.invoked_with == "start_game":
            return True
        return False
        
    return True

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        original = error.original
        if not isinstance(original, discord.HTTPException):
            print(original)

            application = await ctx.bot.application_info()
            owner = application.owner
            await ctx.send(f"{owner.mention}: {original}")
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send(error)
    elif isinstance(error, commands.CommandOnCooldown):
        time_to_wait = math.ceil(error.retry_after)
        await ctx.send(f"You're doing that command too fast! Try again after {time_to_wait} seconds.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(
            "This command has failed! Most likely, it's because you're not in the bot arcades, this is a DM, or " +
            "the game has not started yet."
        )
    elif isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the correct role to do that!")
    else:
        print(error)
        
        application = await ctx.bot.application_info()
        owner = application.owner
        await ctx.send(f"{owner.mention}: {error}")

bot.run(os.environ.get("MAIN_TOKEN"))
