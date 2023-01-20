from discord.ext.commands import has_permissions
from discord.ext import commands
from io import BytesIO
import requests
import discord
import asyncio
import random
import json
import time


class User_inform:
    def __init__(self, message):
        self.message = message
        self.user = discord.utils.get(message.guild.members, id=message.author.id)
        self.user_list = json.load(open('usii.json', 'r', encoding='utf-8'))

    def __w_info(self, name="", s_name="", role_for_bot=""):
        if not name:
            name = self.message.author.name
        if not s_name:
            s_name = self.message.author.name

        obj_write_user = \
            {
                f"{self.user.id}": {
                    "name": f"{name}",
                    "second_name": f"{s_name}",
                    "role_for_bot": f"{role_for_bot}",
                    "roles_list": [

                    ],
                    "techno_info": "",
                    "balance": {
                        "gems": 0,
                        "coins": 0
                    }
                }
            }

        with open('usii.json', 'r') as jfr:
            json_file = json.load(jfr)
        if str(json_file).find(f"{self.user.id}") == -1:
            with open('usii.json', 'w') as jf:
                cursor = json_file
                cursor.append(obj_write_user)
                json.dump(json_file, jf, indent=4)
            return "info writing!"
        else:
            return "info writing!"

    def find_user(self):
        try:
            a = 0
            for i in self.user_list[0:]:
                print(i)
                if str(i).find(f'{self.user.id}') != -1:
                    return self.user_list[a][f'{self.user.id}']
                a += 1
        except:
            print("ERROR!!!!!USER_LIST")
            return "NF"

    def give_user_info(self, auto_write=False):
        temp = self.find_user()

        if temp != "NF":
            return temp

        elif temp == "NF" and auto_write == False:
            return "info is not writing for user"

        elif temp == "NF" and auto_write == True:
            temp = self.__w_info()

            if temp == "info writing!":
                return self.find_user()
            else:
                return "error writing!!!"

    def pay_money(self, gems=0, coin=0):

        with open('usii.json', 'r') as file:
            json_data = json.load(file)
            for item in json_data[0:]:
                if str(item).find(f"{self.user.id}") != -1:
                    item[f"{self.user.id}"]['balance']["gems"] += gems
                    item[f"{self.user.id}"]['balance']["coins"] += coin

        with open('usii.json', 'w') as file:
            json.dump(json_data, file, indent=2)


#загрузки файлов json
config = json.load(open('config.json', 'r'))


#создание бота
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def lang_locate(User):
    locate = ""
    for lang in config['locals']:
        try:
            if str(User.roles).find(lang) != -1:
                locate = json.load(open(f'locals/locate-{lang}.json', 'r', encoding='utf-8'))
                break
            else:
                locate = json.load(open(f'locals/locate-en.json', 'r', encoding='utf-8'))
        except:
            if str(User.roles).find(lang) != -1:
                locate = json.load(open(f'locals/locate-{lang}.json', 'r', encoding='utf-8'))
                break
            else:
                locate = json.load(open(f'locals/locate-en.json', 'r', encoding='utf-8'))
    return locate


#TODO: когда бот готов К ПОЛНОЙ ЭКСПЛУОТАЦИИ!!!
@bot.event
async def on_ready():
    print(f"{bot.user.name} в сети")
    discord.Component()

cords = [0, 0, 0, 0, 0, 0, 0, 0, 0]


