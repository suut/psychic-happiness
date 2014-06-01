psychic-happiness
=================

A public-domain IRC bot written in Python 3.
This is version 2!

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the google.py file
* The username and password of the admin user hashed in SHA-1 in the users/users.ini file
* Your IRC servers in servers.ini, then the channels and infos in config/<server>.ini

The irc python module is not needed anymore, if you have it installed please uninstall it (neither is the six module).
You'll need the bs4 module (`pip install beautifulsoup4` or install this: http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/beautifulsoup4-4.3.2.tar.gz )

To add more fantasy commands:

Create the function in functions.py, it must look like this:

```
from core import ToSend
...
@Function('myfunc')
def my_func(args, source, target):
  """the thing to be printed by the help command"""
  # do something
  return ToSend(target, 'this will be printed back to channel')
```
If the function requires a certain auth level (`known`, `admin` or `master`), specify it in the decorator: `@Function('myfunc', authlvl='known')`.

(to be continued soon)
