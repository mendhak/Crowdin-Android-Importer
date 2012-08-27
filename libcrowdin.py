import tempfile
import urllib
import urllib2
import pycurl
from cStringIO import StringIO

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

    def UploadTranslationFile(self, pathToStringsXml):
        url ="http://api.crowdin.net/api/project/{0}/update-file?key={1}".format(self.projectIdentifier, self.apiKey)
        filename=pathToStringsXml
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.HTTPPOST, [(('files[strings.xml]', (c.FORM_FILE, filename)))])
        #c.setopt(c.VERBOSE, 1)
        bodyOutput = StringIO()
        headersOutput = StringIO()
        c.setopt(c.WRITEFUNCTION, bodyOutput.write)
        c.setopt(c.URL, url )
        c.setopt(c.HEADERFUNCTION, headersOutput.write)
        c.perform()
        bodyOutput.getvalue()

