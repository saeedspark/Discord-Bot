import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@bot.event
async def on_ready():
    message = await bot.get_channel(1187365733680820245).fetch_message(1200697535342325875)
    embed_message = discord.Embed(title= 'Get Start', color = discord.Color.blue())
    embed_message.add_field(name= f'<#1187360762625261609>', value= "> The rules channel in Discord is a public channel where the server's rules are written. These rules cover a variety of topics, such as appropriate behavior on the server, prohibited content, and how to handle violations.\n", inline= False)
    embed_message.add_field(name= f'<#1187365620279427072>', value= "> The welcome channel in Discord is a public channel that is used to welcome new users to the server.\n", inline= False)
    embed_message.add_field(name= f'<#1187365733680820245>', value= "> By reading the message in this channel, you can learn important information about the different channels on the server.\n", inline= False)
    embed_message.add_field(name= f'<#1187367548983980123>', value= "> By sending a message in this channel, you can talk to other server members about topics that you are interested in.\n", inline= False)
    embed_message.add_field(name= f'<#1199723080331837510>', value= "> By joining <@&1200042595108270142> role in the <#1187368520888107078> channel, you can be informed of the latest news and information about server events.\n", inline= False)
    embed_message.add_field(name= f'<#1187368520888107078>', value= "> You can learn about the types of roles available on the server and the responsibilities and privileges of each role. You can also choose some roles.\n", inline= False)
    embed_message.add_field(name= f'<#1200833022937796718>', value= "> The raffle channel is a great place to win free prizes. You can participate in raffles by collecting points.\n", inline= False)
    embed_message.add_field(name= f'<#1187363490130825226>', value= "> The Booboos channel is a public channel where you can download Booboos images and set them as your profile picture.\n", inline= False)
    embed_message.add_field(name= f'<#1187363775091839046>', value= "> The level channel is a public channel where user levels are displayed.\n", inline= False)
    embed_message.add_field(name= f'<#1199723718717485217>', value= "> By Using this channel, you can use bot commands.\n> !level : show your level\n> !leaderboard : show ranking leaderboard\n> /set twitter : set your twitter account\n> /set wallet : set your wallet\n", inline= False)
    embed_message.add_field(name= f'<#1187361934186664057>', value= "> The official links channel is a public channel where the official links of the server are published.\n", inline= False)
    embed_message.add_field(name= f'<#1200832991367266396>', value= "> You can get more information about engage by reading this channel.\n", inline= False)
    embed_message.add_field(name= f'<#1187362907411984445>', value= "> By having the <@&1200042527571578951> role in the <#1187368520888107078> channel, you can find out about our news in this channel.\n", inline= False)
    embed_message.add_field(name= f'<#1187368161494978580>', value= "> By having the <@&1200042241180311583> role in the <#1187368520888107078> channel, you can find out about our news in this channel.\n", inline= False)
    embed_message.add_field(name= f'<#1200833006814904371>', value= "> First, you must register your Twitter account in <#1199723718717485217> channel with the /set twitter command and register and support the tweets that are placed in this channel by clicking on the Twitter button and after the support, click on the green button to get your points.\n", inline= False)
    embed_message.add_field(name= f'<#1187364533350715514>', value= "> In this channel, users can create tickets to report problems, submit requests, or ask questions.\n", inline= False)
    await message.edit(embed=embed_message)


@bot.command()        
async def embed(ctx):
    embed_message = discord.Embed(title= 'Get Start', color = discord.Color.blue())
    embed_message.add_field(name= f'<#1187360762625261609>', value= "> The rules channel in Discord is a public channel where the server's rules are written. These rules cover a variety of topics, such as appropriate behavior on the server, prohibited content, and how to handle violations.\n", inline= False)
    embed_message.add_field(name= f'<#1187365620279427072>', value= "> The welcome channel in Discord is a public channel that is used to welcome new users to the server.\n", inline= False)
    embed_message.add_field(name= f'<#1187365733680820245>', value= "> By reading the message in this channel, you can learn important information about the different channels on the server.\n", inline= False)
    embed_message.add_field(name= f'<#1187367548983980123>', value= "> By sending a message in this channel, you can talk to other server members about topics that you are interested in.\n", inline= False)
    embed_message.add_field(name= f'<#1199723080331837510>', value= "> By joining <@&1200042595108270142> role in the <#1187368520888107078> channel, you can be informed of the latest news and information about server events.\n", inline= False)
    embed_message.add_field(name= f'<#1187368520888107078>', value= "> You can learn about the types of roles available on the server and the responsibilities and privileges of each role. You can also choose some roles.\n", inline= False)
    embed_message.add_field(name= f'<#1187363490130825226>', value= "> The Booboos channel is a public channel where you can download Booboos images and set them as your profile picture.\n", inline= False)
    embed_message.add_field(name= f'<#1187363775091839046>', value= "> The level channel is a public channel where user levels are displayed.\n", inline= False)
    embed_message.add_field(name= f'<#1199723718717485217>', value= "> By Using this channel, you can use bot commands.\n> !level : show your level\n> !leaderboard : show ranking leaderboard\n", inline= False)
    embed_message.add_field(name= f'<#1187361934186664057>', value= "> The official links channel is a public channel where the official links of the server are published.\n", inline= False)
    embed_message.add_field(name= f'<#1187362907411984445>', value= "> By having the <@&1200042527571578951> role in the <#1187368520888107078> channel, you can find out about our news in this channel.\n", inline= False)
    embed_message.add_field(name= f'<#1187368161494978580>', value= "> By having the <@&1200042241180311583> role in the <#1187368520888107078> channel, you can find out about our news in this channel.\n", inline= False)
    embed_message.add_field(name= f'<#1187364533350715514>', value= "> In this channel, users can create tickets to report problems, submit requests, or ask questions.\n", inline= False)

    await ctx.send(embed = embed_message)
bot.run('MTE4NzM1NzQ4MzAxOTI4NDU3Mw.GyUlut.rBFv9lTV1h8VmD1ywU3q3S62JWaeUiZiiOeIiw')