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


def getLanguageCodeFromPath(path):
    if path is None:
        raise ValueError

    if "values" not in path:
        return "all"

    langCodes = re.search("values(\-)?(?P<country>([a-zA-Z]{1,2})?)(\-)?(?P<variant>([a-zA-Z]{1,3})?)", path, re.IGNORECASE)
    country = langCodes.group('country')
    variant = langCodes.group('variant')

    androidLanguageCode = country

    if androidLanguageCode is None:
        return "all"

    if not len(androidLanguageCode):
        return "en"

    androidLanguageCode = androidLanguageCode.lower()

    if variant is not None and len(variant) > 0:
        androidLanguageCode = androidLanguageCode + "-" + variant[1:]

    return androidLanguageCode


def getTargetDirectoryPath(pathToStringsXml, languageCode):
    return None