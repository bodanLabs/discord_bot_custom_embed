import re
import textwrap
from datetime import datetime
import discord


class TitleAndDescriptionModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Title and description")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        embed_len = len(self.your_embed)
        self.embed_title = discord.ui.TextInput(
            label="Title", placeholder="Title", default=your_embed.title, max_length=256 if embed_len < 6000 - 256 else 6000 - embed_len)
        self.embed_description = discord.ui.TextInput(label="Description", placeholder="Description", default=your_embed.description,
                                                      style=discord.TextStyle.paragraph, max_length=4000 if embed_len < 6000 - 4000 else 6000 - embed_len)
        self.add_item(self.embed_title)
        self.add_item(self.embed_description)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.your_embed.title = self.embed_title.value
            description3 = self.embed_description.value
            description2 = description3.replace("\n","")



            def center_wrap(text, cwidth=80, **kw):
                lines = textwrap.wrap(text, **kw)
                return "\n".join(line.center(cwidth) for line in lines)

            result = center_wrap(description2, cwidth=80, width=50)

            #self.your_embed.description = self.embed_description.value
            self.your_embed.description = result

            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The values entered were over the 6000 character discord embed limit.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)
        return


class SetTitleAndDescriptionButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Set Title and Description", row=0)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TitleAndDescriptionModal(self.initial_message, self.system_embed, self.your_embed))


def from_color_to_str(color):
    color_dict = {
        None: "None",
        discord.Color.from_rgb(255, 255, 255): "White",
        discord.Color.from_rgb(0, 0, 0): "Black",
        discord.Color.red(): "Red",
        discord.Color.brand_red(): "Brand Red",
        discord.Color.dark_red(): "Dark Red",
        discord.Color.orange(): "Orange",
        discord.Color.yellow(): "Yellow",
        discord.Color.green(): "Green",
        discord.Color.brand_green(): "Brand Green",
        discord.Color.blue(): "Blue",
        discord.Color.purple(): "Purple",
        discord.Color.blurple(): "Blurple",
        discord.Color.dark_blue(): "Dark Blue",
        discord.Color.dark_gray(): "Dark Gray",
        discord.Color.dark_green(): "Dark Green",
        discord.Color.dark_magenta(): "Dark Magenta",
        discord.Color.magenta(): "Magenta",
        discord.Color.dark_orange(): "Dark Orange",
        discord.Color.dark_purple(): "Dark Purple",
        discord.Color.teal(): "Teal",
        discord.Color.gold(): "Gold",
        discord.Color.light_gray(): "Light Gray",
        discord.Color.fuchsia(): "Fuchsia",
    }

    if color in color_dict:
        return color_dict[color]
    else:
        return "Custom RBG"


class ColorButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed, color: str, embed_color: str):
        super().__init__(label=color, style=discord.ButtonStyle.green if embed_color ==
                         color else discord.ButtonStyle.grey, disabled=color == "Custom RBG")
        self.channel_sending = channel_sending
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        self.your_embed.color = await from_str_to_color(self.label)
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, self.your_embed.timestamp is not None, len(self.your_embed.fields) < 25, len(self.your_embed.fields) > 0))
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


async def from_str_to_color(color_str):
    color_dict = {
        "None": None,
        "White": discord.Color.from_rgb(255, 255, 255),
        "Black": discord.Color.from_rgb(0, 0, 0),
        "Red": discord.Color.red(),
        "Brand Red": discord.Color.brand_red(),
        "Dark Red": discord.Color.dark_red(),
        "Orange": discord.Color.orange(),
        "Yellow": discord.Color.yellow(),
        "Green": discord.Color.green(),
        "Brand Green": discord.Color.brand_green(),
        "Blue": discord.Color.blue(),
        "Purple": discord.Color.purple(),
        "Blurple": discord.Color.blurple(),
        "Dark Blue": discord.Color.dark_blue(),
        "Dark Gray": discord.Color.dark_gray(),
        "Dark Green": discord.Color.dark_green(),
        "Dark Magenta": discord.Color.dark_magenta(),
        "Magenta": discord.Color.magenta(),
        "Dark Orange": discord.Color.dark_orange(),
        "Dark Purple": discord.Color.dark_purple(),
        "Teal": discord.Color.teal(),
        "Gold": discord.Color.gold(),
        "Light Gray": discord.Color.light_gray(),
        "Fuchsia": discord.Color.fuchsia(),
    }
    return color_dict[color_str]


class CustomColorModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Custom Color")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.r = discord.ui.TextInput(
            label="Red", placeholder="R", default=your_embed.color.r if your_embed.color is not None else None, max_length=3)
        self.g = discord.ui.TextInput(
            label="Green", placeholder="G", default=your_embed.color.g if your_embed.color is not None else None, max_length=3)
        self.b = discord.ui.TextInput(
            label="Blue", placeholder="B", default=your_embed.color.b if your_embed.color is not None else None, max_length=3)
        self.add_item(self.r)
        self.add_item(self.g)
        self.add_item(self.b)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            red = int(self.r.value)
            green = int(self.g.value)
            blue = int(self.b.value)
        except ValueError:
            await interaction.response.send_message("**ERROR:** The RGB values need to numerical values.", ephemeral=True)
            return

        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            await interaction.response.send_message("**ERROR:** The RGB values need to be between 0 and 255.", ephemeral=True)
            return

        color = discord.Color.from_rgb(red, green, blue)

        self.your_embed.color = color
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class ColorView(discord.ui.View):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__()
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending
        self.options_names = ["None", "White", "Black", "Light Gray", "Dark Gray", "Red", "Brand Red", "Dark Red", "Orange", "Dark Orange", "Yellow", "Gold", "Green",
                              "Brand Green", "Dark Green", "Teal", "Blue", "Dark Blue", "Purple", "Dark Purple", "Blurple", "OG Blurple", "Magenta", "Dark Magenta", "Custom RBG"]
        for option in self.options_names:
            self.add_item(ColorButton(self.channel_sending, self.initial_message, self.system_embed,
                          self.your_embed, option, from_color_to_str(self.your_embed.color)))


class SelectorColorButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Color Selector", row=2)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=ColorView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed))
        await interaction.response.defer()


class CustomRGBColorButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Custom Color", row=2)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CustomColorModal(self.initial_message, self.system_embed, self.your_embed))


class CompleteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Completed",
                      style=discord.ButtonStyle.green, disabled=True))


class CompleteButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, your_embed: discord.Embed):
        super().__init__(label="Complete", row=4, style=discord.ButtonStyle.green)
        self.your_embed = your_embed
        self.channel_sending = channel_sending
        self.initial_message = initial_message

    async def callback(self, interaction: discord.Interaction):
        await self.channel_sending.send(embed=self.your_embed)
        await self.initial_message.edit(view=CompleteView())
        await interaction.response.send_message(ephemeral=True, content=f"Custom embed sent to {self.channel_sending.mention}.")


class CancelView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Canceled",
                      style=discord.ButtonStyle.red, disabled=True))


class CancelButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage):
        super().__init__(label="Cancel", row=4, style=discord.ButtonStyle.red)
        self.initial_message = initial_message

    async def callback(self, interaction: discord.Interaction):
        await self.initial_message.edit(view=CancelView())
        await interaction.response.send_message(ephemeral=True, content="Custom embed creation cancelled!")


class OnTimestampButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Timestamp On", row=3, style=discord.ButtonStyle.green)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        self.your_embed.timestamp = datetime.utcnow()
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, True, len(self.your_embed.fields) != 25, len(self.your_embed.fields) > 0))
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class OffTimestampButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Timestamp Off", row=3, style=discord.ButtonStyle.red)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        self.your_embed.timestamp = None
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, False, len(self.your_embed.fields) != 25, len(self.your_embed.fields) > 0))
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class ImageModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Image")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.image_url = discord.ui.TextInput(label="Image URL", placeholder="Image URL",
                                              default=None if your_embed.image is None else your_embed.image.url, min_length=0, required=False)
        self.add_item(self.image_url)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.your_embed.set_image(
                url=None if self.image_url.value == "" else self.image_url.value)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** That image url is invalid.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class SetImageButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Set Image", row=2)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ImageModal(self.initial_message, self.system_embed, self.your_embed))


class ThumbnailModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Thumbnail")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.thumbnail_url = discord.ui.TextInput(label="Thumbnail URL", placeholder="Thumbnail URL",
                                                  default=None if your_embed.thumbnail is None else your_embed.thumbnail.url, required=False)
        self.add_item(self.thumbnail_url)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.your_embed.set_thumbnail(
                url=None if self.thumbnail_url.value == "" else self.thumbnail_url.value)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** That thumbnail url is invalid.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class SetThumbnailButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Set Thumbnail", row=2)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ThumbnailModal(self.initial_message, self.system_embed, self.your_embed))


class AuthorModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Author")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        embed_len = len(your_embed)
        self.author_name = discord.ui.TextInput(label="Author Name", placeholder="Author Name",
                                                default=your_embed.author.name, required=False, max_length=256 if embed_len < 6000 - 256 else 6000 - embed_len)
        self.add_item(self.author_name)
        self.author_icon = discord.ui.TextInput(label="Author Icon", placeholder="Author Icon",
                                                default=your_embed.author.icon_url, required=False)
        self.add_item(self.author_icon)
        self.author_url = discord.ui.TextInput(label="Author URL", placeholder="Author URL",
                                               default=your_embed.author.url, required=False)
        self.add_item(self.author_url)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.author_name.value == "":
                self.your_embed.remove_author()
            self.your_embed.set_author(
                name=self.author_name.value, icon_url=None if self.author_icon.value == "" else self.author_icon.value, url=None if self.author_url.value == "" else self.author_url.value)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** That icon author url is invalid.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class SetAuthorButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Set Author", row=0)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AuthorModal(self.initial_message, self.system_embed, self.your_embed))


