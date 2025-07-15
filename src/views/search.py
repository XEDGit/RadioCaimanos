import discord


async def make_search_view(player, interaction, search_result):
    entries = search_result['entries'][:10]  # Limit to 10 for dropdown

    # Create embed
    embed = discord.Embed(
        title=f"Found {len(entries)} results:",
        description='',
        color=0x00ff00
    )

    # Create dropdown options
    options = []
    for i, entry in enumerate(entries):
        duration = entry.get('duration', 0)
        duration_str = f"{duration//60}:{duration%60:02f}" if duration else "Unknown"

        options.append(discord.SelectOption(
            label=entry['title'][:100],
            description=f"Duration: {duration_str}",
            value=str(i),
            emoji="🎵"
        ))

    class SearchView(discord.ui.View):
        def __init__(self, player, entries):
            super().__init__(timeout=60.0)
            self.player = player
            self.entries = entries
            self.selected_url: str | None = None

        @discord.ui.select(placeholder="Choose a song...", options=options)
        async def select_song(self, interaction: discord.Interaction, select: discord.ui.Select):

            choice = int(select.values[0])
            self.selected_url = self.entries[choice]['url']

            embed = discord.Embed(
                title="✅ Song Selected",
                description=f"Selected: **{self.entries[choice]['title']}**",
                color=0x00ff00
            )

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

    view = SearchView(player, entries)
    msg = await interaction.followup.send(embed=embed, view=view)

    # Wait for selection
    await view.wait()
    await msg.delete()
    return view.selected_url
