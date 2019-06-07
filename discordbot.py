import discord

import googlecalendar

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


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


client.run('NTg2NDc3MDM4NjAxMjQwNTc2.XPol_Q.d_ZTf7UXch_EahhhQ4FSiCXIp7I')
