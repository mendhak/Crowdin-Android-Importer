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
            helper.getLanguageCodeFromPath(None)
            self.fail("Exception was not thrown")
        except ValueError:
            pass

    def test_getLanguageCodeFromAndroidPath_PathDefault_ReturnsEnglish(self):
        languageCode = helper.getLanguageCodeFromPath("/res/values")
        self.assertEqual(languageCode,"en")

    def test_getLanguageCodeFromAndroidPath_PathFr_ReturnsFrench(self):
        languageCode = helper.getLanguageCodeFromPath("/res/values-fr/strings.xml")
        self.assertEqual(languageCode, "fr")

    def test_getLanguageCodeFromAndroidPath_PathFRUPPERCASE_ReturnsFrench(self):
            languageCode = helper.getLanguageCodeFromPath("/res/values-FR")
            self.assertEqual(languageCode, "fr")

    def test_getLanguageCodeFromAndroidPath_PathPTRBR_ReturnsPortugueseBrazil(self):
            languageCode = helper.getLanguageCodeFromPath("/res/values-pt-rBR/")
            self.assertEqual(languageCode, "pt-BR")

    def test_getLanguageCodeFromAndroidPath_PathDoesNotContainValues_ReturnsAll(self):
            languageCode = helper.getLanguageCodeFromPath("/res/")
            self.assertEqual(languageCode, "all")
