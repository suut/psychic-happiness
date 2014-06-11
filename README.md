psychic-happiness
=================

A public-domain IRC bot written in Python 3.
This is version 2!

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the `google.py` file
* The username and password of the admin user hashed in SHA-1 in the `users/users.ini` file
* Your IRC servers in servers.ini, then the channels and infos in `config/<server>.ini`

The `irc` python module is not needed anymore (neither is the `six` module), if you have it please remove it.
You'll need the `bs4` module (`pip install beautifulsoup4` or install [this](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/beautifulsoup4-4.3.2.tar.gz)), and the `requests` module: `pip install requests` or [this](https://github.com/kennethreitz/requests/tarball/master).

To add more commands:

* Create the function in `functions.py` (you can put it in another file but be sure to import it in `main.py`, it must look like this:
```python
from functions_core import Function
...
@Function('myfunc')
def my_func(args, source, target):
  """the thing to be printed by the help command"""
  # do something
  return 'this will be printed back to channel'
```
* If the function requires a certain auth level (`known`, `admin` or `master`), specify it in the decorator: `@Function('myfunc', authlvl='known')`.
* If the function requires the Channel object, specify it in the decorator: `@Function('myfunc', requestchans=True) then modify the function header: `def my_func(args, source, target, channels)`. To get the userlist: `channels[target].userdict.keys()`.
* If the function requires special action of the serv (e.g. notice of private message), specify it in the decorator: `@Function('myfunc', requestserv=True)` then modify the function header: `def my_func(args, source, target, serv)`.

Note: every command can be sent to the bot via channel msg, or via privmsg
### Admin commands
| Description                     | Requires | Usage                                                                    |
| :-----------------------------: | :------: | :----------------------------------------------------------------------: |
| Know if you're authed           |          | `WHOAMI`                                                                 |
| To log in                       |          | `AUTH username password` (use that only in privmsg..)                    |
| Change nick                     | `master` | `NICK newnickname`                                                       |
| Quit                            | `master` | `DIE [reason]`                                                           |
| Join a channel                  | `admin`  | `JOIN #channel`                                                          |
| Part a channel                  | `admin`  | `part #channel [reason]` or `part [reason]` (when on the target channel) |
| Adjust flood-control (in secs)  | `admin`  | `THROTTLE [time]`
| Notice an user/channel          | `known`  | `NOTICE user message`                                                    |
| Performs an action on a channel | `known`  | `ACT #channel action`                                                    |
| Say something on a channel      | `known`  | `SAY #channel message`                                                   |
| Saves configuration             | `admin`  | `SAVECONFIG`                                                             |
