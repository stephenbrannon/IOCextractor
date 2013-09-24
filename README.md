IOCextractor
============

IOC (Indicator of Compromise) Extractor: a program to help extract IOCs from text files. The general goal is to speed up the process of parsing structured data (IOCs) from unstructured or semi-structured data (like case reports or security bulletins). 

Compatibility and Requirements
------------------------------
* Compatible and tested Python versions: 2.7
* Compatible and tested operating systems: Windows 7, Mac OS 10.8.4, Ubuntu 13.04
* IOCextractor requires TkInter (http://wiki.python.org/moin/TkInter). 
* OpenIOC exporting requires the ioc_writer library (https://github.com/mandiant/ioc_writer).
* CybOX exporting requires python-cybox >= 2.0.1.0 (https://pypi.python.org/pypi/cybox/)

The program is written in Python 2.7, and a binary version for Windows is provided (IOCextractor.zip). 

Usage
-----
This program helps extract indicators of compromise from a plain text file. It currently identifies MD5 hashes, IPv4 addresses, domains, URLs, and email addresses. First, when a user opens a file, the program identifies potential IOCs using regular expressions (ignoring a few obvious false positives, like IP addresses that start with 10). It tags and highlights the potential IOCs for a user to review. 

A user can remove a tag by selecting its range of text and then either clicking the "Clear" button or right-clicking the selected text (command-click instead in Mac OS). It's also possible to remove all the tags from a large range of text, like a list of victim IP addresses, by selecting the whole range and clicking "Clear" or right-clicking. A user can add a tag by selecting a range of text and then clicking the corresponding button, for example "MD5." For any range of text that is either rejected or added, the program will search through the rest of the text to apply the same change everywhere. So if a user removes a tag from a victim IP address, the program will un-tag that IP address everywhere; it works the same for tagging a new IP address. 

After a user has reviewed the tagging for accuracy, the program will export a list of unique tagged IOCs. It currently either exports to the console or saves a file in one of the following formats: CSV, CybOX Observables XML, OpenIOC 1.1. It is also set up so anyone could easily add another output format for a specific application. 

A simple demonstration case report (DemonstrationCaseReport.txt) and a testing file (TestDocument.txt) are also provided. 

Credits
------
* [bworrell] (https://github.com/bworrell) - For adding the ability to export a CybOX Observables XML document. 
* [williamgibb] (https://github.com/williamgibb) - For adding the ability to export in OpenIOC 1.1 format.
