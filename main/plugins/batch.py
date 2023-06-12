#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub


batch = []

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cancel'))
async def cancel(event):
    if not event.sender_id in batch:
        return await event.reply("لا يـوجـد شـي هـنا .")
    batch.clear()
    await event.reply("Done.")
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if event.sender_id in batch:
        return await event.reply("يـرجـى الانتـظـار العـملـية قيـد التـقدم")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("الان اࢪسـل الـࢪابـط الـذي تـࢪيـد حفـظ الـمحتـوى المـقيـد & بـل رد علـى هـذه الـࢪسـالـه", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("خـطأ يـࢪجـى التـأكد مـن الࢪابـط .")
                    return conv.cancel()
            except Exception as e:
                print(e)
                await conv.send_message("يـࢪجـى الانـتـظاࢪ")
                return conv.cancel()
            await conv.send_message("الان اࢪسـل عـدد الـࢪسـائل التـي تـࢪيد حفـظـها ، /range بل رد علـى هـذه الـࢪسـالـه", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("يـࢪجـى الانـتـظاࢪ")
                return conv.cancel()
            try:
                value = int(_range.text)
                if value > 100:
                    await conv.send_message("يـمكنـك الـحـصول علـى 100 ࢪسالـه مـقيـيده فـي كـل مـࢪه")
                    return conv.cancel()
            except ValueError:
                await conv.send_message("يجـب ان يـكـون عـدد ࢪسـائل لا يتـجاوز الحـد 100")
                return conv.cancel()
            batch.append(event.sender_id)
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.clear()

async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 5
        if i < 50 and i > 25:
            timer = 10
        if i < 100 and i > 50:
            timer = 15
        if not 't.me/c/' in link:
            if i < 25:
                timer = 2
            else:
                timer = 3
        try: 
            if not sender in batch:
                await client.send_message(sender, "اكـتمـلت الـعمـليـة .")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "اكـتمـلت الـعمـليـة .")
            break
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "يـࢪجى الانـتضـار 5 دقـائـق علـى الأقـل")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"يـࢪجى الانـتـضاࢪ قـليلا `{timer}` للأبتـعاد عـن Floodwaits")
        await asyncio.sleep(timer)
        await protection.delete()
            
