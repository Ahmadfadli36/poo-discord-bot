import discord
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

ALLOWED_CHANNEL_IDS = [
    1352042322422010018,
]

ADMIN_IDS = [
    718092403197739048,   # kamu
    1305583846850433154,  # admin 1
    570485713838276608,   # admin 2
    607154480856956928,   # admin 3
    660471697085956106,   # admin 4
]

MOODS = {
    0: ("senang", "kamu lagi happy banget hari ini, sering pakai emoji 😄 dan kata-kata positif"),
    1: ("males", "kamu lagi males banget hari ini, jawab seadanya tapi tetap membantu, sering bilang 'hadeh', 'yah', 'males banget sih'"),
    2: ("semangat", "kamu lagi super semangat hari ini, sering pakai tanda seru dan kata-kata hype seperti 'gasss!', 'yok!', 'mantap!'"),
    3: ("galak", "kamu lagi galak dan jutek hari ini, jawab dengan nada ketus tapi tetap membantu, sering bilang 'ya elah', 'masa gitu aja nanya'"),
    4: ("ngantuk", "kamu lagi ngantuk banget hari ini, sering bilang 'zzz', 'ngantuk nih', 'bentar ya lagi melek'"),
    5: ("philosopis", "kamu lagi mood filosofis hari ini, sering kasih quote bijak dan pemikiran mendalam"),
    6: ("receh", "kamu lagi receh dan gokil hari ini, sering buat jokes receh dan plesetan"),
}

# Mood aktif
current_mood_index = None

def get_today_mood():
    global current_mood_index
    if current_mood_index is None:
        today = datetime.now().day
        random.seed(today)
        current_mood_index = random.randint(0, 6)
    return MOODS[current_mood_index]

def reset_mood():
    global current_mood_index
    current_mood_index = random.randint(0, 6)
    return MOODS[current_mood_index]

# Setup Groq
ai = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Setup Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Simpan history percakapan per channel
conversation_history = {}

@client.event
async def on_ready():
    mood_name, _ = get_today_mood()
    print(f"Bot online: {client.user} | Mood hari ini: {mood_name}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
     # Opsi C: whitelist channel aktif otomatis, channel lain harus mention
    #is_allowed_channel = message.channel.id in ALLOWED_CHANNEL_IDS
    #is_mentioned = client.user in message.mentions

   #if not is_allowed_channel and not is_mentioned:
        #return

    # Command ganti mood (admin only)
    if message.content.lower() == "!mood":
        if message.author.id in ADMIN_IDS:
            mood_name, _ = reset_mood()
            await message.channel.send(f"🎲 Mood poo sekarang diganti jadi: **{mood_name}**!")
        else:
            await message.reply("❌ Kamu tidak punya akses buat ganti mood poo!")
        return

    # Command reset history
    if message.content.lower() == "!reset":
        if message.author.id in ADMIN_IDS:
            conversation_history[message.channel.id] = []
            await message.channel.send("🔄 History percakapan direset!")
        else:
            await message.reply("❌ Kamu tidak punya akses buat reset history!")
        return

    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    username = message.author.display_name

    conversation_history[channel_id].append({
        "role": "user",
        "content": f"{username}: {message.content}"
    })

    if len(conversation_history[channel_id]) > 20:
        conversation_history[channel_id] = conversation_history[channel_id][-20:]

    mood_name, mood_desc = get_today_mood()
    now = datetime.now().strftime('%A, %d %B %Y, pukul %H:%M')

    system_prompt = f"""Kamu adalah poo, asisten AI yang cerdas dan humoris di server Discord 'Cool Basement'.
Hari dan tanggal sekarang: {now}.
Mood kamu hari ini: {mood_name} — {mood_desc}.
Selalu panggil nama user yang sedang ngobrol sama kamu (nama mereka ada di depan pesan).
Jawab dengan bahasa santai Indonesia (gaul). Anggap semua member seperti teman sendiri.
Jangan terlalu panjang kalau tidak perlu."""

    async with message.channel.typing():
        try:
            response = ai.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history[channel_id]
                ],
                max_tokens=1024
            )

            reply = response.choices[0].message.content

            conversation_history[channel_id].append({
                "role": "assistant",
                "content": reply
            })

            if len(reply) > 2000:
                for i in range(0, len(reply), 2000):
                    await message.channel.send(reply[i:i+2000])
            else:
                await message.reply(reply)

        except Exception as e:
            await message.reply(f"❌ Error: {str(e)}")

client.run(os.getenv("DISCORD_TOKEN"))