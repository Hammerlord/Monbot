import discord
from discord.ext import commands

from src.discord_token import TOKEN
from src.ui.view_manager import ViewManager

description = "Collect elementals and battle them!"
bot = commands.Bot(command_prefix=';', description=description)
client = discord.Client()
view_manager = None


@bot.event
async def on_ready():
    global view_manager
    view_manager = ViewManager(bot)
    print("Monbot is ready!")


@bot.command(pass_context=True)
async def status(ctx):
    user = ctx.message.author
    await view_manager.get_status(user)


@bot.command(pass_context=True)
async def battle(ctx):
    # Create or resume a battle
    pass


@bot.event
async def on_reaction_add(reaction, user):
    """
    1) Check if the user is adding a reaction to their own view: if not, do nothing.
    2) If true, the form checks if there is a valid option mapped to the reaction.
    TODO this should do nothing if the reaction is not on the right message.
    """
    if user.bot:
        return
    view = view_manager.get_view(user)
    if view:
        await view.pick_option(reaction.emoji)


@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    view = view_manager.get_view(user)
    if view:
        await view.remove_option(reaction.emoji)


bot.run(TOKEN)
