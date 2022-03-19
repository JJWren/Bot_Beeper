# region [Imports]
import os
import hikari
import lightbulb
import random
from unicodedata import decimal
from keep_alive import keep_alive
# endregion

# region [Gather env secrets]
ID_CHANNEL_STDOUT_FAMILY = os.getenv('ID_CHANNEL_STDOUT_FAMILY')
ID_ME = os.getenv('ID_ME')
ID_SIS = os.getenv('ID_SIS')
ID_BRO = os.getenv('ID_BRO')
ID_MA = os.getenv('ID_MA')
ID_PA = os.getenv('ID_PA')
# endregion

# region [Bot initialization and error event]
bot = lightbulb.BotApp(
    token=os.getenv('BOT_TOKEN'),
    default_enabled_guilds=[
        os.getenv('ID_GUILD_FAMILY'), os.getenv('ID_GUILD_RITHOY')]
)

bot.load_extensions_from("./Beeper/extensions")


@bot.listen(hikari.StartedEvent)
async def bot_started(event: hikari.StartedEvent) -> None:
    beepers_door = await bot.rest.fetch_channel(ID_CHANNEL_STDOUT_FAMILY)
    await beepers_door.send(f'Hello! I am alive and running now!')


@bot.listen(hikari.StoppedEvent)
async def bot_stopped(event: hikari.StoppedEvent) -> None:
    beepers_door = await bot.rest.fetch_channel(ID_CHANNEL_STDOUT_FAMILY)
    await beepers_door.send(f'Goodbye! I am going to rest for a bit.')


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    else:
        raise exception
# endregion


