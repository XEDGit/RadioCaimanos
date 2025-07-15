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

    # Streaming settings
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

    FFMPEG_OPTIONS = {
        'before_options': (
            '-reconnect 1 '
            '-reconnect_streamed 1 '
            '-reconnect_delay_max 5 '
            '-multiple_requests 1 '
            '-fflags +discardcorrupt '
            '-analyzeduration 0 '
            '-probesize 32 '
            '-thread_queue_size 1024 '
            '-loglevel quiet '
            '-re '
            '-avoid_negative_ts make_zero '
            '-copyts '
            '-start_at_zero'
        ),
        'options': (
            '-vn '
            '-bufsize 512k '
            '-maxrate 512k '
            '-threads 4 '
            '-ac 2 '
            '-ar 48000 '
            '-f s16le '
            '-filter:a "aresample=async=1" '
            '-af "asetrate=48000,aresample=48000" '
            '-shortest '
            '-vsync 0'
        ),
    }

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

    HELP_MESSAGE = f"""**🎶 Basic Playback Commands:**
• `/play <url/search>` - Add song or playlist to queue
• `/playnext <url/search>` - Add song to play next in queue
• `/pause` - Pause current song
• `/resume` - Resume paused song
• `/skip [number]` - Skip current song or multiple songs (default: 1)
• `/rewind [number]` - Go back to previous song(s) (default: 1)
• `/stop` - Stop playback and disconnect from voice channel

**🎛️ Interactive Control Panel:**
The bot displays an interactive control panel with clickable buttons:

**Music Controls:**
{EMOJIS['back']} **Previous** - Go back to previous song
{EMOJIS['play']}**/**{EMOJIS['pause']} **Play/Pause** - Toggle playback
{EMOJIS['next']} **Skip** - Skip to next song
{EMOJIS['shuffle']} **Shuffle** - Randomize queue order
{EMOJIS['stop']} **Stop** - Stop and disconnect

**Playlist Navigation:**
{EMOJIS['uparrow']} **Scroll Up** - View past songs in playlist
{EMOJIS['rotate']} **Current Song** - Jump back to currently playing song
{EMOJIS['downarrow']} **Scroll Down** - View later songs in playlist

**Volume Controls:**
{EMOJIS['volumedown']} **Volume Down** - Decrease volume by 10%
{EMOJIS['volume']} **Volume Up** - Increase volume by 10%

**Extras:**
📋 **Send me this playlist**: Send the current playlist to your direct messages
{EMOJIS['minus']}**/**{EMOJIS['plus']} **Minimize/Maximize** - Resize the control panel

**📺 Supported Sources:**
✅ YouTube videos and playlists
✅ Direct audio/video file links
✅ Search terms (automatically searches YouTube)
✅ Most websites with embedded audio/video content"""
    COLOR = 0x2596be
