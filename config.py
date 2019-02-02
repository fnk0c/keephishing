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

#################################
#   Database Configuration      #
#################################

DATABASE = "keephishing"
MYSQL_USER = "keephishing"
MYSQL_PASSWD = "passwd"
TABLE = "watchlist"

#################################
#   Mail Server Configuration   #
#################################

MAIL_SERVER = "smtp.office365.com"
MAIL_PORT = 587

MAIL_USER = "fnkoc@domail.com.br"
MAIL_PASSWD = "myPasswd"
MAILING_LIST = ["myfriend@domain.com.br"]

#################################
#   Mail Message Configuration  #
#################################

MAIL_SUBJECT = "Keephishing Alert"
