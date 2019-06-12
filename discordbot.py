import discord
import asyncio
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

import googlecalendar

TOKEN = os.getenv("TOKEN")

client = discord.Client()


def tomorrowevents():
    allevents = googlecalendar.gettomorrowevents()
    message_list = ""
    if allevents:
        for event in allevents:
            if event[3] == 1:
                message_event = "%s in %s at %s for %s hour.\n" % (event[4], event[5], event[1], event[3])
                message_list += message_event
            elif event[3] >= 2:
                message_event = "%s in %s at %s for %s hours.\n" % (event[4], event[5], event[1], event[3])
                message_list += message_event
        return "Tomorrow events are as follows:\n" + message_list
    else:
        return None


@client.event
async def on_ready():
    print('The bot is Ready. We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!nextevent'):
        contentlist = googlecalendar.getrecentevents(1)
        if contentlist[0][3] == 1:
            await message.channel.send("The event next is %s on the %s at %s for %s hour in %s." % (
                contentlist[0][4], contentlist[0][0], contentlist[0][1], contentlist[0][3], contentlist[0][5]))
        elif contentlist[0][3] >= 2:
            await message.channel.send("The event next is %s on the %s at %s for %s hours in %s." % (
                contentlist[0][4], contentlist[0][0], contentlist[0][1], contentlist[0][3], contentlist[0][5]))
        else:
            await message.channel.send("Could not find any upcoming events")
    if message.content.startswith('!tomorrow'):
        tomorrowsevents = tomorrowevents()
        if tomorrowsevents:
            await message.channel.send(tomorrowsevents)
        else:
            await message.channel.send("There are no events for tomorrow")


async def tomorrows_events():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(), name='general')
    while not client.is_closed():
        now = datetime.datetime.now()
        if now.hour == 18:
            tomorrowsevents = tomorrowevents()
            if tomorrowsevents:
                await channel.send(tomorrowsevents)
            else:
                await channel.send("There are no events for tomorrow")

            await asyncio.sleep(3660)
        else:
            await asyncio.sleep(600)


client.loop.create_task(tomorrows_events())

client.run(TOKEN)
