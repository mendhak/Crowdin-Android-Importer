#!/usr/lib/env python
import ConfigParser
import filecmp
import optparse
from optparse import OptionParser
import os
import shutil
import sys
from zipfile import ZipFile
import helper
from libcrowdin import CrowdinAPI

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


testArgs = ["-p", "/home/mendhak/Code/Crowdin-Android-Importer/res"]
(options, args) = parser.parse_args()

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
isSingleFolderUpdate = helper.IsSingleFolderUpdate(options.path)

if isDirectory:
    pathToStringsXml = helper.locateFile("strings.xml", options.path)

    if not helper.isValidAndroidResourcePath(pathToStringsXml):
        print "Not a valid Android resources directory"
        sys.exit(1)

elif isFile:
    pathToStringsXml = options.path

    if not helper.isValidAndroidResourcePath(pathToStringsXml):
        print "Not a valid Android resource file"
        sys.exit(1)

languageCodes = helper.GetLanguageCodesFromPath(options.path)
print "Language:", languageCodes

# Build new package on Crowdin
print "Rebuilding latest package on Crowdin"
lc = CrowdinAPI(apiKey, projectIdentifier)
lc.ExportTranslations()

# Download all from Crowdin
zipPath = lc.DownloadLanguagesZip("all")
print "Downloaded to", zipPath[0]

#Extract to /tmp/Crowdin
zip = ZipFile(zipPath[0])
extractDir = os.path.join(os.path.dirname(zipPath[0]), "Crowdin")
zip.extractall(extractDir)
print "Extracted to", extractDir

print "Attempting to match Crowdin files with Android"
#Get valid Crowdin folder mappings
crowdinMappings = helper.GetCrowdinMappings(extractDir)

#Get list of files to copy
matchingFiles = helper.GetMatchingCrowdinFiles(languageCodes, crowdinMappings, not isSingleFolderUpdate)


#Get res directory
targetResDirectory = helper.GetResDirectory(options.path)

#Copy the files
if not len(matchingFiles):
    print "No matching files found"

for k,v in matchingFiles.iteritems():
    targetStringsXml = helper.GetTargetStringsXml(targetResDirectory, k)

    if not os.path.exists(os.path.dirname(targetStringsXml)):
           os.makedirs(os.path.dirname(targetStringsXml))

    try:
        if not os.path.exists(targetStringsXml) or not filecmp.cmp(matchingFiles[k], targetStringsXml):
            print "Replacing", targetStringsXml
            shutil.copy(matchingFiles[k], targetStringsXml)
        else:
            print "Skipping", targetStringsXml, ", it is already up to date"
    except:
        print "Error. No Crowdin file for ", targetStringsXml

print "Deleting", extractDir
shutil.rmtree(extractDir)

print "Deleting", zipPath[0]
os.remove(zipPath[0])

