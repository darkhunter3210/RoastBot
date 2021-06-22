import discord
import os
import requests
from replit import db
from keep_alive import keep_alive

client = discord.Client()

def get_quote(name):
    base_url = "https://insult.mattbas.org/api/insult.txt?who={}"
    url = base_url.format(name)
    response = requests.get(url)
    return response.text

def add_roast(key_word,roast_line):
  if key_word in db:
    return "Joke already in database"
  else:
    db[key_word] = roast_line
    return "New Joke added"

def update_joke(key_word,roast_line):
  if key_word in db:
    db[key_word] = roast_line
    return "Joke Updated"
  else:
    return "Joke not found"

def delete_roast(key_word):
  if key_word in db:
    del db[key_word]
    return "Joke Deleted"
  else:
    return "Cannot find joke"



def get_random():
    url = "https://insult.mattbas.org/api/insult.txt"
    response = requests.get(url)
    return response.text


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content 
    check_message = msg.lower()
    arr = check_message.split()

    if msg.startswith('$random'):
        quote = get_random()
        await message.channel.send(quote)

    elif msg.startswith('$roast'):
        person = arr[1].capitalize()
        if person == "Matthew" or person == "Matt":
            quote = "Cannot roast the roast master"
        else:
            quote = get_quote(person)
        await message.channel.send(quote)
    
    elif msg.startswith('$new'):
        if len(arr) < 3:
            await message.channel.send("Must have both the key word and the Joke")
        else:
            key_word = arr[1]        
            roast_arr = arr[2:]
            roast_line = " "
            roast_line = roast_line.join(roast_arr)
            await message.channel.send(add_roast(key_word,roast_line))
      
    elif msg.startswith('$update'):
        if len(arr) < 3:
            await message.channel.send("Must have both the key word and the Joke")
        else:
            key_word = arr[1]        
            roast_arr = arr[2:]
            roast_line = " "
            roast_line = roast_line.join(roast_arr)
            await message.channel.send(update_joke(key_word,roast_line))
    
    elif msg.startswith('$del'):
      await message.channel.send(delete_roast(arr[1]))

    elif any(word in msg.lower() for word in db.keys()):
        for x in arr:
            if not x.isalpha():
                x = x[:-1]
            if x in db:
                roast_line = db.get(x)
                roast_line = roast_line.capitalize()
                await message.channel.send(roast_line)



keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)


