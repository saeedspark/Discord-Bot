import discord
from discord.ext import commands
from easy_pil import *
from discord import File


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready():
        print('Welcome.py is ready')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcome.py is ready')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.client.get_channel(1187365620279427072)
        verify_channel = self.client.get_channel(1199714429021978624)
        rules_channel = self.client.get_channel(1187360762625261609)
        get_start_channel = self.client.get_channel(1187365733680820245)

        background = Editor("image/banner.jpg")
        rectangle = Editor("image/rectangle.png")
        if member.avatar:
            profile_image = await load_image_async(str(member.avatar.url))
            circle_image = Editor(profile_image).circle_image()
            circle_image.save("avatar.png", "PNG")
            file = discord.File('avatar.png')
        else:
            profile_image = await load_image_async("https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcStofcQXkxBcT45zTCjvAXM9pRq6ftig6cCzxMmH2atziHa50j9")
            circle_image = Editor(profile_image).circle_image()
            circle_image.save("discord.png", "PNG")
            file = discord.File('discord.png')

        profile = Editor(profile_image).resize((250, 250)).circle_image()
        
        background.blend(rectangle, alpha=0.5, on_top=False)
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=35, variant="regular")

        rectangle.blend(background, alpha=0.5, on_top=False)

        background.paste(profile, (570, 60))
        background.ellipse((570, 60), 250, 250, outline="#005ce6", stroke_width=5)
        background.text((700, 350), f"{member.name}", color="white", font=poppins, align="center")
        background.text(
            (700, 415), f"Welcome", color="white", font=poppins_small, align="center"
        )
        # background.text(
        #     (400, 360),
        #     "You are the 457th Member",
        #     color="#0BE7F5",
        #     font=poppins_small,
        #     align="center",
        # )
        # background.rectangle((30, 220), width=650, height=40, color="#FFFFFF", radius=20)
        # background.paste(profile, (600, 90))
        # background.ellipse((600, 90), 185, 185, outline="#99ccff", stroke_width=5)
        # background.text(f'{member.name} just joined to Booboos community!', color="#99ccff", font=poppins, align="center")
        file = File(fp=background.image_bytes, filename="banner.jpg")
        
        member_role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(member_role)
        await welcome_channel.send(f"{member.mention}\nWe are glad that you have joined our community.\nThis server is a place for 👻**Booboos**👻 community to connect with each other\nand discuss everything related to Booboos NFT collection.\n✅ Please verify in {verify_channel.mention}\n🛑 Read {rules_channel.mention}\n👋 When you've verified yourself, read {get_start_channel.mention}", file=file)

async def setup(client):
    await client.add_cog(Welcome(client))