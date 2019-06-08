import discord
import asyncio
import datetime
import sched
import time

import googlecalendar
import config

alarm_time = '18:09'

client = discord.Client()


def tomorrowevents():
    allevents = googlecalendar.gettomorrowevents()
    message_list = ""
    for event in allevents:
        if event[3] == 1:
            message_event = "%s in %s at %s for %s hour.\n" % (event[4], event[5], event[1], event[3])
            message_list = message_list + message_event
            return "Tomorrow events are as followed:\n" + message_list
        elif event[3] <= 2:
            message_event = "%s in %s at %s for %s hours.\n" % (event[4], event[5], event[1], event[3])
            message_list = message_list + message_event
            return "Tomorrow events are as followed:\n" + message_list
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
        elif contentlist[0][3] <= 2:
            await message.channel.send("The event next is %s on the %s at %s for %s hours in %s." % (
                contentlist[0][4], contentlist[0][0], contentlist[0][1], contentlist[0][3], contentlist[0][5]))
        else:
            await message.channel.send("Could not find any upcoming events")
    if message.content.startswith('!tomorrow'):
        await message.channel.send(tomorrowevents())


"""async def tomorrows_events():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(), name='general')
    while not client.is_closed:
        now = datetime.datetime.now()
        print(now)
        if now.hour == 18:
            # TODO: send message of tomorrowevents()
            print(tomorrowevents())
            await channel.send(tomorrowevents())

            # await asyncio.sleep(3660)
            await asyncio.sleep(5)
        else:
            # await asyncio.sleep(600)
            await asyncio.sleep(5)"""


async def tomorrows_events():
    await client.wait_until_ready()
    while not client.is_closed:
        channel = discord.utils.get(client.get_all_channels(), name='general')

        now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
        # get the difference between the alarm time and now
        diff = (datetime.datetime.strptime(alarm_time, '%H:%M') - datetime.datetime.strptime(now, '%H:%M')).total_seconds()

        # create a scheduler
        s = sched.scheduler(time.perf_counter, time.sleep)
        # arguments being passed to the function being called in s.enter
        args = (channel.send(tomorrowevents()))1
        # enter the command and arguments into the scheduler
        seconds = datetime.timedelta(hour=diff.hour, minute=diff.minute).total_seconds()
        s.enter(seconds, 1, client.loop.create_task, args)
        s.run()  # run the scheduler, will block the event loop


client.loop.create_task(tomorrows_events())

client.run(config.TOKEN)
