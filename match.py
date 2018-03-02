befvar = (
"./",
"",
".\\",
"file:",
"file:/",
"file://",
"file:///",
)

dotvar = (
"/..",
"....//",
"//....",
"%252e%252e%255c",
"%2e%2e%5c",
"..%255c",
"..%5c",
"%5c../",
"/%5c..",
"..\\",
"%2e%2e%2f",
"../",

)

match = {
# Windows
"c:\\boot.ini": "boot\W*loader",
"c:\windows\system32\drivers\hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\W+[a-zA-Z0-9-_.]*",

# Linux
"etc/hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\W+[a-zA-Z0-9-_.]*",
"etc/passwd": "\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*\w\:[\/a-zA-Z0-9]*",

# TODO
#"etc/group": "\w+\:\w\:[0-9]\:(|[a-z,]*)",

# Apache
".htaccess": "AccessFileName|RewriteEngine|allow from all|deny from all|DirectoryIndex|AuthUserFile|AuthGroupFile",

# PHP
# http://php.net/manual/pt_BR/reserved.variables.php
"login.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
"index.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
}