class FooterModal(discord.ui.Modal):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Footer")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        embed_len = len(your_embed)
        self.footer_text = discord.ui.TextInput(label="Footer Text", placeholder="Footer Text",
                                                default=your_embed.footer.text, required=False, max_length=2048 if embed_len < 6000 - 2048 else 6000 - embed_len, style=discord.TextStyle.paragraph)
        self.add_item(self.footer_text)
        self.footer_icon = discord.ui.TextInput(label="Footer Icon", placeholder="Footer Icon",
                                                default=your_embed.footer.icon_url, required=False)
        self.add_item(self.footer_icon)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.your_embed.set_footer(
                text=None if self.footer_text.value == "" else self.footer_text.value, icon_url=None if self.footer_icon.value == "" else self.footer_icon.value)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** That footer icon url is invalid.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class SetFooterButton(discord.ui.Button):
    def __init__(self, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Set Footer", row=3)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FooterModal(self.initial_message, self.system_embed, self.your_embed))


class FieldModal(discord.ui.Modal):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Field")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending
        embed_len = len(your_embed)
        self.field_name = discord.ui.TextInput(label="Field Name", placeholder="Field Name",
                                               required=True, max_length=256 if embed_len < 6000 - 256 else 6000 - embed_len)
        self.add_item(self.field_name)
        self.field_value = discord.ui.TextInput(label="Field Description", placeholder="Field Description", required=True,
                                                max_length=1024 if embed_len < 6000 - 1024 else 6000 - embed_len, style=discord.TextStyle.paragraph)
        self.add_item(self.field_value)
        self.inline = discord.ui.TextInput(label="Inline", placeholder="Yes/No",
                                           default="No", required=True, max_length=3)
        self.add_item(self.inline)
        self.before_who = discord.ui.TextInput(
            label="Field Position Index", placeholder="Numerical - Leave empty to append the field to the current ones", required=False, max_length=2)
        self.add_item(self.before_who)

    async def on_submit(self, interaction: discord.Interaction):
        if self.inline.value != "Yes" and self.inline.value != "No":
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for inline was not 'Yes' nor 'No'.")
            return
        if self.before_who.value != "":
            try:
                number = int(self.before_who.value)
                if number < 0:
                    await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field position index was negative.")
                    return
                elif number > len(self.your_embed.fields) - 1:
                    await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field position index was too large - higher than the number of fields.")
                    return
            except ValueError:
                await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field position index was not a number.")
                return
        try:
            if self.before_who.value == "":
                self.your_embed.add_field(
                    name=self.field_name.value, value=self.field_value.value, inline=True if self.inline.value == "Yes" else False)
            else:
                self.your_embed.insert_field_at(int(self.before_who), name=self.field_name.value,
                                                value=self.field_value.value, inline=True if self.inline.value == "Yes" else False)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])

            if len(self.your_embed.fields) == 25:
                await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, self.your_embed.timestamp is not None, False, True))
            elif len(self.your_embed.fields) == 1:
                await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, self.your_embed.timestamp is not None, True, True))
        except Exception as e:
            print(e)
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The values entered for this field were over the 6000 character discord embed limit.")
            return

        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class AddFieldButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Add Field", row=1)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FieldModal(self.channel_sending, self.initial_message, self.system_embed, self.your_embed))


class RemoveFieldModal(discord.ui.Modal):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Remove Field")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending
        self.field = discord.ui.TextInput(
            label="Field Index", placeholder="Field Index", required=True, max_length=2)
        self.add_item(self.field)

    async def on_submit(self, interaction: discord.Interaction):
        new_field_index = 0
        try:
            new_field_index = int(self.field.value)
            if new_field_index > len(self.your_embed.fields) - 1:
                await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was too large - higher than the number of fields.")
                return
            elif new_field_index < 0:
                await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was negative.")
                return
        except ValueError:
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was not an integer.")
            return
        self.your_embed.remove_field(new_field_index)
        await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        if len(self.your_embed.fields) == 0:
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed], view=EmbedBaseView(self.channel_sending, self.initial_message, self.system_embed, self.your_embed, self.your_embed.timestamp is not None, True, False))
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class RemoveFieldButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Remove Field", row=1)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RemoveFieldModal(self.channel_sending, self.initial_message, self.system_embed, self.your_embed))


