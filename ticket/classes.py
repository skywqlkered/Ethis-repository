import discord
from discord import ui

# input_field:discord.ui.InputText = discord.ui.InputText(required=True, placeholder="Please give your Minecraft username...")

class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.Label(text='Name', component=ui.TextInput())
    answer = ui.Label(text='Answer', component=ui.TextInput(style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name.component.value}!', ephemeral=True) # type: ignore
        
class OpenModalView(discord.ui.View):
    @discord.ui.button(label="Open Questionnaire")
    async def open_questionnaire(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            Questionnaire()
        )