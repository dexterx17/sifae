'''
    #verifico por primera vez en el chexbox si hay info de la cedula seteada
    element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_Esp']")
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        value = option.get_attribute("value")
        print("Value is: %s" % value)
        #if int(value)==int(destino):
        #    option.click()
        #    break
        #
    #como no hay nada, cambio el destino a seleccionar para reiniciarlo
    try:
        element = browser.find_element_by_xpath("//select[@name='ctl00$Main$ddl_D']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            value = option.get_attribute("value")
            #print("Value is: %s" % value)
            if int(value)==-1:
                option.click()
                break
    except:
        print('Was not able to find <%s> ' % ('//select[@name="ctl00$Main$ddlTipoM"]') )
        abort(404)
    time.sleep(1)
    #vuelvo a setear en la opcion de destino
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
    #si el destino es Finca con CUV vuelvo a setear la cedula
    if int(destino) == 1:
        print "Reset ci"
        elem = browser.find_element_by_id('ctl00_Main_txtNC1')
        elem.send_keys(ci)
        elem.send_keys(Keys.TAB);
        #elem.sendKeys(Keys.ENTER);
    time.sleep(2)'''