import discord
from discord.ext import commands
import os
import requests
"""from a import keep_alive"""
from discord.utils import get
import time

intents = discord.Intents.default()
intents.members = True
client=commands.Bot(command_prefix="!",intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ronzy.py"))


"""webhook = await ctx.channel.create_webhook(name=member.name)"""

@client.event
async def on_message(message):
  if not message.guild:
    guild = client.get_guild(758389422969716746)
    if not f"destek-{message.author.id}" in str(guild.text_channels):
        if not message.author.bot:
          overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)}
          cat = discord.utils.get(guild.categories, name="Wis Contact Bot")
          channel = await guild.create_text_channel(name=f"destek-{message.author.id}", category=cat, overwrites=overwrites)
          global kullanici
          global kadi
          global diss
          kullanici = message.author.mention
          kadi = message.author.name
          diss = message.author.discriminator
          if not kullanici:
            await channel.send(f"{message.author.name}#{message.author.discriminator} Kullanıcısının Destek İsteği")
          else:
            await channel.send(f"{message.author.mention} Kullanıcısının Destek İsteği")
          for attachment in message.attachments:
            b = str(message.attachments)
            adim1 = b.split("filename='")[1].split("'")[0]
            await attachment.save(f"./{adim1}")
            await channel.send(file=discord.File(f"./{adim1}"))
          else:
            await channel.send(str(message.content))
    else:
        if not message.author.bot:
          cb=discord.utils.get(guild.text_channels, name=f"destek-{message.author.id}")
          for attachment in message.attachments:
            b = str(message.attachments)
            adim1 = b.split("filename='")[1].split("'")[0]
            await attachment.save(f"./{adim1}")
            await cb.send(file=discord.File(f"./{adim1}"))
          else:
            await cb.send(str(message.content))

  if message.guild:
    if not message.author.bot:
      if message.content == "!kapat":
        await message.delete()
        kanal = get(message.guild.text_channels, name=message.channel.name)
        await message.channel.send("Bu Kanal 10 Saniye Sonra Kapanıyor")
        time.sleep(10)
        await kanal.delete()
      elif message.content == "!kbilgi":
        id=message.channel.name.split("destek-")[1]
        kullanici1 = message.guild.get_member(int(id))
        if not kullanici1:
          await message.channel.send(f"{kullanici1.name}#{kullanici1.discriminator} Kullanıcısının Destek İsteği")
        else:
            await message.channel.send(f"{kullanici1.mention} Kullanıcısının Destek İsteği")
      else:
        if "destek" in str(message.channel.name):
          id=message.channel.name.split("destek-")[1]
          try:
            user = message.guild.get_member(int(id))
          except:
            await message.channel.send("Kullanıcı Bulunamadı")
          else:
            if not message.author.bot:
              try:
                ca = await user.create_dm()
                for attachment in message.attachments:
                  b = str(message.attachments)
                  adim1 = b.split("filename='")[1].split("'")[0]
                  await attachment.save(f"./{adim1}")
                  await user.send(file=discord.File(f"./{adim1}"))
                else:
                  await user.send(str(message.content))
              except:
                await user.send(message.content)
                
  if message.guild:
    if message.content.startswith("!mesajgönder"):
        role = discord.utils.get(message.guild.roles, name="Wis Contact Bot")
        if role in message.author.roles:
            kisi = message.content.split(f"!mesajgönder ")[1].split(">")[0]
            kisi = kisi.replace(" ","")
            
            kisi1 = kisi.split(f"<@")[1]
            user = message.guild.get_member(int(kisi1))
            try:
                mesaj = message.content.split(f"{kisi}> ")[1]
            except:
                return await message.channel.send("Mesaj Kısmı Boş Olamaz")
            
            
            if not f"destek-{user.id}" in str(message.guild.text_channels):
                overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.guild.me: discord.PermissionOverwrite(read_messages=True)}
                cat = discord.utils.get(message.guild.categories, name="Wis Contact Bot")
                channel = await message.guild.create_text_channel(name=f"destek-{user.id}", category=cat, overwrites=overwrites)
                for attachment in message.attachments:
                    b = str(message.attachments)
                    adim1 = b.split("filename='")[1].split("'")[0]
                    await attachment.save(f"./{adim1}")
                    await user.send(file=discord.File(f"./{adim1}"))
                    kanal=discord.utils.get(message.guild.text_channels, name=f"destek-{user.id}")
                    webhook = await kanal.create_webhook(name = message.author.name)
                    await webhook.send(file=discord.File(f"./{adim1}"),username = message.author.name,avatar_url = message.author.avatar_url)
                    """try:
                        await channel.send(str(mesaj))
                    except:
                        pass"""
                else:
                    await user.send(str(mesaj))
                    kanal=discord.utils.get(message.guild.text_channels, name=f"destek-{user.id}")
                    webhook = await kanal.create_webhook(name = message.author.name)
                    await webhook.send(str(mesaj),username = message.author.name,avatar_url = message.author.avatar_url)
                await message.channel.send(f"Yazdığınız Mesaj Gönderildi Ve Kanal Kuruldu Kanalı Aşağıya Etiketledim\n{kanal.mention}")
            else:
                kanal=discord.utils.get(message.guild.text_channels, name=f"destek-{user.id}")
                await message.channel.send(f"Zaten Halihazırda Yazma Kanalı Mevcut Kanalı Senin İçin Aşağıya Etiketliyorum\n{kanal.mention}")
        else:
            await message.channel.send("Bu Komudu Kullanmak İçin Yetkin Yok")


"""for dosya in os.listdir("./Mesaj Gönder"):
  if dosya.endswith(".py"):
    client.load_extension("Mesaj Gönder."+str(dosya[:-3]))
    print(f"{str(dosya[:-3])} Komudu Yüklendi")"""

client.run("MTAwMjY4ODc2NzkwOTQzNzQ4MA.GwW266.A-9Z8EHNaRlAjxWt6y4QC-nqwlJQbqoZf5LWjE")