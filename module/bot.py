from random import randint
import youtube_dl
import discord

# PREP
prefix = '-'
pronoun = 'sir'
version = '0.1.3'

queue = {}
voiceChannelClient = {}

client = discord.Client()
commandsGeneral = ['help', 'queue']
commandsAudio = ['play', 'pause', 'resume', 'rickroll']
commandsAdmin = ['pronoun', 'thebeast', 'dock', 'bonus']

dialogueHelp = ["These Are Wi'in My Paycheck, " + pronoun.capitalize(), "These Are Wi'in My Paycheck", "How May I Be Of Assistance, " + pronoun.capitalize() + '?', 'How May I Be Of Assistance?']
dialoguePlay = ['Of Course, ' + pronoun.capitalize(), 'Of Course, ' + pronoun.capitalize() + ". I'll Put It In The Gramophone Now", 'As You Wish']
dialogueQueue = ['Your Queue, ' + pronoun.capitalize(), 'These Are Our Records, ' + pronoun.capitalize(), 'I Have These Records Ready To Play']
dialoguePause = ['Of Course, ' + pronoun.capitalize(), 'It Will Be There When You Get Back, ' + pronoun.capitalize()]
dialogueResume = ['Of Course, ' + pronoun.capitalize()]

for i in range(len(commandsGeneral)):
    commandsGeneral[i] = prefix + commandsGeneral[i]
for i in range(len(commandsAudio)):
    commandsAudio[i] = prefix + commandsAudio[i]

# HELPER FUNCTIONS
def ParsePlayCommand(message):
    splitMessage = message.content.split(' ')
    if message.content.count(' ') == 1 and len(splitMessage) == 2:
        info = splitMessage[1]
        return info
    else:
        return None

def ParseYouTubeLink(link):
    dl = youtube_dl.YoutubeDL({'format': 'bestaudio'})
    info = dl.extract_info(link, download = False)
    info = {
        'id': info['id'],
        'title': info['title'],
        'url': link,
        'urlAUDIO': info['url']
    }
    return info

def PlayFromQueue(guild, index):
    if type(queue[guild]) is dict:
        url = queue[guild]['urlAUDIO']
    else:
        url = queue[guild][index]['urlAUDIO']
    voiceChannelClient[guild].play(discord.FFmpegPCMAudio(source = url), after = lambda e: FinishedPlaying(guild))

def FinishedPlaying(guild):
    if type(queue[guild]) is list:
        del queue[guild][0]
    else:
        del queue[guild]
    try:
        PlayFromQueue(guild, 0)
    except KeyError:
        pass

# COMMANDS
async def Help(content, channel):
    content = content.lower().split(' ')
    randomDialogue = dialogueHelp[randint(0, len(dialogueHelp) - 1)]
    
    if len(content) == 1:
        embed = discord.Embed(title = '**' + randomDialogue + '**', description = '_' + pronoun.capitalize() + ', you can use ``-help <category>`` to view commands\nYour prefix_: ' + prefix, color=0xff0000)
        embed.add_field(name = '**General**', value = '``General-Use Commands``', inline = False)
        embed.add_field(name = '**Audio**', value = '``Commands Specific To Audio``', inline = False)
        embed.add_field(name = '**Admin**', value = '``Commands Specific To Admins``', inline = False)
        embed.set_footer(text = 'Geoffrey v' + version)
        await channel.send(embed=embed)
    else:
        if content[1] == 'general':
            embed = discord.Embed(title = '**' + randomDialogue + '**', description = '_' + pronoun.capitalize() + ', you can use ``' + prefix + '<command>`` to use a command\nYour prefix_: ' + prefix, color=0xff0000)
            embed.add_field(name = '**Help**', value = '``Is My Assistance Needed?``', inline = False)
            embed.add_field(name = '**Queue**', value = '``Would You Like To See The Records, ' + pronoun.capitalize() + '?``', inline = False)
            embed.set_footer(text = 'Geoffrey v' + version)
            await channel.send(embed=embed)
        if content[1] == 'audio':
            embed = discord.Embed(title = '**' + randomDialogue + '**', description = '_' + pronoun.capitalize() + ', you can use ``' + prefix + '<command>`` to use a command\nYour prefix_: ' + prefix, color=0xff0000)
            embed.add_field(name = '**Play <link>**', value = '``Would You Like To Choose A Tune For The Gramophone?\nI Support Both YouTube And Spotify``', inline = False)
            embed.add_field(name = '**Pause**', value = '``I Could Stop The Record, Sir``', inline = False)
            embed.add_field(name = '**Resume**', value = '``I Could Also Resume The Record, If You Wish``', inline = False)
            embed.add_field(name = '**Rickroll**', value = '``This One Has Special Meaning To You, Correct?``', inline = False)
            embed.set_footer(text = 'Geoffrey v' + version)
            await channel.send(embed=embed)
        if content[1] == 'admin':
            embed = discord.Embed(title = '**' + randomDialogue + '**', description = '_' + pronoun.capitalize() + ', you can use ``' + prefix + '<command>`` to use a command\nYour prefix_: ' + prefix, color=0xff0000)
            embed.add_field(name = '**Pronoun**', value = '``How Shall I Refer To You?``', inline = False)
            embed.add_field(name = '**TheBeast**', value = "``Shall I Bring Out My Wil'er Side?\ntrue`` or ``false``", inline = False)
            embed.add_field(name = '**Dock**', value = "``Have I Made A Mis'ake, " + pronoun.capitalize() + '? Shall I Take Less Payment?``', inline = False)
            embed.add_field(name = '**Bonus**', value = "``I'm Always Happy To Take A Tip``", inline = False)
            embed.set_footer(text = 'Geoffrey v' + version)
            await channel.send(embed=embed)

