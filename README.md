# dotdotslash
An tool to help you search for Directory Transversal Vulnerabilities

# Benchmarks
Platforms that I tested to validate tool efficiency:
* [DVWA](https://github.com/ethicalhack3r/DVWA) (low/medium/high)
* [bWAPP](http://www.itsecgames.com/) (low/medium/high)


# Screenshots

![Screenshot](https://raw.githubusercontent.com/jcesarstef/dotdotslash/master/poc1.png)

![Screenshot](https://raw.githubusercontent.com/jcesarstef/dotdotslash/master/poc2.png)



# Instalation
You can download the last version cloning this repository

```
git clone https://github.com/jcesarstef/dotdotslash/
```

This tool has made to work with Python3

# Usage

```
python3 dotdotslash.py --help

usage: dotdotslash.py [-h] --url URL --string STRING [--cookie COOKIE]

dot dot slash - A automated Path Transversal Tester. Created by @jcesrstef.

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Url to attack.
  --string STRING  String in --url to attack. Ex: document.pdf
  --cookie COOKIE  Document cookie.
```

Example:

```
python3 dotdotslash.py \
--url "http://192.168.58.101/bWAPP/directory_traversal_1.php?page=a.txt" \
--string "a.txt" \
--cookie "PHPSESSID=089b49151627773d699c277c769d67cb; security_level=3"

```
# Links
* My twitter: https://twitter.com/jcesarstef
* My Linkedin: https://www.linkedin.com/in/jcesarstef
* My Blog(Brazilian Portuguese only for now): http://www.inseguro.com.br
