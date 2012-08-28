import os
import re

def locateFile(fileName, rootDirectory=os.curdir):
    for path,directories,files in os.walk(rootDirectory):
        for file in files:
            if file.lower() == fileName.lower():
                 return os.path.join(path,file)

def locateDir(dirName, rootDirectory=os.curdir):
    for path,directories,files in os.walk(rootDirectory):
        for d in directories:
            if d.lower() == dirName.lower():
                 return os.path.join(path,d)


def isValidAndroidResourcePath(pathToStringsXml):
    if pathToStringsXml is None or len(pathToStringsXml) == 0:
        return False

    if "res" in pathToStringsXml and "values" in pathToStringsXml:
        if re.match(".*/res/values[\-a-zA-Z]*/strings\.xml", pathToStringsXml):
            return True
    return False


def GetLanguageCodesFromPath(path, langList=[]):

    if path is None:
        raise ValueError

    if "values" not in path:
        for d in os.listdir(path):
            subPath = os.path.join(path,d)
            if "res" in subPath and os.path.isdir(subPath):
                langList += GetLanguageCodesFromPath(subPath, langList)
        return list(set(langList))

    langCodes = re.search("values(\-)?(?P<country>([a-zA-Z]{1,2})?)(\-)?(?P<variant>([a-zA-Z]{1,3})?)", path, re.IGNORECASE)
    country = langCodes.group('country')
    variant = langCodes.group('variant')

    androidLanguageCode = country

    if not len(androidLanguageCode):
        return ["en"]

    androidLanguageCode = androidLanguageCode.lower()

    if variant is not None and len(variant) > 0:
        androidLanguageCode = androidLanguageCode + "-" + variant[1:]

    return [androidLanguageCode]


def GetCrowdinMappings(extractDir, fileName="strings.xml"):
    mappingDict = {}
    for d in os.listdir(extractDir):
        if os.path.isdir(os.path.join(extractDir, d)):
            stringsXml = locateFile(fileName,os.path.join(extractDir,d))
            if os.path.getsize(stringsXml) > 84:
                mappingDict[d] = stringsXml
    return mappingDict


def GetMatchingCrowdinFiles(languageCodes, crowdinMappings, includeNewFolders=False):
    mappingDict = {}
    languageCodes = sorted(languageCodes, reverse=True)

    #Map existing languageCodes
    for lc in languageCodes:

        if lc in crowdinMappings:
            #Direct match
            mappingDict[lc] = crowdinMappings[lc]
            crowdinMappings[lc] = None
        else:
            country = lc[0:2]
            basicVariant = country + "-" + country.upper()
            if basicVariant in crowdinMappings:
                #Doubled name variant, such as es-ES, pt-PT
                mappingDict[lc] = crowdinMappings[basicVariant]
                crowdinMappings[basicVariant] = None
            else:
                #First match on country
                for k,v in crowdinMappings.iteritems():
                    if k.startswith(country) and crowdinMappings[k] is not None:
                        mappingDict[lc] = crowdinMappings[k]
                        crowdinMappings[k] = None
                        break

    if includeNewFolders:
    #Map new languageCodes FROM Crowdin
        for k,v in crowdinMappings.iteritems():
            if v is not None:
                mappingDict[k] = v


    return mappingDict


def GetResDirectory(path):
    if "/res" not in path:
        return locateDir("res", path)
    else:
        resPosition = path.find("/res")
        if resPosition > -1:
            return path[0:path.find("/res")+4]


def GetTargetStringsXml(targetResDirectory, langCode):
    country = langCode[0:2]
    variant = langCode[3:]
    if variant is not None and len(variant) > 0:
        variant = "-r" + variant

    return os.path.join(targetResDirectory, "values-" + country + variant , "strings.xml")


def IsSingleFolderUpdate(path):
    if "/values" in path.lower():
        return True

    return False


def IsDefaultStringsXml(path):
    if "res/values/strings.xml" in path:
        return True
    return False