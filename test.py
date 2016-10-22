 #!/usr/bin/env python
#coding: utf8 
opciones_destino=[3,2,1,5,6]
for opcion in opciones_destino:
	print opcion

destino={}
destino['IDprovincia'] = "0201"
destino['provincia']="GUAR"

with open('provincias.txt','a+') as f:
	if (destino['IDprovincia']+':'+destino['provincia']+'\n') not in f: 
		f.write(destino['IDprovincia']+':'+destino['provincia']+'\n')