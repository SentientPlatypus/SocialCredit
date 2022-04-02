from ast import excepthandler
from more_itertools import first
import nextcord
import constants
from pymongo import MongoClient
import gspread
import pandas as pd
import requests
import random
from socialCreditHandler import socialCreditHandler



def getNumMembers(client):
    membersz=0
    for x in client.guilds:
        membersz+=len(x.members)+1
    return membersz

async def updatePresence(client):
    await client.change_presence(
        status=nextcord.Status.online, 
        activity=nextcord.Game(
            name = "%shelp %s comrades"%(
                constants.CMD_PREFIX, getNumMembers(client)
                )
            )
        )

async def handleBadWords(message:nextcord.Message):
    if any(word in constants.BANNED_WORDS for word in message.content.lower().split(" ")):
        # foundBannedWord = returnHighestPenaltyBannedWord(message)
        # if foundBannedWord:
        await message.delete()
        # penalty = constants.BANNED_WORDS[foundBannedWord]["penalty"]
        penalty = constants.BANNED_WORDS_PENALTY
        await socialCreditHandler.updateSocialCredit(message.guild, message.author, -penalty)
        em = nextcord.Embed(title = "Banned word detected", description= f"```{message.author.display_name} will lose {penalty} social credit```")
        em.color = nextcord.Color.red()
        em.timestamp = message.created_at
        await message.channel.send(embed=em)
    
def returnHighestPenaltyBannedWord(message:nextcord.Message):
    highestPenaltyWord = None
    content = message.content.split(" ")
    for word in content:
        for bannedWord in constants.BANNED_WORDS.keys():
            if word == bannedWord:
                try:
                    if constants.BANNED_WORDS[highestPenaltyWord]["penalty"] < constants.BANNED_WORDS[bannedWord]["penalty"]:
                        highestPenaltyWord = bannedWord
                except:
                    highestPenaltyWord = bannedWord
    return highestPenaltyWord



def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"


class TriviaQuestion:
    def __init__(self, question:str, incorrectAnswers:list, correctAnswer:str, category:str, ) -> None:
        self.question = question
        self.incorrectAnswers = incorrectAnswers
        self.correctAnswer = correctAnswer
        self.category = category





    def initializeAnswers(self):
        self.allAnswers = self.incorrectAnswers
        self.allAnswers.append(self.correctAnswer)
        self.allAnswers = random.shuffle(self.allAnswers)
        self.optionStr = ""
        self.optionDict = {}
        for i in range(len(self.allAnswers)):
            self.optionStr += constants.ALPHABET[i] + ": " + self.allAnswers[i] + "\n"
            self.optionDict[constants.ALPHABET[i]] = self.allAnswers[i]





def getTriviaQuestion() -> TriviaQuestion:
    data = requests.get("https://opentdb.com/api.php?amount=1&difficulty=hard&type=multiple").json()
    print(data)
    firstRes = data["results"][0]
    q = TriviaQuestion(
        question=firstRes["question"],
        category=firstRes["category"],
        correctAnswer=firstRes["correct_answer"],
        incorrectAnswers=firstRes["incorrect_answers"]
    )
    q.initializeAnswers()
    return q
        