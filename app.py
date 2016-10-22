#!flask/bin/python
#PAQUETES NECESARIOS            TESTEADO EN VERSIONES
#python                         2.7.6 
#pip install flask              0.11.1
#pip install selenium           2.53.5
#pip install BeautifulSoup      3.2.1
#python app.py
#RESULTADO: http://127.0.0.1:5000/
from flask import Flask, jsonify
from flask import render_template
from flask import abort
from flask import make_response
from flask import request

import time
from random import randint
from utiles import Utiles

import webbrowser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import json
import sys
import pkg_resources

print "Python: "
print sys.version_info
print "BeautifulSoup: "+pkg_resources.get_distribution("BeautifulSoup").version
print "selenium: "+pkg_resources.get_distribution("selenium").version
print "flask: "+pkg_resources.get_distribution("flask").version

#seteando utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

#instancia Webservice
app = Flask(__name__)

#binary = FirefoxBinary('F:\FirefoxPortable\Firefox.exe')
binary = FirefoxBinary('./firefox/firefox')
#binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
#inicia el navegador, abre la pagina de agrocalidad y logea a un usuario
print "iniciando browser"
browser = webdriver.Firefox(firefox_binary=binary)
#inicializo funciones utiles
utl = Utiles(browser)
#abri pagina de inicio
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

#llamar desde http://127.0.0.1:5000/api/v1.0/abrir_form_gm
@app.route('/api/v1.0/abrir_form_gm')
def abrir_form_gm():
    '''
        Abre la pagina <a href="http://sistemas.agrocalidad.gob.ec/sifae/paginasComiteL/Guia_MovilizacionNC.aspx">http://sistemas.agrocalidad.gob.ec/sifae/paginasComiteL/Guia_MovilizacionNC.aspx</a>
        y selecciona el Lugar de emision: CEMEAG
    '''
    resultado={}
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
    #lectura de input ci
    resultado['ci']=utl.leer_input_by_id('ctl00_Main_txtNC')
    #lectura de span propietario
    resultado['propietario']=utl.leer_span_by_id('ctl00_Main_lblP')
    #lectura de span # cuv
    resultado['cuv']=utl.leer_span_by_id('ctl00_Main_lblCuv')
    #lectura de span fecha cuv
    resultado['fechacuv']=utl.leer_span_by_id('ctl00_Main_lblFC')
    #lectura de span # animales
    resultado['animales']=utl.leer_span_by_id('ctl00_Main_lblTA')
    #lectura de span operadora
    resultado['operadora']=utl.leer_span_by_id('ctl00_Main_lblNC')

    #resultado['stock']={}
    table = browser.find_element_by_id('ctl00_Main_GV_AniM')
    for fila in table.find_elements_by_tag_name('tr')[1:]:
        tipo=""
        stock=0
        for columna in fila.find_elements_by_tag_name('td')[1:2]:
            print columna.text
            tipo=columna.text
        for columna in fila.find_elements_by_tag_name('input')[1:]:
            print columna.get_attribute("value")
            stock = columna.get_attribute("value")
        resultado[tipo]=stock
        #resultado['stock'][tipo]=stock

    return jsonify(resultado)

#llamar desde http://127.0.0.1:5000/api/v1.0/setear_ci/0101707685/0
@app.route('/api/v1.0/setear_ci/<ci>/<tipo_user>')
def setear_ci(ci,tipo_user):
    destino=1
    try:
        #tipo_user = 0 # 0=PROPIETARIO; 1=COMERCIANTE;
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
    elem.clear()
    elem.send_keys(ci)

    time.sleep(1)
    setear_destino(1,ci)

    try:
        resultado={}
        resultado['A']=1
        #lectura de combobox Especifique
        usuario = utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
        resultado['usuario']=usuario.split('>')[1]
        elem = browser.find_element_by_id('ctl00_Main_txtDS')
        elem.send_keys(usuario.split('>')[1])
        resultado['IDusuario']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$ddl_Esp']") 
        #lectura de combobox provincia
        resultado['provincia']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLPv2']")
        resultado['IDprovincia']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLPv2']")
        #lectura de combobox canton    
        resultado['canton']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLCa2']")
        resultado['IDcanton']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLCa2']")
        #lectura de combobox parroquia    
        resultado['parroquia']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLPq2']")
        resultado['IDparroquia']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLPq2']")
        #lectura de input location
        resultado['location']=utl.leer_input_by_id('ctl00_Main_txtLSKH')
        #lectura de span # CUV
        resultado['cuv']=utl.leer_span_by_id('ctl00_Main_lblCuv1')

        return jsonify(resultado)
    except:
        return jsonify({'A':0})

