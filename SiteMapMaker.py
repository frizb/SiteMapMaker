#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SiteMapMaker - Creates a site map based on a target folder and root url
# Helpful for manual testing with tools like BurpSuite and for uncovering hidden functionality
#
# Copyright (c) 2017, Austin Scott
#
# Contact information:
# Austin Scott
#


"""
Main application logic and automation functions
"""

__version__ = '0.1'
__lastupdated__ = 'April 13, 2017'

###
# Imports
###
import os
import sys
import time
import urllib

class logger:
    DEBUG = False;
    VERBOSE = False;

    @staticmethod
    def debug(msg):
        if logger.DEBUG == True:
            print(msg)

    @staticmethod
    def verbose(msg):
        if logger.VERBOSE == True:
            print(msg)


class Colored:

    @staticmethod
    def red_back(printString):
        return "\033[0m\033[37m\033[41m" + printString

    @staticmethod
    def black(printString):
        return '\033[0;30m' + printString

    @staticmethod
    def red(printString):
        return '\033[0;31m' + printString

    @staticmethod
    def green(printString):
        return '\033[0;32m' + printString

    @staticmethod
    def yellow(printString):
        return '\033[0;33m' + printString

    @staticmethod
    def blue(printString):
        return '\033[0;34m' + printString

    @staticmethod
    def magenta(printString):
        return '\033[0;35m' + printString

    @staticmethod
    def cyan(printString):
        return '\033[0;36m' + printString

    @staticmethod
    def white(printString):
        return '\033[0;37m'  + printString

    @staticmethod
    def grey(printString):
        return '\033[0;38m' + printString

    @staticmethod
    def reset(printString):
        # return printString
        return '\033[0;39m' + printString

class SiteMapMaker:
    def __init__(self, argv):
        self.argv = argv
        self._start_time = time.clock()
        self._task_start_time = time.clock()
        self._column_width = 60
        self._root_url = "http://localhost"
        self._ignore_files = ("robots.txt",".ignore")
        self._site_map_file = ("sitemap.html")
        self._path_to_scan = "."
        self._text_list_mode = False
        self._summaryReport = []
        self._summaryReportTimer = []
        self._summaryRiskTotal = 0
        self._summaryRiskCount = 0

        # parse arguments
        self.parse_args()

    def get_version(self):
        return "%s" % (__version__)

    def add_to_summary_report(self, text):
        self._summaryReport.append(text)

    def print_banner(self):
        """
        Prints banner
        """
        print(Colored.red("Site Map Maker Version: " + __version__ + " Updated: " + __lastupdated__))

    def usage(self):
        print Colored.red_back("RedBack")
        print Colored.red("Red")
        print Colored.cyan("Cyan")
        print Colored.blue("Blue")
        print Colored.green("green")
        print Colored.white("White")
        print Colored.yellow("Yellow")
        print Colored.black("Black")
        print Colored.grey("Grey")
        print Colored.magenta("Magenta")
        print Colored.reset("Reset")

        print "\n- Command Line Usage\n\t``# %.65s [options]``\n" % sys.argv[0]
        print "Options\n-------"
        print "====================== =============================================================="
        print "-r --rootUrl            root URL to append file paths to (default=" + str(self._root_url) + ")"
        print "-s --siteMapFile        site map html file path to be created (default=" + str(self._site_map_file) + ")"
        print "-p --pathToScan         specify the path to scan (default=" + str(self._path_to_scan) + ")"
        print "                        use the forward slash / for both *nix and windows paths"
        print "-i --ignoreFiles        specify files to not scan (default=" + str(self._ignore_files) + ")"
        print "                        ignored files and file types should be comma separated "
        print "-t --textList           output as a text list rather than an HTML file"
        print "-v --verbose            verbose mode"
        print "-d --debug              show debug output"
        print "-l --log                output to log file"
        print "====================== =============================================================="
        print "Example:"
        print " python " + sys.argv[0] + " -r http://foo.bar -p c:/testpath/test/ -i .zip,.bak,robots.txt"

    def parse_args(self):
        import getopt
        try:
            opts, args = getopt.getopt(self.argv, "fhvdnr:s:p:i:",
                                       ["help"])
        except getopt.GetoptError, err:
            print str(err)
            self.usage()
            return 32

        for o, a in opts:
            if o in ("-v", "--verbose"):
                print "verbose"
                logger.VERBOSE = True
            elif o in ("-d", "--debug"):
                print "debug"
                logger.DEBUG = True
            elif o in ("-t", "--textList"):
                print "text list mode"
                self._text_list_mode = True
            elif o in ("-r", "--rootUrl"):
                self._root_url = a
            elif o in ("-s", "--siteMapFile"):
                self._site_map_file = a
            elif o in ("-p", "--pathToScan"):
                self._path_to_scan = a
            elif o in ("-i", "--ignoreFiles"):
                self._ignore_files = tuple(a.split(','))
            elif o in ("-h", "--help"):
                self.usage()
                sys.exit(0)
                return 0
            else:
                assert False, "unknown option"

    def site_map_maker(self):
        # Generate Validation Data Dumps
        logger().verbose(Colored.red("Starting site map build..."))
        with open(self._site_map_file, 'a') as site_map_file_handle:
            for root, subdirs, files in os.walk(os.path.normpath(self._path_to_scan)):
                logger().verbose('--\nroot = ' + root)
                for subdir in subdirs:
                    logger().verbose('\t- subdirectory ' + subdir)
                for filename in files:
                    file_path = os.path.join(root, filename)
                    logger().debug('\t\t- file %s (full path: %s)' % (filename, file_path))
                    if not file_path.lower().endswith(self._ignore_files):
                        url = file_path.replace(os.path.abspath(self._path_to_scan), '', 1)  # only replace the first in case of a period
                        logger().verbose('\t\t\t- ' + url)
                        url = urllib.pathname2url(url)
                        logger().verbose('\t\t\t- ' + url)
                        url = self._root_url + url
                        logger().verbose('\t\t\t- ' + url)
                        if self._text_list_mode:
                            site_map_file_handle.write(url + "\n")
                        else:
                            site_map_file_handle.write("<a href=\"%s\" title=\"%s\">%s</a><br>\n" % (url, file_path, url))
        print "DONE!"
        print "Site map file created: " + self._site_map_file
    ##################################################################################
    # Entry point for command-line execution
    ##################################################################################

    def main(self):
        self.print_banner()
        print(Colored.red("Recursively building site map from: " + str(self._path_to_scan)))
        print(Colored.red("for the base URL: " + str(self._root_url)))
        sys.stderr = open("errorlog.txt", 'w')

        # remove previous report
        if os.path.isfile(self._site_map_file):
            os.remove(self._site_map_file)

        self.site_map_maker()
        sys.exit(0)
        return 0

def main(argv=None):
    siteMapMaker = SiteMapMaker(argv if argv else sys.argv[1:])
    return siteMapMaker.main()


if __name__ == "__main__":
    sys.exit(main())
