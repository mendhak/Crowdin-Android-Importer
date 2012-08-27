import os
import re

def locate(fileName, rootDirectory=os.curdir):
    for path,directories,files in os.walk(rootDirectory):
        for file in files:
            if file.lower() == fileName.lower():
                 return os.path.join(path,file)


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
            stringsXml = locate(fileName,os.path.join(extractDir,d))
            if os.path.getsize(stringsXml) > 84:
                mappingDict[d] = stringsXml
    return mappingDict


def GetMatchingCrowdinFiles(languageCodes, crowdinMappings):
    mappingDict = {}
    for lc in languageCodes:

        if lc in crowdinMappings:
            #Direct match
            mappingDict[lc] = crowdinMappings[lc]
        else:
            country = lc[0:2]
            variant = lc[4:]
            basicVariant = country + "-" + country.upper()
            if basicVariant in crowdinMappings:
                #Doubled name variant, such as es-ES, pt-PT
                mappingDict[lc] = crowdinMappings[basicVariant]
            else:
                #First match on country
                for k,v in crowdinMappings.iteritems():
                    if k.startswith(country):
                        mappingDict[lc] = crowdinMappings[k]

    return mappingDict