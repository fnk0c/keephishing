#!/usr/bin/python
#coding: utf-8

__AUTHOR__ = "Fnkoc"
__LICENSE__= "MIT"

"""
MIT License
Copyright (c) 2018 Franco Colombino
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from keephishing import ConnectMysql, GetSource
from config import * 

from html_similarity import style_similarity, structural_similarity, similarity
from difflib import unified_diff

from datetime import datetime
import smtplib


def smtpModule(site, updated_status, update_date, former_status, sim_result):

    if updated_status != former_status:
        update_type = "status"
    else:
        update_type = "Código Fonte"

    alert_mail = """
Keephishing alert,

It was detected an modification at domain '{0}'

Domain: {0}
Status Atual: {1}
Status Anterior: {2}
Modification Date: {3}
Type of Modification: {4}

For source code modifications:

{5}

The changes can be verified at:
    changelog/{0}.diff
""".format(
        site[7:], 
        updated_status,
        former_status,
        update_date,
        update_type,
        sim_result)

    msg = """\
Content-Type": text/html; charset=utf-8
Content-Disposition: inline
Content-Transfer-Enconding: 8bit
From: %s
To: %s
Subject: %s

%s
""" %(
        MAIL_USER, 
        ", ".join(MAILING_LIST), 
        MAIL_SUBJECT, 
        alert_mail)

    try:
        print("Sending E-mail")
        mailserver = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(MAIL_USER, MAIL_PASSWD)
        mailserver.sendmail(MAIL_USER, MAILING_LIST, msg.encode("utf-8"))
        mailserver.quit()
        print("E-mail Sent")

    except Exception as e:
        print(e)
        exit()

print("Starting...")
print("Date: ", datetime.now().date())

sites = ConnectMysql().lookup("list", "service_mode")

for site_info in sites:
    changed = False
    status = site_info[0]
    site = site_info[1]
    old_source = site_info[2]
    
    html = GetSource(site)

    if html[0] != status:
        print("> {} \t|\t status".format(site))
        changed = True
        source_change = False
        ConnectMysql().update(site, "status", html[0])
        sim_result = None
    
    if html[0] != "offline":
        new_source = html[1]

        if "type=\"text/css\"" in old_source:
            style = round(style_similarity(new_source, old_source), 4)
            similar = round(similarity(new_source, old_source), 4)
            structure = round(structural_similarity(new_source, old_source), 4)
            
            print("> {} \t|\t {} - {} - {}".format(site, style, similar, structure))

            if style < 0.70 or similar < 0.71 or structure < 0.77:
                changed = True
                source_change = True

            sim_result = "Style: {}\nStructure: {}\nTotal: {}".format(style, structure, similar)

        else:
            structure = round(structural_similarity(new_source, old_source), 4)
            
            print("> {} \t|\t {}".format(site, structure))
            if structure < 0.77:
                changed = True
                source_change = True

            sim_result = "Structure: {}".format(structure)

    if changed == True:
        ConnectMysql().update(site, "date", datetime.now().date())
        if source_change:
            ConnectMysql().update(site, "source", new_source)
        smtpModule(
            site,
            status,
            datetime.now().date(),
            html[0],
            sim_result)

        with open("changelog/%s.diff" %site[7:], "w") as log:
           for line in unified_diff(old_source.split("\n"), new_source.split("\n")):
               log.write(line + "\n")
