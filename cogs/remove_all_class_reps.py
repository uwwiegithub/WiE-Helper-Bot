import discord
from discord import app_commands
from discord.ext import commands
from constants import can_user_run

class RemoveAllClassReps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="remove_all_class_reps",
        description="Remove WiE Class Rep role from everyone who has it"
    )
    async def remove_all_class_reps(self, interaction: discord.Interaction):
        await interaction.response.defer()
        roles_of_caller = {r.name for r in interaction.user.roles}

        if not can_user_run(roles_of_caller):
            await interaction.followup.send(content="You need to be a Director to run this command")
            return

        class_rep_role = discord.utils.get(interaction.guild.roles, name="WiE Class Rep")
        if not class_rep_role:
            await interaction.followup.send("❌ Could not find a role named 'WiE Class Rep'")
            return

        users = class_rep_role.members
        users_removed_count = 0
        users_not_removed_count = 0
        not_removed_users_message = ""

        for user in users:
            try:
                await user.remove_roles(class_rep_role)
                users_removed_count += 1
            except discord.Forbidden:
                not_removed_users_message += f"{user.name} ({user.nick}) Missing permissions\n"
                users_not_removed_count += 1
            except Exception as e:
                not_removed_users_message += f"{user.name} ({user.nick}) Error: {e}\n"
                users_not_removed_count += 1

        embed = discord.Embed(title="Remove All Class Reps Status", color=discord.Color.purple())
        embed.add_field(name=f"We Started With {len(users)} Class Reps", value="", inline=False)
        embed.add_field(name=f"Successfully removed role from {users_removed_count} members", value="\u200b", inline=False)
        embed.add_field(name=f"Failed to remove role from {users_not_removed_count} members", value=not_removed_users_message or "None", inline=False)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RemoveAllClassReps(bot))