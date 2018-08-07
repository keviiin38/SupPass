![SupPass Official 
Logo](https://github.com/keviiin38/SupPass/blob/master/SupPass-WebExtension/img/logos/SupPass_Official_Logo.png)


<p align="center"><b>-- No Credentials Storage. No Problem. --</b></p>

<br>

# Intro

SupPass is a light weight app that allow you to generate password based on 3 inputs: username, domain name, and a master password.
The algorithm generate a password for the site you are visiting for you to use it has login/registration.
<br><br>
The main advantage to use SupPass is that password are not stored anywhere online nor offline, so you only need to remember your master password and username.
<br><br>
This app generate hard to brute-force/guess passwords, but we are NOT responsible if your master password or generated passwords are stolen.
  
<br>

# Python Version #

## Requirements ##

- [Python 3.x](https://www.python.org/downloads/)


## Usage ##
- List all options :

  `./SupPass.py`**`-h`**
  
  `python3 SupPass.py`**`--help`**
  
- Get your password :

  `./SupPass.py`**`-u`**_`USERNAME`_**`-d`**_`DOMAIN`_**`-p`**_`PASSWORD`_
  
  `python3 SupPass.py`**`--username`**_`USERNAME`_**`--domain`**_`DOMAIN`_**`--password`**_`PASSWORD`_

## Options ##

```
  -h, --help          Show the help
  
  -u, --username      Input username for the site (pseudo, mail, etc...)
  -d, --domain        Domain name of the site (example.org, google.com, etc...)
  -p, --password      Master password of the user
  
  -s, --see           Enable the print of the password
  -c, --clipoff       Disable the copy in clipboard
  -t, --timer         Timer before flushing the clipboard
```

<br>

# Web Extension Version #

## Requierements ##

| Browser | Support | Versions | Download |
| ------- | :-----: | :------: | :------: |
| Firefox | ✔ | _all_ | [Firefox Add-on](https://addons.mozilla.org/en-US/firefox/addon/suppass/) |
| Chrome | ✔ | _all_ | [Chrome Add-on](https://chrome.google.com/webstore/detail/suppass/fklgepdjmpjieiaimccffgplclogcbbf) |
| Chromium | ✔ | _all_ | [Chrome Add-on](https://chrome.google.com/webstore/detail/suppass/fklgepdjmpjieiaimccffgplclogcbbf) |
| Safari | **?** | _?_ | |
| Edge | **?** | _?_ | |
| I.E | **?** | _?_ | |
| Opera | **?** | _?_ | |

## Usage ##

Download the web extension from the link above.

<br>

# Credits

- [@keviiin38](https://github.com/keviiin38)
- [@Johnny201](https://github.com/2O4)
- [@yloukili](https://github.com/yloukili)
- [@Dramelac](https://github.com/Dramelac)

<br>
<br>

<p align="center">Projet d'excellence 2018 - Laboratoire Sécurité - SUPINFO Lyon
