import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import re

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store active timers
timers = {}

@client.event
async def on_ready():
    print('Bot started as {0.user}'.format(client))

@client.command()
async def tree(ctx, Land: str):
    # Verify that Land has maximum 4 numerical digits
    if not re.match(r'^\d{1,4}$', Land):
        await ctx.send("Wrong Land number.")
        return

    # If the timer is already active, do nothing
    if Land in timers:
        await ctx.send("Timer started!")
        return

    # Add the timer to the dictionary with 15 minutes (900 seconds) remaining
    timers[Land] = datetime.now() + timedelta(seconds=9000)
    await ctx.send(f"Timer active for Land {Land}.")

    # Wait for 14 minutes and 30 seconds (870 seconds) before sending the alert
    await asyncio.sleep(8940)
    await ctx.send(f"!Warning! Land {Land} trees spawning in ~1 minute.")

    # Wait for additional 30 seconds before the timer actually ends
    await asyncio.sleep(30)

    # Remove the timer from the dictionary
    del timers[Land]

@client.command()
async def delete(ctx, Land: str):
    # Verify that Land exists in the active timers and delete it
    if Land in timers:
        del timers[Land]
        await ctx.send(f"{Land} timer deleted.")
    else:
        await ctx.send(f"Land {Land} timer not found.")

@client.command()
async def stump(ctx, Land: str):
    # Verify that Land has maximum 4 numerical digits
    if not re.match(r'^\d{1,4}$', Land):
        await ctx.send("Wrong Land number.")
        return

    # If the timer is already active, do nothing
    if Land in timers:
        await ctx.send("Timer started!")
        return

    # Add the timer to the dictionary with 7 hours and 15 minutes (26100 seconds) remaining
    timers[Land] = datetime.now() + timedelta(seconds=26100)
    await ctx.send(f"Timer active for Land {Land}.")

    # Wait for 7 hours, 14 minutes, and 30 seconds (26070 seconds) before sending the alert
    await asyncio.sleep(26070)
    await ctx.send(f"!Warning! Land {Land} trees spawning in ~1 minute.")

    # Wait for additional 30 seconds before the timer actually ends
    await asyncio.sleep(30)

    # Remove the timer from the dictionary
    del timers[Land]

@client.command()
async def bot(ctx):
    # Explanation on how to use the bot
    explanation = ("Welcome to Tree Timers for BYAC Guild!\n"
                   "Type `!tree Land` to start a timer.\n"
                   "Type `!delete Land` to delete a timer.\n"
                   "Type `!stump Land` to start a 7 hours and 15 minutes timer.\n"
                   "Type `!check` to see active timers.\n"
                   "Enjoy!")

    await ctx.send(explanation)

@client.command()
async def check(ctx):
    # Show active timers and their remaining time in hours and minutes
    if timers:
        message = "Active timers:\n"
        for Land, tiempo_restante in timers.items():
            tiempo_restante = tiempo_restante - datetime.now()
            horas = tiempo_restante.seconds // 3600
            minutos = (tiempo_restante.seconds % 3600) // 60
            message += f"Land: {Land}, Time left: {horas} h, {minutos} m\n"
    else:
        message = "No timers active."

    await ctx.send(message)

@client.event
async def on_message(message):
    # Verify if the message is a timer command and has the correct format
    if message.content.startswith('!tree'):
        # Get the Land from the message (after the !tree command and a space)
        Land = message.content.split(' ', 1)[1]
        if re.match(r'^\d{1,4}$', Land):
            await client.process_commands(message)  # Process the message as a command
        else:
            await message.channel.send("Land # wrong.")
    else:
        # Ignore other bot messages to avoid infinite loops
        if message.author == client.user:
            return

        # Process the message for commands
        await client.process_commands(message)



client.run('MTI1MDI5MTI1ODM5MjMxMzg2Nw.Gjr_2p.SLPC77I476ylZLadY47onFxJw2p4o331Cfzg_8')




