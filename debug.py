#!/usr/bin/python3

import argparse

from urllib import request

parser = argparse.ArgumentParser(description = 'Um programa de exemplo.')
parser.add_argument('--url', action = 'store', dest = 'url', required = True, help = 'Url to attack.')
arguments = parser.parse_args()
print(arguments.url)


def req(self, cookie=None):
	req = request.Request(self)
	if cookie is not None:
		req.add_header('Cookie', cookie)
	response = request.urlopen(req)
	return response.read().decode()


a = req('http://192.168.58.101/bWAPP/directory_traversal_1.php?page=robots.txt', 'PHPSESSID=839296168c14a90c694c27eb245217be; security_level=0')
print(a)
	
