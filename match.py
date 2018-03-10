befvar = (
"",
"./",
"/",
"\\",
"",
".\\",
"file:",
"file:/",
"file://",
"file:///",
)

dotvar = (
"",
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
"..%2f",
"%2e%2e/",
"%2e%2e%2f",
"..%252f",
"%252e%252e/",
"%252e%252e%252f",
"..%5c..%5c",
"%2e%2e\\",
"%2e%2e%5c",
"%252e%252e\\",
"%252e%252e%255c",
"..%c0%af",
"%c0%ae%c0%ae/",
"%c0%ae%c0%ae%c0%af",
"..%25c0%25af",
"%25c0%25ae%25c0%25ae/",
"%25c0%25ae%25c0%25ae%25c0%25af",
"..%c1%9c",
"%c0%ae%c0%ae\\",
"%c0%ae%c0%ae%c1%9c",
"..%25c1%259c",
"%25c0%25ae%25c0%25ae\\",
"%25c0%25ae%25c0%25ae%25c1%259c",
"..%%32%66",
"%%32%65%%32%65/",
"%%32%65%%32%65%%32%66",
"..%%35%63",
"%%32%65%%32%65/",
"%%32%65%%32%65%%35%63",
"../",
"...\\",
"..../",
"....\\",
"........................................................................../",
"..........................................................................\\",
"..%u2215",
"%uff0e%uff0e%u2215"
"..%u2216",
"..%uEFC8",
"..%uF025",
"%uff0e%uff0e\\",
"%uff0e%uff0e%u2216",

)

match = {
# Windows
"c:\\boot.ini": "boot\W*loader",
"c:\windows\system32\drivers\hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[ \t]+[a-zA-Z0-9-_.]*",

# Linux
"etc/hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[ \t][a-zA-Z0-9-_.]*",
"etc/passwd": "\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]+:[\/a-zA-Z0-9]*",
# TODO
#"etc/group": "\w+\:\w\:[0-9]\:(|[a-z,]*)",

# Apache
".htaccess": "AccessFileName|RewriteEngine|allow from all|deny from all|DirectoryIndex|AuthUserFile|AuthGroupFile",

# PHP
# http://php.net/manual/pt_BR/reserved.variables.php
"login.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
"index.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
}
