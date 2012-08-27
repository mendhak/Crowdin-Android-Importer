#!/usr/lib/env python
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
parser = optparse.OptionParser(usage = "usage: %prog --p=PATH -a=get|upload -i my-crowdin-project -k 1234567", epilog="""
Examples:
    crowdin.py --path=/projectname/res/ -i my-crowdin-project -k 1234567
                        (Gets all translations from Crowdin. 'get' is implied)
    crowdin.py --path=/projectname/res/values-fr --action=get -i my-crowdin-project -k 1234567
                        (Gets French translations from Crowdin)
    crowdin.py --path=/projectname/res/values-fr/strings.xml --action=get -i my-crowdin-project -k 1234567
                        (Gets French translations from Crowdin)
    crowdin.py --path=/projectname/res/values/strings.xml --action=upload -i my-crowdin-project -k 1234567
                        (Replaces strings.xml on Crowdin. Use with caution.)
""")

parser.add_option("-p", "--path",
                  action="store", type="string", dest="path", help="The path to the file or directory of Android strings")
parser.add_option("-a", "--action",
                  action="store", type="string", dest="action", default="get", help="get or upload")
parser.add_option("-i", "--identifier",
                  action="store", type="string", dest="identifier", help="The Crowdin project identifier")
parser.add_option("-k", "--apikey",
                  action="store", type="string", dest="apikey", help="The Crowdin project API key")


testArgs = ["-p", "/home/mendhak/Code/Crowdin-Android-Importer/res/values/strings.xml", "-i", "identifier", "-k", "123456"]
(options, args) = parser.parse_args()

if options.path is None or options.identifier is None or options.apikey is None:
    args = ["-h"]
    parser.parse_args(args)


apiKey = options.apikey
projectIdentifier = options.identifier

print "Evaluating", options.path

if not os.path.exists(options.path):
    print "Path not found: " + options.path
    sys.exit(1)

isDirectory = os.path.isdir(options.path)
isFile = os.path.isfile(options.path)

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


if options.action == "update":
    if not helper.IsDefaultStringsXml(pathToStringsXml):
        print "Please only specify the default '/res/values/strings.xml' for upload"
        sys.exit(1)

    lc = CrowdinAPI(apiKey, projectIdentifier)
    lc.UploadTranslationFile(pathToStringsXml)
    print "Upload complete"

else:
    #Default is get

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
    isSingleFolderUpdate = helper.IsSingleFolderUpdate(options.path)
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

