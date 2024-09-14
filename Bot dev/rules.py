import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@bot.event
async def on_ready():
    # Edit a message
    message = await bot.get_channel(1187360762625261609).fetch_message(1192423758149996674)

    # ویرایش پیام
    await message.edit(content="""
    # Rules
                   
**1. Be respectful and inclusive:**
> • This means treating everyone with kindness and respect, regardless of their race, religion, gender, sexual orientation, or any other personal characteristic. 

**2. No hate speech or discrimination:**
> • This includes any language or behavior that is intended to incite hatred or discrimination against any group of people. 

**3. No spam or self-promotion:**
> • This includes sending unwanted messages or links, or promoting your own content or products without permission. 

**4. No harassment or bullying:**
> • This includes any behavior that is intended to intimidate or upset another person. 

**5. No illegal or harmful content:**
> • This includes any content that is illegal, harmful, or offensive.

**6. Official Language:**
> • All members are required to speak English in all channels on this server.

|| @everyone ||"""
)

@bot.command()        
async def rules(ctx):
    # embed_message = discord.Embed(title= 'Rules', color = discord.Color.red())

    # embed_message.add_field(name= '1. Be respectful and inclusive:', value= '> • This means treating everyone with kindness and respect, regardless of their race, religion, gender, sexual orientation, or any other personal characteristic.\n', inline= False)
    # embed_message.add_field(name= '', value='', inline= False)

    # embed_message.add_field(name= '2. No hate speech   hujkhjkjkyuk discrimination:', value= '> • This includes any language or behavior that is intended to incite hatred or discrimination against any group of people.\n', inline= False)
    # embed_message.add_field(name= '', value='', inline= False)

    # embed_message.add_field(name= '3. No spam or self-promotion:', value= '> • This includes sending unwanted messages or links, or promoting your own content or products without permission.\n', inline= False)
    # embed_message.add_field(name= '', value='', inline= False)

    # embed_message.add_field(name= '4. No harassment or bullying:', value= '> • This includes any behavior that is intended to intimidate or upset another person.\n', inline= False)
    # embed_message.add_field(name= '', value='', inline= False)

    # embed_message.add_field(name= '5. No illegal or harmful content:', value= '> • This includes any content that is illegal, harmful, or offensive.', inline= False)
    # embed_message.set_image(url= "https://black-bitter-whitefish-451.mypinata.cloud/ipfs/QmNPaRuPJnFkms3tz2mt2X31Pnj2McWFwc8xDRF6CngYz6?_gl=1*1xpjkye*_ga*MTMwMjkzMTQ4MS4xNzAyMTkxNzE1*_ga_5RMPXG14TE*MTcwNDM2MTA1NC4zLjEuMTcwNDM2MTA4NS4yOS4wLjA.")

    # await ctx.send(embed= embed_message)
    await ctx.send(f"""
    # Rules
                   
**1. Be respectful and inclusive:**
> • This means treating everyone with kindness and respect, regardless of their race, religion, gender, sexual orientation, or any other personal characteristic. 

**2. No hate speech or discrimination:**
> • This includes any language or behavior that is intended to incite hatred or discrimination against any group of people. 

**3. No spam or self-promotion:**
> • This includes sending unwanted messages or links, or promoting your own content or products without permission. 

**4. No harassment or bullying:**
> • This includes any behavior that is intended to intimidate or upset another person. 

**5. No illegal or harmful content:**
> • This includes any content that is illegal, harmful, or offensive.

**5. Official Language:**
> • All members are required to speak English in all channels on this server.

|| @everyone ||
""")

bot.run('MTE4NzM1NzQ4MzAxOTI4NDU3Mw.GyUlut.rBFv9lTV1h8VmD1ywU3q3S62JWaeUiZiiOeIiw')