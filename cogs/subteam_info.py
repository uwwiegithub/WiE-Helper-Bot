import discord
from discord import app_commands
from discord.ext import commands
from constants import subteamChoiceOptions

# Displays all roles from ../constants.py with the names of the people who have the role
class SubteamInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subteam_info", description="Shows which members are in each subteam")
    async def subteam_info(self, interaction: discord.Interaction):
        visitedUsers = set()
        embed = discord.Embed(
            title="Director Role Info",
            description="Shows which members are in each Sub Team",
            color=discord.Color.purple()
        )

        for role in subteamChoiceOptions:
            listOfUsers = ""
            users = (discord.utils.get(interaction.guild.roles, name=role.value)).members
            for user in users:
                listOfUsers += f"@{user.name}"
                if user.nick:
                    listOfUsers += f" ({user.nick})\n"
                else:
                    listOfUsers += "\n"
                visitedUsers.add(user)

            embed.add_field(name=role.name, value=listOfUsers or "None")

        # handle directors without subteam role
        director_role = discord.utils.get(interaction.guild.roles, name="Director")
        listOfUsers = ""
        for user in director_role.members:
            if user not in visitedUsers:
                listOfUsers += f"@{user.name} ({user.nick})\n" if user.nick else f"@{user.name}\n"

        if listOfUsers:
            embed.add_field(name="People with Director role but no Sub Team role", value=listOfUsers)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SubteamInfo(bot))
