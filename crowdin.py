import optparse

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
(options, args) = parser.parse_args()

if options.path is None:
    args = ["-h"]
    parser.parse_args(args)


