import discord, os, asyncio, math, datetime
from discord.ext import commands
from cogs.checks import check_cooldown, check_for_channel, check_for_role

bot = commands.Bot(command_prefix='v!', fetch_offline_members=True)
bot.remove_command("help")

@bot.event
async def on_ready():

    bot.config_file = None
    bot.user_cooldowns = {}
    bot.load_extension("cogs.fetch_config_file")

    while bot.config_file == None:
        await asyncio.sleep(0.1)

    cogs_list = ["cogs.infected_cmds", "cogs.etc_cmds", "cogs.tasks",
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

@bot.event
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
    elif isinstance(error, commands.CheckFailure):
        if not check_for_role(ctx):
            await ctx.send("You do not have the proper role to do that!")
        elif not check_cooldown(ctx):
            current_time = datetime.datetime.utcnow().timestamp()
            available_at = bot.user_cooldowns[ctx.author][ctx.invoked_with] + ctx.bot.config_file["cooldowns"][ctx.invoked_with]

            secs_till = math.ceil(available_at - current_time)

            if secs_till < 60:
                await ctx.send(f"You need to wait {secs_till} second(s) until you can run that command again!")
            else:
                mins_till = math.floor(secs_till / 60)
                secs_till -= mins_till * 60

                minute_plural = "minute" if mins_till == 1 else "minutes"
                second_plural = "second" if secs_till == 1 else "seconds"

                await ctx.send(f"You need to wait {mins_till} {minute_plural} and {secs_till} {second_plural} until you can run that command again!")
    else:
        print(error)
        
        application = await ctx.bot.application_info()
        owner = application.owner
        await ctx.send(f"{owner.mention}: {error}")

bot.run(os.environ.get("MAIN_TOKEN"))
