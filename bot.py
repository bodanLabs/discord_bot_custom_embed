from datetime import datetime
import discord
from discord import app_commands
from embed_creator import EmbedBaseView

COLOR = 0x3498db


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=1024380355379200110))
        await self.tree.sync(guild=discord.Object(id=1024380355379200110))
        return


intents = discord.Intents.all()
client = Bot(intents=intents)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    return


@client.tree.command(description="Create a new custom embed message to send to a specific channel.")
@app_commands.describe(channel="The channel to send this embed message to.")
@app_commands.default_permissions()
async def embed(interaction: discord.Interaction, channel: discord.TextChannel):
    file = discord.File("embed.png", filename="embed.png")
    system_embed = discord.Embed(
        title="Embed Creator", description=f"Creating new custom embed to be sent to {channel.mention}.\nWhat action would you like to perform next?\n\n*The embed below is how your custom embed currently looks like ⤵️*", color=COLOR, timestamp=datetime.utcnow())
    system_embed.set_image(url="attachment://embed.png")
    system_embed.set_footer(
        text="The system has a 3 minute timeout since the last interaction.")
    your_embed = discord.Embed(title="NONE", description="NONE")
    await interaction.response.send_message(embeds=[system_embed, your_embed], file=file)
    initial_message = await interaction.original_response()
    await initial_message.edit(view=EmbedBaseView(channel, initial_message, system_embed, your_embed, False, True, False))
    return




TOKEN = "BOT_TOKEN"

client.run(TOKEN)
