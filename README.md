## sendo erika on [NoneBot](https://github.com/richardchien/nonebot)
[![License](https://img.shields.io/github/license/richardchien/nonebot.svg)](LICENSE) ![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

### Description
I am a QQ group chatting bot based on Coolq, Coolq http api and Nonebot which takes advantages on Python's [asyncio](https://docs.python.org/3/library/asyncio.html) mechanisms thus supporting a high volume of message i/o. I do provide useful plugins extended from Nonebot framework to ensure the bot operates at an acceptable and useable level.
Like what was described on Nonebot,  I only run on over Python 3.7+ and CoolQ HTTP plugin v4.7+.

### Plugins
I do
  * detect keywords from group chats and reply from customized settings
  * be controlled from owner directly to send messages
  * repeat
  * sign in
  * notify you to wake up from bed at 6 am
  * search weather data and etc

You can freely only absorb part of this repo to merge it into your own coolq applications.
### XXXXXXXXXXXX
  * <del>First follow https://cqp.cc/ and instructions to get CoolQ ready then</del>  
  * <del>Start the CoolQ application and makes sure it is working properly.</del>
  *** <del>If you use docker, go here: https://github.com/CoolQ/docker-wine-coolq to deploy a docker application by</del>
  ```
     mkdir coolq && cd coolq
     docker run --rm -p 9000:9000 -v `pwd`:/home/user/coolq coolq/wine-coolq
  ```
  * <del>Follow https://cqhttp.cc/ to get http api plugin enabled on CoolQ.</del>
  * then refer to https://nonebot.cqp.moe/ to get familiar with Nonebot
  * have required dependency: 
  ```
     pip3 install nonebot
     ...
  ```
  * Plugin documentation is available, see it and finish initialization.

### Update since August 1 2020
Since Coolq is dead, please refer to [this issue](https://github.com/nonebot/nonebot/issues/217) for alternative ways of deploying it.

### Update since March 20 2020
[NoneBot](https://github.com/richardchien/nonebot) has updated to v3.5.0, abandoning the use of `Context_T` and discarding Python 3.6. As a result, this bot, after bumping versions, only runs above Python 3.7.

### Related
 * [scripter for sendo erika](https://github.com/cleoold/scripter-for-sendo-erika)
