import os
import nextcord

BOT_TOKEN                  = "OTU2MjU1MzA3MzM0NTU3NzQ2.YjtkJw.NapQInn6w-1Hq09ry8GZBbuLRSU"
CMD_PREFIX                 = "!"
INVITE_URL                 = "https://discord.com/api/oauth2/authorize?client_id=956255307334557746&permissions=8&scope=bot"
IHS_GUILD_ID               = 909239991501226034

ERROR_EXCLAMATION_ICON = "https://flyclipart.com/thumb2/alert-danger-error-exclamation-mark-red-icon-227724.png"
SPINNING_COIN_GIF      = "https://cdn.dribbble.com/users/6257/screenshots/3833147/coin.gif"




FINAL_READY_PRINT      = "--------------------------------------we out--------------------------------------"
DB_CHECK_READY_PRINT   = "------------------------------------DB CHECK DONE---------------------------------"

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
    "None":{
        "color":(255, 255, 255)
    },
    "Person":{
        "color":(241, 242, 22)
    },
    "Worker":{
        "color":(241, 118, 28)
    },
    "Comrade":{
        "color":(255, 36, 19)
    },
    "Revolutionary":{
        "color":(182, 26, 14)
    },
}


USER_DATABASE_PATH      = os.path.join(os.path.dirname(__file__),r"./Databases/users.json")
GUILD_DATABASE_PATH     = os.path.join(os.path.dirname(__file__),r"./Databases/guilds.json")