#llamar desde http://127.0.0.1:5000/api/v1.0/setear_nombre/james bond
@app.route('/api/v1.0/setear_nombre/<nombre>')
def setear_nombre(nombre):
    elem = browser.find_element_by_id('ctl00_Main_txtDS')
    elem.send_keys(nombre)
    return jsonify({'nombre': nombre})

#llamar desde http://127.0.0.1:5000/api/v1.0/setear_movilizacion/1/TAS-1234/por alla/Jaime Santana/1600392359/555
#0=CAMION; 1=CAMIONETA; 2=TRAILER; 3=CAMINANDO; 4=ALQUITER
@app.route('/api/v1.0/setear_movilizacion/<tipo>/<placa>/<ruta>/<conductor>/<ci>/<tlf>')
def setear_movilizacion(tipo,placa,ruta,conductor,ci,tlf):
    #seteo tipo
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddlTipoT']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            value = option.get_attribute("value")
            #print("Value is: %s" % value)
            if int(value)==int(tipo):
                option.click()
                break
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoT"]') )
        abort(404)
    time.sleep(2)
    el_placa = browser.find_element_by_id('ctl00_Main_txtPla')
    el_placa.send_keys(placa)

    el_ruta = browser.find_element_by_id('ctl00_Main_txtRS')
    el_ruta.send_keys(ruta)

    el_conductor = browser.find_element_by_id('ctl00_Main_txtDPA')
    el_conductor.send_keys(conductor)

    el_ci = browser.find_element_by_id('ctl00_Main_txtNL')
    el_ci.send_keys(ci)

    el_tlf = browser.find_element_by_id('ctl00_Main_txtTM')
    el_tlf.send_keys(tlf)

    return jsonify({
        'tipo': tipo,
        'placa':placa,
        'ruta':ruta,
        'conductor':conductor,
        'ci':ci,
        'tlf':tlf
        })

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
        browser.find_element_by_id('ctl00_Main_txtNC1').clear()
        elem = browser.find_element_by_id('ctl00_Main_txtNC1')
        elem.send_keys(ci)
        elem.send_keys(Keys.TAB);
        #elem.sendKeys(Keys.ENTER);
    time.sleep(2)
    #verifico nuevamente en el chexbox si hay info de la cedula seteada
    element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
    all_options = element.find_elements_by_tag_name("option")
    print len(all_options)
    res = "NO"
    if len(all_options) >= 2:
        res = "SI"
        index=1
        for option in all_options:
            value = option.get_attribute("value")
            print index
            print("Value is: %s" % value)
            if index==len(all_options):
                option.click()
                break
            index+=1

    return jsonify({'destino': destino,'registrado':res})

