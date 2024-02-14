funcdict = {
"rename" : 
"""`!rename [flag] [offset] [name]`
\tRename a channel/category name
\t`flag`
\t\t`-v` Rename a voice channel name
\t\t`-t` Rename a text channel name
\t\t`-c` Rename a category name
\t`offset` The index of the channel (1 means first)
\t`name` The new name
\tExample:
\t\tSuppose the discord server structure is as follow:
\t\t\t`|-text channel: text1      `
\t\t\t`|-voice channel: voice1    ` 
\t\t\t`|-category: cat1           ` 
\t\t\t`||-voice channel: voice2   ` 
\t\t\t`||-text channel: text2     ` 
\t\t\t`|                          ` 
\t\t\t`|-category: cat2           ` 
\t\t\t`||-voice channel: voice3   ` 
\t\t\t`|                          `
\t\t`!rename -v 2 sth` will rename 'voice2' to 'sth'
\t\t`!rename -t 1 sthtoo` will rename 'text1' to 'sthtoo'
\t\t`!rename -c 2 haha` will rename 'cat2' to 'haha'
*Shortcut usage*
`!rename [name]` 
\tRename the voice channel you are curently at to the `name` specified""",

"wolf" : 
"`!wolf [query]`\n\tGet the simple result of the `query` from Wolfram Alpha",

"wolf+" : 
"`!wolf+ [query]`\n\tGet the full result of the `query` from Wolfram Alpha",

"random" :
"""`!random [flag] [arguments]`
\tGenerate a random result
\t`flag & arguments`
\t\t`-d [integer A] [integer B] [step=1]`
\t\t\tGenerate random integers between A and B inclusively
\t\t\tStep can be specified to modify the list of potential result
\t\t\t\tExample: `A = 2, B = 8, step = 3` will randomly select an integer from `[2, 5, 8]` 
\t\t`-b` 
\t\t\tGenerate Yes/No, *NO* argument needed
\t\t`-f [decimal A] [decimal B]` 
\t\t\tGenerate random decimal number between A and B inclusively
\t\t`-c [item_1] [item_2] ... [item_n]` 
\t\t\tRandomly pick an item from the list of items given
*Shortcut usage*
`!random` 
\tRoll a dice"""
           }



