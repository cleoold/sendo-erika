You can talk to the bot to schedule a timer, when the timer expires, the bot will get back to you

```
[11:00:00] > 千堂定时提醒 5 30 吃饭
[11:00:00] 已设定：
           05月06日 16:30 吃饭
...
[16:30:00] @你 吃饭
```

Partial natural language is supported. example:

```
[11:00:00] > 千堂5小时30分后提醒我吃饭
[11:00:00] 已设定：
           05月06日 16:30 吃饭
[11:00:20] > 千堂取消定时提醒
[11:00:20] 已取消定时提醒
```

limitation:

currently the scheduled job store is not persistent, which means after rebooting the bot all scheduled jobs will be lost.
