#This script helps extract indicators of compromise (IOCs) from a text file.
#A user can add or remove tagged indicators then export the remaining tags.
#Usage: "python IOCextractor.py" or "python IOCextractor.py document.txt"
#2012 Stephen Brannon, Verizon RISK Team

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
import sys

tags = ['md5', 'ipv4', 'url', 'domain', 'email']
reIPv4 = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"

def tag_initial():
    lines = text.get(1.0, 'end').split('\n')

    #md5
    text.tag_configure('md5', background='#FE6AA8')
    linenumber = 1
    for line in lines:
        for m in re.finditer(r"([A-Z]|[0-9]){32}", line, re.IGNORECASE):
            text.tag_add('md5',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #ipv4
    text.tag_configure('ipv4', background='#6CB23E')
    linenumber = 1
    for line in lines:
        for m in re.finditer(reIPv4, line, re.IGNORECASE):
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            # if result.find('10.') != 0: #reject matches that begin with 10.
            if not (result.find('10.') == 0 or result.find('192.168.') == 0 or result.find('172.16.') == 0):
                text.tag_add('ipv4',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #url
    text.tag_configure('url', background='#378A20')
    linenumber = 1
    for line in lines:
        for m in re.finditer(r"[A-Z0-9\-\.]+\.(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)(/\S+)", line, re.IGNORECASE):
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            end = m.end()
            #drop trailing punctuation
            while ('.,”"\'’').find(result[len(result)-1:len(result)]) != -1:
                result = result[:len(result)-1]
                end -= 1
            text.tag_add('url',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(end))
        linenumber += 1

    #domain
    text.tag_configure('domain', background='#5DC5D1')
    linenumber = 1
    for line in lines:
        for m in re.finditer(r"[A-Z0-9\-\.]+\.(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)\b", line, re.IGNORECASE):
            #reject if preceding character is @ or following character is /
            if not text.get(str(linenumber) + '.' + str(m.start()-1), str(linenumber) + '.' + str(m.start())) == '@':
                if not text.get(str(linenumber) + '.' + str(m.end()), str(linenumber) + '.' + str(m.end()+1)) == '/':
                    text.tag_add('domain',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

    #email
    text.tag_configure('email', background='#0224F2')
    linenumber = 1
    for line in lines:
        for m in re.finditer(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|NAME|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW)\b", line, re.IGNORECASE):
            #reject @verizonbusiness.com
            result = text.get(str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            if result.find('@verizonbusiness.com') == -1:
                text.tag_add('email',str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
        linenumber += 1

def askopen():
    filename = askopenfilename(title="Select plain-text file", filetypes=[("txt file",".txt"),("All files",".*")])
    if filename != '':
        with open(filename) as f:
            text.delete('1.0',END)
            doc = f.read()
            text.insert('1.0', doc)
            tag_initial()

def clear_tag(holder = 0):
    if len(text.tag_ranges("sel")) != 0: #selection is not empty
        #untag all occurrences of selected string
        key = text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])
        lines = text.get(1.0, 'end').split('\n')
        linenumber = 1
        for line in lines:
            for m in re.finditer(key, line, re.IGNORECASE):
                for t in tags:
                    text.tag_remove(t, str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            linenumber += 1

        for t in tags: #necessary backup in case the regex fails to match
            text.tag_remove(t, text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])

def tag_new(tag):
    if len(text.tag_ranges("sel")) != 0: #selection is not empty
        #tag all occurences of selected string
        key = text.get(text.tag_ranges("sel")[0], text.tag_ranges("sel")[1])
        lines = text.get(1.0, 'end').split('\n')
        linenumber = 1
        for line in lines:
            for m in re.finditer(key, line, re.IGNORECASE):
                for t in tags:
                    text.tag_add(tag, str(linenumber) + '.' + str(m.start()), str(linenumber) + '.' + str(m.end()))
            linenumber += 1

def export_console():
    #need better way to iterate through highlights
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
                if not text.get(mystart,mystop) in indicators:
                    indicators.append(text.get(mystart,mystop))
                mystart = 0
        for i in indicators:
            print(i)
        print()

def export_csv():
    filename = asksaveasfilename(title="Save As", filetypes=[("csv file",".csv"),("All files",".*")])
    if filename != '':
        output = 'IOC,Type\n'
        #need better way to iterate through highlights
        for t in tags:
            indicators = []
            myhighlights = text.tag_ranges(t)
            mystart = 0
            for h in myhighlights:
                if mystart == 0:
                    mystart = h
                else:
                    mystop = h
                    if not text.get(mystart,mystop) in indicators:
                        indicators.append(text.get(mystart,mystop))
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

root = Tk()
root.title('IOCextract')

topframe = Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

openb = Button(topframe, text = "Open File", command = askopen)
openb.pack({"side": "left"})

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

#build main text area
text = Text(bottomframe, width=120, height=50)
text.pack({"side": "left"})
scrollbar = Scrollbar(bottomframe)
scrollbar.pack({"side": "left", "fill" : "y"})
scrollbar.config(command = text.yview)
text.config(yscrollcommand = scrollbar.set)

text.bind('<Button-3>', clear_tag) #right-click selection to untag

#insert doc if received as commandline argument
if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        doc = f.read()
    if len(doc) != 0:
        text.insert('1.0', doc)
    tag_initial()

root.mainloop()
