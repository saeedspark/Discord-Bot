import discord
from discord.ext import commands
import random
import aiosqlite
import asyncio
import os
import discord
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font, Canvas
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from src.log import setup_logger
from src.db_function.init_db import init_db
from configs.load_configs import configs
import discord.ui

log = setup_logger(__name__)

load_dotenv()

bot = commands.Bot(command_prefix= '!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready')
    bot.add_view(Roles(bot))
    setattr(bot, "db", await aiosqlite.connect("database\leveling.db"))
    await asyncio.sleep(3)
    async with bot.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS ranking (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER, next_level_xp INTEGER, rank INTEGER)")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=configs['activity_name']))
    if not(os.path.isfile(f"{os.getenv('DATA_PATH')}tracked_accounts.db")): init_db()
    bot.tree.on_error = on_tree_error
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    log.info(f'{bot.user} is online')
    slash = await bot.tree.sync()
    log.info(f'synced {len(slash)} slash commands')
            


                 
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} done.')
    
    
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')
    
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')
    
@bot.command()
@commands.is_owner()
async def download_log(ctx : commands.context.Context):
    message = await ctx.send(file=discord.File('console.log'))
    await message.delete(delay=15)
    
@bot.command()
@commands.is_owner()
async def download_data(ctx : commands.context.Context):
    message = await ctx.send(file=discord.File(f"{os.getenv('DATA_PATH')}tracked_accounts.db"))
    await message.delete(delay=15)
    
@bot.command()
@commands.is_owner()
async def upload_data(ctx : commands.context.Context):
    raw = await [attachment for attachment in ctx.message.attachments if attachment.filename[-3:] == '.db'][0].read()
    with open(f"{os.getenv('DATA_PATH')}tracked_accounts.db", 'wb') as wbf:
        wbf.write(raw)
    message = await ctx.send('successfully uploaded data')
    await message.delete(delay=5)
    
@bot.event
async def on_tree_error(itn : discord.Interaction, error : app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.CheckFailure):
        await itn.response.send_message('Permission denied.', ephemeral=True)
    else:
        await itn.response.send_message(error, ephemeral=True)
    log.warning(f'an error occurred but was handled by the tree error handler, error message : {error}')
    
@bot.event
async def on_command_error(ctx : commands.context.Context, error : commands.errors.CommandError):
    if isinstance(error, commands.errors.CommandNotFound): return
    else: await ctx.send(error)
    log.warning(f'an error occurred but was handled by the command error handler, error message : {error}')
            







#-----Level System-----#

