def replaceDoubleCharacters(string):
    s = set()
    list = []
    for ch in string:
         if ch not in s:
            s.add(ch)
            list.append(ch)

    return ''.join(list)

def replaceSpaces(string):
    replacedString = string.replace(" ", "") # Replaces space with nothing
    return replacedString

def replaceExclamationMark(string):
    replacedString = string.replace("!", "i") # Replaces ! with i
    return replacedString

def replaceFakeI(string):
    replacedString = string.replace("|", "i") # Replaces | with i
    return replacedString

def replaceDot(string):
    replacedString = string.replace(".", "") # Replaces . with nothing
    return replacedString

def replaceDotWithDot(string):
    replacedString = string.replace(".", "") # Replaces dot with .
    return replacedString

def replaceThing(string):
    replacedString = string.replace("'", "") # Replaces ' with nothing
    return replacedString

def replaceV(string):
    replacedString = string.lower() and string.replace("v", "") # Replaces v with nothing
    return replacedString

def replaceZ(string):
    replacedString = string.lower() and string.replace("z", "") # Replaces z with nothing
    return replacedString

def replaceH(string):
    replacedString = string.lower() and string.replace("h", "") # Replaces z with nothing
    return replacedString

def replaceWeirdA(string):
    replacedString = string.lower() and string.replace("ä", "a") # Replaces ä with a
    return replacedString

def replaceWeirdO(string):
    replacedString = string.lower() and string.replace("ö", "o") # Replaces ö with o
    return replacedString

def replaceWeirdU(string):
    replacedString = string.lower() and string.replace("ü", "u") # Replaces ü with u
    return replacedString

def removePlusSigns(string):
    replacedString = string.lower() and string.replace("+", "") # Replaces + with nothing
    return replacedString

def removeMinusSign(string):
    replacedString = string.lower() and string.replace("-", "") # Replaces - with nothing
    return replacedString

def removeUnderscoresSign(string):
    replacedString = string.lower() and string.replace("_", "") # Replaces + with nothing
    return replacedString

def removeEqualsSign(string):
    replacedString = string.lower() and string.replace("=", "") # Replaces = with nothing
    return replacedString

def removeTideSign(string):
    replacedString = string.lower() and string.replace("~", "") # Replaces = with nothing
    return replacedString

def weirdLetter1(string):
    replacedString = string.lower() and string.replace("~", "") # Replaces = with nothing
    return replacedString

def replaceDEmoji(string):
    replacedString = string.lower() and string.replace("🇩", "d") # Replaces 🇩 with D
    return replacedString

def replaceHeart(string):
    replacedString = string.lower() and string.replace("♡", "u") # Replaces ♡ with u
    return replacedString

def replaceStar(string):
    replacedString = string.lower() and string.replace("☆", "u") # Replaces ♡ with u
    return replacedString

def replaceBrackets(string):
    replacedString = string.lower() and string.replace("{}", "i") # Replaces {} with i
    return replacedString

def replaceWeirdI(string):
    replacedString = string.lower() and string.replace("¡", "i") # Replaces ¡ with i
    return replacedString

def replaceWeirdQuestionMark(string):
    replacedString = string.lower() and string.replace("¿", "i") # Replaces ¿ with i
    return replacedString

def replaceWeirdArrow(string):
    replacedString = string.lower() and string.replace("《", "i") # Replaces 《 with i
    return replacedString

