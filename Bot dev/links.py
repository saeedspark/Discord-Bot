import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')


@bot.command()        
async def embed(ctx):
    embed_message = discord.Embed(title= 'Official Links', color = discord.Color.blue())
    embed_message.add_field(name= 'Opensea', value= 'https://opensea.io/collection/booboos1001', inline= False)
    embed_message.add_field(name= 'Rarible', value= 'https://rarible.com/booboos1001', inline= False)
    embed_message.add_field(name= 'Twitter', value= 'https://twitter.com/booboos1001', inline= False)
    embed_message.add_field(name= 'Instagram', value= 'https://instagram.com/booboos1001', inline= False)
    embed_message.set_image(url= "https://drive.google.com/file/d/1xpifyIw_MAUmGgSWD_JozErYi73pc9Oo/view?usp=sharing")

    await ctx.send(embed = embed_message)
bot.run('MTE4NzM1NzQ4MzAxOTI4NDU3Mw.GyUlut.rBFv9lTV1h8VmD1ywU3q3S62JWaeUiZiiOeIiw')