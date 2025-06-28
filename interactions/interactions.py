import discord
import asyncio

async def _delete_after_delay(message, delay: int | None = 10):
    """Helper function to delete a message after a delay"""
    if not delay:
        return
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except discord.NotFound:
        pass

async def send_response(interaction: discord.Interaction, content: str, embed=None, delay: int | None = 10):
    if embed:
        asyncio.create_task(_delete_after_delay(await interaction.followup.send(content, embed=embed, ephemeral=True), delay))
    else:
        asyncio.create_task(_delete_after_delay(await interaction.followup.send(content, ephemeral=True), delay))

async def defer(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass