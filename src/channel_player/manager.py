import discord
from channel_player.player import ChannelPlayer
import logging

logger = logging.getLogger(__name__)

class ChannelManager:
    def __init__(self, bot):
        self.channels = []
        self.bot = bot

    @property
    def channel_ids(self) -> list[int]:
        return [channel.id for channel in self.channels]

    def connected(self, interaction: discord.Interaction) -> ChannelPlayer | None:
        if not interaction.user.voice or not interaction.user.voice.channel: # type: ignore
            return

        id = interaction.user.voice.channel.id # type: ignore
        try:
            player_idx = self.channel_ids.index(id)
        except:
            return

        return self.channels[player_idx]

    async def connect_channel(self, interaction: discord.Interaction) -> ChannelPlayer | None:
        if not interaction.user.voice or not interaction.user.voice.channel: # type: ignore
            logger.error('Tried to connect to user, but they are not in a voice channel')
            return
        player = await ChannelPlayer.new(ChannelPlayer(), interaction.user.voice.channel, self.bot) # type: ignore
        self.channels.append(player)
        return player
