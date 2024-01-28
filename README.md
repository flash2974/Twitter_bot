# Automatic tweets retriever
Hello ! This is my first project :)

I made a twitter bot with Python (you can host it on websites like SolarHosting.cc btw)

First, you will need to run "Installation.bat" to install all the modules needed. You can also just put in your cmd : python.exe -m pip install -r requirements.txt

Then, open the "Code.py" file and write the following informations : 
- server (**INT**) : write the server ID in which the bot will post the tweets (you need to enable developer mode in your discord app, then right-click on the server>Copy server ID)
- ID (**STR**) : the ID of the X/Twitter account you want the bot to post the tweets : this ID is written on the twitter profile : @xxxxx (xxxx is the ID!)
- channel_id (**INT**) : the ID of the discord channel where the tweets will be posted (same you need to enable developer mode in your discord app, then right-click on the channel>Copy server ID)
- TOKEN (**STR**) : the token of your discord bot
- id_of_ok_users (**list of INT**) : put her the IDs of users allowed to use the commands.

Then, run Code.py in your IDE or with the cmd (python3 Code.py)
