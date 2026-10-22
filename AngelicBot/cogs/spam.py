import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class SpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="spam", description="Spam a message infinitely.")
    @app_commands.describe(
        text="The word or message to spam",
        amount="How many times (No limit, but be careful)",
        delay="Seconds between messages (Default 0.01)"
    )
    async def spam(self, interaction: discord.Interaction, text: str, amount: int, delay: float = 0.01):
        
        await interaction.response.defer(ephemeral=True)
        count = 0

        for _ in range(amount):
            sent = False
            
            # 1. Try sending normally (if bot is in the server)
            try:
                await interaction.channel.send(text)
                sent = True
            except discord.Forbidden:
                pass # Bot is not in this server, move to fallback
            except discord.HTTPException as e:
                if e.status == 429: # Rate limited by Discord
                    await asyncio.sleep(e.retry_after) # Wait exactly as long as Discord says
                    try:
                        await interaction.channel.send(text)
                        sent = True
                    except: pass
            
            # 2. Fallback for User App (Bot not in server)
            if not sent:
                try:
                    await interaction.followup.send(text, ephemeral=False)
                    sent = True
                except discord.HTTPException as e:
                    if e.code == 40094: 
                        # Hard limit: Discord only allows 5 followups per interaction
                        await interaction.followup.send("⚠️ Discord limits User Apps to 5 messages. To spam unlimited, invite the bot to the server.", ephemeral=True)
                        break
                    elif e.status == 429: # Rate limited
                        await asyncio.sleep(e.retry_after)
                except Exception:
                    break

            if sent:
                count += 1
                
            # The actual delay between messages
            await asyncio.sleep(delay)

        # Final summary
        try:
            await interaction.followup.send(f"✅ Spam finished. Sent {count} messages.", ephemeral=True)
        except:
            pass

async def setup(bot):
    await bot.add_cog(SpamCog(bot))