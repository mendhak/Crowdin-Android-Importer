import os
import unittest
import helper


class BasicTests(unittest.TestCase):

    def setUp(self):
        pass;

    def test_locate_ExistingFile_ReturnsPathToFile(self):
        l = helper.locate("python", "/usr/bin")
        self.assertEqual("/usr/bin/python", l)

    def test_locate_FileDoesntExist_ReturnsNone(self):
        l = helper.locate("asdfasdf", os.curdir)
        self.assertIsNone(l)

    def test_isValidAndroidResourcePath_NonePath_ReturnsFalse(self):
        p = helper.isValidAndroidResourcePath(None)
        self.assertFalse(p)

    def test_isValidAndroidResourcePath_ContainResValuesStringsXml_ReturnsTrue(self):
        p = helper.isValidAndroidResourcePath("/hello/res/values/strings.xml")
        self.assertTrue(p)

    def test_isValidAndroidResourcePath_FrenchValuesIsValidPath_ReturnsTrue(self):
        p = helper.isValidAndroidResourcePath("/hello/res/values-fr/strings.xml")
        self.assertTrue(p)

    def test_isValidAndroidResourcePath_PTBRValueIsValidPath_ReturnsTrue(self):
            p = helper.isValidAndroidResourcePath("/hello/res/values-pt-rBR/strings.xml")
            self.assertTrue(p)

    def test_isValidAndroidResourcePath_DeValuesFolder_ReturnsFalse(self):
        p = helper.isValidAndroidResourcePath("/hello/res/devalues/strings.xml")
        self.assertFalse(p)

    def test_getLanguageCodeFromAndroidPath_NonePath_ThrowsError(self):
        try:
            helper.GetLanguageCodesFromPath(None)
            self.fail("Exception was not thrown")
        except ValueError:
            pass

    def test_getLanguageCodeFromAndroidPath_PathDefault_ReturnsEnglish(self):
        languageCode = helper.GetLanguageCodesFromPath("/res/values")
        self.assertEqual(languageCode[0],"en")

    def test_getLanguageCodeFromAndroidPath_PathFr_ReturnsFrench(self):
        languageCode = helper.GetLanguageCodesFromPath("/res/values-fr/strings.xml")
        self.assertEqual(languageCode[0], "fr")

    def test_getLanguageCodeFromAndroidPath_PathFRUPPERCASE_ReturnsFrench(self):
        languageCode = helper.GetLanguageCodesFromPath("/res/values-FR")
        self.assertEqual(languageCode[0], "fr")

    def test_getLanguageCodeFromAndroidPath_PathPTRBR_ReturnsPortugueseBrazil(self):
        languageCode = helper.GetLanguageCodesFromPath("/res/values-pt-rBR/")
        self.assertEqual(languageCode[0], "pt-BR")

    def test_getLanguageCodeFromAndroidPath_PathDoesNotContainValues_ReturnsAll(self):
        languageCode = helper.GetLanguageCodesFromPath("/home/mendhak/Code/Crowdin-Android-Importer/")
        self.assertTrue(len(languageCode) == 3)

    def test_GetMatchingCrowdinFiles_MatchingFrench_ReturnsPathToFrenchFile(self):
        lc = ['en', 'fr', 'sv-SE']
        cm = {'fr':'/french'}
        matches = helper.GetMatchingCrowdinFiles(lc, cm)
        self.assertEqual(matches['fr'], "/french")

    def test_GetMatchingCrowdinFiles_NonMatchingEnglish_NotReturnedInDictionary(self):
            lc = ['en', 'fr', 'sv-SE']
            cm = {'fr':'/french'}
            matches = helper.GetMatchingCrowdinFiles(lc, cm)
            self.assertTrue('en' not in matches)

    def test_GetMatchingCrowdinFiles_NoWideScopedLanguageCode_ReturnsPathToNarrowScope(self):
            lc = ['en', 'fr', 'pt']
            cm = {'fr':'/french', 'pt-PT' : '/narrowPortuguese'}
            matches = helper.GetMatchingCrowdinFiles(lc, cm)
            self.assertEqual(matches['pt'], '/narrowPortuguese')

    def test_GetMatchingCrowdinFiles_DifferentNarrowScope_ReturnsPathToDifferentNarrowScope(self):
            lc = ['en', 'fr', 'pt', 'es']
            cm = {'fr':'/french', 'pt-PT' : '/narrowPortuguese', 'es-MX' : '/mexicanPath'}
            matches = helper.GetMatchingCrowdinFiles(lc, cm)
            self.assertEqual(matches['es'], '/mexicanPath')