class tic_tac_toy_buttons(discord.ui.View):
    global cords

    def __init__(self, user, user2, message):
        super().__init__(timeout=None)
        self.ocher = None
        self.user1 = user
        self.user2 = user2
        self.message = message

    def check_win(self, cords):
        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for i in win_coord:
            if cords[i[0]] == cords[i[1]] == cords[i[2]]:
                if cords[i[0]] != 0:
                    print("win", cords[i[1]])
                    return cords[i[1]]
        return -1

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=0, custom_id="1")
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[0] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[0] = 1
                    else:
                        button.emoji = "❌"
                        cords[0] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=0, custom_id="2")
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[1] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[1] = 1
                    else:
                        button.emoji = "❌"
                        cords[1] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=0, custom_id="3")
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[2] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[2] = 1
                    else:
                        button.emoji = "❌"
                        cords[2] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    #row 1

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=1, custom_id="4")
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[3] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[3] = 1
                    else:
                        button.emoji = "❌"
                        cords[3] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=1, custom_id="5")
    async def button_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[4] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[4] = 1
                    else:
                        button.emoji = "❌"
                        cords[4] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=1, custom_id="6")
    async def button_6(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[5] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[5] = 1
                    else:
                        button.emoji = "❌"
                        cords[5] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    #row 2

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=2, custom_id="7")
    async def button_7(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[6] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[6] = 1
                    else:
                        button.emoji = "❌"
                        cords[6] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=2, custom_id="8")
    async def button_8(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[7] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[7] = 1
                    else:
                        button.emoji = "❌"
                        cords[7] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

    @discord.ui.button(label=" ", style=discord.ButtonStyle.grey, row=2, custom_id="9")
    async def button_9(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = self.check_win(cords)
        if check == -1:
            if cords[8] == 0:
                if interaction.user != self.ocher:
                    self.ocher = interaction.user
                    if interaction.user == self.user1:
                        button.emoji = "⭕"
                        cords[8] = 1
                    else:
                        button.emoji = "❌"
                        cords[8] = 2
                await interaction.response.edit_message(view=self)
        else:
            if check == 1:
                win_user = self.user1
            else:
                win_user = self.user2
            USII = User_inform(self.message)
            USII.user = win_user
            USII.pay_money(coin=100)
            print(11111)
            embed = discord.Embed(
                title=f"Win {win_user}!",
                description=f"+100 coin's",
                color=0x0F02FF
            )
            await interaction.response.edit_message(view=self, embed=embed, delete_after=40.0)

bot.remove_command('help')


@bot.command()
async def help(ctx):
    user = discord.utils.get(ctx.author.guild.members, id=ctx.message.author.id)
    locate = lang_locate(user)
    text = ""

    if ctx.message.author.guild_permissions.administrator:
        for i in locate['!help'][1:]:
            text += i
    else:
        for i in locate['!help'][1:]:
            if i[0] != "#":
                text += i

    help_message = discord.Embed(
        title=f"{locate['!help'][0]}",
        description=f"{text}",
        color=0x00FF00
    )
    await ctx.channel.send(embed=help_message)


@bot.command()
async def XO(ctx, member):
    #view.add_item(discord.ui.Button(label="Default Button",style=discord.ButtonStyle.gray,custom_id="Default Button")) , view=Buttons(user)

    first_user = discord.utils.get(ctx.author.guild.members, id=ctx.message.author.id)
    print("-", first_user.roles)
    message = ctx.message.content
    locate = lang_locate(first_user)

    print(ctx.message.content)

    if ctx.message.content.find("<@") != -1:
        sec_user_id = message[message.find("@")+1:-1]

        sec_user = bot.get_user(int(sec_user_id))

        await sec_user.send(locate['question_start_game'] + " \n❌&⭕")

        def check(arg):
            return str(arg.emoji) == '👍' or str(arg.emoji) == '❌'

        payload = await bot.wait_for('raw_reaction_add', timeout=60.0, check=check)
        if str(payload.emoji) == '👍':
            await ctx.send(f"{locate['user']}: {sec_user} {locate['accept']}!", delete_after=15.0)
            await ctx.send("❌&⭕", view=tic_tac_toy_buttons(first_user, sec_user, ctx.message))

    else:
        await ctx.send(locate['error_game_user'])
        await ctx.send(f"{locate['tic_tac_toy']}")


@bot.command()
async def pay(ctx):
    USII = User_inform(ctx.message)
    USII.pay_money(coin=100)
    #print(USII.give_user_info(False))


@bot.command()
@has_permissions(administrator=True)
async def Item(ctx):
    user = discord.utils.get(ctx.author.guild.members, id=ctx.message.author.id)
    locate = lang_locate(user)

    for attach in ctx.message.attachments:
        if attach.filename.find(".json") and attach.filename[-1] == "n":
            await attach.save(f"C:/Users/Monik/PycharmProjects/DiscordBot_1/products_json/{attach.filename}")
        else:
            error_message = discord.Embed(
                title=f"{locate['Item_error'][0]}",
                description=f"{locate['Item_error'][1]}",
                color=0xFF0000
            )
            #await ctx.author.send("недопустимый формат файла(используйте .json)")
            await ctx.channel.send(embed=error_message)


@bot.command()
async def Games(ctx):
    user = discord.utils.get(ctx.author.guild.members, id=ctx.message.author.id)
    locate = lang_locate(user)
    text = ""
    for i in locate['!game'][1:]:
        text += i

    message = discord.Embed(
        title=f"{locate['!game'][0]}",
        description=f"{text}",
        color=0xFF00FF
    )

    await ctx.channel.send(embed=message)

@bot.command()
async def balance(ctx):
    USII = User_inform(ctx.message)
    data = USII.give_user_info(True)
    print(data)

    message = discord.Embed(
        title=f"Your balance {ctx.message.author.name}",
        description=f"Gems: {data['balance']['gems']}\n"
                    f"Coins: {data['balance']['coins']}",
        color=0xFF00FF
    )

    await ctx.channel.send(embed=message)


#TODO: Когда человек пишет любое сообщение
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content, message)



#TODO: Когда человек зашел на сервер
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=config['Roles']['default_role'])
    channel = member.guild.system_channel

    hello_message = discord.Embed(
        title="@everyone Разойдитесь все у нас новенький!",
        description=f'{member.name}#{member.discriminator}',
        color=0xb7e7a4
    )
    await member.add_roles(role)
    await channel.send(embed=hello_message)


