psychic-happiness
=================

An public-domain IRC bot written in Python 3.

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the google.py file
* The username and password of the admin user hashed in SHA-1 in the users.ini file
* Your IRC servers and channels in the servers.ini
* And the selectionned server in config.ini

The irc python module is needed (and it needs the six module), install it via pip or download it from the following links (copy the irc directory to the `<python dir>/lib/sites-package/` directory, and run `python install.py install` into the unzipped six dir):
* https://pypi.python.org/pypi/irc
* https://pypi.python.org/pypi/six

To add more fantasy commands:

Create the function in fantasy.py, it must look like this:

```
def my_func(source, args):
  """the thing to be printed by the help command"""
  # do something
  return 'this will be printed back to channel'
```

* `source` is a `NickMask` object, use source.nick to know who called the command
* args is a tuple containing every arguments that was in the command call, if you want to get them back as a plain string, use `' '.join(args)`. Calling the command like this `.my_command a b c` will call the function with `args = ('a', 'b', 'c')`, using `' '.join(args)` will return `'a b c'`.
* The docstring is mandatory
* You can use `\n` in the returned string, it will automatically be split into several messages, but most server will get angry if there is more than 3 messages at a time

Then add the function to the binding dictionnary:

```
binding = {...,
           'my_command': my_func}
```

How to use the bot:
* Type `.help` (replace . with the command prefix you chose) to have a list of all commands, and `.help <command>` to know more about a particular command
* To auth with the bot, use `/MSG <bot name> AUTH <username> <password>`
* To logout with the bot, use `/MSG <bot name> LOGOUT`
