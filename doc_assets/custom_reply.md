In a group chat, you might want the bot to do a "keyword reply". For example, if someone says `在吗？` the bot replies `在！`.
The custom reply plugin is based on the private chat window. By chatting with the bot with command one can easily modify the keyword settings.

All matchings are stored in a json file called `group_data.json` under its module path. Matchings split into qq groups, which means these settings are group-specific. One special part is there exist a "group number" called `global`, which means keywords in this dict respond to every groups.

  ```
           ┌ "global": .... groups 123456 654321 also apply
  settings-┼ "123456": ....
           └ "654321": ....
  ```

In each group, there are three modes: full match (1), inclusive match (2), and regex match (3).
  * full: replies only when the keywords completely matches the message
  * inclusive: replies when keywords are *in* the message
  * regex: replies when the message matches given pattern

##### Creating keyword pairs
Open a private message box with the box as a superuser. hit and observe
  ```
     >> 群关键字 add global 3
        在这里输入关键字
     >> ^[A-Z]{3,4}[-\._]?[0-9]{3,5}$
        在这里输入回复
     >> ナニコレ？？
        success!
  ```
In the first line, `群关键字` is the name of the command, `add` is the add mode which means you are adding keywords, `global` means you are adding stuff in the global folder so that it works in every group, `3` means the keyword works in regex-matching mode.
You then typed `^[A-Z]{3,4}[-\._]?[0-9]{3,5}$`, this is a keyword. You then typed the reply, and the bot responds with a success message. The pair will take effect instantly.

Thus when any group member's message matches this pattern, like `AAA1111`, the bot replies with `ナニコレ？？`.

Or it might say `?`, this is because this keyword already exists in the factory configure file, adding an existing keyword is in fact appending: two replies both exist and a randomly chosen one will be sent. This is why in the configure the reply is in the form of a list.

##### Removing keyword pairs
Note the deleting mode will delete *all* replies paired with the given keyword.
  ```
     >> 群关键字 del global 3
        在这里输入关键字
     >> ^[A-Z]{3,4}[-\\._]?[0-9]{3,5}$
        success!
  ```
The match we just set was then deleted. In other occasions, if you typed a keyword that does not exist, an error will be reported.

Note, instead, you can actually delete all pairs in one group at once:
  ```
     >> 群关键字 delall 123456
        success!
  ```

##### Editing keyword pairs directly from the json file
The json file come along has its pre-setup reply pairs which will guide you the proper format to edit them.

##### Variable as reply
In any reply, you can insert variables. To plug a variable inside the content, just type these in place of the variable:
  * `{SENDER_ID]` sender's qq
  * `{SENDER_NICK]` sender's nickname
  * `{SENDER_CARD]` sender's namecard
  * `{SENDER_ROLE]` sender's role (member or admin)
  * `{SENDER_TITLE]` sender's title

The availability of them depends on the context.

##### Checking keyword pairs
This command will list the first 10 replies of *each* keyword match
  ```
     >> 群关键字 view global 3
        global, regex_match
        "^[A-Z]{3,4}[-\._]?[0-9]{3,5}$": "?"; "ナニコレ？？"
  ```