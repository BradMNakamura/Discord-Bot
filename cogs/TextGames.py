import discord
from discord.ext import commands
from Games import Connect4

#used to get other emojis
oneEmoji="1️⃣"
twoEmoji="2️⃣"
threeEmoji="3️⃣"
fourEmoji="4️⃣"
fiveEmoji="5️⃣"
sixEmoji="6️⃣"
sevenEmoji="7️⃣"

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMessage = ""
        self.playGame = Connect4.ConnectFour()
        self.savedCtx = ''
        self.counter = 0
        
    @commands.command()
    async def connect4(self, ctx):
      self.savedCtx = ctx
      embed = discord.Embed(color=discord.Color.blurple())
      embed.title = "Player Vs Player"
      embed.description = self.playGame.PrintBoard()
      await ctx.send(embed=embed) 
      self.lastMessage = ctx.channel.last_message_id
      message = await ctx.channel.fetch_message(int(self.lastMessage))
      self.ctx = await self.bot.get_context(message)
      await message.add_reaction(oneEmoji)
      await message.add_reaction(twoEmoji) 
      await message.add_reaction(threeEmoji)
      await message.add_reaction(fourEmoji)
      await message.add_reaction(fiveEmoji) 
      await message.add_reaction(sixEmoji)
      await message.add_reaction(sevenEmoji)
      
    @commands.command()
    async def DisplayBoard(self, ctx):
      embed = discord.Embed(color=discord.Color.blurple())
      embed.title = "Player Vs Player"
      embed.description = self.playGame.PrintBoard()
      message = await ctx.channel.fetch_message(int(self.lastMessage))
      await message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      currRow = 0
      currCol = 0
      playerNum = 0
      if(payload.user_id == 730310615968776223 or payload.message_id != self.lastMessage):
        return
      if (self.counter % 2):
        currPlayer = ":yellow_circle:"
      else :
        currPlayer = ":red_circle:"
        playerNum = 1

      self.counter += 1

      if(payload.emoji.name == twoEmoji):
        currRow = currCol = 1
      elif(payload.emoji.name == threeEmoji):
        currRow = currCol = 2
      elif(payload.emoji.name == fourEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == fiveEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == sixEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == sevenEmoji):
        currRow = currCol = 3
      if (self.playGame.TakeTurn(currPlayer, playerNum, self.playGame.GetRow(currRow), currCol)):
        await self.DisplayWinner(self.savedCtx)
      else:
        await self.DisplayBoard(self.savedCtx)

    @commands.command()
    async def DisplayWinner(self, ctx):
      embed = discord.Embed(color=discord.Color.blurple())
      embed.title = "WINNER"
      embed.description = "kale sucks lmao. Good job whoever won"
      message = await ctx.channel.fetch_message(int(self.lastMessage))
      await message.edit(embed=embed)   
      
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      currRow = 0
      currCol = 0
      playerNum = 0
      if(payload.user_id == 730310615968776223 or payload.message_id != self.lastMessage):
        return
      if (self.counter % 2):
        currPlayer = ":yellow_circle:"
      else :
        currPlayer = ":red_circle:"
        playerNum = 1

      self.counter += 1

      if(payload.emoji.name == twoEmoji):
        currRow = currCol = 1
      elif(payload.emoji.name == threeEmoji):
        currRow = currCol = 2
      elif(payload.emoji.name == fourEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == fiveEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == sixEmoji):
        currRow = currCol = 3
      elif(payload.emoji.name == sevenEmoji):
        currRow = currCol = 3
      if (self.playGame.TakeTurn(currPlayer, playerNum, self.playGame.GetRow(currRow), currCol)):
        await self.DisplayWinner(self.savedCtx)
      else:
        await self.DisplayBoard(self.savedCtx)




def setup(bot):
    bot.add_cog(GameCommands(bot))