#TODO: Когда задается реакция проходит все через проверки
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config['Posts_ids']['give_role_on_reaction']:

        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        user = discord.utils.get(message.guild.members, id=payload.user_id)

        emoji = str(payload.emoji)

        try:
            role = discord.utils.get(message.guild.roles, id=config['Roles'][emoji])

            #if len([i for i in user.roles if i.id not in list_users[user_id_]['roles_list']]) <= config['max_roles']:
            if len(user.roles) <= config['max_roles']:

                await user.add_roles(role)
                print(f"{user.name} получил роль {role.name}")
            else:

                await message.remove_reaction(payload.emoji, user)
                print(f"Ошибка! пользователь {user.name} пытался получить слишком много ролей")

        except Exception as _ex:
            print(repr(_ex))

    if payload.message_id == config['Posts_ids']['give_lang_on_reaction']:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        user = discord.utils.get(message.guild.members, id=payload.user_id)

        emoji = str(payload.emoji)

        try:
            role = discord.utils.get(message.guild.roles, id=config['Roles'][emoji])

            # if len([i for i in user.roles if i.id not in list_users[user_id_]['roles_list']]) <= config['max_roles']:
            if len(user.roles) <= config['max_roles']:

                await user.add_roles(role)
                print(f"{user.name} получил роль {role.name}")
            else:

                await message.remove_reaction(payload.emoji, user)
                print(f"Ошибка! пользователь {user.name} пытался получить слишком много ролей")

        except Exception as _ex:
            print(repr(_ex))


#TODO: Когда снимается реация проходит через проверки
@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    await channel.fetch_message(payload.message_id)

    user = discord.utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)

        role = discord.utils.get(message.guild.roles, id=config['Roles'][emoji])
        await user.remove_roles(role)
    except Exception as _ex:
        print(repr(_ex))

bot.run(config['token'])
