#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#This script helps extract indicators of compromise (IOCs) from a text file.
#A user can add or remove tagged indicators then export the remaining tags.
#Usage: "python IOCextractor.py" or "python IOCextractor.py document.txt"
#2012 Stephen Brannon, Verizon RISK Team

import re
import sys

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename, askdirectory

try:
    import cybox
    from cybox import helper as cybox_helper
    from cybox.core import Observables, Observable
    from cybox.objects.uri_object import URI
    import cybox.utils
    
    if hasattr(cybox, "__version__") and cybox.__version__.startswith("2"):
        python_cybox_available = True
    else:
        raise ImportError("python-cybox must be v2.0.0 or greater")
    
except Exception as e:
    print "ERROR: Could not load python-cybox. Will not be able to export IOCs in CybOX 2.0 format.\nException:[%s]" % (str(e))
    python_cybox_available = False
    
try:
    from ioc_writer import ioc_api, ioc_common
    ioc_writer_available = True
except ImportError, e:
    print 'ERROR: Could not load ioc_writer.  Will not be able to export IOCs in OpenIOC 1.1 format.'
    ioc_writer_available = False

tags = ['md5', 'ipv4', 'url', 'domain', 'email']

reMD5 = r"([A-F]|[0-9]){32}"
reIPv4 = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|\[\.\])){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
reURL = r"[A-Z0-9\-\.\[\]]+(\.|\[\.\])(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)(/\S+)"
reDomain = r"[A-Z0-9\-\.\[\]]+(\.|\[\.\])(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)\b"
reEmail = r"\b[A-Za-z0-9._%+-]+(@|\[@\])[A-Za-z0-9.-]+(\.|\[\.\])(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)\b"

def dotToNum(ip): return int(''.join(["%02x"%int(i) for i in ip.split('.')]),16)

def tag_initial():
    lines = text.get(1.0, 'end').split('\n')

    #md5
    text.tag_configure('md5', background='#FE6AA8')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reMD5, line, re.IGNORECASE):
            text.tag_add('md5',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #ipv4
    text.tag_configure('ipv4', background='#6CB23E')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reIPv4, line, re.IGNORECASE):
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            result = result.replace('[','').replace(']','') #remove brackets
            #reject private, link-local, and loopback IPs
            if result.find('10.') != 0 and \
               result.find('192.168') != 0 and \
               result.find('127') != 0:
                if (dotToNum(result) < dotToNum('172.16.0.0') or \
                   dotToNum(result) > dotToNum('172.31.255.255')) and \
                   (dotToNum(result) < dotToNum('169.254.1.0') or \
                   dotToNum(result) > dotToNum('169.254.254.255')):
                    text.tag_add('ipv4',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #url
    text.tag_configure('url', background='#378A20')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reURL, line, re.IGNORECASE):
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            end = m.end()
            #drop trailing punctuation
            while (u'.,\u201d"\'\u2019').find(result[len(result)-1:len(result)]) != -1:
                result = result[:len(result)-1]
                end -= 1
            text.tag_add('url',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(end))
        linenumber += 1

    #domain
    text.tag_configure('domain', background='#5DC5D1')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reDomain, line, re.IGNORECASE):
            #reject if preceding character is @ or following character is /
            if not text.get(str(linenumber) + '.' + str(m.start()-1), str(linenumber) + '.' + str(m.start())) == '@':
                if not text.get(str(linenumber) + '.' + str(m.end()), str(linenumber) + '.' + str(m.end()+1)) == '/':
                    text.tag_add('domain',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #email
    text.tag_configure('email', background='#0224F2')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reEmail, line, re.IGNORECASE):
            #reject verizon emails
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            if result.find('@verizon.com') == -1 and \
               result.find('@verizonbusiness.com') == -1 and \
               result.find('@one.verizon.com') == -1 and \
               result.find('@jp.verizonbusiness.com') == -1:
                text.tag_add('email',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

def askopen(filename = ''):
    if filename == '':
        filename = askopenfilename(title="Select plain-text file", filetypes=[("txt file",".txt"),("All files",".*")])
    if filename != '':
        with open(filename, 'rb') as f: #read as binary
            doc = f.read()
            doc = doc.decode('utf_8', 'ignore') #drop any non-ascii bytes
            
            #if a carriage return is orphaned, replace it with a new line
            doc = list(doc)
            i = 0
            while (i < len(doc) - 1):
                if ord(doc[i]) == 13: #it's a carriage return
                    if ord(doc[i + 1]) != 10: #it's not followed by a new line
                        doc[i] = chr(10) #replace it with a new line
                i += 1
            if ord(doc[len(doc)-1]) == 13: #end
                doc[len(doc)-1] = chr(10)
            
            #drop carriage returns
            i = 0
            while (i < len(doc) - 1):
                if ord(doc[i]) == 13: #it's a carriage return
                    doc.pop(i)
                else:
                    i += 1
                    
            doc = ''.join(doc)

            text.delete('1.0',END)
            text.insert('1.0', doc)
            tag_initial()
            root.title(filename + ' - IOCextractor')

def clear_tag(holder = 0):
    if len(text.tag_ranges("sel")) != 0: #selection is not empty
        #untag all occurrences of selected string
        key = text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])        
        lines = text.get(1.0, 'end').split('\n')
        linenumber = 1

        for line in lines:
            for m in re.finditer(re.escape(key), line, re.IGNORECASE):
                for t in tags:
                    text.tag_remove(t, str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            linenumber += 1

        for t in tags: #necessary backup in case the regex fails to match
            text.tag_remove(t, text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])
        
