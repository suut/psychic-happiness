psychic-happiness
=================

An public-domain IRC bot written in Python 3.

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the google.py file
* The username and password hashed in SHA-1 in the users.ini file
* Your IRC servers and channels in the servers.ini
* And the selectionned server in config.ini

The irc python module is needed (and it needs the six module), install it via pip or download it from the following links (copy the irc directory to the [python dir]/lib/sites-package/ directory, and run `python install.py install` into the unzipped six dir):
* https://pypi.python.org/pypi/irc
* https://pypi.python.org/pypi/six/

To add more fantasy commands:

Create the function in fantasy.py, it must look like this:

```
def my_func(source, args):
  # do something
  return 'this will be printed back to channel'
```
    
Then add it to the binding dictionnary:

```
binding = {...,
           'my_func': my_func}
```
