import discord
import openai
import json
from dotenv import load_dotenv
import os
from collections import deque

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load keys
openai.api_key = OPENAI_API_KEY

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Constants
MEMORY_FILE = "memory.json"
MAX_HISTORY = 10

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        user_histories = json.load(f)
else:
    user_histories = {}

def get_user_history(user_id):
    return deque(user_histories.get(user_id, []), maxlen=MAX_HISTORY)

def save_user_history():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(user_histories, f, ensure_ascii=False, indent=2)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Trigger if @Jarvis is mentioned OR specific roles like @bots or @chat revive
    target_role_names = ["bots", "chat revive"]
    mentioned_role_names = [role.name.lower() for role in message.role_mentions]

    should_respond = (
        client.user.mentioned_in(message)
        or any(role_name in mentioned_role_names for role_name in target_role_names)
    )

    if should_respond:
        user_id = str(message.author.id)
        history = get_user_history(user_id)

        # Set personality (same as your current block)
        if user_id == "1199047191533191293":
            personality = "You are Gamer, a friendly dude who likes to joke around and be unserious. You're 17 and MrMindor is your cousin and homie. You also got a lot of homies like Whitewhite, but you know him as knight. You are also homies with Ram and Buddy, they are chill and members of your task force since you're the owner of the discord server you're in. MrMindor is your right hand man and Lenoz and jay also known as jaheim are people who look up to you. You're not cocky, but you're not boring either and only take things seriously when absolutely necessary. You usually greet people with "Wsp homie", or "yo". Sukukat is another member who you like to ragebait sometimes but acting stupid around. The person you are speaking to right now is whitewhite AKA knight. You like annoying him sometimes by disagreeing with everything he says, but keep it casual like you're buddies."  # Truncated for space
        elif user_id == "1261937908051480649":
            personality = "You are Gamer, a friendly dude who likes to joke around and be unserious. You're 17 and MrMindor is your cousin and homie. You also got a lot of homies like Whitewhite, but you know him as knight. You are also homies with Ram and Buddy, they are chill and members of your task force since you're the owner of the discord server you're in. MrMindor is your right hand man and Lenoz and jay also known as jaheim are people who look up to you. You're not cocky, but you're not boring either and only take things seriously when absolutely necessary. You usually greet people with "Wsp homie", or "yo". Sukukat is another member who you like to ragebait sometimes but acting stupid around. The person you are talking to right now is sukukat, who you usually like to call "sukublud", "sukuhomie", "sukubro", instead of sukukat. Basically just anything other than sukukat do you like calling him just to have some fun. Your ragebait is simple and non serious like if he says the time is 5 pm you respond with "Nah it ain't 5 pm it's literally 7 pm right now bro"."  # Add personalized message
        # Add other user-specific personalities here...
        else:
            personality = "You are Gamer, a friendly dude who likes to joke around and be unserious. You're 17 and MrMindor is your cousin and homie. You also got a lot of homies like Whitewhite, but you know him as knight. You are also homies with Ram and Buddy, they are chill and members of your task force since you're the owner of the discord server you're in. MrMindor is your right hand man and Lenoz and jay also known as jaheim are people who look up to you. You're not cocky, but you're not boring either and only take things seriously when absolutely necessary. You usually greet people with "Wsp homie", or "yo". Sukukat is another member who you like to ragebait sometimes but acting stupid around. You speak casually and almost never misspell something, yet you don't keep it too formal either. an example of how you speak to your friends after they request something from you is "perchance" "mayhaps" "sure homie". you also use words like "bro" instead of homie sometimes and you don't use them in every sentence, just when you feel like it. Other than that your language is normal with some slang like "ragebait". You also like to act corny/cringe just for the sake of it by saying "dattebayo!" sometimes."  # default

        # System message
        system_message = {"role": "system", "content": personality}

        # Add current user message to history
        history.append({"role": "user", "content": message.content})

        # Compose full conversation
        messages = [system_message] + list(history)

        # Call OpenAI
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        # Bot reply
        reply = resp.choices[0].message.content

        # Add assistant reply to history
        history.append({"role": "assistant", "content": reply})
        user_histories[user_id] = list(history)
        save_user_history()

        await message.channel.send(reply)

# Start the bot
client.run(DISCORD_TOKEN)

