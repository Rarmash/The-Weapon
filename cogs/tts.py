import discord
from discord.ext import commands
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
from options import servers_data

FFMPEG_OPTIONS = {'options': '-vn'}

class Tts(commands.Cog):
    def __init__(self, bot, servers_data):
        self.Bot = bot
        self.servers_data = servers_data
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
            server_data = self.servers_data.get(str(ctx.guild.id))
            if not server_data:
                return
            user = ctx.author
            try:
                vc = user.voice.channel
                if ctx.channel.id == vc.id and ctx.channel.id not in server_data.get("bannedTTSChannels", []):
                    tempfile = "speech.mp3"
                    try:
                        ch = await vc.connect()
                    except discord.errors.ClientException:
                        await ctx.guild.voice_client.disconnect()
                        ch = await vc.connect()
                    speech = f"{user.display_name} пишет: {ctx.content}"
                    tts = gTTS(speech, lang="ru")
                    tts.save(tempfile)
                    audio = AudioSegment.from_mp3(tempfile)
                    new_file = speedup(audio,1.3,130)
                    new_file.export(tempfile, format="mp3")
                    ch.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=Path(".")/tempfile, **FFMPEG_OPTIONS))
            except:
                pass
        except:
            pass
            
    
def setup(bot):
    bot.add_cog(Tts(bot, servers_data))