#!flask/bin/python
#pip install flask
#python versiones.py
#RESULTADO: http://127.0.0.1:5000/
from flask import Flask, jsonify
from flask import render_template
from flask import abort
from flask import make_response
from flask import request

import time
from random import randint

import webbrowser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import json
import sys

import pip
from utiles import Utiles

if sys.version_info.major >= 3:
    from io import StringIO
else:
    from StringIO import StringIO


def get_version(package):
    f = StringIO()
    sys.stdout = f
    pip.main(["show", package])
    sys.stdout = sys.__stdout__
    return next((line.split(":", 1)[1].strip()
    	for line in f.getvalue().splitlines() if line.startswith("Version")), "No match")

import pkg_resources
print "BeautifulSoup: "+pkg_resources.get_distribution("BeautifulSoup").version
print "selenium: "+pkg_resources.get_distribution("selenium").version
print "webbrowser: "
print get_version('webbrowser')

utl = Utiles('test')

utl.test('joder')