async def Play(message, rickroll = False):
    if rickroll:
        await message.channel.send('Rickrolling\n``' + message.author.voice.channel.name + '``')
        return

    info = ParsePlayCommand(message)
    if info == None:
        await message.channel.send("I'm unable to play that song, " + pronoun + '. Your command is not formatted correctly')
    else:
        try:
            info = ParseYouTubeLink(info)
        except youtube_dl.utils.DownloadError:
            await message.channel.send('Searching for _')

        if message.guild.id in queue:
            if type(queue[message.guild.id]) is list:
                queue[message.guild.id].append(info)
            else:
                queue[message.guild.id] = [queue[message.guild.id], info]
            randomDialogue = dialoguePlay[randint(0, len(dialoguePlay) - 1)]
            await message.channel.send('**' + randomDialogue + '**\nAdding ``' + info['url'] + '`` to queue')
        else:
            if message.guild.id not in voiceChannelClient:
                voiceChannelClient[message.guild.id] = await message.author.voice.channel.connect()
            queue[message.guild.id] = info
            PlayFromQueue(message.guild.id, 0)
            randomDialogue = dialoguePlay[randint(0, len(dialoguePlay) - 1)]
            await message.channel.send('**' + randomDialogue + '**\n_Now Playing:_ ``' + info['url'] + '``')

async def Queue(channel):
    randomDialogue = dialogueQueue[randint(0, len(dialogueQueue) - 1)]
    embed = discord.Embed(title = '**' + randomDialogue + '**', color=0xff0000)

    queueTxt = ''
    if type(queue[channel.guild.id]) is list:
        embed.add_field(name = '__Current Song:__', value = '``' + queue[channel.guild.id][0]['title'] + '``', inline = False)
        for song in queue[channel.guild.id][1:]:
            queueTxt = queueTxt + '\n``' + song['title'] + '``'
        if queueTxt == '':
            queueTxt = '\u200b'
        embed.add_field(name = '__Queue:__', value = queueTxt, inline = False)
    else:
        embed.add_field(name = '__Current Song:__', value = '``' + queue[channel.guild.id]['title'] + '``', inline = False)

    embed.set_footer(text = 'Geoffrey v' + version)

    await channel.send(embed = embed)

async def Pause(channel):
    guild = channel.guild.id
    randomDialogue = dialoguePause[randint(0, len(dialoguePause) - 1)]
    try:
        if type(queue[guild]) is list:
            await channel.send('**' + randomDialogue + '**\n_Pausing_ ``' + queue[guild][0]['title'] + '``')
        else:
            await channel.send('**' + randomDialogue + '**\n_Pausing_ ``' + queue[guild]['title'] + '``')
        voiceChannelClient[guild].pause()
    except KeyError:
        await channel.send("There's nothing to pause, " + pronoun)

async def Resume(channel):
    guild = channel.guild.id
    randomDialogue = dialogueResume[randint(0, len(dialogueResume) - 1)]
    try:
        if type(queue[guild]) is list:
            await channel.send('**' + randomDialogue + '**\n_Resuming_ ``' + queue[guild][0]['title'] + '``')
        else:
            await channel.send('**' + randomDialogue + '**\n_Resuming_ ``' + queue[guild]['title'] + '``')
        voiceChannelClient[guild].resume()
    except KeyError:
        await channel.send("There's nothing to resume, " + pronoun)

# LOGIC
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)

@client.event
async def on_message(message):
    msg = message.content.lower()
    channel = message.channel
    if message.author == client.user or message.author.bot == True:
        return

    if msg.startswith(tuple(commandsGeneral)):
        if msg.startswith(commandsGeneral[0]):
            await Help(message.content, channel)
        elif msg.startswith(commandsGeneral[1]):
            await Queue(channel)
    
    elif msg.startswith(tuple(commandsAudio)):
        if message.author.voice == None:
            await message.channel.send('Unable To Play Audio:\n``You Must Be In A Voice Channel to Use This Command``')
            return
        if msg.startswith(commandsAudio[0]):
            await Play(message)
        elif msg.startswith(commandsAudio[1]):
            await Pause(channel)
        elif msg.startswith(commandsAudio[2]):
            await Resume(channel)
        elif msg.startswith(commandsAudio[3]):
            await Play(message, rickroll = True)
            
client.run('TOKEN HERE')

