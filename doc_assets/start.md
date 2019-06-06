### START

open config_bot.py and modify:
  *  `SUPERUSERS: dict` This contains all qq IDs that have full control to the bot, type yours here.
  *  `COMMAND_START: dict` the prefix to call the bot. If you have an empty string `''` this means no prefix will be used.
  *  `NICKNAME: dict` Applies only in a group chat, except special settings, the bot will respond only to those messages which start with an `@` or this nickname, for example:
  ```python
     千堂查天气 new york # responds
     查天气 new york # does not respond
  ```
  * Change `HOST` and `PORT` as appropriate; because CoolQ http plugin will open a server to process requests, you plug in its location. Refer to https://cqhttp.cc/docs/4.10/#/ if you do not know.

  * run `python3 bot.py` and the bot is working. If there are exceptions prompting you to install modules, do so.

Open a private message window with the bot, and hit: 
  ```
        发送到QQ 12345678 hello, world
  ```
Where you know where your qq goes (12345678). Since it does not matter in private chats whether you call the nickname, you will see:
  ```
        hello, world
        success!
  ```
The first message indicates you controlled the bot to send a message to you: "hello, world", the other says it is successful. Sometimes if you do not see the success! message, there might be some problems.

Now the bot is working properly. But to use more features, read the following docs...

Or you might want to type `help` to the bot.