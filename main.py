import os
import discord
from discord.ext import commands
import discord.ext
from discord import app_commands

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
my_secret = os.environ['token']

@client.event
async def on_ready():
  print("bot is now ready to use")

  # need to sync all commands
  await client.tree.sync()
  print("slash commands are now synced")


#########################
# constants
#########################
subteamChoiceOptions = [
  app_commands.Choice(name="pres / vp", value="VP - Term A"),
  app_commands.Choice(name="sponsorship", value="sponsorship director"),
  app_commands.Choice(name="discord", value="discord director"),
  app_commands.Choice(name="socials", value="socials director"),
  app_commands.Choice(name="events", value="events director"),
  app_commands.Choice(name="promotions/liaison", value="promotions/liaison director"),
  app_commands.Choice(name="mentorship", value="mentorship director"),
  app_commands.Choice(name="graphics", value="graphics director"),
  app_commands.Choice(name="volunteer", value="volunteer director"),
  app_commands.Choice(name="merch design", value="merch design director"),
  app_commands.Choice(name="wie coordinator", value="wie coordinator"),
  app_commands.Choice(name="wie co-op", value="wie co-op"),
]


#########################
# View sub team members
#########################
@client.tree.command(name="subteam_info", description="Shows which members are in each subteam")
async def subteamInfo(interaction): 
  visitedUsers = set()

  embed = discord.Embed(title="Director Role Info", 
                  description="Shows which members are in each Sub Team", 
                  color=discord.Color.purple())

  for role in subteamChoiceOptions:
    listOfUsers = f""
    users = (discord.utils.get(interaction.guild.roles, name=role.value)).members
    for user in users:
      listOfUsers += f"@{user.name}" 
      if user.nick:
        listOfUsers += f" ({(user.nick)}) \n" 
      else:
        listOfUsers += " \n" 
      visitedUsers.add(user)
    
    embed.add_field(name=role.name, value=listOfUsers)

    # spacing
    if role.name == "discord" or role.name == "podcast" or role.name == "advocacy":
      embed.add_field(name=" ", value=" ")
      embed.add_field(name=" ", value=" ")
      embed.add_field(name=" ", value=" ")

  # some users may have a director role but not a subteam role
  usersWithDirectorRole = (discord.utils.get(interaction.guild.roles, name="Director")).members
  listOfUsers = f""
  for user in usersWithDirectorRole:
    if user not in visitedUsers:
      listOfUsers += f"@{user.name}" 
      if user.nick:
        listOfUsers += f" ({(user.nick)}) \n" 
      else:
        listOfUsers += " \n" 
  
  if listOfUsers != "":
    # embed.add_field(name=" ", value=" ")
    # embed.add_field(name=" ", value=" ")
    embed.add_field(name="People with Director role but no Sub Team role", value=listOfUsers)
  
  await interaction.response.send_message(embed=embed)


#########################
# Add new members to roles
#########################
@client.tree.command(name="assign_role", description="add a new member to a subteam - will add director AND subteam role")
@app_commands.choices(role=subteamChoiceOptions)
async def addRole(interaction, user_who_needs_role: discord.Member, role:app_commands.Choice[str]):
  userWhoCalled = interaction.user
  rolesOfCaller = set()
  for r in userWhoCalled.roles:
    rolesOfCaller.add(r.name)

  if "Director" not in rolesOfCaller:
    await interaction.response.send_message(content="You need to be a Director to run this command")
    return
  
  # now add the role
  subteamRole = discord.utils.get(interaction.guild.roles, name=role.value)
  directorRole = discord.utils.get(interaction.guild.roles, name="Director")
  await user_who_needs_role.add_roles(subteamRole, directorRole)

  # send update to the user
  embed = discord.Embed(title="Status", color=discord.Color.purple(), 
                        description=f"added to {user_who_needs_role.nick} ({user_who_needs_role.mention})")
  embed.add_field(name="Roles Added:", value=f"{role.value} \n Director")
  await interaction.response.send_message(embed=embed)

  
#########################
# removes director roles
#########################
@client.tree.command(name="unassign_role", description="remove a member to a subteam")
@app_commands.choices(role=subteamChoiceOptions)
async def removeRole(interaction, user_to_remove_role: discord.Member, role:app_commands.Choice[str]):
  userWhoCalled = interaction.user
  rolesOfCaller = set()
  for r in userWhoCalled.roles:
    rolesOfCaller.add(r.name)

  if "Director" not in rolesOfCaller:
    await interaction.response.send_message(content="You need to be a Director to run this command")
    return
  
  # now remove the roles
  subteamRole = discord.utils.get(interaction.guild.roles, name=role.value)
  directorRole = discord.utils.get(interaction.guild.roles, name="Director")
  await user_to_remove_role.remove_roles(subteamRole, directorRole)

  # send update to the user
  embed = discord.Embed(title="Status", color=discord.Color.purple(), 
                        description=f"removed from {user_to_remove_role.nick} ({user_to_remove_role.mention})")
  embed.add_field(name="Roles Removed:", value=f"{role.value} \n Director")
  await interaction.response.send_message(embed=embed)

  
#########################
# run bot
#########################
client.run(my_secret)
