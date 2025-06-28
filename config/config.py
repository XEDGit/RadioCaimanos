"""Configuration module for Caimanos Radio Bot."""

import discord

class Config:
    """Bot configuration settings."""
    
    # Time settings
    MINUTE = 60
    IDLE_TIMEOUT = 10 * MINUTE
    SONGS_PER_PAGE = 8
    
    # Bot settings
    COMMAND_PREFIX = '/'
    
    # Audio settings
    DEFAULT_VOLUME = 0.5
    MAX_HISTORY_SIZE = 100
    
    # YouTube DL options
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        'keep_fragments': False,
        'buffersize': 16384,
    }
    
    # FFmpeg options
    FFMPEG_OPTIONS = {
        'before_options': (
            '-reconnect 1 '
            '-reconnect_streamed 1 '
            '-reconnect_delay_max 5 '
            '-multiple_requests 1 '
            '-fflags +discardcorrupt '
            '-analyzeduration 0 '
            '-probesize 32 '
            '-thread_queue_size 512 '
            '-loglevel quiet '
            '-re '
            '-avoid_negative_ts make_zero '
            '-copyts '
            '-start_at_zero'
        ),
        'options': (
            '-vn '
            '-bufsize 128k '
            '-maxrate 128k '
            '-threads 1 '
            '-ac 2 '
            '-ar 48000 '
            '-f s16le '
            '-filter:a "aresample=async=0" '
            '-af "asetrate=48000,aresample=48000" '
            '-shortest '
            '-vsync 0 '
            '-async 0'
        ),
    }
    
    # Bot emojis
    EMOJIS_RAW = {
        'next': 1386494925562052709,
        'uparrow': 1386494535130943579,
        'rotate': 1386494526260117564,
        'shuffle': 1386494511789772880,
        'stop': 1386494503954808842,
        'volumedown': 1386494495972921354,
        'volume': 1386494485365653534,
        'play': 1386494475232088105,
        'downarrow': 1386494465451233331,
        'back': 1386494450456465408,
        'minus': 1388260212716212274,
        'plus': 1388260203920887990,
        'pause': 1388263760065724506,
    }

    EMOJIS = dict(
        [(k, discord.PartialEmoji(name=k, id=v)) for k, v in EMOJIS_RAW.items()]
    )
    
    # Help message
    HELP_MESSAGE = f"""**🎵 Caimanos Radio Commands:**
`!rcplay <url>` - Add song/playlist to bottom of queue (alias: `!rcp`)
`!rcplaynow <url>` - Play song/playlist to top of the queue (alias: `!rcpn`)
`!rcpause` - Pause current song
`!rcresume` - Resume paused song
`!rcskip [number]` - Skip current song or multiple songs (default 1)
`!rclast [number]` - Rewind to previous song(s) (default 1)
`!rcqueue` - Show current queue
`!rctop [number]` - Move specified song to top of queue (default: 1)
`!rcshuffle` - Shuffle the entire queue
`!rcvolume <0-100>` - Set volume (0-100%)
`!rcstop` - Stop playback and clear the queue
`!rchelp` - Show this help message

**📱 Interactive Control Panel Buttons:**
**Top Row:**
{EMOJIS['back']} - Previous track (rewind to last song)
{EMOJIS['play']} - Play/Pause toggle
{EMOJIS['next']} - Skip current song
{EMOJIS['shuffle']} - Shuffle queue
{EMOJIS['stop']} - Stop and disconnect

**Bottom Row:**
{EMOJIS['uparrow']} - Scroll up in song list
{EMOJIS['rotate']} - Reset view to current song
{EMOJIS['downarrow']} - Scroll down in song list
{EMOJIS['volumedown']} - Volume down (-10%)
{EMOJIS['volume']} - Volume up (+10%)

Caimanos Radio can read any type of links which direct to a page with a video/audio content in it"""
    COLOR = 0x2596be
