import youtube_dl
import asyncio


class MusicPlayer:
    is_playing = False
    player = None
    volume = 0.1
    url_holder = ""

    def __init__(self):
        pass

    def Set_Playing(value):
        MusicPlayer.is_playing = value

    def Get_Playing():
        return MusicPlayer.is_playing

    def Get_Volume():
        return MusicPlayer.volume

    #if the player is playing stop it
    def Stop_Playing(self):
        if MusicPlayer.Get_Playing():
            MusicPlayer.player.stop()
            MusicPlayer.Set_Playing(False)

    #check if the bot is connected to the voice channel of the author requesting the song if not connect
    async def Bot_Voice_Connected(context, client, server):
        if not client.is_voice_connected(server):
            channel = context.message.author.voice.voice_channel
            await client.join_voice_channel(channel)

    #Set the volume of the player. Ranges from 0 to 1
    def Set_Volume(self, context, value):
        MusicPlayer.volume = value / 100
        id = context.message.server.id
        MusicPlayer.player.volume = MusicPlayer.Get_Volume()

    async def Now_Playing(self, context, client):
        #youtube_dl options.
        ydl_opts = {
            'default_search': 'ytsearch',
            'skip_download': True,

        }
        #use those youtube_dl options
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #get the info of the song playing/requested
            info = ydl.extract_info(MusicPlayer.url_holder, download=False)
            #if it's a youtube link we can just use the info extracted from above
            if ("https://" in MusicPlayer.url_holder) or ("http://" in MusicPlayer.url_holder):
                await client.send_message(context.message.channel, "```Now Playing: {}. Requested by {} ```".format(info['title'], context.message.author.name))
            else : #if it's not a youtube url and just a song name then loop the info array and only use the info we need.
                for _data in info['entries']:
                    if not _data: #edge case if no data then can't get info
                        print('ERROR: Unable to get info. Continuing...')
                        continue
                    await client.send_message(context.message.channel, "```Now Playing: {}. Requested by {} ```".format(_data['title'], context.message.author.name))

    #create the player that will play the song in the form of a url OR artist name/song name
    async def Create_Player(self, url, context, client):
        server = context.message.server
        MusicPlayer.url_holder = url
        #check if the bot is connected to the voice channel of the author who requested the song
        await MusicPlayer.Bot_Voice_Connected(context,client, server)
        #stop the song if the player is playing
        MusicPlayer.Stop_Playing(self)
        #get the channel the bot is connected to
        voice_client = client.voice_client_in(server)
        #create the player with options to allow youtube links or song name/artist name. Set player playing to true and set the volume
        MusicPlayer.player = await voice_client.create_ytdl_player(url, ytdl_options={'default_search': 'auto'}, after=lambda: Set_Playing(False))
        MusicPlayer.Set_Playing(True)
        MusicPlayer.player.volume = MusicPlayer.Get_Volume()
        MusicPlayer.player.start()
        await MusicPlayer.Now_Playing(self, context, client)
        