import discord
import asyncio

async def _delete_after_delay(message, delay: int = 10):
    """Helper function to delete a message after a delay"""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except discord.NotFound:
        pass

async def send_response(interaction: discord.Interaction, content: str):
    asyncio.create_task(_delete_after_delay(await interaction.followup.send(content, ephemeral=True)))

async def defer(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass