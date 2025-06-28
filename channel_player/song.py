import logging

logger = logging.getLogger(__name__)

class Song:
    def __init__(self, url: str, name, artist, ytdl):
        if i := url.find('v=') != -1 and 'index=' in url:
            url = url[:url.find('&', i)]

        self.url = url
        self.data = None
        self.name = name
        self.artist = artist
        self.ytdl = ytdl

    def load(self):
        if not self.data:
            logger.info(f'Loading song data for {self.name} from {self.url}')
            self.data = self.ytdl(self.url)

    def unload(self):
        if self.data:
            self.data = None

    def format_song(self, long=True):
        s = self.name
        if self.artist and long and '-' not in s:
            s += f' - {self.artist}'
        if long and self.data and 'duration_string' in self.data:
            s += f' ({self.data["duration_string"]})'
        return s

    def __str__(self):
        return f'Song(name={self.name}, artist={self.artist}, url={self.url} data={self.data})'