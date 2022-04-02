import os
import nextcord

BOT_TOKEN                  = "OTU2MjU1MzA3MzM0NTU3NzQ2.YjtkJw.EsUkd258oS6Zasr-q1u0Pg9agtQ"
CMD_PREFIX                 = "!"
INVITE_URL                 = "https://discord.com/api/oauth2/authorize?client_id=956255307334557746&permissions=8&scope=bot"
IHS_GUILD_ID               = 909239991501226034

ERROR_EXCLAMATION_ICON = "https://flyclipart.com/thumb2/alert-danger-error-exclamation-mark-red-icon-227724.png"
SPINNING_COIN_GIF      = "https://cdn.dribbble.com/users/6257/screenshots/3833147/coin.gif"
FLAG_IMG               = "https://cdn.britannica.com/90/7490-004-BAD4AA72/Flag-China.jpg"


FINAL_READY_PRINT      = "--------------------------------------we out--------------------------------------"
DB_CHECK_READY_PRINT   = "------------------------------------DB CHECK DONE---------------------------------"


# BANNED_WORDS           = {
#     "mukund": {
#         "penalty":10
#     }
# }
BANNED_WORDS           = [
    "mukund"
]

BANNED_WORDS_PENALTY   = 10
DAILY_BONUS_REWARD     = 15
SHAME_PENALTY   = 10
MINIMUM_SHAME_VOTES = 5

TRIVIA_REWARD          = 30
TRIVIA_PENALTY         = 45
ALPHABET               = [":A:",":B:",":C:",":D:",":E:",":F:",":G:"]
TRIVIA_TIME_LIMIT      = 25

USER_DATABASE_DEFAULTS = {
    "needsUpdate":True,
    "socialCredit":0,
    "rank":"None"
}
GUILD_DATABASE_DEFAULTS = {
    "needsUpdate":True,
    "socialCredit":0,
    "victories":0,
    "prefix":"!"
}

RANK_ROLES = {
    "Felon":{
        "minSocialCredit":-10000,
        "color":(50, 50, 50),
        "desc":"keeps breaking rules, or is just hated by the admins"
    },
    "None":{
        "minSocialCredit":0,
        "color":(255, 255, 255),
        "desc":"Go get social credit"
    },
    "Person":{
        "minSocialCredit":100,
        "color":(241, 242, 22),
        "desc":"Go get more social credit"
    },
    "Worker":{
        "minSocialCredit":1000,
        "color":(241, 118, 28),
        "desc":"fulfull your quota."
    },
    "Comrade":{
        "minSocialCredit":10000,
        "color":(255, 36, 19),
        "desc":"welcome, comrade."
    },
    "Revolutionary":{
        "minSocialCredit":25000,
        "color":(182, 26, 14),
        "desc":"sheeeeesh, go outside for once"
    },
}


USER_DATABASE_PATH      = os.path.join(os.path.dirname(__file__),r"./Databases/users.json")
GUILD_DATABASE_PATH     = os.path.join(os.path.dirname(__file__),r"./Databases/guilds.json")
