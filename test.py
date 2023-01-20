class Buttons(discord.ui.View):
    def __init__(self, *, timeout=50):
        super().__init__(timeout=None)


    @discord.ui.button(label="0",style=discord.ButtonStyle.blurple,row=0,custom_id="count",emoji="🎁") # or .primary
    async def blurple_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message('Hello!', ephemeral=True)
        print(int(button.label))
        label = int(button.label)
        label += 1
        button.label = str(label)
        await interaction.response.edit_message(view=self)





    @discord.ui.button(label="Gray Button",style=discord.ButtonStyle.gray,row=1,emoji="\U0001f974") # or .secondary/.grey
    async def gray_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Green Button",style=discord.ButtonStyle.green) # or .success
    async def green_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Red Button",style=discord.ButtonStyle.red) # or .danger
    async def red_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)

@bot.command()
async def button(ctx):
    view=Buttons()
    view.add_item(discord.ui.Button(label="Default Button",style=discord.ButtonStyle.gray,custom_id="Default Button"))
    await ctx.send("This message has buttons!",view=view)
