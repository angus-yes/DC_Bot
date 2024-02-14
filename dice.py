import random

flag = {'-d': 0, '-f': 1, '-b': 2, '-c': 3}

async def roll(msglist, message):
    if (len(msglist) == 1):
        await message.channel.send(f'Result: `{random.randrange(1, 7)}`')
    else:
        state = 0
        if msglist[1] in flag:
            state = flag[msglist[1]]
        else:
            await message.channel.send(f'Error: Invalid flag ({msglist[1]})')
            return
        parm = msglist[2:]

        if state == 0:
            if len(parm) != 3 and len(parm) != 2:
                await message.channel.send(f'Error: Mismathced number of arguments; Found {len(parm)}')
                return
            elif len(parm) == 3:
                try:
                    step = int(parm[2])
                except:
                    await message.channel.send(f'Error: Parameter "step" is not an integer ({msglist[2]})')
                    return
            else:
                step = 1
            try:
                start = int(parm[0])
            except:
                await message.channel.send(f'Error: Parameter "start" is not an integer ({msglist[2]})')
                return
            try:
                end = int(parm[1])
            except:
                await message.channel.send(f'Error: Parameter "end" is not an integer ({msglist[2]})')
                return
            
            low = end if end < start else start
            high = end if end > start else start
            
            try: 
                await message.channel.send(f'Result: `{random.randrange(low, high+1, step)}`')
            except:
                await message.channel.send(f'Error: Range({low}, {high}) with step {step} is empty')
                return
        
        elif state == 1:
            if len(parm) != 2:
                await message.channel.send(f'Error: Requires 2 arguments; Found {len(parm)}')
                return
            else:
                try:
                    start = float(parm[0])
                except:
                    await message.channel.send(f'Error: Parameter "start" is not a number ({msglist[2]})')
                    return
                try:
                    end = float(parm[1])
                except:
                    await message.channel.send(f'Error: Parameter "end" is not a number ({msglist[2]})')
                    return
                
                ran = abs(end - start)
                low = end if end < start else start

                await message.channel.send(f'Result: `{random.random()*ran+low}`')
        
        elif state == 2:
            if len(parm) > 0:
                await message.channel.send(f'Error: Function does not require arguments; Found {len(parm)}')
            else:
                await message.channel.send(f'Result: `{bool(random.getrandbits(1))}`')

        else:
            if len(parm) < 1:
                await message.channel.send('Error: Missing list of items')
            else:
                await message.channel.send(f'Result: `{random.choice(parm)}`')
