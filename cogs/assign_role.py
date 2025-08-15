import discord
from discord import app_commands
from discord.ext import commands
from constants import subteamChoiceOptions, can_user_run

# Assisns a specific role to a given user
class AssignRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="assign_role", description="Add a new member to a subteam (adds director + subteam role)")
    @app_commands.choices(role=subteamChoiceOptions)
    async def assign_role(self, interaction: discord.Interaction, user_who_needs_role: discord.Member, role: app_commands.Choice[str]):
        roles_of_caller = {r.name for r in interaction.user.roles}
        if not can_user_run(roles_of_caller):
            await interaction.response.send_message(content="You need to be a Director to run this command")
            return

        subteamRole = discord.utils.get(interaction.guild.roles, name=role.value)
        directorRole = discord.utils.get(interaction.guild.roles, name="Director")
        await user_who_needs_role.add_roles(subteamRole, directorRole)

        embed = discord.Embed(title="Status", color=discord.Color.purple(),
                              description=f"Added to {user_who_needs_role.nick} ({user_who_needs_role.mention})")
        embed.add_field(name="Roles Added:", value=f"{role.value} \n Director")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AssignRole(bot))
