import discord
from discord.ext import commands
from pathlib import Path
import gtts
from pydub import AudioSegment
from pydub.effects import speedup

FFMPEG_OPTIONS = {'options': '-vn'}

class Tts(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        user = ctx.author
        voice = discord.utils.get(self.Bot.voice_clients, guild=ctx.guild)
        try:
            vc = user.voice.channel
            if ctx.channel.id == vc.id:
                tempfile = "speech.mp3"
                try:
                    ch = await vc.connect()
                except:
                    await ctx.guild.voice_client.disconnect()
                    ch = await vc.connect()
                speech = f"{user.display_name} пишет: {ctx.content}"
                tts = gtts.gTTS(speech, lang="ru")
                tts.save(tempfile)
                audio = AudioSegment.from_mp3(tempfile)
                new_file = speedup(audio,1.3,130)
                new_file.export(tempfile, format="mp3")
                ch.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=Path(".")/tempfile, **FFMPEG_OPTIONS))
        except:
            pass
            
    
def setup(bot):
    bot.add_cog(Tts(bot))