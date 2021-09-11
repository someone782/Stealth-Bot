import discord, asyncio, json, yaml
from discord.ext import commands
from discord import VoiceRegion

def get_perms(permissions):
    perms = []
    if permissions.administrator:
        perms.append("Administrator")
        return ["Administrator"]
    if permissions.manage_guild:
        perms.append("Manage guild")
    if permissions.ban_members:
        perms.append("Ban members")
    if permissions.kick_members:
        perms.append("Kick members")
    if permissions.manage_channels:
        perms.append("Manage channels")
    if permissions.manage_emojis:
        perms.append("Manage custom emotes")
    if permissions.manage_messages:
        perms.append("Manage messages")
    if permissions.manage_permissions:
        perms.append("Manage permissions")
    if permissions.manage_roles:
        perms.append("Manage roles")
    if permissions.mention_everyone:
        perms.append("Mention everyone")
    if permissions.manage_emojis:
        perms.append("Manage emojis")
    if permissions.manage_webhooks:
        perms.append("Manage webhooks")
    if permissions.move_members:
        perms.append("Move members")
    if permissions.mute_members:
        perms.append("Mute members")
    if permissions.deafen_members:
        perms.append("Deafen members")
    if permissions.priority_speaker:
        perms.append("Priority speaker")
    if permissions.view_audit_log:
        perms.append("See audit log")
    if permissions.create_instant_invite:
        perms.append("Create instant invites")
    if len(perms) == 0:
        return None
    return perms

def get_member_badges(member):
    author_flags = member.public_flags
    flags = dict(author_flags)
    emoji_flags = ""
    if flags['staff'] is True:
        emoji_flags = f"{emoji_flags} <:staff:860644241800429639>"
    if flags['partner'] is True:
        emoji_flags = f"{emoji_flags} <:partnernew:860644259107569685>"
    if flags['hypesquad'] is True:
        emoji_flags = f"{emoji_flags} <:hypesquad:860644277687943208:>"
    if flags['bug_hunter'] is True:
        emoji_flags = f"{emoji_flags} <:bughunter:860644408353357894>"
    if flags['hypesquad_bravery'] is True:
        emoji_flags = f"{emoji_flags} <:bravery:860644425319710760>"
    if flags['hypesquad_brilliance'] is True:
        emoji_flags = f"{emoji_flags} <:brilliance:860644445435199539>"
    if flags['hypesquad_balance'] is True:
        emoji_flags = f"{emoji_flags} <:balance:860644467933839410>"
    if flags['early_supporter'] is True:
        emoji_flags = f"{emoji_flags} <:supporter:860644501067268106>"
    if member.premium_since:
        emoji_flags = f"{emoji_flags} <:nitro:878983758970257428> <:boost:858326699234164756>"
    if flags['bug_hunter_level_2'] is True:
        emoji_flags = f"{emoji_flags} <:bughunter_gold:850843414953984041>" #not from bots.gg
    if flags['verified_bot_developer'] is True:
        emoji_flags = f"{emoji_flags} <:earlybotdev:850843591756349450>" #not from bots.gg
    if emoji_flags == "": emoji_flags = None
    return emoji_flags

def get_server_region_emote(server : discord.Guild):

    r = discord.VoiceRegion.us_central
    region = server.region

    if region == VoiceRegion.amsterdam:
        return "🇳🇱"
    if region == VoiceRegion.brazil:
        return "🇧🇷"
    if region == VoiceRegion.dubai:
        return "🇦🇪"
    if region == VoiceRegion.eu_central:
        return "🇪🇺"
    if region == VoiceRegion.eu_west:
        return "🇪🇺"
    if region == VoiceRegion.europe:
        return "🇪🇺"
    if region == VoiceRegion.frankfurt:
        return "🇩🇪"
    if region == VoiceRegion.hongkong:
        return "🇭🇰"
    if region == VoiceRegion.india:
        return "🇮🇳"
    if region == VoiceRegion.japan:
        return "🇯🇵"
    if region == VoiceRegion.london:
        return "🇬🇧"
    if region == VoiceRegion.russia:
        return "🇷🇺"
    if region == VoiceRegion.singapore:
        return "🇸🇬"
    if region == VoiceRegion.southafrica:
        return "🇿🇦"
    if region == VoiceRegion.south_korea:
        return "🇰🇷"
    if region == VoiceRegion.sydney:
        return "🇦🇺"
    if region == VoiceRegion.us_central:
        return "🇺🇸"
    if region == VoiceRegion.us_east:
        return "🇺🇸"
    if region == VoiceRegion.us_south:
        return "🇺🇸"
    if region == VoiceRegion.us_west:
        return "🇺🇸"
    if region == VoiceRegion.vip_amsterdam:
        return "🇳🇱🌟"
    if region == VoiceRegion.vip_us_east:
        return "🇺🇸🌟"
    if region == VoiceRegion.vip_us_west:
        return "🇺🇸🌟"
    else:
        return ":x:"

def get_server_region(server : discord.Guild):

    r = discord.VoiceRegion.us_central
    region = server.region

    if region == VoiceRegion.amsterdam:
        return "Amsterdam"
    if region == VoiceRegion.brazil:
        return "Brazil"
    if region == VoiceRegion.dubai:
        return "Dubai"
    if region == VoiceRegion.eu_central:
        return "EU central"
    if region == VoiceRegion.eu_west:
        return "EU west"
    if region == VoiceRegion.europe:
        return "Europe"
    if region == VoiceRegion.frankfurt:
        return "Frankfurt"
    if region == VoiceRegion.hongkong:
        return "Hong Kong"
    if region == VoiceRegion.india:
        return "India"
    if region == VoiceRegion.japan:
        return "Japan"
    if region == VoiceRegion.london:
        return "London"
    if region == VoiceRegion.russia:
        return "Russia"
    if region == VoiceRegion.singapore:
        return "Singapore"
    if region == VoiceRegion.southafrica:
        return "South Africa"
    if region == VoiceRegion.south_korea:
        return "South Korea"
    if region == VoiceRegion.sydney:
        return "Sydney"
    if region == VoiceRegion.us_central:
        return "US Central"
    if region == VoiceRegion.us_east:
        return "US East"
    if region == VoiceRegion.us_south:
        return "US South"
    if region == VoiceRegion.us_west:
        return "US West"
    if region == VoiceRegion.vip_amsterdam:
        return "VIP Amsterdam"
    if region == VoiceRegion.vip_us_east:
        return "VIP US East"
    if region == VoiceRegion.vip_us_west:
        return "VIP US West"
    else:
        return "Unknown region"

class NotSH(commands.CheckFailure):
    pass

def is_sh_server():
    def predicate(ctx):
        if ctx.guild.id == 799330949686231050:
            return True
        else:
            raise NotSH("You can only use this command in `Stealth Hangout`!\ndiscord.gg/ktkXwmD2kF")
    return commands.check(predicate)

class NotCSMP(commands.CheckFailure):
    pass

def is_csmp_server():
    def predicate(ctx):
        if ctx.guild.id == 882341595528175686: return True
        else:
            raise NotCSMP("You can only use this command in `ClassicSMP`!\nhttps://discord.gg/afBDa2Kqc9")
    return commands.check(predicate)

#blacklisted_ids = []

class Blacklisted(commands.CheckFailure):
    pass

def is_user_blacklisted():
    blacklisted_ids = []
    def predicate(ctx):
        if ctx.author.id not in blacklisted_ids: return True
        else:
            raise Blacklisted("It appears that you're blacklisted from this bot. Contact Ender2K89#9999 if you think this is a mistake.")
    return commands.check(predicate)
