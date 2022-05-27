import os
import random
import discord



bot_token = os.environ['bot_token']
prefix ='w?'

word_list = []
global vocab, name_list, mode, leaderboard

mode = "singleplayer"
name_list = []
leaderboard = {}
vocab = []

with open('word_list.txt', "r") as f:
    data = f.read()
    word_list = data.split()

with open('vocab.txt', "r") as f:
    vocab_data = f.read()
    vocab = vocab_data.split()
    print(len(vocab))

global word, game
game = False
word = random.choice(word_list)
print(word)

client = discord.Client()


def check(guess, actual_word):
    global vocab
    guess_list = []
    actual_word_list = []
    return_emoji_list = ['', '', '', '', '']
    for letter in guess:
        guess_list.append(letter)

    for letter1 in actual_word:
        actual_word_list.append(letter1)

    if len(guess_list) > 5 or len(guess_list) < 5:
        return "Give a 5 letter word only please. "
    else:
        if guess.lower() in vocab:
            for i in range(0, 5):
                if guess_list[i] != actual_word_list[i]:
                    return_emoji_list[i] = '⬛'

                if guess_list[i] in actual_word_list:
                    return_emoji_list[i] = '🟨'

                if guess_list[i] == actual_word_list[i]:
                    return_emoji_list[i] = '🟩'

            return return_emoji_list
        else:
            return "Not In my vocabulary, please try again."


def reset_vars():
    global name_list, mode, leaderboard, score_mode
    mode = "singleplayer"
    name_list = []
    leaderboard = {}
    score_mode = False


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Playing wordle in " + str(len(client.guilds)) + " servers!"))
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global word, game, name_list, mode, leaderboard

    if message.author == client.user:
        return
    if "<@bot_user_id>" in message.content:
        welcome = f"""**__👋 I'm WORDZ!__**
      
I'll let you play a game like wordle all inside discord!
      
Use `{prefix}help` to get my commands. 
"""
        await message.channel.send(welcome)
        pass
    if message.content.startswith(prefix + 'help'):
        help = f"""
**Commands listed below** 
`w?info` - Get info about the bot.
`w?wordz` - Play a solo game of ***WORDZ***! 
`w?wordzwar` - Play a mutiplayer game!(use `w?add @user` to add players) 
`w?guess _____` - Guess your entry. 
`w?end` - End game and view leaderboards.
"""
        await message.channel.send(help)
        pass


    if message.content.startswith(prefix + 'invite'):
        invite = f"""
**Thanks for your interest in adding @WORDZ#0587 to your server!** 
Please view my profile and select `ADD TO SERVER`.
"""
        await message.channel.send(invite)



    if message.content.startswith(prefix + 'info'):
        info = f"""
**Thanks for using!**
**Developed & Hosted by:** BankkRoll.ETH#0573")
**Pricing?:** **Free!!** *Buy me a coffee* to help hosting costs, greatly appreciated but not required, thanks!
**Buy me a coffee!:** **ETH**- 0x19C6f06D3ca908F1B276c13e0e0166bD830D992c 
**Invite me by viewing my @WORDZ#0587 profile, select `ADD TO SERVER`.**")
**Contact:** https://twitter.com/bankkroll_eth 
"""
        await message.channel.send(info)
        pass
     
  
    if message.content.startswith(prefix + 'wordz'):
        game = True
        wordz = f"""
*To play multiplayer, use `w?wordzwar` *
**WORDZ is picking a word...**
**Please start with your first guess below `w?guess _____` **
"""
        await message.channel.send(wordz)
        pass

  
    if message.content.startswith(prefix + 'guess'):
        if game:
            if mode == "singleplayer":
                test_word = message.content.replace(prefix + "guess ", "")
                if test_word != word:
                    return_string = check(test_word, word)
                    await message.channel.send(' '.join(return_string), reference=message)

                if test_word == word:
                    old_word = word
                    word = random.choice(word_list)
                    if word == old_word:
                        word = random.choice(word_list)
                    print(word)
                    await message.channel.send("**Guessed the Word Correctly! You win! **")
                    await message.channel.send("**A new word has been set, play again! **")
            elif mode == "multiplayer":
                test_word = message.content.replace(prefix + "guess ", "")
                if test_word.lower() != word:
                    return_string = check(test_word, word)
                    await message.channel.send(' '.join(return_string), reference=message)

                if test_word == word:
                    old_word = word
                    word = random.choice(word_list)
                    if word == old_word:
                        word = random.choice(word_list)
                    print(word)
                    user_id = message.author.id
                    username = "<@" + str(user_id) + ">"
                    await message.channel.send(
                        username + " Guessed the Word Correctly! +5 points ")
                    leaderboard[message.author.name] = leaderboard[message.author.name] + 5

    if message.content.startswith(prefix + 'end'):
        if mode == "singleplayer":
            reset_vars()
            game = False
            await message.channel.send("**Game Over... Hope to see you playing again!**")
        elif mode == "multiplayer":
            game = False

            formatted_msg = []
            for i in leaderboard.keys():
                formatted_msg.append(i)
                formatted_msg.append(" : ")
                formatted_msg.append(str(leaderboard[i]))
                formatted_msg.append("\n")
            await message.channel.send("**Game Ended Final Scores :**")
            await message.channel.send(''.join(formatted_msg))
            reset_vars()

    if message.content.startswith(prefix + "wordzwar"):

        if name_list != []:
            await message.channel.send("**Multiplayer war declared! Goodluck!**\n**GUESS THE WORD NOW FIRST ONE TO GUESS WINS!!**")
            mode = "multiplayer"
            game = True
        else:

            await message.channel.send("**Please add more players for a multiplayer game.**\n**Use `w?add @user` to add them to the game.**\n**Use `w?wordz` to play a game solo.**")
    if message.content.startswith(prefix + "add"):
        stripped_msg = message.content.replace(prefix + "add ", "")
        name_list.append(stripped_msg)

        user_id = message.author.id
        username = "<@" + str(user_id) + ">"
        leaderboard[stripped_msg] = 0

        await message.channel.send(username + " added: " + stripped_msg)


if __name__ == '__main__':
    client.run(bot_token)
