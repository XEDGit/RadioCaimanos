import discord
from config.config import Config

class PlaylistEmbed:
    def __init__(self, player):
        self._manual_scroll = False
        self.queue_offset = 0
        self.player = player
        self.make_embed()

    def make_embed(self):
        total_songs = len(self.player.playlist)
        if not total_songs:
            self.embed = discord.Embed(color=Config.COLOR, title="Nothing is playing", description="No songs in playlist, use /play *youtube link* to play something" if not self.player.minimized else None)
            return self.embed

        playing = self.player.playlist[self.player.index]
        if total_songs == 1:
            self.embed = discord.Embed(color=Config.COLOR, title=f"🎵 {playing.name}", description="No songs in playlist, use /play *youtube link* to play something" if not self.player.minimized else None)
            return self.embed

        if not self._manual_scroll:
            self.queue_offset = max(1, self.player.index + 1)

        max_offset = max(0, total_songs - Config.SONGS_PER_PAGE)
        self.queue_offset = max(0, min(self.queue_offset, max_offset))

        page_slice = self.player.playlist[self.queue_offset:self.queue_offset + Config.SONGS_PER_PAGE]

        description = ""

        for i, song in enumerate(page_slice):
            if song is playing:
                description += f'**{song.format_song()}**\n'
            else:
                description += f'`{abs(i+self.queue_offset-self.player.index)}.` {song.format_song(False)}\n'

        description += f"\n**Playlist: {len(self.player.playlist)} songs**"

        volume_percentage = int(self.player.volume * 100)
        description += f"\n**Volume: {volume_percentage}%**"

        self.embed = discord.Embed(color=Config.COLOR, title=playing.format_song(), description=description if not self.player.minimized else None)

        if playing.data and 'thumbnail' in playing.data:
            if self.player.minimized:
                self.embed.set_thumbnail(url=playing.data['thumbnail'])
                self.embed.set_image(url=None)
            else:
                self.embed.set_image(url=playing.data['thumbnail'])
                self.embed.set_thumbnail(url=None)

        return self.embed
