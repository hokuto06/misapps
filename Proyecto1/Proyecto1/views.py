from django.http import HttpResponse
from django.template import Template,Context
import datetime

def saludo(request):
	return HttpResponse("Hola Django - Coder")

def segunda_vista(request):
	return HttpResponse("<br><br>Ya entendimos esto, es muy simple :)")

def diaDeHoy(request):
    dia = datetime.datetime.now()
    documentoDeTexto = f"Hoy es dia: <br> {dia}"
    return HttpResponse(documentoDeTexto)

def miNombreEs(self, nombre):
	documentoDeTexto = f"Mi nombre es: <br><br> {nombre}"
	return HttpResponse(documentoDeTexto)

def probandoTemplate(self):
    nom = "Nicolas"
    ap = "Perez"
    diccionario = {"nombre":nom, "apellido":ap}
    miHtml = open("C:/Users/Hokuto/Desktop/curso/tests/Proyecto1/Proyecto1/templates/template1.html")
    plantilla = Template(miHtml.read())
    miHtml.close()
    miContexto = Context(diccionario)
    documento = plantilla.render(miContexto)
    return HttpResponse(documento)