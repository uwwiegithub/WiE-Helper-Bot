import discord
from discord import app_commands
from discord.ext import commands
from constants import subteamChoiceOptions, can_user_run

# Unassigns a specific role from a user
class UnassignRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unassign_role", description="Remove a member from a subteam (removes director + subteam role)")
    @app_commands.choices(role=subteamChoiceOptions)
    async def unassign_role(self, interaction: discord.Interaction, user_to_remove_role: discord.Member, role: app_commands.Choice[str]):
        roles_of_caller = {r.name for r in interaction.user.roles}
        if not can_user_run(roles_of_caller):
            await interaction.response.send_message(content="You need to be a Director to run this command")
            return

        subteamRole = discord.utils.get(interaction.guild.roles, name=role.value)
        directorRole = discord.utils.get(interaction.guild.roles, name="Director")
        await user_to_remove_role.remove_roles(subteamRole, directorRole)

        embed = discord.Embed(
            title="Status",
            color=discord.Color.purple(),
            description=f"Removed from {user_to_remove_role.nick} ({user_to_remove_role.mention})"
        )
        embed.add_field(name="Roles Removed:", value=f"{role.value} \n Director")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UnassignRole(bot))
