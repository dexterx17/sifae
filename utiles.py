#!flask/bin/python

import webbrowser

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Utiles(object):
	def __init__(self,browser):
		self.browser=browser
	def leer_input_by_id(self,id_elemento=''):
	    #lectura de span
	    try:
	        elem = self.browser.find_element_by_id(id_elemento)
	        elemento = elem.get_attribute('value')
	        print "elemento: "+elemento
	        return elemento
	    except:
	        print "error encontrando input "+id_elemento
	        return ' '

	def leer_span_by_id(self,id_elemento=''):
	    #lectura de span
	    try:
	        elem = self.browser.find_element_by_id(id_elemento)
	        elemento = elem.text
	        print "elemento: "+elemento
	        return elemento
	    except:
	        print "error encontrando span "+id_elemento
	        return ' '
	def leer_select_id_by_xpath(self,xpath):
	  #lectura de combobox provincia
	    try:
	        selectProvincias = Select(self.browser.find_element_by_xpath(xpath))
	        all_selected_options = selectProvincias.all_selected_options
	        for selected_option in all_selected_options:
	            value =selected_option.get_attribute("value")
	            print"selected ID : %s" % (value)
	            return value            
	    except:
	        print "error en lectura de select "+xpath
	        return ' '

	def leer_select_value_by_xpath(self,xpath):
	  #lectura de combobox provincia
	    try:
	        selectProvincias = Select(self.browser.find_element_by_xpath(xpath))
	        all_selected_options = selectProvincias.all_selected_options
	        for selected_option in all_selected_options:
	            text =selected_option.get_attribute("text")
	            print"selected text : %s" % (text)
	            return text            
	    except:
	        print "error en lectura de select "+xpath
	        return " "