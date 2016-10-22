#!flask/bin/python
#pip install flask
#python app.py
#RESULTADO: http://127.0.0.1:5000/
from flask import Flask, jsonify
from flask import render_template
from flask import abort
from flask import make_response
from flask import request

import time
from random import randint

import webbrowser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

#instancia Webservice
app = Flask(__name__)

#binary = FirefoxBinary('F:\FirefoxPortable\Firefox.exe')
binary = FirefoxBinary('/opt/firefox46/firefox')

#inicia el navegador, abre la pagina de agrocalidad y logea a un usuario
print "iniciando browser"
browser = webdriver.Firefox(firefox_binary=binary)
browser.get('http://sistemas.agrocalidad.gob.ec/sifae') #10 minutos

#login en agro
try:
    elem = browser.find_element_by_id('ctl00_LoginArea_Login1_UserName')
    elem.send_keys('suboperadorinnova')
    elem = browser.find_element_by_id('ctl00_LoginArea_Login1_Password')
    elem.send_keys('_suboperadorinnova01')
    elem = browser.find_element_by_id('ctl00_LoginArea_Login1_LoginImageButton')
    elem.click()
except:
    print('Error en Login')

time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

#llamar desde http://127.0.0.1:5000/api/v1.0/setear_ci/0101707685
@app.route('/api/v1.0/setear_ci/<ci>')
def setear_ci(ci):
    browser.get('http://sistemas.agrocalidad.gob.ec/sifae/paginasComiteL/Guia_MovilizacionNC.aspx')
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_FCL']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            print("Value is: %s" % option.get_attribute("value"))
            option.click()
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddl_FCL"]') )
        abort(404)

    try:
        tipo_user = 0 # 0=PROPIETARIO; 1=COMERCIANTE;
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddlTipoM']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            value = option.get_attribute("value")
            #print("Value is: %s" % value)
            if int(value)==int(tipo_user):
                option.click()
                break
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
        abort(404)

    elem = browser.find_element_by_id('ctl00_Main_txtCS')
    elem.send_keys(ci)

    return jsonify({'ci': ci})
    
#llamar desde http://127.0.0.1:5000/api/v1.0/setear_nombre/james bond
@app.route('/api/v1.0/setear_nombre/<nombre>')
def setear_nombre(nombre):
    elem = browser.find_element_by_id('ctl00_Main_txtDS')
    elem.send_keys(nombre)
    return jsonify({'nombre': nombre})

#llamar desde http://127.0.0.1:5000/api/v1.0/setear_destino/1/0101707685
#3=CAMAL; 2=FERIA COM/EXP;1=FINCA CON CUV;4=FINCA SIN CUB;5=CENTRO DE HOSPEDAJE;6=CENTRO DE PESAJE
@app.route('/api/v1.0/setear_destino/<destino>/<ci>')
def setear_destino(destino,ci):
    #seteo destino
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_D']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            value = option.get_attribute("value")
            #print("Value is: %s" % value)
            if int(value)==int(destino):
                option.click()
                break
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
        abort(404)
    time.sleep(2)
    #si el destino es Finca con CUV, tengo que verificar que la cedula este registrada
    if int(destino) == 1:
        print "Reset ci"
        elem = browser.find_element_by_id('ctl00_Main_txtNC1')
        elem.send_keys(ci)
        elem.send_keys(Keys.TAB);
        #elem.sendKeys(Keys.ENTER);
    time.sleep(2)

    #verifico nuevamiente en el chexbox si hay info de la cedula seteada
    element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
    all_options = element.find_elements_by_tag_name("option")
    print "opciones:" + str(len(all_options))
    res = "NO"
    if len(all_options) >= 2:
        res = "SI"
        index=1
        for option in all_options:
            value = option.get_attribute("value")
            print index
            #print("Value is: %s" % value)
            if index==len(all_options):
                option.click()
                break
            index+=1

    return jsonify({'destino': destino,'registrado':res})

@app.route('/api/v1.0/get_destinos')
def get_destinos():
    #3=camal;2=feria com/exp;1=finca; 5=centro de hospedaje; 6=centro de pesaje
    opciones_destino=[3,2,1,5,6]
    destinos=[]
    for opcion in opciones_destino[:1]:
        print opcion
        #seteo destino
        try:
            element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_D']")
            all_options = element.find_elements_by_tag_name("option")
            indice=0
            for option in all_options:
                instanciaElement = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_D']")
                options = instanciaElement.find_elements_by_tag_name("option")
                value = options[indice].get_attribute("value")
                #print("Value is: %s" % value)
                if int(value)==int(opcion):
                    options[indice].click()
                    break
                indice+=1

        except:
            print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
            abort(404)
        time.sleep(1)
        #verifico los camales del combobox
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
        all_options = element.find_elements_by_tag_name("option")
        print "destinos:" + str(len(all_options))
        index=0
        for option in all_options:
            elt = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
            al_options = elt.find_elements_by_tag_name("option")
            value = al_options[index].get_attribute("value")
            text = al_options[index].get_attribute("text")
            print "destino " +str(index)
            print"Value is: %s,%s" % (value,text)
            al_options[index].click()
            index+=1
            try:
                #verifico los camales del chexbox si hay info de la cedula seteada
                elementProvincias = browser.find_element_by_xpath("//select[@name='ctl00$Main$DDLPv2']")
                all_provincias = elementProvincias.find_elements_by_tag_name("option")
                print "provincias:" + str(len(all_provincias))
            except:
                print "error en opcion"+str(index)
            time.sleep(2)
     


    return jsonify({'destinos': destinos})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    print task
    return jsonify({'task': task}), 201

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    print task_id
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=False)