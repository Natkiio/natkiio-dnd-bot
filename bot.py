import discord
from discord import app_commands
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def roll_dice(dice_string):
    """
    Parse and roll dice notation like '2d6', '1d20+5', '3d8-2'
    Returns (result, breakdown)
    """
    # Parse the dice notation
    pattern = r'(\d+)d(\d+)([+-]\d+)?'
    match = re.match(pattern, dice_string.lower().replace(' ', ''))
    
    if not match:
        return None, "Invalid dice format. Use format like: 2d6, 1d20+5, 3d8-2"
    
    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    # Validate input
    if num_dice > 100:
        return None, "Maximum 100 dice per roll"
    if die_size > 1000:
        return None, "Maximum d1000"
    
    # Roll the dice
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    
    # Create breakdown string
    rolls_str = " + ".join(map(str, rolls))
    if modifier > 0:
        breakdown = f"{rolls_str} + {modifier} = **{total}**"
    elif modifier < 0:
        breakdown = f"{rolls_str} - {abs(modifier)} = **{total}**"
    else:
        breakdown = f"{rolls_str} = **{total}**"
    
    return total, breakdown

@tree.command(name="roll", description="Roll dice (e.g., 2d6, 1d20+5)")
async def roll(interaction: discord.Interaction, dice: str):
    """Roll dice using standard notation"""
    result, breakdown = roll_dice(dice)
    
    if result is None:
        await interaction.response.send_message(breakdown, ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"🎲 Rolling {dice}",
        description=breakdown,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="advantage", description="Roll with advantage (roll 2d20, take higher)")
async def advantage(interaction: discord.Interaction, modifier: int = 0):
    """Roll with advantage"""
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)
    result = max(roll1, roll2) + modifier
    
    embed = discord.Embed(
        title="🎲 Advantage Roll",
        description=f"Rolled: {roll1} and {roll2}\nTaking: **{max(roll1, roll2)}**\nModifier: {'+' if modifier >= 0 else ''}{modifier}\nTotal: **{result}**",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="disadvantage", description="Roll with disadvantage (roll 2d20, take lower)")
async def disadvantage(interaction: discord.Interaction, modifier: int = 0):
    """Roll with disadvantage"""
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)
    result = min(roll1, roll2) + modifier
    
    embed = discord.Embed(
        title="🎲 Disadvantage Roll",
        description=f"Rolled: {roll1} and {roll2}\nTaking: **{min(roll1, roll2)}**\nModifier: {'+' if modifier >= 0 else ''}{modifier}\nTotal: **{result}**",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="stats", description="Roll stats for a new character (4d6 drop lowest, 6 times)")
async def stats(interaction: discord.Interaction):
    """Roll character stats"""
    all_stats = []
    breakdown_lines = []
    
    for i in range(6):
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        stat = sum(rolls[:3])  # Take top 3
        all_stats.append(stat)
        breakdown_lines.append(f"**{stat}** ({', '.join(map(str, rolls[:3]))} ~~{rolls[3]}~~)")
    
    embed = discord.Embed(
        title="📊 Character Stats (4d6 drop lowest)",
        description="\n".join(breakdown_lines),
        color=discord.Color.gold()
    )
    embed.add_field(name="Total", value=f"{sum(all_stats)}", inline=False)
    embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} is now running!')
    print(f'Bot is in {len(client.guilds)} servers')

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables")
        print("Create a .env file with: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    client.run(TOKEN)