@bot.event
async def on_message(message):
    chat_channel = bot.get_channel(1187367548983980123)
    commands_channel = bot.get_channel(1199723718717485217)
    level_channel = bot.get_channel(1187363775091839046)
    if message.author.bot:
        return
    if message.content.startswith("!") == False and message.channel == commands_channel: 
        await message.delete()
        
    author = message.author
    guild = message.guild
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM ranking WHERE user = ? AND guild = ?", (author.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT rank FROM ranking WHERE user = ? AND guild = ?", (author.id, guild.id,))
        rank = await cursor.fetchone()
        await cursor.execute("SELECT level FROM ranking WHERE user = ? AND guild = ?", (author.id, guild.id,))
        level = await cursor.fetchone()
        await cursor.execute("SELECT next_level_xp FROM ranking WHERE user = ? AND guild = ?", (author.id, guild.id,))
        next_level_xp = await cursor.fetchone()

        if not xp or not level or not rank:
            await cursor.execute("INSERT INTO ranking (level, xp, user, guild, next_level_xp, rank) VALUES (?, ?, ?, ?, ?, ?)", (0, 0, author.id, guild.id, 100, 0))

        
        await cursor.execute("SELECT user, rank FROM ranking WHERE guild = ? ORDER BY level DESC, xp DESC", (guild.id,))
        data = await cursor.fetchall()
        if data:
            count = 0
            for table in data:
                count += 1
                user = guild.get_member(table[0])
                rank = count
                await cursor.execute("SELECT rank FROM ranking WHERE user = ? AND guild = ? ORDER BY level DESC, level DESC", (user.id, guild.id,))
                rank = await cursor.fetchone()
        
        try:
            xp = xp[0]
            level = level[0]
            next_level_xp = next_level_xp[0]
            rank = rank[0]
        except TypeError:
            xp = 0
            level = 0
            next_level_xp = 100
            rank = 0
        
        if message.channel == chat_channel:
            xp += random.randint(2, 4)
            await cursor.execute("SELECT user, rank FROM ranking WHERE guild = ? ORDER BY level DESC, xp DESC", (guild.id,))    
            data = await cursor.fetchall()
        if data:
            count = 0
            for table in data:
                count += 1
                user = guild.get_member(table[0])
                rank = count
                await cursor.execute("UPDATE ranking SET rank = ? WHERE user = ? AND guild = ?", (rank, user.id, guild.id,))                
        await cursor.execute("UPDATE ranking SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))

        if xp >= next_level_xp:
            level += 1
            next_level_xp = round(next_level_xp * 1.25)
            await cursor.execute("UPDATE ranking SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
            await cursor.execute("UPDATE ranking SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
            await cursor.execute("UPDATE ranking SET next_level_xp = ? WHERE user = ? AND guild = ?", (next_level_xp, author.id, guild.id,))
            await cursor.execute("SELECT user, rank FROM ranking WHERE guild = ? ORDER BY level DESC, xp DESC", (guild.id,))
            data = await cursor.fetchall()
            if data:
                count = 0
                for table in data:
                    count += 1
                    user = guild.get_member(table[0])
                    rank = count
                    await cursor.execute("UPDATE ranking SET rank = ? WHERE user = ? AND guild = ?", (rank, user.id, guild.id,))

            level_up_message = discord.Embed(title= f'{author.name} has leveled up', description=f"Congratulations {author.mention}. you have leveled up to level **{level}**!", color = discord.Color.yellow())

            await level_channel.send(embed = level_up_message)
            if level == 5:
                LVL5_role = discord.utils.get(author.guild.roles, name="LVL 5")
                await author.add_roles(LVL5_role)
                
            if level == 10:
                LVL10_role = discord.utils.get(author.guild.roles, name="LVL 10")
                await author.add_roles(LVL10_role)
                
            if level == 15:
                LVL15_role = discord.utils.get(author.guild.roles, name="LVL 15")
                await author.add_roles(LVL15_role)
                
            if level == 20:
                LVL20_role = discord.utils.get(author.guild.roles, name="LVL 20")
                await author.add_roles(LVL20_role)
                
            if level == 25:
                LVL25_role = discord.utils.get(author.guild.roles, name="LVL 25")
                await author.add_roles(LVL25_role)
                
            if level == 25:
                LVL25_role = discord.utils.get(author.guild.roles, name="LVL 25")
                await author.add_roles(LVL25_role)
                
            if level == 30:
                LVL30_role = discord.utils.get(author.guild.roles, name="LVL 30")
                await author.add_roles(LVL30_role)
                
            if level == 35:
                LVL35_role = discord.utils.get(author.guild.roles, name="LVL 35")
                await author.add_roles(LVL35_role)
                
            if level == 40:
                LVL40_role = discord.utils.get(author.guild.roles, name="LVL 40")
                await author.add_roles(LVL40_role)
                
            if level == 45:
                LVL45_role = discord.utils.get(author.guild.roles, name="LVL 45")
                await author.add_roles(LVL45_role)
                
            if level == 50:
                LVL50_role = discord.utils.get(author.guild.roles, name="LVL 50")
                await author.add_roles(LVL50_role)
                
            if level == 55:
                LVL55_role = discord.utils.get(author.guild.roles, name="LVL 55")
                await author.add_roles(LVL55_role)
                
            if level == 60:
                LVL60_role = discord.utils.get(author.guild.roles, name="LVL 60")
                await author.add_roles(LVL60_role)
                
            if level == 65:
                LVL65_role = discord.utils.get(author.guild.roles, name="LVL 65")
                await author.add_roles(LVL65_role)
                
            if level == 70:
                LVL70_role = discord.utils.get(author.guild.roles, name="LVL 70")
                await author.add_roles(LVL70_role)
                
            if level == 75:
                LVL75_role = discord.utils.get(author.guild.roles, name="LVL 75")
                await author.add_roles(LVL75_role)
                
            if level == 80:
                LVL80_role = discord.utils.get(author.guild.roles, name="LVL 80")
                await author.add_roles(LVL80_role)
                
            if level == 85:
                LVL85_role = discord.utils.get(author.guild.roles, name="LVL 85")
                await author.add_roles(LVL85_role)
                
            if level == 90:
                LVL90_role = discord.utils.get(author.guild.roles, name="LVL 90")
                await author.add_roles(LVL90_role)
                
            if level == 95:
                LVL95_role = discord.utils.get(author.guild.roles, name="LVL 95")
                await author.add_roles(LVL95_role)
                
            if level == 100:
                LVL100_role = discord.utils.get(author.guild.roles, name="LVL 100")
                await author.add_roles(LVL100_role)
                
    await bot.db.commit()
    await bot.process_commands(message)
    
@bot.command(aliases=["lvl", "rank"])       
async def level(ctx, member: discord.Member = None):
    commands_channel = bot.get_channel(1199723718717485217)
    if member is None:
        member = ctx.author
    if ctx.message.channel != commands_channel:
        return
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT level FROM ranking WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        level = await cursor.fetchone()
        await cursor.execute("SELECT xp FROM ranking WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT next_level_xp FROM ranking WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        next_level_xp = await cursor.fetchone()
        await cursor.execute("SELECT user, rank FROM ranking WHERE guild = ? ORDER BY level DESC, xp DESC", (ctx.guild.id,))    
        data = await cursor.fetchall()
        if data:
            count = 0
            for table in data:
                count += 1
                user = ctx.guild.get_member(table[0])
                rank = count
                await cursor.execute("UPDATE ranking SET rank = ? WHERE user = ? AND guild = ?", (rank, user.id, ctx.guild.id,))
        await cursor.execute("SELECT rank FROM ranking WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        rank = await cursor.fetchone()

    if not level or not xp or not next_level_xp or not rank:
        await cursor.execute("INSERT INTO ranking VALUES (?, ?, ?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id, next_level_xp, rank))
        await bot.db.commit()

    try:
        xp = xp[0]
        level = level[0]
        next_level_xp = next_level_xp[0]
        rank = rank[0]
    except TypeError:
        xp = 0
        level = 0
        next_level_xp = 100
        rank = 0
    percent = (xp / next_level_xp) * 100
    
    desplay_xp = f'{xp}'
    desplay_next_level_xp = f'{next_level_xp}'
    desplay_rank = f'{rank}'
    if xp >= 1000:
        desplay_xp = f'{round(xp/1000, 1)}k'
    if next_level_xp >= 1000:
        desplay_next_level_xp = f'{round(next_level_xp/1000, 1)}k'
    if rank >= 1000:
        desplay_xp = f'{round(rank/1000, 1)}k'
        
    user_data = {
        "name": f"{member.name}",
        "xp": desplay_xp,
        "level": level,
        "next_level_xp": desplay_next_level_xp,
        "percentage": percent,
        "rank": desplay_rank,
    }


    if member.avatar:
        profile_picture = await load_image_async(str(member.avatar.url))

    else:
        profile_picture = await load_image_async("https://black-bitter-whitefish-451.mypinata.cloud/ipfs/Qmb2wVZP6VEja3rrWHWKmwk2oUrjkuLpm2fJofJV78RfYm?_gl=1*1r0r3yf*_ga*MTMwMjkzMTQ4MS4xNzAyMTkxNzE1*_ga_5RMPXG14TE*MTcwMjE5MTcxNC4xLjEuMTcwMjE5MTg1MS42MC4wLjA.")

    # background = Editor(Canvas((900, 300), color="#141414"))
    # profile = Editor(profile_picture).resize((150, 150)).circle_image()

    # poppins = Font.poppins(size=40)
    # poppins_small = Font.poppins(size=30)

    # card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

    # background.polygon(card_right_shape, color="#FFFFFF")
    # background.paste(profile, (30, 30))
    
    
    # background.rectangle((30, 220), width=650, height=40, color="#FFFFFF", radius=20)
    # background.bar((30.5, 220), max_width=650, height=40, percentage=min(100, user_data["percentage"]), color="#0080ff", radius=20,)
    # background.text((200, 40), user_data["name"], font=poppins, color="#FFFFFF")

    # background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
    # background.text(
    #     (200, 130),
    #     f"Level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}",
    #     font = poppins_small,
    #     color = "#FFFFFF",
    # )


    background = Editor(Canvas((934, 282), "#23272a"))
    profile = Editor(profile_picture).resize((190, 190)).circle_image()

    # For profile to use users profile picture load it from url using the load_image/load_image_async function
    # profile_image = load_image(str(ctx.author.avatar_url))
    # profile = Editor(profile_image).resize((150, 150)).circle_image()


    poppins = Font.poppins(size=30)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))
    # background.ellipse((42, 42), width=206, height=206, outline="#0080ff", stroke_width=10)
    background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=user_data["percentage"],
        fill="#0080ff",
        radius=20,
    )
    background.text((270, 120), user_data["name"], font=poppins, color="#FFFFFF")
    background.text(
        (870, 125),
        f"{user_data['xp']} / {user_data['next_level_xp']}",
        font=poppins,
        color="#FFFFFF",
        align="right",
    )

    # rank_level_texts = [
    #     Text("Rank ", color="#00fa81", font=poppins),
    #     Text(f"{user_data['rank']}", color="#1EAAFF", font=poppins),
    #     Text("   Level ", color="#00fa81", font=poppins),
    #     Text(f"{user_data['level']}", color="#1EAAFF", font=poppins),
    # ]


    background.text((490, 30), "Rank ", color="#0080ff", font=poppins, align="right")
    # if rank != 0:
    background.text((530, 30), f"{user_data['rank']}", color="#FFFFFF", font=poppins, align="right")
    # else:
    #     background.text((580, 30), f"{user_data['rank']}", color="#FFFFFF", font=poppins, align="right")
    background.text((840, 30), "   Level ", color="#0080ff", font=poppins, align="right")
    background.text((880, 30), f"{user_data['level']}", color="#FFFFFF", font=poppins, align="right")





    file = discord.File(fp=background.image_bytes, filename="levelcard.png")
    await ctx.send(file=file)
    
    
@bot.command(aliases=["lb", "lbr"])
async def leaderboard(ctx):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT level, xp, user FROM ranking WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10", (ctx.guild.id,))
        ranks = await cursor.fetchall()
        if ranks:
            embed_leaderboard = discord.Embed(title=f"Leveling Leaderboard", color=discord.Color.blue())
            count_rank = 0
            for table in ranks:
                count_rank += 1
                user = ctx.guild.get_member(table[2])
                embed_leaderboard.add_field(name=f"{count_rank}. {user.name}", value=f"Level - **{table[0]}** | XP - **{table[1]}**", inline=False)
            return await ctx.send(embed=embed_leaderboard)
        return await ctx.send("No one has any xp yet.")
#-----Level System-----#




#-----Roles System-----#
tweets_role = 1200042241180311583
events_role = 1200042595108270142
announcement_role = 1200042527571578951
class Roles(discord.ui.View):

    def __init__(self, client):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Tweets", custom_id="Tweets", style=discord.ButtonStyle.blurple, emoji="🐦")
    async def tweets(self, interaction, button):
        user = interaction.user
        if tweets_role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(tweets_role))
            await interaction.response.send_message(f"<@&{tweets_role}> removed ❎" , ephemeral=True)
        
        else:
            await user.add_roles(user.guild.get_role(tweets_role))
            await interaction.response.send_message(f"<@&{tweets_role}> added ✅", ephemeral=True)
            
    @discord.ui.button(label="Events", custom_id="Events", style=discord.ButtonStyle.blurple, emoji="🎉")
    async def events(self, interaction, button):
        user = interaction.user
        if events_role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(events_role))
            await interaction.response.send_message(f"<@&{events_role}> removed ❎" , ephemeral=True)
        
        else:
            await user.add_roles(user.guild.get_role(events_role))
            await interaction.response.send_message(f"<@&{events_role}> added ✅", ephemeral=True)
            
    @discord.ui.button(label="Announcement", custom_id="Announcement", style=discord.ButtonStyle.blurple, emoji="📣")
    async def announcement(self, interaction, button):
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
        embed = discord.Embed(title= "Roles", description= f"<@&{tweets_role}> : With this role, you will receive tweet notifications.\n\n<@&{events_role}> : With this role, you receive event notifications.\n\n<@&{announcement_role}> : With this role, you receive announcements notifications.", color = discord.Color.red())
        await ctx.send(embed=embed, view=Roles(bot))

async def main():
    async with bot:
        await bot.start('MTE4NzM1NzQ4MzAxOTI4NDU3Mw.GyUlut.rBFv9lTV1h8VmD1ywU3q3S62JWaeUiZiiOeIiw')
        
if __name__ == '__main__':
    asyncio.run(main())