import discord
import asyncio
import datetime

import googlecalendar
import config

client = discord.Client()

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
        if contentlist[3] == 1:
            await message.channel.send("The event next is %s on the %s at %s for %s hour in %s." % (
            contentlist[4], contentlist[0], contentlist[1], contentlist[3], contentlist[5]))
        else:
            await message.channel.send("The event next is %s on the %s at %s for %s hours in %s." % (
            contentlist[4], contentlist[0], contentlist[1], contentlist[3], contentlist[5]))
    if message.content.startswith('!tomorrow'):
        print(tomorrowevents())
        await message.channel.send(tomorrowevents())


async def user_metrics_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.datetime.now()
        if now.hour == 18:
            # TODO: send message of tomorrowevents()

            await asyncio.sleep(3660)
        else:
            await asyncio.sleep(600)


client.run(config.TOKEN)
