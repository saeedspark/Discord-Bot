import discord
from discord.ext import commands
import discord.ui

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print('roles.py is ready')
    bot.add_view(Roles(bot))

class Roles(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Tweets", custom_id="Tweets", style=discord.ButtonStyle.blurple, emoji="🐦")
    async def tweets(self, interaction, button):
        tweets_role = 1199784968419819630
        user = interaction.user
        if tweets_role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(tweets_role))
            await interaction.response.send_message(f"<@&{tweets_role}> removed ❎" , ephemeral=True)
        
        else:
            await user.add_roles(user.guild.get_role(tweets_role))
            await interaction.response.send_message(f"<@&{tweets_role}> added ✅", ephemeral=True)
            
    @discord.ui.button(label="Events", custom_id="Events", style=discord.ButtonStyle.blurple, emoji="🎉")
    async def events(self, interaction, button):
        events_role = 1199785116290011350
        user = interaction.user
        if events_role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(events_role))
            await interaction.response.send_message(f"<@&{events_role}> removed ❎" , ephemeral=True)
        
        else:
            await user.add_roles(user.guild.get_role(events_role))
            await interaction.response.send_message(f"<@&{events_role}> added ✅", ephemeral=True)
            
    @discord.ui.button(label="Announcement", custom_id="Announcement", style=discord.ButtonStyle.blurple, emoji="📣")
    async def announcement(self, interaction, button):
        announcement_role = 1199785164436418752
        user = interaction.user
        if announcement_role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(announcement_role))
            await interaction.response.send_message(f"<@&{announcement_role}> removed ❎" , ephemeral=True)
        
        else:
            await user.add_roles(user.guild.get_role(announcement_role))
            await interaction.response.send_message(f"<@&{announcement_role}> added ✅", ephemeral=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def roles(ctx):
    embed = discord.Embed(title= "Roles", description="pick your roles" ,color = discord.Color.red())
    await ctx.send(embed=embed, view=Roles(bot))

bot.run('MTE5Mjg3ODE2NzU3MzE0MzU3Mg.GKAJHQ.CJIKTusjE6_n7VXDKevQfd2hYkhkcAWbTBCy9w')