import discord
from discord.ext import commands

from src.combat.battle_manager import BattleManager
from src.data.data_manager import DataManager
from src.discord_token import TOKEN
from src.elemental.elemental_factory import ElementalInitializer
from src.shop.general_shop import GeneralShop
from src.team.combat_team import CombatTeam
from src.ui.view_manager import ViewCommandManager

description = "Collect elementals and battle them!"
bot = commands.Bot(command_prefix=';', description=description)
client = discord.Client()
view_manager: ViewCommandManager = None
battle_manager: BattleManager = BattleManager()
data_manager: DataManager = DataManager()


@bot.event
async def on_ready():
    global view_manager
    view_manager = ViewCommandManager(bot)
    print("Monbot is ready!")


@bot.command(pass_context=True)
async def status(ctx):
    user = ctx.message.author
    await view_manager.delete_message(ctx.message)
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    if player.is_busy:
        return
    if player.has_elemental:
        await view_manager.show_status(player)
    else:
        await view_manager.show_starter_selection(player)


@bot.command(pass_context=True)
async def shop(ctx):
    user = ctx.message.author
    await view_manager.delete_message(ctx.message)
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    if not player.has_elemental or player.is_busy:
        return
    await view_manager.show_shop(GeneralShop(), player)


@bot.command(pass_context=True)
async def versus(ctx):
    user = ctx.message.author
    await view_manager.delete_message(ctx.message)
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    if not player.has_elemental:
        await view_manager.show_starter_selection(player)
        return
    if player.is_busy:
        return
    await view_manager.show_versus(player, data_manager, ctx.message.server)


@bot.command(pass_context=True)
async def battle(ctx):
    # Create or resume a battle
    user = ctx.message.author
    await view_manager.delete_message(ctx.message)
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    if not player.has_elemental:
        await view_manager.show_starter_selection(player)
    elif player.is_busy:
        await player.primary_view.render()
    elif player.can_battle:
        combat_team = battle_manager.create_pve_combat(player)
        await view_manager.show_battle(player, combat_team)
    else:
        await view_manager.show_status(player)


@bot.command(pass_context=True)
async def summon(ctx):
    # Add a random Elemental to your team.
    user = ctx.message.author
    await view_manager.delete_message(ctx.message)
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    if player.is_busy:
        return
    if player.has_elemental:
        elemental = ElementalInitializer.make_random(player.level, player.team.elementals)
        player.add_elemental(elemental)
        await view_manager.show_status(player)
    else:
        await view_manager.show_starter_selection(player)


@bot.event
async def on_reaction_add(reaction, user):
    """
    1) Check if the user is adding a reaction to their own view.
    2) Check if the user is adding a reaction to a ChallengeForm.
    If either are true, the form sees if there is a valid option mapped to the reaction.
    """
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    view = player.primary_view
    if view and view.matches(reaction.message):
        await view.pick_option(reaction.emoji)
        return
    challenge = player.get_challenge(reaction.message)
    if challenge:
        await challenge.validate_option(player, reaction.emoji)


@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    player = data_manager.get_created_player(user)
    view = player.primary_view
    if view and view.matches(reaction.message):
        await view.remove_option(reaction.emoji)


@bot.event
async def on_message(message):
    """
    Check if the user has a view that is awaiting an input, eg. renaming an Elemental.
    """
    if message.author.bot:
        return
    await bot.process_commands(message)
    player = data_manager.get_created_player(message.author)
    view = player.primary_view
    if view and view.is_awaiting_input:
        await view.receive_input(message)

bot.run(TOKEN)
