## sendo erika on [NoneBot](https://github.com/richardchien/nonebot)
[![License](https://img.shields.io/github/license/richardchien/nonebot.svg)](LICENSE) ![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

### Description
I am a QQ group chatting bot based on Coolq, Coolq http api and Nonebot which takes advantages on Python's [asyncio](https://docs.python.org/3/library/asyncio.html) mechanisms thus supporting a high volume of message i/o. I do provide useful plugins extended from Nonebot framework to ensure the bot operates at an acceptable and useable level.
Like what was described on Nonebot,  I only run on over Python 3.6.1+ and CoolQ HTTP plugin v4.7+.

### Plugins
I do
  * detect keywords from group chats and reply from customized settings
  * be controlled from owner directly to send messages
  * repeat
  * search weather data and etc

You can freely to only absorb part of this repo to merge it into your own coolq applications.
### XXXXXXXXXXXX
  * First follow https://cqp.cc/ and instructions to get CoolQ ready then  
  * Start the CoolQ application and makes sure it is working properly.
  *** If you use docker, go here: https://github.com/CoolQ/docker-wine-coolq to deploy a docker application by 
  ```
     mkdir coolq && cd coolq
     docker run --rm -p 9000:9000 -v `pwd`:/home/user/coolq coolq/wine-coolq
  ```
  * Follow https://cqhttp.cc/ to get http api plugin enabled on CoolQ.
  * then refer to https://none.rclab.tk/guide/ to get familiar with Nonebot
  * have required dependency: 
  ```
     pip3 install nonebot
     ...
  ```
  * I have plugin documentation, see it and finish initialization.
