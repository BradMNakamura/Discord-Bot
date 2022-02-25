Aimport discord
import re
import lavalink
import os
import emoji
import random
from discord.ext import commands
from lavalink.utils import format_time

#I Dont know what to call it in Python
#Consts Variables
playPause = '\U000023EF'
seeMonkey = '\U0001F648'
callHand = '\U0001F919'
repeatEmoji = '\U0001F501'
url_rx = re.compile(r'https?://(?:www\.)?.+')
CONST_DESC = "\n\n:play_pause: Play/Pause\n:see_no_evil: Skip Song\n:call_me: Disconnect\n:repeat: Replay Song"
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #Private Variables
        self.brysonSounds = True
        self.isPaused = False
        self.isReplay = False
        self.lastMessage = ''
        self.savedCtx = ''
        self.trackList = []
        self.trackTime = []
        self.introIndex = 0;
        self.introSong = [
          "https://www.youtube.com/watch?v=sUn0ZSnOIyE",
          "https://www.youtube.com/watch?v=szprR5IBYUA",
          "https://www.youtube.com/watch?v=MvhB_P_rT4I",
          "https://www.youtube.com/watch?v=GLoz_iQsC4M"
        ]
        if not hasattr(bot, 'lavalink'): 
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('0.0.0.0', 7000, 'testing', 'na', 'default-node')
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):

        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

        should_connect = ctx.command.name in ('play', 'clown', 'disconnect')
        if not ctx.author.voice or not ctx.author.voice.channel:

            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                return
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):

            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)


    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):

        self.savedCtx = ctx
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)

        if self.brysonSounds:
          await self.playSong(ctx, self.introSong[0])
        else:
          if self.introIndex == len(self.introSong):
            self.introIndex = 0;
          await self.playSong(ctx, self.introSong[self.introIndex])
          
          self.introIndex += 1
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                trackInfo = str(f'[{track["info"]["title"]}]({track["info"]["uri"]})')
                trackInfo += CONST_DESC
                self.trackList.append(trackInfo)
                
                #Convert milliseconds to seconds
                player.add(requester=ctx.author.id, track=track)
        else:      
            track = results['tracks'][0]
            trackInfo = str(f'[{track["info"]["title"]}]({track["info"]["uri"]})')
            trackInfo += CONST_DESC
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            self.trackList.append(trackInfo)
            player.add(requester=ctx.author.id, track=track)
        #Show Embed Message to chat
        await self.currentSong(ctx)
    

    async def currentSong(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        embed = discord.Embed(color=discord.Color.blurple())
        embed.title = 'Current Track'
        if not player.is_playing:
          await player.play()
        embed.description = self.trackList[0]
        await ctx.send(embed=embed)
        
        #Add Reactions 
        self.lastMessage = ctx.channel.last_message_id
        message = await ctx.channel.fetch_message(int(self.lastMessage))
        await message.add_reaction(playPause)
        await message.add_reaction(seeMonkey)
        await message.add_reaction(callHand)
        await message.add_reaction(repeatEmoji)

    @commands.command(aliases=['d'])
    async def disconnect(self, ctx):
        #Reset UI
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.queue.clear()
        if not player.is_connected:
            return await ctx.send("I'm not connected dumbass")
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        #Embed Text
        if self.brysonSounds == True:
          await self.playSong(ctx, "https://www.youtube.com/watch?v=mJfObdbyQWY")
        embed = discord.Embed(color=discord.Color.blurple())    
        embed.title = 'Shaka Brah ' + callHand
        embed.description = ''
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/243315618927869973/270812776866381824/dab.jpg')
        message = await ctx.channel.fetch_message(int(self.lastMessage))
        await message.edit(embed=embed)
        await self.resetPlayer()
        await player.play()


    @commands.command(aliases=['s'])
    async def skip(self, ctx):
      player = self.bot.lavalink.player_manager.get(ctx.guild.id)
      message = await ctx.channel.fetch_message(int(self.lastMessage))
      embed = discord.Embed(color=discord.Color.blurple())
      #Make sure replay doesnt break skip function
      self.isReplay = False
      self.trackList.pop(0)
      if (len(self.trackList) == 0 and self.brysonSounds == True):
        await self.resetPlayer()
        await self.playSong(ctx, "https://www.youtube.com/watch?v=mJfObdbyQWY")
        embed.title = 'Shaka Brah ' + callHand
        embed.description = ''
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/243315618927869973/270812776866381824/dab.jpg')
      else: 
        embed.title = 'Current Track Len 1'
        embed.description = self.trackList[0]
      await message.edit(embed=embed)
      await player.play()
    
    @commands.command()
    async def pause(self, ctx):
      player = self.bot.lavalink.player_manager.get(ctx.guild.id)
      self.isPaused = not self.isPaused
      await player.set_pause(self.isPaused)

    @commands.command()
    async def repeatSong(self,ctx):
      player = self.bot.lavalink.player_manager.get(ctx.guild.id)
      self.isReplay = not self.isReplay
      player.set_repeat(self.isReplay)

    @commands.command()
    async def clown(self, ctx):
        await ctx.send(':clown: :beverage_box:')
        await self.playSong(ctx,"https://www.youtube.com/watch?v=at1MAMYZddY")


    @commands.command()
    async def toggle(self, ctx):
      self.brysonSounds = not self.brysonSounds
      await ctx.send("Bryson Sounds: " + str(self.brysonSounds))


    @commands.command()
    async def toggleList(self, ctx):
      embed = discord.Embed(color=discord.Color.blurple())
      embed.title = "Toggle List"
      embed.description = "Bryson Sounds: " + str(self.brysonSounds)
      await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      if(payload.user_id == 730310615968776223 or payload.message_id != self.lastMessage):
        return
      if(payload.emoji.name == playPause):
        await self.pause(self.savedCtx)
      if(payload.emoji.name == seeMonkey):
        await self.skip(self.savedCtx)
      if(payload.emoji.name == callHand):
        await self.disconnect(self.savedCtx)
      if(payload.emoji.name == repeatEmoji):
        await self.repeatSong(self.savedCtx)
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      if(payload.user_id == 730310615968776223 or payload.message_id != self.lastMessage):
        return
      if(payload.emoji.name == playPause):
        await self.pause(self.savedCtx)
      if(payload.emoji.name == seeMonkey):
        await self.skip(self.savedCtx)
      if(payload.emoji.name == callHand):
        await self.disconnect(self.savedCtx)
      if(payload.emoji.name == repeatEmoji):
        await self.repeatSong(self.savedCtx)
  

    async def playSong(self, ctx,  query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        else:
            track = results['tracks'][0]
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    async def resetPlayer(self):
      self.lastMessage = ''
      self.isPaused = False
      self.isReplay = False
      player = self.bot.lavalink.player_manager.get(self.savedCtx.guild.id)
      player.set_repeat(False)
      self.trackList.clear()
      self.trackTime.clear()
def setup(bot):
    bot.add_cog(Music(bot))