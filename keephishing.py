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

from urllib.request import urlopen, Request
from urllib.error import URLError
from datetime import datetime
from mysql import connector
from config import MYSQL_USER, MYSQL_PASSWD, DATABASE, TABLE

def GetSource(url):
    try:
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
#        html = urlopen(Request(url, headers=header)).read().decode("utf-8")
        html = urlopen(url).read().decode("utf-8")
        return("online", html)
    except Exception:
        return("offline", "NULL")

class ConnectMysql():
    def __init__(self):
        self.cnx = connector.connect(
                user=MYSQL_USER,
                password=MYSQL_PASSWD,
                database=DATABASE)
        self.cursor = self.cnx.cursor()

    def insert(self, client, status, url, today_date, source):
        addSite = ("INSERT INTO {} "
                "(client, status, website, created, source) "
                "VALUES (%s, %s, %s, %s, %s)".format(TABLE))

        data = (client, status, url, today_date, source)
        self.cursor.execute(addSite, data)
        self.close()

    def lookup(self, search_type, search_term):
        if search_type == "client":
            searchQuery = (
                    "SELECT client, status, website, created FROM {} "
                    "WHERE client = %s").format(TABLE)
        
        elif search_type == "date":
            searchQuery = (
                    "SELECT client, status, website, created FROM {} "
                    "WHERE created = %s").format(TABLE)
        
        elif search_type == "site":
            searchQuery = (
                    "SELECT client, status, website, created FROM {} "
                    "WHERE website = %s").format(TABLE)

        elif search_type == "list":
            if search_term == "service_mode":
                searchQuery = (
                    "SELECT status, website, source FROM {}").format(TABLE)
            else:
                searchQuery = (
                    "SELECT client, status, website FROM {}").format(TABLE)

        if search_term != None and search_term != "service_mode":
            self.cursor.execute(searchQuery, (search_term, ))
        else:
            self.cursor.execute(searchQuery)
        
        queryResult = []
        for info in self.cursor:
            queryResult.append(info)
        return(queryResult)

        self.close()

    def remove(self, url):
        removeSite = (
            "DELETE FROM {0} WHERE website = '{1}'".format(TABLE, url))
        self.cursor.execute(removeSite)
        self.close()

    def update(self, site, update_type, update_data):
        if update_type == "date":
            updateQuery = (
                "UPDATE {0} SET updated = %s "
                "WHERE website = '{1}'").format(TABLE, site)
        
        elif update_type == "source":
            updateQuery = (
                "UPDATE {0} SET source = %s "
                "WHERE website = '{1}'").format(TABLE, site)

        elif update_type == "status":
            updateQuery = (
                "UPDATE {0} SET status = %s "
                "WHERE website = '{1}'").format(TABLE, site)
        self.cursor.execute(updateQuery, (update_data, ))
        self.close()
        
    def close(self):    
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

def InsertSite():  
    client = input("Client:\n >> ")
    url = input("Inform website to be added in watchlist:\n >> ")

    if "http" not in url:
        url = "http://" + url

    today_date = datetime.now().date()
    website_rsp = GetSource(url)
    status = website_rsp[0]
    source = website_rsp[1]
 
    print("Summary:")
    print("Client: ", client)
    print("Website: ", url)
    print("Status: ", status)
    
    if source != None: 
        print("Source: ", source[:100])


    confirm = input("Confirm? [y/N]\n >> ").lower()

    if confirm == "y":
        ConnectMysql().insert(client, status, url, today_date, source)
    else:
        print(" [-] Aborted")
        Main()

def DeleteSite():
    url = input("Inform website to be removed:\n >> ")
    ConnectMysql().remove(url)

def ConsultarSites():
    print("""Search in database
 [1] By client
 [2] By date
 [3] By website
 [4] List all

 [0] Go back
    """)
    option = int(input(" >> "))

    if option == 1:
        client = input("Client:\n >> ")
        response = ConnectMysql().lookup("client", client)
    elif option == 2:
        date = input("Date [yyyy-mm-dd]:\n >> ")
        response = ConnectMysql().lookup("date", date)
    elif option == 3:
        url = input("URL:\n >> ")
        response = ConnectMysql().lookup("site", url)
    elif option == 4:
        response = ConnectMysql().lookup("list", None)
    elif option == 0:
        Main()
    else:
        print(" [!] Option not recognized")
        ConsultarSites()

    for item in response:
        print(item)

def MainMenu():
    print("""
 [1] - Insert website
 [2] - Retrieve websites
 [3] - Remove website

 [0] - Exit
 """)
    return(input(" >> "))

def Main():
    option = MainMenu()
    functions = {
    "0": "exit()",
    "1": "InsertSite()",
    "2": "ConsultarSites()",
    "3": "DeleteSite()"
    }
    try:
        exec(functions[option])
    except KeyError:
        print(" [!] Option not recognized")
        Main()

if __name__ == "__main__":
    Main()
