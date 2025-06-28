import asyncio
from discord.ext import commands
import discord
from config.config import Config
import logging
from channel_player.manager import ChannelManager
import yt_dlp
import concurrent.futures
from interactions.interactions import send_response, defer

logger = logging.getLogger(__name__)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=Config.COMMAND_PREFIX, help_command=None, intents=intents)
        self.manager = ChannelManager(self)
        self.ytdl = yt_dlp.YoutubeDL(Config.YTDL_OPTIONS)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._setup_commands()

    def _setup_commands(self):
        @self.event
        async def on_ready():
            while not self.user:
                await asyncio.sleep(1)
            logger.info(f'Logged in as {self.user} (ID: {self.user.id}), bot is ready')
            logger.info('------')

        @self.tree.command(name="play", description="Play song from url or search a song")
        async def play(interaction: discord.Interaction, url: str | None = None):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                player = await self.manager.connect_channel(interaction)
            if not player:
                await send_response(interaction, "You need to be in a voice channel to play music")
                return
            await player.play(interaction, url)
            await send_response(interaction, f"Done!")

        @self.tree.command(name="playnext", description="Play song from url or search a song, play as next song")
        async def playnext(interaction: discord.Interaction, url: str | None = None):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                player = await self.manager.connect_channel(interaction)
            if not player:
                return
            await player.play_next(interaction, url)
            await send_response(interaction, f"Done!")

        @self.tree.command(name="pause", description="Pause current song")
        async def pause(interaction: discord.Interaction):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                return await send_response(interaction, "I'm not in a channel")
            await player.pause()
            await send_response(interaction, f"Done!")

        @self.tree.command(name="resume", description="Resume paused song")
        async def resume(interaction: discord.Interaction):
            await defer(interaction)
            player = self.manager.connected(interaction)

            if not player:
                return await send_response(interaction, "I'm not in a channel")
            if not player.client.is_paused():
                return await send_response(interaction, "The playback is not paused")

            await player.play(interaction)
            await send_response(interaction, f"Done!")

        @self.tree.command(name="skip", description="Skip current song or multiple songs")
        async def skip(interaction: discord.Interaction, n: int = 1):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                return await send_response(interaction, "I'm not in a channel")
            await player.skip(interaction, n)

        @self.tree.command(name="rewind", description="Go back to previous song(s)")
        async def rewind(interaction: discord.Interaction, n: int = 1):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                return await send_response(interaction, "I'm not in a channel")
            await player.rewind(interaction, n)

        @self.tree.command(name="stop", description="Stop playback and disconnect from voice channel")
        async def stop(interaction: discord.Interaction):
            await defer(interaction)
            player = self.manager.connected(interaction)
            if not player:
                return await send_response(interaction, "I'm not in a channel")
            await player.stop()
        
        @self.tree.command(name="rchelp", description="Show help message for Radio Caimanos")
        async def rchelp(interaction: discord.Interaction):
            await defer(interaction)
            help_message = Config.HELP_MESSAGE
            embed = discord.Embed(title="🎵 Caimanos Radio Bot - Music Commands & Controls", description=help_message, color=Config.COLOR)
            await interaction.response.send_message(embed=embed)

        @self.command('sync')
        async def sync(ctx):
            try:
                logger.info('Syncing...')
                synced = await self.tree.sync(guild=None)
                logger.info(f'Synced {len(synced)} command(s)')
            except Exception as e:
                logger.error(f'Failed to sync commands: {e}')

