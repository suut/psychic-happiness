psychic-happiness
=================

An public-domain IRC bot written in Python.

If you are willing to use it, please fill in the proper informations:
* Your Google API key in the google.py file
* The username and password hashed in SHA-1 in the users.ini file
* Your IRC servers and channels in the servers.ini
* And the selectionned server in config.ini

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
