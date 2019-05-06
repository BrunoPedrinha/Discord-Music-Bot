import discord
from discord.ext import commands
import MusicPlayer

music_player = MusicPlayer.MusicPlayer()
#cog class for the music commands.
class MusicCommands:

    global music_player

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief='Paste url or use "SONG NAME" with quotes')
    async def play(self, context, url):
        await music_player.Create_Player(url, context, self.client)

    @commands.command(pass_context = True)
    async def stop(self, context):
        music_player.Stop_Playing()

    @commands.command(pass_context=True)
    async def volume(self, context, value):
        music_player.Set_Volume(context, int(value))

    @commands.command(pass_context=True)
    async def current(self, context):
        await music_player.Now_Playing(context, self.client)

def setup(client):
    client.add_cog(MusicCommands(client))