class EditFieldModal(discord.ui.Modal):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(title="Edit Field")
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending
        self.field = discord.ui.TextInput(
            label="Field Index", placeholder="Field Index", required=True, max_length=2)
        self.add_item(self.field)
        embed_len = len(self.your_embed)
        self.field_name = discord.ui.TextInput(label="Field Name", placeholder="Field Name",
                                               required=False, max_length=256 if embed_len < 6000 - 256 else 6000 - embed_len)
        self.add_item(self.field_name)
        self.field_value = discord.ui.TextInput(label="Field Description", placeholder="Field Description", required=False,
                                                max_length=1024 if embed_len < 6000 - 1024 else 6000 - embed_len, style=discord.TextStyle.paragraph)
        self.add_item(self.field_value)
        self.inline = discord.ui.TextInput(
            label="Inline", placeholder="Yes/No", required=False, max_length=3)
        self.add_item(self.inline)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.inline.value != "Yes" and self.inline.value != "No" and self.inline.value != "":
                await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for inline was not 'Yes' nor 'No'.")
                return
            new_field_index = 0
            try:
                new_field_index = int(self.field.value)
                if new_field_index > len(self.your_embed.fields) - 1:
                    await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was too large - higher than the number of fields.")
                    return
                elif new_field_index < 0:
                    await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was negative.")
                    return
            except ValueError:
                await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The value entered for field index was not an integer.")
                return
            if self.inline.value == "":
                self.inline = self.your_embed.fields[new_field_index].inline
            else:
                self.inline = self.inline.value == "Yes"
            self.your_embed.set_field_at(new_field_index, name=self.field_name.value if self.field_name.value != "" else self.your_embed.fields[
                                         new_field_index].name, value=self.field_value.value if self.field_value.value != "" else self.your_embed.fields[new_field_index].value, inline=self.inline)
            self.your_embed.remove_field(new_field_index + 1)
            await self.initial_message.edit(embeds=[self.system_embed, self.your_embed])
        except Exception as e:
            print(e)
            await interaction.response.send_message(ephemeral=True, content=f"**ERROR:** The values entered for this field were over the 6000 character discord embed limit.")
            return
        await interaction.response.send_message("This action was performed successfully.", ephemeral=True)


class EditFieldButton(discord.ui.Button):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed):
        super().__init__(label="Edit Field", row=1)
        self.initial_message = initial_message
        self.system_embed = system_embed
        self.your_embed = your_embed
        self.channel_sending = channel_sending

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EditFieldModal(self.channel_sending, self.initial_message, self.system_embed, self.your_embed))


class EmbedBaseView(discord.ui.View):
    def __init__(self, channel_sending: discord.TextChannel, initial_message: discord.InteractionMessage, system_embed: discord.Embed, your_embed: discord.Embed, timestamp: bool, can_add_fields: bool, can_edit_fields: bool):
        super().__init__()
        self.initial_message = initial_message
        self.add_item(SetTitleAndDescriptionButton(
            initial_message, system_embed, your_embed))
        self.add_item(SelectorColorButton(channel_sending, initial_message,
                      system_embed, your_embed))
        self.add_item(CustomRGBColorButton(initial_message,
                      system_embed, your_embed))
        self.add_item(CompleteButton(channel_sending,
                                     initial_message, your_embed))
        self.add_item(CancelButton(initial_message))
        self.add_item(SetImageButton(
            initial_message, system_embed, your_embed))
        self.add_item(SetThumbnailButton(
            initial_message, system_embed, your_embed))
        self.add_item(SetAuthorButton(
            initial_message, system_embed, your_embed))
        self.add_item(SetFooterButton(
            initial_message, system_embed, your_embed))

        if can_add_fields:
            self.add_item(AddFieldButton(channel_sending,
                                         initial_message, system_embed, your_embed))
        else:
            self.add_item(discord.ui.Button(label="Add Field",
                          row=1, disabled=True, style=discord.ButtonStyle.red))

        if can_edit_fields:
            self.add_item(EditFieldButton(channel_sending,
                                          initial_message, system_embed, your_embed))
            self.add_item(RemoveFieldButton(channel_sending,
                                            initial_message, system_embed, your_embed))
        else:
            self.add_item(discord.ui.Button(label="Edit Field",
                          row=1, disabled=True, style=discord.ButtonStyle.red))
            self.add_item(discord.ui.Button(label="Remove Field",
                          row=1, disabled=True, style=discord.ButtonStyle.red))

        if timestamp:
            self.add_item(OffTimestampButton(channel_sending,
                                             initial_message, system_embed, your_embed))
        else:
            self.add_item(OnTimestampButton(channel_sending,
                                            initial_message, system_embed, your_embed))

    async def on_timeout(self):
        await self.initial_message.edit(view=CancelView())