def removeWeirdSlash(string):
    replacedString = string.lower() and string.replace('\\', "") # Replaces \ with nothin
    return replacedString


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send("fuck off")
    if message.guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        await client.process_commands(message) # Processes commands
        return # Return (do nothing)
    else: # If it wasn't then:
      try: # Try to:
        if message.author.bot: # If the author of the message is the bot then:
          return # Return (ignore)
        if message.content in no_u: # If the content of the message is in the array "no_u" then:
          await message.reply("no u") # Reply with "no u"
        else: # Else
            if len(message.content) >  500: # If the length of the message is over 500 then:
                await message.delete() # Deletes the message
                warnMessage = f"Hey {message.author.mention}! Your message was over 500 characters so I had to delete it!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to not send messages over 500 messages
                await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
            else: # If the length of the message isn't over 500 then:
              swear_perms_role = discord.utils.get(message.guild.roles, name="Swear Perms")
              if message.channel.id not in [828667602351161354]: # If the message was sent in the channel with this ID: 828667602351161354, then:
                if prof.contains_profanity(message.content) or prof.contains_profanity(unidecode(message.content)) or prof.contains_profanity(replaceDoubleCharacters(message.content)) or prof.contains_profanity(replaceSpaces(message.content)) or prof.contains_profanity(replaceExclamationMark(message.content)) or prof.contains_profanity(replaceFakeI(message.content)) or prof.contains_profanity(replaceDot(message.content)) or prof.contains_profanity(replaceThing(message.content)) or prof.contains_profanity(replaceV(message.content)) or prof.contains_profanity(replaceZ(message.content)) or prof.contains_profanity(replaceH(message.content)) or prof.contains_profanity(replaceWeirdA(message.content)) or prof.contains_profanity(replaceWeirdO(message.content)) or prof.contains_profanity(replaceWeirdU(message.content)) or prof.contains_profanity(removePlusSigns(message.content)) or prof.contains_profanity(removeMinusSign(message.content)) or prof.contains_profanity(removeUnderscoresSign(message.content)) or prof.contains_profanity(removeEqualsSign(message.content)) or prof.contains_profanity(removeTideSign(message.content)) or prof.contains_profanity(replaceDEmoji(message.content)) or prof.contains_profanity(replaceHeart(message.content)) or prof.contains_profanity(replaceStar(message.content)) or prof.contains_profanity(replaceBrackets(message.content)) or prof.contains_profanity(replaceWeirdI(message.content)) or prof.contains_profanity(replaceWeirdQuestionMark(message.content)) or prof.contains_profanity(replaceWeirdArrow(message.content)):
                  if swear_perms_role in message.author.roles:
                      await client.process_commands(message) # Processes commands
                      return # Return (ignore)
                  else:
                    await message.delete() # Deletes the message |||| prof.contains_profanity
                    warnMessage = f"Hey {message.author.mention}! Don't say that!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to stop saying that
                    await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds

                    channel = client.get_channel(836232733126426666) # Gets the channel "stealth_logs" (836232733126426666) and stores it as the channel variable

                    embed = discord.Embed(title="Someone tried to swear!", colour=0x2F3136) # Creates a embed with the title being "Someone tried to swear!" and the color being: 0x2F3136
                    embed.add_field(name="Person who tried to swear", value=f"{message.author.mention} | {message.author.name} | {message.author.id}", inline=True) # Adds a new field to the embed with the name being "Person who tried to swear:" and the value being the author's mention, name and ID.
                    embed.add_field(name="What they tried to say", value=f"`{message.content}`", inline=True) # Adds a new field to the embed with the name being "What they tried to say:" and the value being what the user said.
                    embed.add_field(name="What they tried to say but censored (no checks)", value=f"`{prof.censor(message.content, '-')}`", inline=True)
                    embed.add_field(name="Channel they tried to swear in", value=f"<#{message.channel.id}>", inline=True) # Adds a new field to the embed with the name being "Channel they tried to swear in:" and the value being the channel's mentioned.

                    await channel.send(embed=embed) # Sends the embed in the channel
                    pass # Pass
                else: # Else
                    if message.channel.id in social_category or message.channel.id in fun_stuff_category or message.channel.id in no_mic_channel: # If the message was sent in the social, fun stuff category or the no mic channel then:
                        #url_regex = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
                        #url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
                        invite_regex = re.compile(r"<?(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\b([-a-zA-Z0-9/]*)>?")
                        link_perms_role = discord.utils.get(message.guild.roles, name="Link Perms")

                        if link_perms_role in message.author.roles:
                            await client.process_commands(message) # Processes commands
                            return # Return (ignore)
                        else:
                            if invite_regex.search(message.content) or invite_regex.search(unidecode(message.content)) or invite_regex.search(removeWeirdSlash(message.content)) or invite_regex.search(replaceDotWithDot(message.content)) or invite_regex.search(replaceDoubleCharacters(message.content)) or invite_regex.search(replaceSpaces(message.content)) or invite_regex.search(replaceExclamationMark(message.content)) or invite_regex.search(replaceFakeI(message.content)) or invite_regex.search(replaceDot(message.content)) or invite_regex.search(replaceThing(message.content)) or invite_regex.search(replaceV(message.content)) or invite_regex.search(replaceZ(message.content)) or invite_regex.search(replaceH(message.content)) or invite_regex.search(replaceWeirdA(message.content)) or invite_regex.search(replaceWeirdO(message.content)) or invite_regex.search(replaceWeirdU(message.content)) or invite_regex.search(removePlusSigns(message.content)) or invite_regex.search(removeMinusSign(message.content)) or invite_regex.search(removeUnderscoresSign(message.content)) or invite_regex.search(removeEqualsSign(message.content)) or invite_regex.search(removeTideSign(message.content)) or invite_regex.search(replaceDEmoji(message.content)) or invite_regex.search(replaceHeart(message.content)) or invite_regex.search(replaceStar(message.content)) or invite_regex.search(replaceBrackets(message.content)) or invite_regex.search(replaceWeirdI(message.content)) or invite_regex.search(replaceWeirdQuestionMark(message.content)) or invite_regex.search(replaceWeirdArrow(message.content)): # If theres a link in message.content
                                await message.delete() # Deletes the message
                                warnMessage = f"Hey {message.author.mention}! Sending discord invites is not allowed!" # String that tells the author to stop sending discord invites
                                await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
                            else: # If it didn't match then:
                                pass # I don't know what to put here so I just put pass
        await client.process_commands(message) # Processes commands
      except Exception as e: # If something failed while trying then except the exception as e and then:
          pass # I don't know what to put here so I just put pass
          # print(e) # Prints "e"

