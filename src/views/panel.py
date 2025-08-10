import io
import discord
from config.config import Config
from interactions.interactions import send_response, defer

class ControlPanel(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=None)
        self.playlist = player.playlist
        self.player = player

    @discord.ui.button(emoji=Config.EMOJIS['back'], style=discord.ButtonStyle.secondary, row=0)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        await self.player.rewind(interaction, 1)

    @discord.ui.button(emoji=Config.EMOJIS['pause'], style=discord.ButtonStyle.secondary, row=0)
    async def play_pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        if self.player.client and self.player.client.is_playing():
            await self.player.pause()
            button.emoji = Config.EMOJIS['play']
        elif self.player.client and self.player.client.is_paused():
            await self.player.play(interaction)
            button.emoji = Config.EMOJIS['pause']
        else:
            await send_response(interaction, "❌ Nothing is playing!")
            return
        await self.player.make_control_panel()

    @discord.ui.button(emoji=Config.EMOJIS['next'], style=discord.ButtonStyle.secondary, row=0)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        await self.player.skip(interaction, 1)

    @discord.ui.button(emoji=Config.EMOJIS['shuffle'], style=discord.ButtonStyle.secondary, row=0)
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        await self.player.shuffle(interaction)

    @discord.ui.button(emoji=Config.EMOJIS['stop'], style=discord.ButtonStyle.secondary, row=0)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        await self.player.stop()

    @discord.ui.button(emoji=Config.EMOJIS['uparrow'], style=discord.ButtonStyle.secondary, row=1)
    async def scroll_up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        if self.player.embed.queue_offset > 0:
            self.player.embed.queue_offset = max(0, self.player.embed.queue_offset - Config.SONGS_PER_PAGE)
            self.player.embed._manual_scroll = True
            await self.player.make_control_panel()

    @discord.ui.button(emoji=Config.EMOJIS['rotate'], style=discord.ButtonStyle.secondary, row=1)
    async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        if not self.player.embed._manual_scroll:
            return
        self.player.embed._manual_scroll = False
        await self.player.make_control_panel()

    @discord.ui.button(emoji=Config.EMOJIS['downarrow'], style=discord.ButtonStyle.secondary, row=1)
    async def scroll_down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        total_songs = len(self.playlist)
        max_offset = max(0, total_songs - Config.SONGS_PER_PAGE)
        if self.player.embed.queue_offset < max_offset:
            self.player.embed.queue_offset = min(max_offset, self.player.embed.queue_offset + Config.SONGS_PER_PAGE)
            self.player.embed._manual_scroll = True
            await self.player.make_control_panel()

    @discord.ui.button(emoji=Config.EMOJIS['volumedown'], style=discord.ButtonStyle.secondary, row=1)
    async def volume_down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        current_volume = int(self.player.volume * 100)
        new_volume = max(0, current_volume - 10)
        await self.player.change_volume(interaction, str(new_volume))

    @discord.ui.button(emoji=Config.EMOJIS['volume'], style=discord.ButtonStyle.secondary, row=1)
    async def volume_up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        current_volume = int(self.player.volume * 100)
        new_volume = min(100, current_volume + 10)
        await self.player.change_volume(interaction, str(new_volume))


    @discord.ui.button(label="📋 Send me this playlist", style=discord.ButtonStyle.secondary, row=2)
    async def send_playlist_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        description = ''
        for i, song in enumerate(self.playlist):
            title = song.name
            artist = song.artist
            url = song.url
            description += f"{i+1}. {title} - {artist}\n{url}\n\n"

        if not self.playlist:
            description += 'No songs in the queue, use /play *url* to play songs'

        file_content = io.StringIO(description)
        file = discord.File(file_content, filename="playlist.txt") # type: ignore

        try:
            await interaction.user.send("🎵 **Current Playlist**", file=file)
        except discord.Forbidden:
            await interaction.followup.send("❌ I can't send you DMs, please enable them and try again.", ephemeral=True)
            return
        await interaction.followup.send("✅ Playlist sent to your DMs!", ephemeral=True)

    @discord.ui.button(emoji=Config.EMOJIS['minus'], style=discord.ButtonStyle.secondary, row=2)
    async def minimize_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await defer(interaction)
        self.player.minimized = not self.player.minimized
        if self.player.minimized:
            button.emoji = Config.EMOJIS['plus']
        else:
            button.emoji = Config.EMOJIS['minus']
        await self.player.make_control_panel()

