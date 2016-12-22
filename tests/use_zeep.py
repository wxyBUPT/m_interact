#coding=utf-8

import zeep
from zeep import xsd

wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
client = zeep.Client(wsdl=wsdl)
print client.service.Method1('Zeep', 'is cool')
