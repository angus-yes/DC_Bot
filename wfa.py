import sys
import string
import random
import wolframalpha
import discord
import asyncio
import re
import funcdoc as fd

# Regex for IP address
ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
ipv6_regex = re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

# Wolfram Alpha credentials and client session
app_id = 'U5WY6L-KA68RHXH5K'
waclient = wolframalpha.Client(app_id)

# Globals for message removal
messageHistory = set()
computemessageHistory = set()
previousQuery = ''

# Fun strings for invalid queries
invalidQueryStrings = ["Nobody knows.", "It's a mystery.", "I have no idea.", "No clue, sorry!", "I'm afraid I can't let you do that.", "Maybe another time.", "Ask someone else.", "That is anybody's guess.", "Beats me.", "I haven't the faintest idea."]

# Prints a single result pod
async def printPod(channel, text, title):
    text = text.replace("Wolfram|Alpha", "Wolfbot")
    text = text.replace("Wolfram", "Wolf")
    text = re.sub(ipv4_regex, "IP Redacted", text)
    text = re.sub(ipv6_regex, "IP Redacted", text)
    newmessage = await channel.send("__**" + title + ":**__\n" + "`" + text + "`")
    messageHistory.add(newmessage)

# Prints a single image pod
async def printImgPod(channel, img, title):
    newmessage = await channel.send("__**" + title + ":**__\n" + img)
    messageHistory.add(newmessage)


async def wfa(message):
    global previousQuery
    # Check if message isnt the bot and query/command exists

    if len(message.content) > 5:

        # Strip !wolf
        query = message.content[6:]
        
        # Run wolfram alpha query
        if len(query) > 1:
                queryComputeMessage = await message.channel.send(":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
                print(message.author.name + " | Query: " + query)
        else:
                print(message.author.name + " | Query: " + previousQuery)
                queryComputeMessage = await message.channel.send(":wolf: Computing '" + previousQuery + "' :computer: :thought_balloon: ...")

        computemessageHistory.add(queryComputeMessage)

        if message.content.startswith('!wolf+'):
                # Expanded query
                if len(query) > 1:
                    res = waclient.query(query)
                    if len(list(res.info)) > 0:
                        for pod in list(res.info):
                            #print(pod)
                            if isinstance(pod['subpod'], list):
                                if pod['subpod'][0]['plaintext'] != None:
                                    await printPod(message.channel, pod['subpod'][0]['plaintext'], pod['@title'])
                                elif 'img' in pod['subpod'][0]:
                                    await printImgPod(message.channel, pod['subpod'][0]['img']['@src'], pod['@title'])
                            else:
                                if pod['subpod']['plaintext'] != None:
                                    await printPod(message.channel, pod['subpod']['plaintext'], pod['@title'])
                                elif 'img' in pod['subpod']:
                                    await printImgPod(message.channel, pod['subpod']['img']['@src'], pod['@title'])

                        await queryComputeMessage.edit(content = (queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:"))
                    else:
                        await message.channel.send(random.choice(invalidQueryStrings))
                else:
                    res = waclient.query(previousQuery)
                    if len(list(res.info)) > 0:
                        for pod in list(res.info):
                            if pod['subpod']['plaintext'] != None:
                                await printPod(message.channel, pod['subpod']['plaintext'], pod['@title'])
                            elif 'img' in pod['subpod']:
                                await printImgPod(message.channel, pod['subpod']['img']['@src'], pod['@title'])

                        await queryComputeMessage.edit(content =(queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:"))
        else:
                # Short answer query
                res = waclient.query(query)

                if len(list(res.info)) > 0:
                    resultPresent = 0
                    podLimit = 0

                    # WA returns a "result" pod for simple maths queries but for more complex ones it returns randomly titled ones
                    for pod in list(res.info):
                        if pod['@title'] == 'Result':
                            resultPresent = 1

                    for pod in list(res.info):
                        if pod.text:
                            if resultPresent == 1:
                                if pod['@title'] == 'Result':
                                    await printPod(message.channel, pod['subpod']['plaintext'], pod['@title'])
                            # If no result pod is present, prints input interpretation and 1 other pod (normally contains useful answer)
                            else:
                                if podLimit < 2:
                                    await printPod(message.channel, pod['subpod']['plaintext'], pod['@title'])
                                    podLimit += 1
                else:
                    await message.channel.send(random.choice(invalidQueryStrings))
                    
                if len(list(res.info))-2 > 0:
                    await queryComputeMessage.edit(content = (queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag: (" + str(len(list(res.info))-2) + " more result pods available, rerun query with !wolf+)"))
                else:
                    await queryComputeMessage.edit(content = (queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:"))
        previousQuery = query
    else:
        await message.channel.send(f"{fd.funcdict['wolf']}\n{fd.funcdict['wolf+']}")
        
