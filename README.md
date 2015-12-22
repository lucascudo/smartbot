# Smartbot
The smartest bot for telegram/slack


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
- **Friendly**: Support seamless useo of knowledge systems like Wolfram, Evi and redirect configured mentions to behaviours;
- **Loader**: Enable/Disable behaviours on the fly.


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

```
usage: smartbot_full.py [-h] [--telegram-bot-token TELEGRAM_BOT_TOKEN]
                        [--slack-bot-token SLACK_BOT_TOKEN]
                        [--wolfram-app-id WOLFRAM_APP_ID]
                        [--admin-id ADMIN_ID] [--config CONFIG]

Run smartbot

optional arguments:
  -h, --help            show this help message and exit
  --telegram-bot-token TELEGRAM_BOT_TOKEN
                        The telegram bot token (or
                        env[SMARTBOT_TELEGRAM_TOKEN])
  --slack-bot-token SLACK_BOT_TOKEN
                        The slack bot token (or env[SMARTBOT_SLACK_TOKEN])
  --wolfram-app-id WOLFRAM_APP_ID
                        The wolfram app id (or env[SMARTBOT_WOLFRAM_APPID])
  --admin-id ADMIN_ID   The user id to admin (or env[SMARTBOT_ADMIN_ID])
  --config CONFIG       The configuration file (or env[SMARTBOT_CONFIG])
```

#### Configuration
Since version 1.0 you can use configuration file to customize bot behaviour. Some configuration options are supported already (examples in *config* directory). The most important is the **language** option where you can set the country language to make the bot answer the questions appropriately. The configuration file is set with *--config* argument or environment variables (please see *--help* for details).

```ini
# set bot basic knowledge
[main]
creator = Pedro Lira
language = pt-BR

# redirect to behaviour when first interaction word is one of below
[friendly_aliases]
standup = jalk
diga = talk
fale = talk
traduz = translateen
traduza = translateen
nasa = nasa
piada = joke
manda = gimage
quero = bimage

# Set default answers when bot does not have answer to that question
[friendly]
default-answer0 = Prefiro não comentar
default-answer1 = Não tenho informações suficientes na minha base para responder
default-answer2 = Não sei (ainda)
default-answer3 = Estou em fase de crescimento
default-answer4 = Me pergunte amanhã
```

#### Development
You are free to contribute with this project and even fork it. Of cource, following the license instructions. We will be available as much as possible to solve any doubts or issues about this project.

#### Documentation and Tests
The code and wiki documentation are in development.
The test suite is not that perfect, but we are in a pursuit to improve it. Manual tests confirm the project is stable enough to be in a public repository. Enjoy
