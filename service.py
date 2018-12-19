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
from difflib import unified_diff
from datetime import datetime

def smtpModule(site, updated_status, update_date, former_status, update_type):
    txt = """
Foi detectada uma alteração no domínio '{0}'

Domínio: {0}
Status Atual: {1}
Status Anterior: {2}
Data da alteração: {3}
Tipo da Alteração: {4}

As alterações de código fonte podem ser obtidas em:
    changelog/{0}.diff
""".format(
        site[7:], 
        updated_status,
        former_status,
        update_date,
        update_type)
    print(txt)

print("Starting...")
print("Date: ", datetime.now().date())

sites = ConnectMysql().lookup("list", "service_mode")

for site_info in sites:
    status = site_info[0]
    site = site_info[1]
    source = site_info[2]
    
    html = GetSource(site)

    print("[{0}] | {1}".format(html[0], site))

    if html[0] != status:
        print("\tStatus atualizado")
        print("\tDe {0} para {1}".format(status, html[0]))

        ConnectMysql().update(site, "status", html[0])
        smtpModule(
                site,
                status,
                datetime.now().date(),
                html[0],
                "Status")

    else:
        print("\tSem alterações de status")

    if html[0] != "offline":
        change = False
        for new in html[1]:
            if new not in source:
                change = True
                
        if change == True:
            print("\tA página foi modificada")

            ConnectMysql().update(site, "date", datetime.now().date())
            ConnectMysql().update(site, "source", html[1])
            smtpModule(
                site,
                status,
                datetime.now().date(),
                html[0], 
                "Código Fonte")

            with open("changelog/%s.diff" %site[7:], "w") as log:
                for line in unified_diff(source.splitlines(), html[1].splitlines()):
                    log.write(line)
            
        else:
            print("\tA página não sofreu modificações")
    print("\n")
