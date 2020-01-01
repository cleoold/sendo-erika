involke in a group chat like this:
```
> 千堂签到
@你 [some custom sentences] 好感度：1.8 (+0.4)
> 千堂签到
今日签到过啦~ 好感度：1.8
> 千堂签到信息
好感度：1.4
历史签到次数：5
上次签到：2019.08.27
```

This plugin overlaps with test_rp plugin. Please remove it to use this.

The sign_in plugin provides basic daily signing feature. It is a group-based feature. User in different groups can sign in and gain points.

The data is stored in a sqlite database and is managed by `SignInSession` class. The structure of the signin data is dipicted as follows

```
table name: sign

fields:
identity (format: userid_groupid)(str), 
last sign in time (str), 
score (int),
luck (not used)(str), 
score2 (stores the sign in count)(int), 
score3 (not used)(int)
```

There are some fields that are not used. Feel free to implement.

A row fetch looks like this:
```py
('12345678_7777777', '27082019', 140, '', 5, 0)
```

