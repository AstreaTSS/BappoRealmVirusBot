import datetime

def check_for_role(ctx):
    if ctx.invoked_with in ("hug", "travel"):
        if ctx.bot.config_file["roles"]["infected"] in ctx.author.roles:
            return True
    elif ctx.invoked_with in ("work", "cure"):
        if ctx.bot.config_file["roles"]["scientist"] in ctx.author.roles:
            return True
    return False

def check_cooldown(ctx):
    current_time = datetime.datetime.utcnow().timestamp()

    if not ctx.author in ctx.bot.user_cooldowns.keys():
        ctx.bot.user_cooldowns[ctx.author] = {}
        ctx.bot.user_cooldowns[ctx.author][ctx.invoked_with] = current_time
        return True

    elif not ctx.invoked_with in ctx.bot.user_cooldowns[ctx.author].keys():
        ctx.bot.user_cooldowns[ctx.author][ctx.invoked_with] = current_time
        return True

    available_at = ctx.bot.user_cooldowns[ctx.author][ctx.invoked_with] + ctx.bot.config_file["cooldowns"][ctx.invoked_with]

    if current_time < available_at:
        return False

    return True

def check_for_channel(ctx):
    return ctx.channel.id in ctx.bot.config_file["bot_channels"]