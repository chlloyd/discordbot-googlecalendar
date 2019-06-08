import discord
import asyncio
import datetime

import googlecalendar
import config

client = discord.Client()

channel = "general"

def tomorrowevents():
    allevents = googlecalendar.gettomorrowevents()
    message_list = ""
    for event in allevents:
        if event[3] == 1:
            message_event = "%s in %s at %s for %s hour.\n" % (event[4], event[5], event[1], event[3])
            message_list = message_list + message_event
        else:
            message_event = "%s in %s at %s for %s hours.\n" % (event[4], event[5], event[1], event[3])
            message_list = message_list + message_event
    return "Tomorrow events are as followed:\n" + message_list



@client.event
async def on_ready():
    print('The bot is Ready. We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!nextevent'):
        contentlist = googlecalendar.getrecentevents(1)
        if contentlist[0][3] == 1:  # TODO: FIX THIS PART
            await message.channel.send("The event next is %s on the %s at %s for %s hour in %s." % (
            contentlist[0][4], contentlist[0][0], contentlist[0][1], contentlist[0][3], contentlist[0][5]))
        else:
            await message.channel.send("The event next is %s on the %s at %s for %s hours in %s." % (
            contentlist[4], contentlist[0], contentlist[1], contentlist[3], contentlist[5]))
    if message.content.startswith('!tomorrow'):
        await message.channel.send(tomorrowevents())


async def tomorrows_events():
    await client.wait_until_ready()
    print("shere")
    while not client.is_closed():
        now = datetime.datetime.now()
        if now.hour == 16:
            # TODO: send message of tomorrowevents()
            channel = discord.utils.get(client.get_all_channels(), name='general')
            print(channel)
            await channel.send(tomorrowevents())

            #await asyncio.sleep(3660)
            await asyncio.sleep(5)
        else:
            # await asyncio.sleep(600)
            await asyncio.sleep(5)


client.run(config.TOKEN)