# region [GROUP /wave]
@bot.command
@lightbulb.command('wave', '"Hello" and "bye" commands.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def wave_group(ctx: lightbulb.Context) -> None:
    pass


@wave_group.child
@lightbulb.command('h', 'Hello command.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hello(ctx: lightbulb.Context) -> None:
    # Me
    if str(ctx.user.id) == str(ID_ME):
        await ctx.respond('https://tenor.com/view/star-wars-hello-there-hello-obi-wan-kenobi-gif-13903117')
    # Evie
    elif str(ctx.user.id) == str(ID_SIS):
        await ctx.respond('WHAT IS UP MY BIZNITCHES?!\nhttps://tenor.com/view/whats-up-wazzup-scary-movie-scream-gif-16474707')
    # Chris
    elif str(ctx.user.id) == str(ID_BRO):
        await ctx.respond('https://tenor.com/view/forrest-gump-hello-wave-hi-waving-gif-22571528')
    # Mom
    elif str(ctx.user.id) == str(ID_MA):
        await ctx.respond('*Puppy Wave*...\nhttps://tenor.com/view/hi-gingin-hi-in-french-dog-pet-lick-gif-17055714')
    # Dad
    elif str(ctx.user.id) == str(ID_PA):
        await ctx.respond('https://tenor.com/view/bugs-bunny-carrot-super-man-cape-gif-5666757')
    else:
        await ctx.respond(f'{random.choice(["https://tenor.com/view/forrest-gump-hello-wave-hi-waving-gif-22571528", "https://tenor.com/view/napoleon-dynamite-wave-bye-gif-15387504", "https://tenor.com/view/hey-there-turn-around-sassy-fabulous-hair-flip-gif-16899626"])}')


@wave_group.child
@lightbulb.command('b', 'Bye command.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bye(ctx: lightbulb.Context) -> None:
    # Me
    if str(ctx.user.id) == str(ID_ME):
        await ctx.respond('https://tenor.com/view/obi-wan-obi-wan-kenobi-hello-there-goodbye-there-hello-gif-24946322')
    # Evie
    elif str(ctx.user.id) == str(ID_SIS):
        await ctx.respond(f'{random.choice(["https://tenor.com/view/suck-yousuck-sucka-sucker-simpsons-gif-4700420", "https://tenor.com/view/spongebob-plankton-goodbye-everyone-ill-remember-you-all-in-therapy-therapy-gif-21654437"])}')
    # Chris
    elif str(ctx.user.id) == str(ID_BRO):
        await ctx.respond('https://tenor.com/view/awkward-the-simpsons-weirdo-roll-goodbye-gif-16982419')
    # Mom
    elif str(ctx.user.id) == str(ID_MA):
        await ctx.respond('https://tenor.com/view/im-done-goodbye-the-office-ciao-gif-10583001')
    # Dad
    elif str(ctx.user.id) == str(ID_PA):
        await ctx.respond('https://tenor.com/view/are-you-stupid-head-shake-farted-fart-gif-12278020')
    else:
        await ctx.respond(f'{random.choice(["https://tenor.com/view/awkward-the-simpsons-weirdo-roll-goodbye-gif-16982419", "https://tenor.com/view/ahaha-wave-bye-fearless-im-out-gif-14503554", "https://tenor.com/view/spongebob-plankton-goodbye-everyone-ill-remember-you-all-in-therapy-therapy-gif-21654437"])}')
# endregion


# region [GROUP /roll]
@bot.command
@lightbulb.command('roll', 'Roll some dice.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def roll_group(ctx: lightbulb.Context) -> None:
    pass


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d4', 'A four-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d4(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 4
    compl_roll = die_roll(die_type, num_of_die_rolled)

    await ctx.respond(f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}')


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d6', 'A six-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d6(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 6
    compl_roll = die_roll(die_type, num_of_die_rolled)

    await ctx.respond(f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}')


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d8', 'An eight-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d8(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 8
    compl_roll = die_roll(die_type, num_of_die_rolled)

    await ctx.respond(f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}')


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d10', 'A ten-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d10(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 10
    compl_roll = die_roll(die_type, num_of_die_rolled)

    await ctx.respond(f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}')


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d12', 'A twelve-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d12(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 12
    compl_roll = die_roll(die_type, num_of_die_rolled)

    await ctx.respond(f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}')


@roll_group.child
@lightbulb.option('num', 'Number of this die to roll.', type=int)
@lightbulb.command('d20', 'A twenty-sided die.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def d20(ctx: lightbulb.Context) -> None:
    if ctx.options.num < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.num == 0:
        await ctx.respond(f"You didn't roll anything...")
        return
    num_of_die_rolled = int(ctx.options.num)
    if num_of_die_rolled > 500:
        await ctx.respond(f"Use 500 or less dice. Max 2000 character limits in the text field.")
        return
    die_type = 20
    compl_roll = die_roll(die_type, num_of_die_rolled)

    message_response = f'{ctx.author.username} -> {ctx.invoked.qualname} x {num_of_die_rolled}:\r\tRolls: {compl_roll.rolls}\r\tTotal: {compl_roll.total}\r\tAverage: {compl_roll.average}\r'
    if compl_roll.had_critfail and compl_roll.had_nat20:
        message_response += 'A critical fail and natural 20 occurred...\r'
        message_response += 'https://tenor.com/view/happy-sad-despair-snusnu-prisoners-gif-8671067'
    elif compl_roll.had_critfail:
        message_response += 'A critical fail occurred...\r'
        message_response += 'https://tenor.com/view/crit-fail-youre-fucked-gg-gif-13084139'
    elif compl_roll.had_nat20:
        message_response += 'A natural 20 occurred...\r'
        message_response += 'https://tenor.com/view/amazing-work-of-gumble-dnd-d20-natural-20-gif-14065301'

    await ctx.respond(message_response)


@bot.command
@lightbulb.option('bonus', 'Cumulative modifiers and/or proficiency bonuses to add to the roll(s).', type=int)
@lightbulb.option('d4', 'Number of d4 to roll.', type=int)
@lightbulb.option('d6', 'Number of d6 to roll.', type=int)
@lightbulb.option('d8', 'Number of d8 to roll.', type=int)
@lightbulb.option('d10', 'Number of d10 to roll.', type=int)
@lightbulb.option('d12', 'Number of d12 to roll.', type=int)
@lightbulb.option('d20', 'Number of d20 to roll.', type=int)
@lightbulb.command('big_roll', 'Roll a set of varying types of dice.')
@lightbulb.implements(lightbulb.SlashCommand)
async def big_roll(ctx: lightbulb.Context) -> None:
    if ctx.options.d20 > 50 or ctx.options.d12 > 50 or ctx.options.d10 > 50 or ctx.options.d8 > 50 or ctx.options.d6 > 50 or ctx.options.d4 > 50:
        await ctx.respond(f"Use 50 or less of each dice type. Max 2000 character limits in the text field.")
        return
    elif ctx.options.d20 < 0 or ctx.options.d12 < 0 or ctx.options.d10 < 0 or ctx.options.d8 < 0 or ctx.options.d6 < 0 or ctx.options.d4 < 0:
        await ctx.respond(f"You cannot roll a negative amount of dice.")
        return
    elif ctx.options.d20 == 0 and ctx.options.d12 == 0 and ctx.options.d10 == 0 and ctx.options.d8 == 0 and ctx.options.d6 == 0 and ctx.options.d4 == 0:
        await ctx.respond(f"You didn't roll anything...")
        return

    total = 0
    crit_s = 0
    crit_f = 0
    all_rolls = {
        'd20': [],
        'd12': [],
        'd10': [],
        'd8': [],
        'd6': [],
        'd4': [],
    }
    message_response = f'{ctx.author.username}:\r'

    if ctx.options.d20 > 0:
        for idx in range(1, ctx.options.d20 + 1):
            rand_num = random.choice([*range(1, 21)])
            total += rand_num
            all_rolls['d20'].append(rand_num)
            if rand_num == 1:
                crit_f += 1
            elif rand_num == 20:
                crit_s += 1
        message_response += f'\tRolled {ctx.options.d20} D20: {all_rolls["d20"]}\r'
        if crit_f > 0:
            message_response += f'\t\t{crit_f} critical failures! :( \r'
        if crit_s > 0:
            message_response += f'\t\t{crit_s} critical successes! :D \r'

    if ctx.options.d12 > 0:
        for idx in range(1, ctx.options.d12 + 1):
            rand_num = random.choice([*range(1, 13)])
            total += rand_num
            all_rolls['d12'].append(rand_num)
        message_response += f'\tRolled {ctx.options.d12} D12: {all_rolls["d12"]}\r'

    if ctx.options.d10 > 0:
        for idx in range(1, ctx.options.d10 + 1):
            rand_num = random.choice([*range(1, 11)])
            total += rand_num
            all_rolls['d10'].append(rand_num)
        message_response += f'\tRolled {ctx.options.d10} D10: {all_rolls["d10"]}\r'

    if ctx.options.d8 > 0:
        for idx in range(1, ctx.options.d8 + 1):
            rand_num = random.choice([*range(1, 9)])
            total += rand_num
            all_rolls['d8'].append(rand_num)
        message_response += f'\tRolled {ctx.options.d8} D8: {all_rolls["d8"]}\r'

    if ctx.options.d6 > 0:
        for idx in range(1, ctx.options.d6 + 1):
            rand_num = random.choice([*range(1, 7)])
            total += rand_num
            all_rolls['d6'].append(rand_num)
        message_response += f'\tRolled {ctx.options.d6} D6: {all_rolls["d6"]}\r'

    if ctx.options.d4 > 0:
        for idx in range(1, ctx.options.d4 + 1):
            rand_num = random.choice([*range(1, 5)])
            total += rand_num
            all_rolls['d4'].append(rand_num)
        message_response += f'\tRolled {ctx.options.d4} D4: {all_rolls["d4"]}\r'

    message_response += f'\tBonus: {ctx.options.bonus}\r'
    message_response += f'\tTotal of Rolls with Bonus: {total + ctx.options.bonus}'
    await ctx.respond(message_response)


class CompletedRoll:
    def __init__(self, rolls: list, total: int, average: decimal, had_critfail: bool, had_nat20: bool):
        self.rolls = rolls
        self.total = total
        self.average = round(average, 2)
        self.had_critfail = had_critfail
        self.had_nat20 = had_nat20


def die_roll(dice_type: int, num_of_dice: int) -> CompletedRoll:
    """Rolls dice (Standard D&D Set) of chosen type and chosen number.

    Args:
        dice_type (int): D4 (4), D6 (6)... D20 (20)
        num_of_dice (int): Number of dice to be rolled.

    Returns:
        CompletedRoll instance:
        (self, rolls: list, total: int, had_critfail: bool, had_nat20: bool)
    """

    dice_sides = []
    for x in range(1, dice_type + 1):
        dice_sides.append(x)
    dice_rolled = []
    crit_fails = False
    crit_successes = False

    for x in range(num_of_dice):
        roll = int(random.choice(dice_sides))
        dice_rolled.append(roll)
        if roll == 1 and dice_type == 20:
            crit_fails = True
        elif roll == 20:
            crit_successes = True

    return CompletedRoll(dice_rolled, sum(dice_rolled), sum(dice_rolled)/len(dice_rolled), crit_fails, crit_successes)
# endregion


if __name__ == "__main__":
    keep_alive()
    bot.run()
