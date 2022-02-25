import discord
from discord.ext import commands
import os
import random
kaleSafe = []
kaleQuotes = []
i = 0

deployCode = "AWS"

kQuotes = "./kalePics/kaleQuotes.txt"
kPics = "./kalePics/"


for filename in os.listdir('./kalePics'):
    if filename.endswith('.jpg'):
        kaleSafe.append(os.listdir('./kalePics')[i])
        i += 1

f = open(kQuotes)
for x in f:
    kaleQuotes.append(x[:-1] + " -Zboy32")


class SimpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Kiss me on my bolo head') 

    @commands.command()
    async def coqui(self, ctx):
        await ctx.send('Check out my SoundCloud dude')
        await ctx.send('https://soundcloud.com/cornelius-clout/coqui')

    @commands.command()
    async def add(self, ctx, numOne, numTwo):
        sum = int(numOne) + int(numTwo)
        if sum > 20 or sum < 0:
            await ctx.send("What the heck dude! I can't count that high!")
        else:
            await ctx.send("That's easy little gamer! It's {0}".format(sum))

    @commands.command()
    async def kale(self, ctx):
        randPic = random.randint(0, len(kaleSafe))
        randQuote = random.randint(0, len(kaleQuotes))
        await ctx.send(
            file=discord.File(kPics + kaleSafe[randPic]))
        await ctx.send(kaleQuotes[randQuote])


def setup(bot):
    bot.add_cog(SimpCommands(bot))