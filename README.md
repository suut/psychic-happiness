psychic-happiness
=================

A public-domain IRC bot written in Python 3.
This is version 2!

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the `google.py` file
* The username and password of the admin user hashed in SHA-1 in the `users/users.ini` file
* Your IRC servers in servers.ini, then the channels and infos in `config/<server>.ini`

The `irc` python module is not needed anymore (neither is the `six` module), if you have it please remove it.
Modules needed: `beautifulsoup4`, `requests`, `forbiddenfruit`. Just run `pip install beautifulsoup4 requests forbiddenfruit`.

To add more commands:

* Create the function in `functions.py` (you can put it in another file but be sure to import it in `main.py`, it must look like this:
```python
from functions_core import Function
...
@Function('myfunc')
def my_func(args, source, target):
  """the thing to be printed by the help command"""
  # do something
  yield 'this will be printed back to channel'
  yield 'and this too'
  yield 'yet another line'
  yield '{color.red.bold}this will be bold red'
```
* If the function requires a certain auth level (`known`, `admin` or `master`), specify it in the decorator: `@Function('myfunc', authlvl='known')`.
* If the function requires the Channel object, specify it in the decorator: `@Function('myfunc', requestchans=True) then modify the function header: `def my_func(args, source, target, channels)`. To get the userlist: `channels[target].userdict.keys()`.
* If the function requires special action of the serv (e.g. notice of private message), specify it in the decorator: `@Function('myfunc', requestserv=True)` then modify the function header: `def my_func(args, source, target, serv)`.
* You can use `return` in a function but this is deprecated. If you want to emulate the behavior of `return`, just add `stop()` the line after your `yield`.

### Colors
* You can chain the attributes in whatever order you want, like that: {colors.red.blue.bold.underlined.italic}. You can specify up to two colors, first will be the text color, and second will be background color. Valid attributes are: bold, underlined, italic, reverse (inverses background and text color), and reset, to reset every attributes. Valid colors could be found in format.py.
* If you're using the serv object directly, and you need colors, you'll need to add `.format(color=format.color)` after your string. Make sure `format` is included.

Note: every command can be sent to the bot via channel msg, or via privmsg
### Admin commands
| Description                     | Requires | Usage                                                                    |
| :-----------------------------: | :------: | :----------------------------------------------------------------------: |
| Know if you're authed           |          | `WHOAMI`                                                                 |
| To log in                       |          | `AUTH username password` (use that only in privmsg..)                    |
| Change nick                     | `master` | `NICK newnickname`                                                       |
| Quit                            | `master` | `DIE [reason]`                                                           |
| Save configuration              | `master` | `SAVECONFIG`                                                             |
| Join a channel                  | `admin`  | `JOIN #channel`                                                          |
| Part a channel                  | `admin`  | `part #channel [reason]` or `part [reason]` (when on the target channel) |
| Adjust flood-control (in secs)  | `admin`  | `THROTTLE [time]`                                                        |
| Saves configuration             | `admin`  | `SAVECONFIG`                                                             |
| Notice a user/channel           | `known`  | `NOTICE user message`                                                    |
| Performs an action on a channel | everyone | `ACT #channel action`                                                    |
| Say something on a channel      | everyone | `SAY #channel message`                                                   |
| Show configuration              | everyone | `SHOWCONFIG`                                                             |


### User commands
User commands require no authentication, normal user priviledges, and of course: known users, admins and masters can run these commands.

| Description                                | Usage                                                                    |
| :----------------------------------------: | :----------------------------------------------------------------------: |
| Pongs you                                  | `PING`                                                                   |
| Gives you eye cancer                       | `EYECANCER`                                                              |
| Obtains the first result from Google       | `G query` or `GOOGLE query`                                              |
| Obtains the first result from YouTube      | `YT query` or `YOUTUBE query`                                            |
| A command you can hold on to               | `HELP`                                                                   |
| Tries to determine exactly who/what you are| `QUISUISJE`                                                              |
| Tests how the bot handles exceptions       | `ERROR`                                                                  |
| Gives you a URL to the source code         | `SOURCE`                                                                 |
| Gives you the current version of the bot   | `VERSION`                                                                |
| Gives you a RAINBOW (color test) :p        | `RAINBOW`                                                                |
| Obtains the first result from SoundCloud   | `SC query` or `SOUNDCLOUD query`                                         |
| Feels the weather at a specified location  | `W city, country` or `WEATHER city, country`                             |

***For the WEATHER command*** If the specified city or country is written in another script instead Latin script, sometimes specifying it in Latin Transliteration helps, instead of เชียงใหม่ , write it as: Chiang Mai.

This is so with characters that are not specified in ***Basic Latin***. Such as: Hafnarfjörður, Iceland; should be transliterated to: Hafnarfjordur, Iceland (Change o with diaeresis to: 'o', and Eth to 'd')
