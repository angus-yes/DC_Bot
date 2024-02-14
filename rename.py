import funcdoc as fd

vcerror = 'Error: Function caller is not inside a voice channel'
flag = {'-v': 0, '-t': 1, '-c': 2}

async def rename(msglist, orimsg):   
    state = 0

    if len(msglist) == 1:
        await message.channel.send(f"{fd.funcdict['rename']}")
    else:
        if msglist[1] in flag:
            state = flag[msglist[1]]
        else:
            if not(orimsg.author.voice):
                await orimsg.channel.send(vcerror)
            else:
                if len(msglist) > 2:
                    for i in range(2, len(msglist)):
                        if state == 1:
                            msglist[1] += '-' + msglist[i]
                        else:
                            msglist[1] += ' ' + msglist[i]
                await orimsg.author.voice.channel.edit(name = msglist[1])
            return
    
        if len(msglist) < 4:
            await orimsg.channel.send('Error: Not enough arguments; Type "?rename" for help')
        else:
            try:
                ofs = int(msglist[2]) - 1
            except:
                await orimsg.channel.send(f'Error: Parameter "offset" is not a positive integer ({msglist[2]})')
                return
            if ofs < 0:
                await orimsg.channel.send(f'Error: Parameter "offset" is not a positive integer ({msglist[2]})')
                return

            if len(msglist) > 4:
                for i in range(4, len(msglist)):
                    if state == 1:
                        msglist[3] += '-' + msglist[i]
                    else:
                        msglist[3] += ' ' + msglist[i]
            await rn(state, msglist[3], ofs, orimsg)

async def rn(state, nname, ofs, message):
    if state == 0:
        listch = [c for c in message.guild.voice_channels if not(c.category)]
        listch += [c for n in message.guild.categories if n.voice_channels for c in n.voice_channels]
    elif state == 1:
        listch = [c for c in message.guild.text_channels if not(c.category)]
        listch += [c for n in message.guild.categories if n.text_channels for c in n.text_channels]
    else:
        listch = [c for c in message.guild.categories]
    
    #print(listch)

    if len(listch) > ofs:
        if listch[ofs].name == 'bot-channel':
            await message.channel.send('Warning: Changing the name of "bot-channel" may disable the bot due to no input channel')
        else:
            if state == 0:
                await message.channel.send(f'Changing voice channel "{listch[ofs].name}" (id: {listch[ofs].id}) name to "{nname}". ')
            elif state == 1:
                await message.channel.send(f'Changing text channel "{listch[ofs].name}" (id: {listch[ofs].id}) name to "{nname}". ')
            else:
                await message.channel.send(f'Changing category "{listch[ofs].name}" (id: {listch[ofs].id}) name to "{nname}". ')
            await listch[ofs].edit(name = nname)
    else:
        if state == 0:
            await message.channel.send('Error: Target voice channel not found')
        elif state == 1:
            await message.channel.send('Error: Target text channel not found')
        else:
            await message.channel.send('Error: Target category not found')
        
        
