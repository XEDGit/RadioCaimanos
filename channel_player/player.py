import discord
import asyncio
import logging
import random

from channel_player.song import Song
from config.config import Config
from interactions.interactions import send_response
from views.search import make_search_view
from views.panel import ControlPanel
from views.playlist import PlaylistEmbed

logger = logging.getLogger(__name__)

class ChannelPlayer:
    async def new(self, channel: discord.VoiceChannel, bot):
        self.bot = bot
        self.playlist: list[Song] = []
        self.index = 0
        self.channel = channel
        self.id = channel.id
        self.client = await channel.connect()
        self.volume = 0.5
        self.song = None
        self.minimized = False
        self.embed = PlaylistEmbed(self)
        self.view = ControlPanel(self)
        self.control_panel_msg = None
        return self

    async def _check_empty_channel(self):
        """Check if voice channel is empty and disconnect if so"""
        while self.client and self.client.is_connected():
            try:
                await asyncio.sleep(30)
                human_members = [member for member in self.channel.members if not member.bot]
                
                if len(human_members) == 0:
                    logger.info(f"No users in voice channel {self.channel.name}, disconnecting...")
                    await self.stop()
                    return

            except Exception as e:
                logger.error(f"Error checking empty channel: {e}")
                break

    async def play(self, interaction: discord.Interaction, url: str | None = None):
        if url:
            await self.parse_url(interaction, url)

        if not url and self.client.is_paused():
            self.client.resume()

        elif not self.client.is_playing():
            await self.loop()

    async def loop(self):
        if self.index >= len(self.playlist):
            # No more songs to play
            await self.stop()
            return

        self.song = self.playlist[self.index]
        self.song.load()
        await self.make_control_panel()
        if not self.song.data or (self.song.data and 'url' not in self.song.data):
            self.index += 1
            await self.loop()
            return
        if self.index + 1 < len(self.playlist):
            self.bot.loop.run_in_executor(
                self.bot.executor,
                self.playlist[self.index + 1].load
            )
        logger.info(f'Playing song: {self.song.name}')
        audio_source = discord.FFmpegPCMAudio(self.song.data['url'], before_options=Config.FFMPEG_OPTIONS['before_options'], options=Config.FFMPEG_OPTIONS['options'])
        volume_source = discord.PCMVolumeTransformer(audio_source, volume=self.volume)
        self.client.play(volume_source, after=lambda _: asyncio.run_coroutine_threadsafe(self.after_loop(), self.bot.loop))

    async def after_loop(self):
        if self.song:
            self.song.unload()
            self.song = None
        self.index += 1
        if not self.client or not self.client.is_connected():
            await self.stop()
            return
        if self.index < len(self.playlist):
            await self.loop()
        else:
            pass

    async def pause(self):
        if self.client.is_playing():
            self.client.pause()

    async def play_next(self, interaction: discord.Interaction, url):
        if url:
            await self.parse_url(interaction, url, at_end=False)

        if not url and self.client.is_paused():
            self.client.resume()
        elif not self.client.is_playing():
            await self.loop()
    
    async def skip(self, interaction, n):
        try:
            n = int(n)
        except:
            await send_response(interaction, f"The amount of songs to skip specified: '{n}' is not a number")
        self.index += n - 1
        self.client.stop()
    
    async def rewind(self, interaction, n):
        try:
            n = int(n)
        except:
            await send_response(interaction, f"The amount of songs to skip specified: '{n}' is not a number")
        self.index -= n
        self.client.stop()
    
    async def change_volume(self, interaction, volume_str: str):
        """Change the volume (0-100)"""
        try:
            volume_int = int(volume_str)
            if volume_int < 0 or volume_int > 100:
                await send_response(interaction, "❌ Volume must be between 0 and 100!")
                return

            volume_float = volume_int / 100.0
            self.volume = max(0.0, min(1.0, volume_float))

            # Update current playing volume if something is playing
            if self.client and self.client.source:
                if hasattr(self.client.source, 'volume'):
                    self.client.source.volume = self.volume # type: ignore

            await self.make_control_panel()

        except ValueError:
            await send_response(interaction, "❌ Please provide a valid volume between 0 and 100!")
    
    async def shuffle(self, interaction: discord.Interaction):
        if len(self.playlist) < 2:
            await send_response(interaction, "Not enough songs to shuffle!")
            return

        # Shuffle the playlist
        random.shuffle(self.playlist)

        self.index = 0
        self.client.stop()
        await send_response(interaction, "Playlist shuffled!")

    async def stop(self):
        if not self.client or not self.client.is_connected():
            return
        if self.control_panel_msg:
            await self.control_panel_msg.delete()
        self.client.stop()
        await self.client.disconnect()
        self.bot.manager.channels.remove(self)
    
    async def search_yt(self, interaction: discord.Interaction, url: str | None):
        if not url:
            return None
        search_result = await self.bot.loop.run_in_executor(
            self.bot.executor,
            lambda: self.bot.ytdl.extract_info(f"ytsearch:{url}", download=False)
        )

        if search_result and 'entries' in search_result and search_result['entries']:
            return await make_search_view(self, interaction, search_result)
        else:
            return None

    def parse_url_impl(self, url):
        try:
            return self.bot.ytdl.extract_info(url, download=False)
        except:
            return {}

    async def parse_url(self, interaction: discord.Interaction, url: str, at_end = True):
        parsed_url = url
        if not url.startswith('https://'):
            parsed_url = await self.search_yt(interaction, url)
        
        if not parsed_url:
            await send_response(interaction, f'No search results found for: {url}')
            return

        data = await self.bot.loop.run_in_executor(
            self.bot.executor,
            lambda: self.parse_url_impl(parsed_url)
        )

        if not data:
            await send_response(interaction, f'No results found for: {url}')
            return


        if 'entries' in data:
            for d in data['entries']:
                song_url = d['url'] if d['url'].find('youtube.') == -1 else f'https://www.youtube.com/watch?v={d["id"]}'
                if at_end:
                    self.playlist.append(Song(song_url, d['title'], d.get('artist', d.get('channel', '')), self.parse_url_impl))
                else:
                    self.playlist.insert(self.index+1, Song(song_url, d['title'], d.get('artist', d.get('channel', '')), self.parse_url_impl))
        else:
            if parsed_url.find('youtube.') != -1:
                parsed_url = f'https://www.youtube.com/watch?v={data["id"]}'
            if at_end:
                self.playlist.append(Song(parsed_url, data['title'], data.get('artist', data.get('channel', '')), self.parse_url_impl))
            else:
                self.playlist.insert(self.index+1, Song(parsed_url, data['title'], data.get('artist', data.get('channel', '')), self.parse_url_impl))
        await self.make_control_panel()

    async def make_control_panel(self):
        self.embed.make_embed()
        last_msg = self.control_panel_msg
        is_last = False
        if last_msg:
            async for bottom_msg in self.channel.history(limit=1):
                is_last = bottom_msg.id == last_msg.id
        if is_last and self.control_panel_msg:
            await self.control_panel_msg.edit(embed=self.embed.embed, view=self.view)
        else:
            self.control_panel_msg = await self.channel.send(embed=self.embed.embed, view=self.view)
            if last_msg:
                await last_msg.delete()
