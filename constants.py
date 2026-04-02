from discord import app_commands

directorship_options = [
    app_commands.Choice(name="sponsorship", value="sponsorship director"),
    app_commands.Choice(name="discord", value="discord director"),
    app_commands.Choice(name="socials", value="socials director"),
    app_commands.Choice(name="events", value="events director"),
    app_commands.Choice(name="promotions/liaison", value="promotions/liaison director"),
    app_commands.Choice(name="mentorship", value="mentorship director"),
    app_commands.Choice(name="graphics", value="graphics director"),
    app_commands.Choice(name="editorial", value="editorial director"),
    app_commands.Choice(name="merch design", value="merch design director"),
    app_commands.Choice(name="hackathon", value="hackathon director"),
]

exec_options = [
    app_commands.Choice(name="pres / vp term A", value="VP - Term A"),
    app_commands.Choice(name="pres / vp term B", value="VP - Term B"),
]

other_options = [
    app_commands.Choice(name="wie class rep", value="WiE Class Rep"),
    app_commands.Choice(name="wie coordinator", value="wie coordinator"),
    app_commands.Choice(name="wie co-op", value="wie co-op"),
]

# All committee role options
subteamChoiceOptions = exec_options + directorship_options + other_options

def can_user_run(rolesOfCaller):
    allowed_roles = ["VP - Term A", "VP - Term B", "WiE Admin", "Admin"]
    return any(role in rolesOfCaller for role in allowed_roles)
