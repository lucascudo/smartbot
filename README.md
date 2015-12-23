# Smartbot
The smartest bot for telegram/slack

 ![](https://img.shields.io/pypi/v/smartbot.png)
 ![](https://img.shields.io/travis/pedrohml/smartbot.png)
 ![](https://img.shields.io/pypi/dm/smartbot.png)
 ![](https://img.shields.io/pypi/l/smartbot.png)

#### Description
Smartbot is a python library that helps to write enhanced bots for [Telegram](https://telegram.org/) / [Slack](https://slack.com/).
The concept of **behaviours** makes easier to add costumizable features to your bot. Some features are already built-in in this package:
- **Wolfram**: Use Wolfram knowledge system to query sentences;
- **Evi**: Use Evi knowledge system query sentences;
- **Google Image**: Use google image to search images;
- **Bing Image**: Use bing image to search images;
- **Translate**: Use bing translator to translate sentences;
- **Talk**: Use bing text-to-speech to convert text in spoken sentences;
- **Joke**: Use [PiadasNet](http://piadasnet.com) to search jokes;
- **Nasa**: Retrieve [Nasa Image Of The Day](http://apod.nasa.gov/apod/astropix.html);
- **Friendly**: Support seamless use of knowledge systems like Wolfram, Evi and redirect configured mentions to behaviours;
- **Loader**: Enable/Disable behaviours on the fly.

#### Requirements
- Create a bot and get a token (Please read [TelegramBots](https://core.telegram.org/bots) or [SlackBots](https://api.slack.com/bot-users))
- Python 2.7

#### Instalation
You can install with [pip](https://github.com/pypa/pip):
```
pip install smartbot
```
or inside directory (in case you downloaded the code):
```
python setup.py install
```

#### Usage
Smartbot usually run in foreground logging to stdout. You can simple run a bot like:

For telegram:
```
smartbot_full.py --telegram-bot-token=177224385:AAFYpmN91kZe_JXL_4kOFQTzAVt-XXXXXX
```

For slack:
```
smartbot_full.py --slack-bot-token=xoxb-XXXXXXXXXX-uf63prZee13IGqmn4zXXXXX
```

For a more complete usage see *--help*.

#### Running
When your bot is successfully up you can see a message like `(botname) MAIN - Starting bot`. In this point, you can use the builtin behaviours/commands. For telegram users, commands starts with `/` and slack ones with `_`. See the list of commands:

- `(/|_)wolfram query`
- `(/|_)evi query`
- `(/|_)gimage keyword(s)`
- `(/|_)bimage keyword(s)`
- `(/|_)translate sentence`
- `(/|_)talk sentence`
- `(/|_)joke keyword`
- `(/|_)nasa`
- `(/|_)(un)?load behaviour`

#### Friendly behaviour
Maybe the most important behaviour is the **friendly**. In a telegram group or a slack channel you can interact with seamless like you talk with friends and other users. The bot use command aliases or wolfram/evi knowledge system to decide what to do or what answer (see **Customize** section).

```
@botname send john travolta confused
```
botname:

![John](https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSemNQBABb72tdKLip2dRryDPGxqOFRWMJWjczB8PdDIFx3tw0Dqg)

```
@botname 1 + 1
```
botname: 2

#### Customize
Since version 1.0 you can use configuration file to customize bot behaviour. Some configuration options are supported already (examples in *config* directory). The most important is the **language** option where you can set the country language to make the bot answer the questions appropriately. The configuration file is set with *--config* argument or environment variables (please see *--help* for details).

```ini
[main]
creator = Pedro Lira
language = en-US

[friendly-aliases]
standup = jalk
speak = talk
talk = talk
translate = translateen
nasa = nasa
joke = joke
send = gimage
have = bimage

[friendly]
default-answer0 = I don't intend to comment
default-answer1 = I don't have enough information in my database for this
default-answer2 = I don't know (yet)
default-answer3 = I am in the grow stage
default-answer4 = Ask me tomorrow
```

#### Development
You are free to contribute with this project and even fork it. Of cource, following the license instructions. We will be available as much as possible to solve any doubts or issues about this project.

#### Documentation and Tests
The code and wiki documentation are in development.
The test suite is not that perfect, but we are in a pursuit to improve it. Manual tests confirm the project is stable enough to be in a public repository.

Enjoy !!
