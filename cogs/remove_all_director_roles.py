import discord
from discord import app_commands
from discord.ext import commands
from constants import can_user_run, directorship_options, other_options, exec_options  # import all lists

class RemoveDirectorsAndSubs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="remove_all_directors",
        description="Remove Director role & subroles from everyone with Director role (except execs, faculty & wie reps)"
    )
    async def remove_all_directors(self, interaction: discord.Interaction):
        await interaction.response.defer()
        roles_of_caller = {r.name for r in interaction.user.roles}

        if not can_user_run(roles_of_caller):
            await interaction.followup.send(content="You need to be a Director to run this command")
            return

        director_role = discord.utils.get(interaction.guild.roles, name="Director")
        if not director_role:
            await interaction.followup.send("❌ Could not find a role named 'Director'")
            return

        # Combine other_options and exec_options role names into a single set
        skip_role_names = {choice.value for choice in other_options} | {choice.value for choice in exec_options}

        # Filter directorship_options to exclude roles in skip_role_names
        subroles_to_remove = []
        for choice in directorship_options:
            if choice.value not in skip_role_names:
                role = discord.utils.get(interaction.guild.roles, name=choice.value)
                if role:
                    subroles_to_remove.append(role)

        users = director_role.members
        users_removed_count = 0
        users_not_removed_count = 0
        not_removed_users_message = ""

        for user in users:
            roles_to_remove = [director_role] + subroles_to_remove
            roles_to_remove = [r for r in roles_to_remove if r in user.roles]

            try:
                if roles_to_remove:
                    await user.remove_roles(*roles_to_remove)
                users_removed_count += 1
            except discord.Forbidden:
                not_removed_users_message += f"{user.name} ({user.nick}) Missing permissions\n"
                users_not_removed_count += 1
            except Exception as e:
                not_removed_users_message += f"{user.name} ({user.nick}) Error: {e}\n"
                users_not_removed_count += 1

        embed = discord.Embed(title="Remove All Directors Status", color=discord.Color.purple())
        embed.add_field(name=f"We Started With {len(users)} Directors", value="", inline=False)
        embed.add_field(name=f"Successfully removed roles from {users_removed_count} members", value="\u200b", inline=False)
        embed.add_field(name=f"Failed to remove roles from {users_not_removed_count} members", value=not_removed_users_message or "None", inline=False)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RemoveDirectorsAndSubs(bot))
