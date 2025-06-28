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
                return
            await player.pause()
            await send_response(interaction, f"Done!")
        
        @self.command('sync')
        async def sync(ctx): 
            try:
                logger.info('Syncing...')
                synced = await self.tree.sync(guild=None)
                logger.info(f'Synced {len(synced)} command(s)')
            except Exception as e:
                logger.error(f'Failed to sync commands: {e}')

