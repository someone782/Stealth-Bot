import discord, asyncio, json, yaml
from discord.ext import commands

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

class NotSH(commands.CheckFailure):
    pass

def is_sh_server():
    def predicate(ctx):
        # a function that takes ctx as it's only arg, that returns
        # a truethy or falsey value, or raises an exception
        if ctx.guild.id == 799330949686231050: return True
        else: raise NotSH("You can only use this command in `Stealth Hangout`!\ndiscord.gg/ktkXwmD2kF")
    return commands.check(predicate)