@client.event
async def on_message_edit(before, after):
    if after.guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return (do nothing)
    else: # If it wasn't then:
      try: # Try to:
        if after.author.bot: # If the author of the message is the bot then:
          return # Return (ignore)
        if after.content in no_u: # If the content of the message is in the array "no_u" then:
          await after.reply("no u") # Reply with "no u"
        else: # Else
            if len(after.content) >  500: # If the length of the message is over 500 then:
                await after.delete() # Deletes the message
                warnMessage = f"Hey {after.author.mention}! Your message was over 500 characters so I had to delete it!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to not send messages over 500 messages
                await after.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
            else: # If the length of the message isn't over 500 then:
              swear_perms_role = discord.utils.get(after.guild.roles, name="Swear Perms")
              if after.channel.id not in [828667602351161354]: # If the message was sent in the channel with this ID: 828667602351161354, then:
                if prof.contains_profanity(after.content) or prof.contains_profanity(unidecode(after.content)) or prof.contains_profanity(replaceDoubleCharacters(after.content)) or prof.contains_profanity(replaceSpaces(after.content)) or prof.contains_profanity(replaceExclamationMark(after.content)) or prof.contains_profanity(replaceFakeI(after.content)) or prof.contains_profanity(replaceDot(after.content)) or prof.contains_profanity(replaceThing(after.content)) or prof.contains_profanity(replaceV(after.content)) or prof.contains_profanity(replaceZ(after.content)) or prof.contains_profanity(replaceH(after.content)) or prof.contains_profanity(replaceWeirdA(after.content)) or prof.contains_profanity(replaceWeirdO(after.content)) or prof.contains_profanity(replaceWeirdU(after.content)) or prof.contains_profanity(removePlusSigns(after.content)) or prof.contains_profanity(removeMinusSign(after.content)) or prof.contains_profanity(removeUnderscoresSign(after.content)) or prof.contains_profanity(removeEqualsSign(after.content)) or prof.contains_profanity(removeTideSign(after.content)) or prof.contains_profanity(replaceDEmoji(after.content)) or prof.contains_profanity(replaceHeart(after.content)) or prof.contains_profanity(replaceStar(after.content)) or prof.contains_profanity(replaceBrackets(after.content)) or prof.contains_profanity(replaceWeirdI(after.content)) or prof.contains_profanity(replaceWeirdQuestionMark(after.content)) or prof.contains_profanity(replaceWeirdArrow(after.content)):
                  if swear_perms_role in after.author.roles:
                      return # Return (ignore)
                  else:
                    await after.delete() # Deletes the message |||| prof.contains_profanity
                    warnMessage = f"Hey {after.author.mention}! Don't say that!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to stop saying that
                    await after.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds

                    channel = client.get_channel(836232733126426666) # Gets the channel "stealth_logs" (836232733126426666) and stores it as the channel variable

                    embed = discord.Embed(title="Someone tried to swear!", colour=0x2F3136) # Creates a embed with the title being "Someone tried to swear!" and the color being: 0x2F3136
                    embed.add_field(name="Person who tried to swear", value=f"{after.author.mention} | {after.author.name} | {after.author.id}", inline=True) # Adds a new field to the embed with the name being "Person who tried to swear:" and the value being the author's mention, name and ID.
                    embed.add_field(name="What they tried to say", value=f"`{after.content}`", inline=True) # Adds a new field to the embed with the name being "What they tried to say:" and the value being what the user said.
                    embed.add_field(name="What they tried to say but censored (no checks)", value=f"`{prof.censor(after.content, '-')}`", inline=True)
                    embed.add_field(name="Channel they tried to swear in", value=f"<#{after.channel.id}>", inline=True) # Adds a new field to the embed with the name being "Channel they tried to swear in:" and the value being the channel's mentioned.

                    await channel.send(embed=embed) # Sends the embed in the channel
                    pass # Pass
                else: # Else
                    if after.channel.id in social_category or after.channel.id in fun_stuff_category or after.channel.id in no_mic_channel: # If the message was sent in the social, fun stuff category or the no mic channel then:
                        #url_regex = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
                        #url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
                        invite_regex = re.compile(r"<?(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\b([-a-zA-Z0-9/]*)>?")
                        link_perms_role = discord.utils.get(after.guild.roles, name="Link Perms")

                        if link_perms_role in after.author.roles:
                            return # Return (ignore)
                        else:
                            if invite_regex.search(after.content) or invite_regex.search(unidecode(after.content)) or invite_regex.search(removeWeirdSlash(after.content)) or invite_regex.search(replaceDotWithDot(after.content)) or invite_regex.search(replaceDoubleCharacters(after.content)) or invite_regex.search(replaceSpaces(after.content)) or invite_regex.search(replaceExclamationMark(after.content)) or invite_regex.search(replaceFakeI(after.content)) or invite_regex.search(replaceDot(after.content)) or invite_regex.search(replaceThing(after.content)) or invite_regex.search(replaceV(after.content)) or invite_regex.search(replaceZ(after.content)) or invite_regex.search(replaceH(after.content)) or invite_regex.search(replaceWeirdA(after.content)) or invite_regex.search(replaceWeirdO(after.content)) or invite_regex.search(replaceWeirdU(after.content)) or invite_regex.search(removePlusSigns(after.content)) or invite_regex.search(removeMinusSign(after.content)) or invite_regex.search(removeUnderscoresSign(after.content)) or invite_regex.search(removeEqualsSign(after.content)) or invite_regex.search(removeTideSign(after.content)) or invite_regex.search(replaceDEmoji(after.content)) or invite_regex.search(replaceHeart(after.content)) or invite_regex.search(replaceStar(after.content)) or invite_regex.search(replaceBrackets(after.content)) or invite_regex.search(replaceWeirdI(after.content)) or invite_regex.search(replaceWeirdQuestionMark(after.content)) or invite_regex.search(replaceWeirdArrow(after.content)): # If theres a link in after.content
                                await after.delete() # Deletes the message
                                warnMessage = f"Hey {after.author.mention}! Sending discord invites is not allowed!" # String that tells the author to stop sending discord invites
                                await after.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
                            else: # If it didn't match then:
                                pass # I don't know what to put here so I just put pass
      except Exception as e: # If something failed while trying then except the exception as e and then:
          pass # I don't know what to put here so I just put pass
          # print(e) # Prints "e"
