# SiteMapMaker
Creates an HTML site map based on a specified base URL and a folder path.  Handy for exploring for hidden content in Burp Suite if you have the application’s source code.
Site Map Maker written in Python 2.7 and supports both Windows and Linux.

## Command Line Parameter Help

'''
python.exe SiteMapMaker.py -h

- Command Line Usage
	``# SiteMapMaker.py [options]``

Options
-------
====================== ==============================================================
-r --rootUrl            root URL to append file paths to (default=http://localhost)
-s --siteMapFile        site map html file path to be created (default=sitemap.html)
-p --pathToScan         specify the path to scan (default=.)
                        use the forward slash / for both *nix and windows paths
-i --ignoreFiles        specify files to not scan (default=('robots.txt', '.ignore'))
                        ignored files and file types should be comma separated 
-t --textList           output as a text list rather than an HTML file
-v --verbose            verbose mode
-d --debug              show debug output
-l --log                output to log file
====================== ==============================================================
Example:
 python SiteMapMaker.py -r http://foo.bar -p c:/testpath/test/ -i .zip,.bak,robots.txt

'''

## Sample Output
'''
python SiteMapMaker.py -r http://localhost -p . -i .zip,.bak,robots.txt
'''
```html
<pre>
<a href="http://localhost/Test/JavaScript.js" title=".\Test\JavaScript.js">http://localhost/Test/JavaScript.js</a><br>
<a href="http://localhost/Test/TEST1.html" title=".\Test\TEST1.html">http://localhost/Test/TEST1.html</a><br>
<a href="http://localhost/Test/TEST2.html" title=".\Test\TEST2.html">http://localhost/Test/TEST2.html</a><br>
<a href="http://localhost/Test/CSS/style.css" title=".\Test\CSS\style.css">http://localhost/Test/CSS/style.css</a><br>
</pre>
```
