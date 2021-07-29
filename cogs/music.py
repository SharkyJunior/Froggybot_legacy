import discord
from main import *

FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPT = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = youtube_dl.YoutubeDL(YDL_OPT)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPT), data=data)

# initializing cog
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music is ready')

    @commands.command()
    async def play_music(self, msg, url):
        server_data = load_server_data(msg.guild)
        if msg.author.voice is None:
            await msg.channel.send('**:x: You are not in a voice channel!**')
        else:
            vc = msg.author.voice.channel
            is_connected = server_data['is_connected']
            if not is_connected:
                await vc.connect()
                server_data['is_connected'] = True
                save_server_data(server_data, msg.guild)
                is_playing = server_data['is_playing']
                if not is_playing:
                    vc = msg.voice_client

                    '''
                    info = ytdl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
                    vc.play(source)'''
                    async with msg.typing():
                        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                        msg.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                        server_data['is_playing'] = True
                        save_server_data(server_data, msg.guild)
                        print('playing')
                else:
                    await msg.channel.send("**:x: I'm already playing music!**")
            else:
                await msg.channel.send("**:x: I'm already playing music somewhere else!**")

    @commands.command()
    async def stop(self, msg):
        msg.voice_client.stop()
        server_data = load_server_data(msg.guild)
        server_data['is_playing'] = False
        save_server_data(server_data, msg.guild)

    @commands.command()
    async def pause(self, msg):
        msg.voice_client.pause()

    @commands.command()
    async def resume(self, msg):
        msg.voice_client.resume()

    @commands.command()
    async def disconnect(self, msg):
        await msg.voice_client.disconnect()
        server_data = load_server_data(msg.guild)
        server_data['is_connected'] = False
        save_server_data(server_data, msg.guild)


# activating cog
def setup(bot):
    bot.add_cog(Music(bot))