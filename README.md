# GDSC Discord Bot

## About

A private general-purpose Discord bot made to organize the Discord server of a volunteer activities club.

The bot is currently hosted in an Azure VM.

## Commands

There are 25 commands in total, divided into 5 categories:

<details>
<summary>Admin (9 Commands - Only for admins)</summary>

- `&announce <message>`: Sends an announcement to the annoucement channel. ([Source code](./src/commands/admin/announce.py))
- `/clear <filter_by_user?> <filter_by_role?> <filter_by_bot?>`: Clears the specified amount of messages in the channel. ([Source code](./src/commands/admin/clear.py))
- `/shut_up`: Deletes every message sent in the channel except the command invoker and other bots. ([Source code](./src/commands/admin/monitor_chat.py))
- `/stop`: Stops the message deletion of `shut_up` command. ([Source code](./src/commands/admin/monitor_chat.py))
- `/move_all`: Moves every member in the voice channel to another voice channel. ([Source code](./src/commands/admin/move_all.py))
- `/say <message> <channel?>`: Sends a message to the channel. ([Source code](./src/commands/admin/say.py))
- `/set_nick <member> <nickname?>`: Sets the nickname of a member. ([Source code](./src/commands/admin/set_nick.py))
- `/slowmode <channel?> <seconds?>`: Sets or removes the slowmode of the channel. ([Source code](./src/commands/admin/slowmode.py))
- `/snipe`: Retrieves the last deleted messages in the channel. ([Source code](./src/commands/admin/snipe.py))

</details>

<details>
<summary>Games (1 Command)</summary>

- `/rps <member>`: Plays rock-paper-scissors with another member. ([Source code](./src/commands/games/rps.py))

</details>

<details>
<summary>Helpful (3 Commands)</summary>

- `/help <command?>`: Get the list of all commands or get help for a specific command. ([Source code](./src/commands/helpful/help.py))
- `/question <question>`: Get the best answer to your question from StackOverflow! ([Source code](./src/commands/helpful/question.py))
- `/social_media`: Get the social media links of GDSC. ([Source code](./src/commands/helpful/social_media.py))

</details>

<details>
<summary>Misc (5 Commands)</summary>

- `/fact`: Get a random fact. ([Source code](./src/commands/misc/fact.py))
- `/joke <word?>`: Get a random joke. ([Source code](./src/commands/misc/joke.py))
- `/meme <subreddit?>`: Get a random meme from a subreddit. ([Source code](./src/commands/misc/meme.py))
- `/quote`: Get a random quote. ([Source code](./src/commands/misc/quote.py))
- `/ping`: Get the bot's latency. ([Source code](./src/commands/misc/ping.py))

</details>

<details>
<summary>Utility (7 Commands)</summary>

- `/avatar <member?>`: Get the avatar of a member. ([Source code](./src/commands/utility/avatar.py))
- `/corona <country?>`: Get the COVID-19 statistics of a country. ([Source code](./src/commands/utility/corona.py))
- `/icon`: Get the icon of the server. ([Source code](./src/commands/utility/icon.py))
- `/move_me <channel>`: Moves the invoker to the specified voice channel. ([Source code](./src/commands/utility/move_me.py))
- `/server_info`: Display information about the server. ([Source code](./src/commands/utility/server_info.py))
- `/user_info <member?>`: Display information about a member. ([Source code](./src/commands/utility/user_info.py))
- `/weather <city?>`: Get the weather of a city. ([Source code](./src/commands/utility/weather.py))

</details>


## Improvements

The bot is not developed to be reusable for other users because it is tightly coupled to work in just the [GDSC Discord server](https://discord.gg/24VKKDyDh7), so this could be a future refactor.

## Demo 

https://github.com/Younes-ch/GDSC-Discord-Bot/assets/56512077/668fa085-d7de-4586-b090-781fee02e366