def get_destinos_de(contenedor=[],tipo=3,ultima_opcion=0):
    print "last"+str(ultima_opcion)
    #indice de opcion seleccionada
    index=1
    #seteo destino
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_D']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            value = option.get_attribute("value")
            #print("Value is: %s" % value)
            if int(value)==int(tipo):
                option.click()
                break

    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
        abort(404)
    time.sleep(randint(5, 6))
    #verifico los camales del combobox
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
        all_options = element.find_elements_by_tag_name("option")
        print "destinos:" + str(len(all_options))
        index+=ultima_opcion
        for option in all_options[ultima_opcion:]:
            destino={}
            elt = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
            al_options = elt.find_elements_by_tag_name("option")
            try:
                value = al_options[index].get_attribute("value")
                text = al_options[index].get_attribute("text")
                print"destino %s : %s,%s" % (str(index),value,text)
                destino['IDdestino']=value
                destino['destino']=text
                al_options[index].click()
            except:
                print"error en destino %s " % (str(index))
                continue

            index+=1
            try:
                #lectura de combobox provincia
                destino['provincia']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLPv2']")
                destino['IDprovincia']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLPv2']")
                if destino['provincia']==" ":
                    print('Provincia vacia %s',(str(index)))
                    browser.get('http://sistemas.agrocalidad.gob.ec/sifae/paginasComiteL/Guia_MovilizacionNC.aspx')
                    index_real=index-1
                    with open('faltantes.log','a+') as f:
                        f.write('DESTINO:'+str(index_real)+'\n')
                    with open('error.log','a+') as f:
                        f.write(json.dumps({'tipo':tipo,'last':index_real}))
                        return get_destinos_de(contenedor,tipo,index_real)
                #lectura de combobox canton    
                destino['canton']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLCa2']")
                destino['IDcanton']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLCa2']")
                #lectura de combobox parroquia    
                destino['parroquia']=utl.leer_select_value_by_xpath("//select[@name='ctl00$Main$DDLPq2']")
                destino['IDparroquia']=utl.leer_select_id_by_xpath("//select[@name='ctl00$Main$DDLPq2']")
                #lectura de input location
                destino['location']=utl.leer_input_by_id('ctl00_Main_txtLSKH')
                #lectura de span # CUV
                destino['cuv']=utl.leer_span_by_id('ctl00_Main_lblCuv1')

                contenedor.append(destino)
                with open('destinos.txt','a+') as f:
                    f.write('tipo:'+str(tipo))
                    print 'writed tipo: %s => destinos.txt' % str(tipo) 
                    f.write(';destino:'+destino['destino'])
                    print('writed destino: %s|||| destinos.txt' % destino['destino'])
                    f.write(';destino:'+destino['destino'])
                    print('writed destino: %s|||| destinos.txt' % str(destino['destino']))
                    f.write(';provincia:'+destino['provincia'])
                    print('writed provincia: %s|||| destinos.txt' % str(destino['provincia']))
                    f.write(';canton:'+destino['canton'])
                    print('writed canton: %s|||| destinos.txt' % str(destino['canton']))
                    f.write(';parroquia:'+destino['parroquia'])
                    print('writed parroquia: %s|||| destinos.txt' %str(destino['parroquia']))
                    f.write(';location:'+destino['location'])
                    print('writed location: %s|||| destinos.txt' %destino['location'])
                    f.write(';cuv:'+destino['cuv']+'\n')
                    print('writed cuv: %s|||| destinos.txt' % destino['cuv'])
                    print "=============================================================================="
                
                with open('provincias.txt','a+') as f:
                    if (destino['IDprovincia']+':'+destino['provincia']+'\n') not in f: 
                        f.write(destino['IDprovincia']+':'+destino['provincia']+'\n')

                with open('cantones.txt','a+') as f:
                    if (destino['IDcanton']+':'+destino['canton']+'\n') not in f: 
                        f.write(destino['IDcanton']+':'+destino['canton']+'\n')

                with open('parroquias.txt','a+') as f:
                    if (destino['IDparroquia']+':'+destino['parroquia']+'\n') not in f: 
                        f.write(destino['IDparroquia']+':'+destino['parroquia']+'\n')
            except:
                print('Error al leer datos de destino ')
                with open('error.log','w+') as f:
                    f.write(json.dumps({'tipo':tipo,'last':index}))
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
        with open('error.log','w+') as f:
            f.write(json.dumps({'tipo':tipo,'last':index}))


@app.route('/api/v1.0/get_destinos')
def get_destinos():
    #3=camal;2=feria com/exp;1=finca; 5=centro de hospedaje; 6=centro de pesaje
    opciones_destino=[3,2,5,6]
    array_destinos={}
    with open('faltantes.log','w+') as f:
        f.write("");
    with open('destinos.txt','w+') as f:
        f.write("");
    with open('provincias.txt','w+') as f:
        f.write("");
    with open('cantones.txt','w+') as f:
        f.write("");
    with open('parroquias.txt','w+') as f:
        f.write("");
    for opcion in opciones_destino[:]:
        print opcion
        array_destinos[opcion]=[]
        get_destinos_de(array_destinos[opcion],opcion,0)
            
        time.sleep(randint(4, 5))
     
    #with open('C:\\Users\\eros\\Desktop\\rest\\camales.json','w+') as f:
    with open('destinos.json','w+') as f:
        f.write(json.dumps(array_destinos))

    return jsonify(array_destinos)

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


if __name__ == '__main__':
    app.run(debug=False)
