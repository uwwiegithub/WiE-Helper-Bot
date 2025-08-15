import discord
from discord import app_commands
from discord.ext import commands
from constants import can_user_run

class AssignPastDirectors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="assign_past_directors", description="Gives everyone with the Director role the Past Director role")
    async def assign_past_directors(self, interaction: discord.Interaction):
        await interaction.response.defer()
        rolesOfCaller = {r.name for r in interaction.user.roles}

        if not can_user_run(rolesOfCaller):
            await interaction.followup.send(content="You need to be a Director to run this command")
            return

        director_role = discord.utils.get(interaction.guild.roles, name="Director")
        past_director_role = discord.utils.get(interaction.guild.roles, name="Past Director")

        users = director_role.members
        users_updated_count = 0
        users_not_updated_count = 0
        director_message = ""
        past_director_message = ""
        users_not_updated = ""

        for user in users:
            director_message += f"{user.name} ({user.nick})\n"

            try:
                await user.add_roles(past_director_role)
                past_director_message += f"{user.name} ({user.nick})\n"
                users_updated_count += 1
            except discord.Forbidden:
                users_not_updated += f"{user.name} ({user.nick}) Missing permissions\n"
                users_not_updated_count += 1
            except Exception as e:
                users_not_updated += f"{user.name} ({user.nick}) Error: {e}\n"
                users_not_updated_count += 1

        embed = discord.Embed(title="Status", color=discord.Color.purple())
        embed.add_field(name=f"We Started With {len(users)} Directors:", value=director_message)
        embed.add_field(name=f"And Assigned {users_updated_count} Of Them To Past Directors:", value=past_director_message)
        embed.add_field(name=f"{users_not_updated_count} Directors Were Not Updated:", value=users_not_updated)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AssignPastDirectors(bot))