def tag_new(tag):
    if len(text.tag_ranges("sel")) != 0: #selection is not empty
        #remove any newline characters from the selection
        if '\n' in text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1]):
            line_start = (str(text.tag_ranges("sel")[0]).split('.'))[1]
            newline_index = text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1]).index('\n')
            del_line = str(text.tag_ranges("sel")[0]).split('.')[0]
            del_position = str(int(line_start) + int(newline_index))
            text.delete(del_line + '.' + del_position)

        #tag all occurences of selected string
        key = text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])
        lines = text.get(1.0, 'end').split('\n')
        linenumber = 1
        for line in lines:
            for m in re.finditer(re.escape(key), line, re.IGNORECASE):
                for t in tags:
                    text.tag_add(tag, str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            linenumber += 1

def export_console():
    #need better way to iterate through highlights and remove brackets
    for t in tags:
        indicators = []
        print(t + ':')
        myhighlights = text.tag_ranges(t)
        mystart = 0
        for h in myhighlights:
            if mystart == 0:
                mystart = h
            else:
                mystop = h
                if t == 'md5': #make all hashes uppercase
                    if not text.get(mystart,mystop).upper() in indicators:
                        indicators.append(text.get(mystart,mystop).upper())
                else:
                    if not text.get(mystart,mystop).replace('[.]','.').replace('[@]','@') in indicators:
                        indicators.append(text.get(mystart,mystop).replace('[.]','.').replace('[@]','@'))
                mystart = 0
        for i in indicators:
            print(i)
        print()

def export_csv():
    filename = asksaveasfilename(title="Save As", filetypes=[("csv file",".csv"),("All files",".*")])
    if filename != '':
        output = 'IOC,Type\n'
        #need better way to iterate through highlights and remove brackets
        for t in tags:
            indicators = []
            myhighlights = text.tag_ranges(t)
            mystart = 0
            for h in myhighlights:
                if mystart == 0:
                    mystart = h
                else:
                    mystop = h
                    if t == 'md5': #make all hashes uppercase
                        if not text.get(mystart,mystop).upper() in indicators:
                            indicators.append(text.get(mystart,mystop).upper())
                    else:
                        if not text.get(mystart,mystop).replace('[.]','.').replace('[@]','@') in indicators:
                            indicators.append(text.get(mystart,mystop).replace('[.]','.').replace('[@]','@'))
                    mystart = 0
            for i in indicators:
                if i.find(',') == -1: #no commas, print normally
                    output += str(i) + ',' + t + '\n'
                else: #internal comma, surround in double quotes
                    output += '"' + str(i) + '",' + t + '\n'
        if len(filename) - filename.find('.csv') != 4:
            filename += '.csv' #add .csv extension if missing
        with open(filename, 'w') as f:
            f.write(output)


def export_cybox():
    """
    Export the tagged items in CybOX format.
    This prompts the user to determine which file they want the CybOX saved
    out too.
    """
    filename = asksaveasfilename(title="Save As", filetypes=[("xml file",".xml"),("All files",".*")])
    observables_doc = None
     
    if filename:
        observables = []
        for t in tags:
            indicators = []
            myhighlights = text.tag_ranges(t)
            mystart = 0
            for h in myhighlights:
                if mystart == 0:
                    mystart = h
                else:
                    mystop = h
                    value = text.get(mystart,mystop).replace('[.]','.').replace('[@]','@')
                    
                    if t == 'md5':
                        value = value.upper()
                        if value not in indicators:
                            observable = cybox_helper.create_file_hash_observable('', value)
                            observables.append(observable)
                            indicators.append(value)
                        
                    elif t == 'ipv4':
                        if not value in indicators:
                            observable = cybox_helper.create_ipv4_observable(value)
                            observables.append(observable)
                            indicators.append(value)

                    elif t == 'domain':
                        if not value in indicators:
                            # CybOX 2.0 contains a schema bug that prevents the use of this function.
                            # The workaround is to not declare a @type attribute for the URI object 
                            #observable = cybox_helper.create_domain_name_observable(value)
                            uri_obj = URI(value=value)
                            uri_obs = Observable(item=uri_obj)
                            observables.append(uri_obs)  
                            indicators.append(value)
                    
                    elif t == 'url':
                        if not value in indicators:
                            observable = cybox_helper.create_url_observable(value)
                            observables.append(observable)
                            indicators.append(value)

                    elif t == 'email':
                        if not value in indicators:
                            observable = cybox_helper.create_email_address_observable(value)
                            observables.append(observable)
                            indicators.append(value)

                    mystart = 0
                # end if
            # end for
        # end for
       
        if len(observables) > 0:
            NS = cybox.utils.Namespace("http://example.com/", "example")
            cybox.utils.set_id_namespace(NS)
            observables_doc = Observables(observables=observables)
 
            if not filename.endswith('.xml'):
                filename = "%s.xml" % filename #add .xml extension if missing
            # end if
            
            with open(filename, "wb") as f:
                cybox_xml = observables_doc.to_xml(namespace_dict={NS.name: NS.prefix})
                f.write(cybox_xml)
            
        # end if
            
def export_openioc():
    '''
    Export the tagged items in OpenIOC 1.1 format.
    This prompts the user to determine which directory they want the IOC saved
    out too.
    
    Email tags default to 'Email/From' address, implying that the email address
    found is the source address of an email.  This may not be accurate in all
    cases.
    '''
    def make_network_uri(uri, condition='contains', negate=False, preserve_case = False):
        document = 'Network'
        search = 'Network/URI'
        content_type = 'string'
        content = uri
        IndicatorItem_node = ioc_api.make_IndicatorItem_node(condition, document, search, content_type, content, negate=negate, preserve_case=preserve_case, context_type = None)
        return IndicatorItem_node
    
    def make_email_from(from_address, condition='contains', negate=False, preserve_case = False):
        document = 'Email'
        search = 'Email/From'
        content_type = 'string'
        content = from_address
        IndicatorItem_node = ioc_api.make_IndicatorItem_node(condition, document, search, content_type, content, negate=negate, preserve_case=preserve_case, context_type = None)
        return IndicatorItem_node

    output_directory = askdirectory(title = "Save IOC To")
        
    if output_directory:
        indicator_nodes = []
        for tag in tags:
            temp_indicators = []
            myhighlights = text.tag_ranges(tag)
            mystart = 0
            for h in myhighlights:
                if mystart == 0:
                    mystart = h
                else:
                    mystop = h
                    # Deobfuscate ip addresses, domain names and email addresses
                    value = text.get(mystart,mystop).replace('[.]','.').replace('[@]','@')
                    if tag == 'md5':
                        value = value.upper()
                        if value not in temp_indicators:
                            indicator_node = ioc_common.make_fileitem_md5sum(value)
                            indicator_nodes.append(indicator_node)
                            temp_indicators.append(value)
                    elif tag == 'ipv4':
                        if value not in temp_indicators:
                            indicator_node = ioc_common.make_portitem_remoteip(value)
                            indicator_nodes.append(indicator_node)
                            temp_indicators.append(value)
                    elif tag == 'domain':
                        if value not in temp_indicators:
                            indicator_node = ioc_common.make_dnsentryitem_recordname(value)
                            indicator_nodes.append(indicator_node)
                            temp_indicators.append(value)
                    elif tag == 'url':
                        if value not in temp_indicators:
                            indicator_node = make_network_uri(value)
                            indicator_nodes.append(indicator_node)
                            temp_indicators.append(value)
                    elif tag == 'email':
                        if value not in temp_indicators:
                            indicator_node = make_email_from(value)
                            indicator_nodes.append(indicator_node)
                            temp_indicators.append(value)
                    else:
                        print 'Unknown tag encountered [%s]' % str(tag)
                    mystart = 0
    
    if len(indicator_nodes) > 0:
        ioc_obj = ioc_api.IOC(name = "IOC Extractor", description = "IOC generated with IOCExtractor")
        for indicator in indicator_nodes:
            ioc_obj.top_level_indicator.append(indicator)
        ioc_obj.write_ioc_to_file(output_directory)
    return True
        
root = Tk()
root.title('IOCextractor')

topframe = Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

openb = Button(topframe, text = "Open File", command = askopen)
openb.pack(side=LEFT)

clear = Button(topframe, text = "Clear", command = clear_tag)
clear.pack({"side": "left"})

md5 = Button(topframe, text = "MD5", command = lambda: tag_new('md5'), bg = "#FE6AA8")
md5.pack({"side": "left"})

ipv4 = Button(topframe, text = "IPV4", command = lambda: tag_new('ipv4'), bg = "#6CB23E")
ipv4.pack({"side": "left"})

url = Button(topframe, text = "URL", command = lambda: tag_new('url'), bg = "#378A20")
url.pack({"side": "left"})

domain = Button(topframe, text = "Domain", command = lambda: tag_new('domain'), bg = "#5DC5D1")
domain.pack({"side": "left"})

email = Button(topframe, text = "Email", command = lambda: tag_new('email'), bg = "#0224F2")
email.pack({"side": "left"})

export_console = Button(topframe, text = "Export Console", command = export_console)
export_console.pack({"side": "left"})

export_csv = Button(topframe, text = "Export CSV", command = export_csv)
export_csv.pack({"side": "left"})

if python_cybox_available:
    export_cybox = Button(topframe, text = "Export CybOX", command = export_cybox)
    export_cybox.pack({"side": "left"})

if ioc_writer_available:
    export_openioc = Button(topframe, text = "Export OpenIOC 1.1", command = export_openioc)
    export_openioc.pack({"side" : "left"})

#build main text area
text = Text(bottomframe, width=120, height=50)
text.pack({"side": "left"})
scrollbar = Scrollbar(bottomframe)
scrollbar.pack({"side": "left", "fill" : "y"})
scrollbar.config(command = text.yview)
text.config(yscrollcommand = scrollbar.set)

text.bind('<Button-3>', clear_tag) #right-click selection to untag (Windows, Linux)
text.bind('<Command-Button-1>', clear_tag) #command-click selection to untag (Mac)

#insert doc if received as commandline argument
if len(sys.argv) == 2:
    askopen(sys.argv[1])

root.mainloop()
