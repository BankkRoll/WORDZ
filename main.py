import os
import random
import discord



bot_token = os.environ['bot_token']
client = discord.Client()

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
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global word, game, name_list, mode, leaderboard

    if message.author == client.user:
        return
    if message.content.startswith('w?help'):
      
        await message.channel.send("**Commands listed below** ")
        await message.channel.send("`w?info` - Get info about the bot.")
        await message.channel.send("`w?wordz` - Play a solo game of ***WORDZ***! ")
        await message.channel.send("`w?wordzwar` - Play a mutiplayer game!(use `w?add @user` to add players) ")
        await message.channel.send("`w?guess _____` - Guess your entry. ")
        await message.channel.send("`w?end` - End game and view leaderboards. ")


    if message.content.startswith('w?invite'):

        await message.channel.send("**Thanks for your interest in adding @WORDZ#0587 to your server!** ")
        await message.channel.send("Please view my profile and select `ADD TO SERVER`. ")
        



    if message.content.startswith('w?info'):
        
        await message.channel.send("**Thanks for using!**")
        await message.channel.send("**Developed & Hosted by:** BankkRoll.ETH#0573")
        await message.channel.send("**Pricing?:** **Free!!** *Buy me a coffee* to help hosting costs, greatly appreciated but not required, thanks!")
        await message.channel.send("**Buy me a coffee!:** **ETH**- 0x19C6f06D3ca908F1B276c13e0e0166bD830D992c ")
        await message.channel.send("**Invite me by viewing my @WORDZ#0587 profile, select `ADD TO SERVER`.**")
        await message.channel.send("**Contact:** https://twitter.com/bankkroll_eth ")
        

     
  
    if message.content.startswith('w?wordz'):
        game = True
        await message.channel.send("*To play multiplayer, use `w?wordzwar` *")
        await message.channel.send("**WORDZ is starting...** ")
        await message.channel.send("**3...**")
        await message.channel.send("**2..**")
        await message.channel.send("**1.**")
        await message.channel.send("**Please start with your first guess below `w?guess _____` **")



  
    if message.content.startswith('w?guess'):
        if game:
            if mode == "singleplayer":
                test_word = message.content.replace("w?guess ", "")
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
                test_word = message.content.replace("w?guess ", "")
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

    if message.content.startswith('w?end'):
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

    if message.content.startswith("w?wordzwar"):

        if name_list != []:
            await message.channel.send("**Multiplayer war declared! Goodluck!** ")
            await message.channel.send("**GUESS THE WORD NOW FIRST ONE TO GUESS WINS!!**")
            mode = "multiplayer"
            game = True
        else:

            await message.channel.send("**Please add more players for a multiplayer game.**")
            await message.channel.send("**Use `w?add @user` to add them to the game.**")
            await message.channel.send("**Use `w?wordz` to play a game solo.**")
    if message.content.startswith("w?add"):
        stripped_msg = message.content.replace("w?add ", "")
        name_list.append(stripped_msg)

        user_id = message.author.id
        username = "<@" + str(user_id) + ">"
        leaderboard[stripped_msg] = 0

        await message.channel.send(username + " added: " + stripped_msg)


if __name__ == '__main__':
    client.run(bot_token)
