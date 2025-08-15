import discord
from discord import app_commands
from discord.ext import commands
from constants import can_user_run

# Given a year role (eg. 2026), give everyone with that role the Alumni role
class YearToAlumni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="year_to_alumni",
        description="Give everyone in a specified year role the Alumni role"
    )
    async def year_to_alumni(self, interaction: discord.Interaction, year_role: discord.Role):
        await interaction.response.defer()

        roles_of_caller = {r.name for r in interaction.user.roles}
        if not can_user_run(roles_of_caller):
            await interaction.followup.send(content="You need to be an Exec to run this command")
            return

        alumni_role = discord.utils.get(interaction.guild.roles, name="Alumni")
        if not alumni_role:
            await interaction.followup.send("❌ Could not find a role named 'Alumni'")
            return

        members = year_role.members
        if not members:
            await interaction.followup.send(f"No members found with the role {year_role.name}")
            return

        updated_count = 0
        failed_count = 0

        for member in members:
            try:
                await member.add_roles(alumni_role)
                updated_count += 1
            except discord.Forbidden:
                failed_count += 1
            except Exception:
                failed_count += 1

        embed = discord.Embed(
            title="Year to Alumni Status",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="Summary",
            value=(
                f"Started with **{len(members)}** members in role `{year_role.name}`\n"
                f"✅ Alumni role added to **{updated_count}** members\n"
                f"❌ Failed for **{failed_count}** members"
            ),
            inline=False
        )

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(YearToAlumni(bot))
