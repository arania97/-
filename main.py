import discord,json,os,random
from discord.ext import commands

with open("setting.json") as file:
    info = json.load(file)
    token = info["token"]
    delete = info["autodel"]
    prefix = info["prefix"]

bot = commands.Bot(command_prefix=prefix)
channel = '00000000000000000'

def embed(embedtype, embedtitle, description):
    if (embedtype == "error"):
        return discord.Embed(color=0x5865f2, title=embedtitle, description=description)
    if (embedtype == "success"):
        return discord.Embed(color=0x5865f2, title=embedtitle, description=description)
    if (embedtype == "warning"):
        return discord.Embed(color=0x5865f2, title=embedtitle, description=description)

@bot.event
async def on_ready():
    print("[+] 와핑샵 𝙂𝙀𝙉 에 접속을 완료 하였습니다.")
    game = discord.Game('𝙂𝙀𝙉 관리')
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.command()
async def 재고(message):
    if not message.channel.id == int(channel):
        return
    stockmenu = discord.Embed(title="🌌 제품목록",description="",color=0x5865f2)
    for filename in os.listdir("재고"):
        with open("재고\\"+filename) as f: 
            ammount = len(f.read().splitlines()) 
            name = (filename[0].upper() + filename[1:].lower()).replace(".cfg","")
            stockmenu.description += f"제품 : `{name}` \n재고 : `{ammount}개`\n-------------------\n"
    await message.send(embed=stockmenu)

@bot.command()
async def 잰(message,name=None):
    if not message.channel.id == int(channel):
        return
        await message.channel.send(embed=embed("error", "❌ 생성 실패" , "계정을 입력해주세요."))
    else:
        name = name.lower()+".cfg"
        if name not in os.listdir("재고"):
            await message.channel.send(embed=embed("error", "❌ 생성 실패" , "해당 계정은 없습니다."))
        else:
            with open("재고\\"+name) as file:
                lines = file.read().splitlines() 
            if len(lines) == 0: 
                await message.channel.send(embed=embed("error", "❌ 생성 실패" , "해당 계정의 재고가 부족합니다."))
            else:
                with open("재고\\"+name) as file:
                    account = random.choice(lines)
                try: 
                    await message.author.send(embed=embed("success", "🌌 생성 성공" , "```" + str(account) + "```\n\n해당 메시지는 30초 뒤에 제거됩니다."),delete_after=delete)
                except: 
                    await message.channel.send(embed=embed("error", "❌ 생성 실패" , "DM 전송을 허용해주세요."))
                else: 
                    await message.channel.send(embed=embed("success", "🌌 생성 성공" , "DM을 확인해주세요."))
                    with open("재고\\"+name,"w") as file:
                        file.write("")
                    with open("재고\\"+name,"a") as file:
                        for line in lines:
                            if line != account: 
                                file.write(line+"\n") 

bot.run(token)