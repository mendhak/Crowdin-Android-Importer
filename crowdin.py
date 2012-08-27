#!/usr/lib/env python
import ConfigParser
import optparse
from optparse import OptionParser
import os
import sys
import helper

parser = OptionParser()

optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog
parser = optparse.OptionParser(usage = "usage: %prog --path=PATH [--action=(get|upload)]", epilog="""
Examples:
    crowdin.py --path=/projectname/res/
                        (Gets all translations from Crowdin. 'get' is implied)
    crowdin.py --path=/projectname/res/values-fr --action=get
                        (Gets French translations from Crowdin)
    crowdin.py --path=/projectname/res/values-fr/strings.xml --action=get
                        (Gets French translations from Crowdin)
    crowdin.py --path=/projectname/res/values/strings.xml --action=upload
                        (Replaces strings.xml on Crowdin. Use with caution.)
""")

parser.add_option("-p", "--path",
                  action="store", type="string", dest="path", help="The path to the file or directory of Android strings")
parser.add_option("-a", "--action",
                  action="store", type="string", dest="action", default="get", help="get or upload")


testArgs = ["-p", "foo.txt"]
(options, args) = parser.parse_args(testArgs)

if options.path is None:
    args = ["-h"]
    parser.parse_args(args)

try:
    config = ConfigParser.RawConfigParser()
    config.read('crowdin.cfg')
    apiKey = config.get('Crowdin', 'apikey')
    projectIdentifier = config.get('Crowdin', 'projectidentifier')
except:
    print """
        Missing config file, please create crowdin.cfg with the contents:
                    [Crowdin]
                    apikey = 123412341234
                    projectidentifier = my-project-name
        You will need to fill the values from the API tab on your Crowdin project page"""
    sys.exit(1)




print "Evaluating", options.path

if not os.path.exists(options.path):
    print "Path not found: " + options.path
    sys.exit(1)

isDirectory = os.path.isdir(options.path)
isFile = os.path.isfile(options.path)

if isDirectory:
    pathToStringsXml = helper.locate("strings.xml", options.path)

    if not helper.isValidAndroidResourcePath(pathToStringsXml):
        print "Not a valid Android resources directory"
        sys.exit(1)

elif isFile:
    pathToStringsXml = options.path

    if not helper.isValidAndroidResourcePath(pathToStringsXml):
        print "Not a valid Android resource file"
        sys.exit(1)

languageCode = helper.getLanguageCodeFromPath(options.path)
print "Language:", languageCode

# Now download all from Crowdin



"""

Check dir or file exists

/home/mendhak/Code/gpslogger/GPSLogger/res/, GET
    Export Translations (http://crowdin.net/page/api/export)
    Download zip (http://crowdin.net/page/api/download)
    Unzip
    Mapping of Crowdin to Android
    Copy strings.xml to mapped folders


/home/mendhak/Code/gpslogger/GPSLogger/res/values-ja, GET
    Export Translations (http://crowdin.net/page/api/export)
    Download zip (http://crowdin.net/page/api/download)
    Unzip
    Mapping of values-ja to Crowdin Folders
    Copy strings.xml to values-ja












"""