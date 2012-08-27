import tempfile
import urllib
import urllib2

class CrowdinAPI():

    def __init__(self, apiKey, projectIdentifier):
        self.apiKey = apiKey
        self.projectIdentifier = projectIdentifier

    def ExportTranslations(self):
        url = 'http://api.crowdin.net/api/project/{0}/export?key={1}'.format(self.projectIdentifier, self.apiKey)
        req = urllib2.Request(url, None)
        response = urllib2.urlopen(req)
        the_page = response.read()

    def DownloadLanguagesZip(self, languageCode):
        url = "http://api.crowdin.net/api/project/{0}/download/{1}.zip?key={2}".format(self.projectIdentifier, languageCode, self.apiKey)
        f = tempfile.TemporaryFile(prefix="Crowdin")
        return urllib.urlretrieve(url)

