import discord
import datetime
import io
import helpers
import unicodedata
import time
import aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
import threading
from platform import python_version
import asyncio
from roblox_py import Client
roblox_py_client = Client()
pythonVersion = python_version()
start_time = time.time()

class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, item):
        embed = discord.Embed(title="Character information", description="\n".join(item), timestamp=discord.utils.utcnow(), color=0x2F3136)
        #embed.set_footer(text=f"Command requested by {self.context.author}", icon_url=self.context.author.avatar.url)

        return embed

class info(commands.Cog):
    "All informative commands like `serverinfo`, `userinfo` and more!"
    def __init__(self, client):
        self.client = client
        client.session = aiohttp.ClientSession()

    @commands.command(help="Shows you information about the member you mentioned", aliases=['ui', 'user', 'member', 'memberinfo'], brief="https://cdn.discordapp.com/attachments/878984821081272401/878986523423416370/userinfo.gif")
    @commands.cooldown(1, 5, BucketType.member)
    async def userinfo(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        fetchedMember = await self.client.fetch_user(member.id)

        if member.bot == True:
            botText = "Yes"
        else:
            botText = "No"

        if member.premium_since == None:
            premiumText = "Not boosting"
        else:
            premiumText = f"{discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"

        if str(member.status).title() == "Online":
            statusEmote = "<:status_online:596576749790429200>"
        elif str(member.status).title() == "Idle":
            statusEmote = "<:status_idle:596576773488115722>"
        elif str(member.status).title() == "Dnd":
            statusEmote = "<:status_dnd:596576774364856321>"
        elif str(member.status).title() == "Streaming":
            statusEmote = "<:status_streaming:596576747294818305>"
        else:
            statusEmote = "<:status_offline:596576752013279242>"

        roles = ""
        for role in member.roles:
            if role is ctx.guild.default_role: continue
            roles = f"{roles} {role.mention}"
        if roles != "":
            roles = f"{roles}"

        badges = helpers.get_member_badges(member)
        if badges: badges = f"{badges}"
        else: badges = ''

        perms = helpers.get_perms(member.guild_permissions)
        if perms: perms = f"{', '.join(perms)}"
        else: perms = ''

        embed = discord.Embed(title=f"Userinfo - {member}", description=f"""
Name: {member}
<:nickname:876507754917929020> Nickname: {member.nick}
Discriminator:  #{member.discriminator}
Display name: {member.mention}
<:greyTick:860644729933791283> ID: {member.id}
:robot: Bot?: {botText}
<a:nitro_wumpus:857636144875175936> Boosting: {premiumText}
<:invite:860644752281436171> Created: {discord.utils.format_dt(member.created_at, style="f")} ({discord.utils.format_dt(member.created_at, style="R")})
<:member_join:596576726163914752> Joined: {discord.utils.format_dt(member.joined_at, style="f")} ({discord.utils.format_dt(member.joined_at, style="R")})
<:moved:848312880666640394> Join position: {sorted(ctx.guild.members, key=lambda member : member.joined_at).index(member) + 1}
Mutual guilds: {len(member.mutual_guilds)}
{statusEmote} Current status: {str(member.status).title()}
:video_game: Current activity: {str(member.activity.type).split('.')[-1].title() if member.activity else 'Not playing'} {member.activity.name if member.activity else ''}
<:role:876507395839381514> Top Role: {member.top_role.mention}
<:role:876507395839381514> Roles: {roles}
<:store_tag:860644620857507901> Staff permissions: {perms}
<:store_tag:860644620857507901> Badges: {badges}
:rainbow: Color: {member.color}
:rainbow: Accent color: {fetchedMember.accent_color}
        """, timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed, mention_author=False)


    @commands.command(help="Shows you information about the server", aliases=['si', 'guild', 'guildinfo'])
    @commands.cooldown(1, 5, BucketType.member)
    async def serverinfo(self, ctx):
        server = ctx.guild

        if ctx.me.guild_permissions.ban_members:
            bannedMembers = len(await server.bans())
        else:
            bannedMembers = "Couldn't get banned members."

        statuses = [len(list(filter(lambda m: str(m.status) == "online", server.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", server.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", server.members))),
                    len(list(filter(lambda m: str(m.status) == "streaming", server.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", server.members)))]

        region = f"{str(server.region).title().replace('-', ' ').replace('_', ' ').replace('Us', 'US')}"

        if region == "Brazil":
            regionEmote = "🇧🇷"
        elif region == "Europe":
            regionEmote = "🇪🇺"
        elif region == "Hong Kong":
            regionEmote = "🇭🇰"
        elif region == "India":
            regionEmote = "🇮🇳"
        elif region == "Russia":
            regionEmote = "🇷🇺"
        elif region == "Singapore":
            regionEmote = "🇸🇬"
        elif region == "South Africa":
            regionEmote = "🇿🇦"
        elif region == "Sydney":
            regionEmote = "🇦🇺"
        elif region == "US East":
            regionEmote = "🇺🇸"
        elif region == "US South":
            regionEmote = "🇺🇸"
        elif region == "US West":
            regionEmote = "🇺🇸"
        elif region == "US Central":
            regionEmote = "🇺🇸"
        else:
            regionEmote = "N/A "

        embed = discord.Embed(title=f"Server info - {server}", description=f"""
Name: {server}
<:greyTick:860644729933791283> ID: {server.id}
<:members:858326990725709854> Members: {len(server.members)} (:robot: {len(list(filter(lambda m : m.bot, server.members)))})
:robot: Bots: {len(list(filter(lambda m: m.bot, server.members)))}
<:owner_crown:845946530452209734> Owner: {server.owner}
Created: {discord.utils.format_dt(server.created_at, style="f")} ({discord.utils.format_dt(server.created_at, style="R")})
{regionEmote} Region: {str(server.region).title().replace('-', ' ').replace('_', ' ').replace('Us', 'US')}
<:members:858326990725709854> Max members: {server.max_members}
<:bans:878324391958679592> Banned members: {bannedMembers}
<:status_offline:596576752013279242> Statuses: <:status_online:596576749790429200> {statuses[0]} <:status_idle:596576773488115722> {statuses[1]} <:status_dnd:596576774364856321> {statuses[2]} <:status_streaming:596576747294818305> {statuses[3]} <:status_offline:596576752013279242> {statuses[4]}
<:text_channel:876503902554578984> Channels: <:text_channel:876503902554578984> {len(server.text_channels)} <:voice_channel:876503909512933396> {len(server.voice_channels)}
<:role:876507395839381514> Roles: {len(server.roles)}
:sunglasses: Animated emojis: {len([x for x in server.emojis if x.animated])}/{server.emoji_limit}
:sunglasses: Non animated emojis: {len([x for x in server.emojis if not x.animated])}/{server.emoji_limit}
<:boost:858326699234164756> Level: {server.premium_tier}
<:boost:858326699234164756> Boosts: {server.premium_subscription_count}
        """)

        if server.banner:
            url1 = server.banner.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_thumbnail(url=url)


        if server.icon:
            url1 = server.icon.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_thumbnail(url=url)

        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows information about the bot", aliases=['bi', 'bot', 'info', 'about'])
    async def botinfo(self, ctx):
        current_time = time.time()
        threads = threading.activeCount()

        embed = discord.Embed(title=f"Bot info - Stealth Bot [-]#1082", description=f"""
Developer: Ender2K89#9999
Ping: {round(self.client.latency * 1000)}ms
Threads: {threads}
Uptime: {self.client.launch_time}
Python version: {pythonVersion}
Discord.py version: {discord.__version__}
Prefixes: <@760179628122964008>, `{ctx.prefix}`
Servers: {len(self.client.guilds)}
Total users: {len(self.client.users)}
Cogs: {len(self.client.cogs)}
""", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url = ctx.author.avatar.url)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows the avatar of the member you mentioned", aliases=['av'])
    async def avatar(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
        if member.avatar:
            if member.avatar.is_animated() == True:
                text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url}) | [GIF]({member.avatar.replace(format='gif', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
            else:
                text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed=discord.Embed(title=f"{member}'s avatar", description=f"{text}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            url1 = member.avatar.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_image(url=url)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("You don't have a avatar.")

    @commands.command(help="Shows the banner of the member you mentioned", aliases=['bn'])
    @commands.cooldown(1, 5, BucketType.member)
    async def banner(self, ctx, member : discord.Member=None):
        errorMessage = f"{member} doesn't have a banner."
        if member == None or member == ctx.author:
            member = ctx.author
            errorMessage = "You don't have a banner"

        fetchedMember = await self.client.fetch_user(member.id)

        if fetchedMember.banner:
            if fetchedMember.banner.is_animated() == True:
                text1 = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
            else:
                text1 = f"[PNG]({fetchedMember.avatar.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed=discord.Embed(title=f"{member}'s avatar", description=f"{text}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            url1 = fetchedMember.banner.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_image(url=url)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(f"{errorMessage}")

    @commands.command(help="Shows you the bot's latency")
    @commands.cooldown(1, 5, BucketType.member)
    async def ping(self, ctx):
        pings = []
        number = 0

        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = (typinge - typings) * 1000
        pings.append(typingms)

        start = time.perf_counter()
        message = await ctx.reply("Getting ping...", mention_author=False)
        end = time.perf_counter()
        messagems = (end - start) * 1000
        pings.append(messagems)

        discords = time.monotonic()
        url = "https://discordapp.com/"
        async with self.client.session.get(url) as resp:
            if resp.status == 200:
                discorde = time.monotonic()
                discordms = (discorde - discords) * 1000
                pings.append(discordms)
            else:
                discordms = 0

        latencyms = self.client.latency * 1000
        pings.append(latencyms)

        pstart = time.perf_counter()
        await self.client.db.fetch("SELECT 1")
        pend = time.perf_counter()
        psqlms = (pend - pstart) * 1000
        pings.append(psqlms)

        for ms in pings:
            number += ms
        average = number / len(pings)

        websocket_latency = f"{round(latencyms)}ms{' ' * (9-len(str(round(latencyms, 3))))}"
        typing_latency = f"{round(typingms)}ms{' ' * (9-len(str(round(typingms, 3))))}"
        message_latency = f"{round(messagems)}ms{' ' * (9-len(str(round(messagems, 3))))}"
        discord_latency = f"{round(discordms)}ms{' ' * (9-len(str(round(discordms, 3))))}"
        database_latency = f"{round(psqlms)}ms{' ' * (9-len(str(round(psqlms, 3))))}"
        average_latency = f"{round(average)}ms{' ' * (9-len(str(round(average, 3))))}"

        embed = discord.Embed(title="Pong!", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name=":globe_with_meridians: Websocket latency", value=f"{websocket_latency}")
        embed.add_field(name="<a:typing:597589448607399949> Typing latency", value=f"{typing_latency}")
        embed.add_field(name=":speech_balloon: Message latency", value=f"{message_latency}")
        embed.add_field(name="<:discord:877926570512236564> Discord latency", value=f"{discord_latency}")
        embed.add_field(name="<:psql:871758815345901619> Database latency", value=f"{database_latency}")
        embed.add_field(name=":infinity: Average latency", value=f"{average_latency}")
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await message.edit(content="Received ping!", embed=embed)

    @commands.command(help="Shows you the uptime of the bot", aliases=['up'])
    async def uptime(self, ctx):
        embed = discord.Embed(title=f'I\'ve been online since {discord.utils.format_dt(self.client.launch_time, style="f")} ({discord.utils.format_dt(self.client.launch_time, style="R")})', timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Sends a suggestion", aliases=['bot_suggestion', 'suggestion', 'make_suggestion', 'botsuggestion', 'makesuggestion'])
    async def suggest(self, ctx, *, suggestion):
        if len(suggestion) > 750:
            return await ctx.reply("Your suggestion exceeded the 750-character limit.")
        else:
            embed = discord.Embed(title="Bot suggestion", description=f"""
Suggestion by: {ctx.author} | {ctx.author.name} | {ctx.author.id}
Suggestion from server: {ctx.guild} | {ctx.guild.id}
Suggestion from channel: {ctx.channel} | {ctx.channel.name} | {ctx.channel.id}
Suggestion: {suggestion}
            """, timestamp=discord.utils.utcnow(), color=0x2F3136)
            channel = self.client.get_channel(879786064473129033)
            await channel.send(embed=embed)
            await ctx.reply("Your suggestion has been sent! It will be reviewed by Ender2K89 soon.")

    @commands.command(help="Shows you information about a character", aliases=['characterinfo', 'character_info', 'char_info'])
    @commands.cooldown(1, 5, BucketType.member)
    async def charinfo(self, ctx, *, characters: str):
        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - **{c}** \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
        msg = '\n'.join(map(to_string, characters))

        menu = menus.MenuPages(EmbedPageSource(msg.split("\n"), per_page=20), delete_message_after=True)
        await menu.start(ctx)

    @commands.command(help="Shows you who helped with the making of this bot", aliases=['credit'])
    async def credits(self, ctx):
        embed = discord.Embed(title="Credits", description="""
Owner: Ender2K89#9999 (<@!564890536947875868>)
Main help command page inspired by: Charles#5244 (<@!505532526257766411>)
A lot of command ideas: Vicente0670 YT#0670 (<@!555818548291829792>)
        """, timestamp=discord.utils.utcnow(), color=0x2F3136)

        await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(info(client))
