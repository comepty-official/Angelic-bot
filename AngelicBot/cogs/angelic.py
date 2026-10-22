import discord
from discord.ext import commands
from discord import app_commands

class AngelicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- 1. ANONYMOUS COMMAND ---
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="anonymous", description="Send an anonymous message.")
    @app_commands.describe(message="The message to send")
    async def anonymous(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        try:
            await interaction.delete_original_response()
        except Exception:
            pass

        # Try Webhook (Requires bot to be in server)
        if interaction.guild is not None:
            try:
                webhook = await interaction.channel.create_webhook(name="Angelic")
                await webhook.send(
                    content=message,
                    username="Anonymous",
                    avatar_url="https://i.imgur.com/8T6yXqB.png"
                )
                await webhook.delete()
                return 
            except discord.Forbidden:
                pass # Fallback
            
        # Fallback for DMs or if bot is not in server
        try:
            await interaction.followup.send(content=message, ephemeral=False)
        except Exception as e:
            print(f"Fallback Error: {e}")

    # --- 2. CLEAR COMMAND ---
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="clear", description="Delete a number of messages.")
    @app_commands.describe(amount="Number of messages to delete")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount > 100:
            return await interaction.response.send_message("❌ Max limit is 100.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"🗑️ Deleted {len(deleted)} messages.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I don't have `Manage Messages` permission here.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AngelicCog(bot))