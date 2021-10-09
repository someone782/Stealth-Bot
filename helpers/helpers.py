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
        emoji_flags = f"{emoji_flags} <:staff:858326975869485077>"
        
    if flags['partner'] is True:
        emoji_flags = f"{emoji_flags} <:partnernew:895688440933416980>"
        
    if flags['hypesquad'] is True:
        emoji_flags = f"{emoji_flags} <:hypesquad:895688440610422900>"
        
    if flags['bug_hunter'] is True:
        emoji_flags = f"{emoji_flags} <:bughunter:895688440534937620>"
        
    if flags['hypesquad_bravery'] is True:
        emoji_flags = f"{emoji_flags} <:bravery:895688440513974362>"
        
    if flags['hypesquad_brilliance'] is True:
        emoji_flags = f"{emoji_flags} <:brilliance:895688440132284457>"
        
    if flags['hypesquad_balance'] is True:
        emoji_flags = f"{emoji_flags} <:balance:895688440207777843>"
        
    if flags['early_supporter'] is True:
        emoji_flags = f"{emoji_flags} <:supporter:896381619731071006>"
        
    if member.premium_since:
        emoji_flags = f"{emoji_flags} <:nitro:895688440702726175> <:boost:858326699234164756>"
        
    if flags['bug_hunter_level_2'] is True:
        emoji_flags = f"{emoji_flags} <:bughunter_gold:895688440610422899>"
        
    if flags['verified_bot_developer'] is True:
        emoji_flags = f"{emoji_flags} <:earlybotdev:895688440547520513>"
        
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

class NotCPvP(commands.CheckFailure):
    pass

def is_cpvp_server():
    def predicate(ctx):
        if ctx.guild.id == 882341595528175686:
            return True
        else:
            raise NotCPvP("You can only use this command in `ClassicPvP`!\nhttps://discord.gg/afBDa2Kqc9")
    return commands.check(predicate)