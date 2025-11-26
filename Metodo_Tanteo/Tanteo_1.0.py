'''En este código está contenido el algoritmo que permite hallar 
la temperatura de bulbo húmedo dadas las condiciones necesarias de la situación particular en la que se encuentren'''

########################## Aquí se encuentran indexados los datos de las tablas A-12 y A-12I para interpolar adecuadamente
tempertaura_CelsiusTablas = [0,4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 40, 45, 50]
presion_BarTablas = [0.00611, 0.00813, 0.00872, 0.00935, 0.01072, 0.01228, 0.01312, 0.01402, 0.01497, 0.01598, 0.01705, 0.01818, 0.01938, 0.02064, 0.02198, 0.02339, 0.02487, 0.02645, 0.02810, 0.02985, 0.03169, 0.03363, 0.03567, 0.03782, 0.04008, 0.04246, 0.04496, 0.04759, 0.05034, 0.05324, 0.05628, 0.05947, 0.06632, 0.07384, 0.09593, 0.1235]
tempertaura_FarenheitTablas = [32, 35, 40, 45, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
presion_PsiaTablas = [0.0886, 0.0999, 0.1217, 0.1475, 0.1780, 0.1917, 0.2064, 0.2219, 0.2386, 0.2563, 0.2751, 0.2952, 0.3165, 0.3391, 0.3632, 0.3887, 0.4158, 0.4440, 0.4750, 0.5073, 0.5414, 0.5776, 0.6158, 0.6562, 0.6988, 0.7439, 0.7914, 0.8416, 0.8945, 0.9503, 1.276, 1.695, 2.225, 2.892, 3.722, 4.745, 5.996, 7.515, 9.343, 11.529]
##########################

def interpolacion( dato_conocido, dato_superior, dato_inferior, complemento_superior, complemento_inferior ):
    #Complemento hacer referencia a los datos que no tienen las mismas unidades del dato que se conoce, por ejemplo:
    #Si se conoce la Temperatura y se desea hallar la presión, las temperaturas hacen referecia a dato_xxx , mientras que la presion hace referencia a los complementos.
    dato_Deseado = ((complemento_superior-complemento_inferior)/(dato_superior-dato_inferior)) * (dato_conocido-dato_inferior) + complemento_inferior
    return dato_Deseado
    
    
# Esta función se usará para obtener el dato de temperatura de la tabla de forma interpolada, "SI" para sistema internacional, "I" para sistema inglés
def obtener_DatoTemperaturaSaturacionTablaTemperatura(dato_conocido, sistema_Medida = "SI"):
    '''Tener en cuenta que esta función recibe datos de presión para hallar datos de temperatura''' 
    if sistema_Medida == "SI" : 
        for elemento in range(0,len(presion_BarTablas)):
            #Se recorre elemento a elemento hasta que se encuentra aquel en el que el dato de presión es mayor, en este punto la presión está entre 
            #el integrando elemento y elemento
            if presion_BarTablas[elemento] >= dato_conocido:
                #Hacemos un early return para no tener que iterar más
                return interpolacion(dato_conocido, presion_BarTablas[elemento],presion_BarTablas[elemento-1], tempertaura_CelsiusTablas[elemento], tempertaura_CelsiusTablas[elemento-1])
    if sistema_Medida == "I" : 
        for elemento in range(0,len(presion_BarTablas)):
            #Se recorre elemento a elemento hasta que se encuentra aquel en el que el dato de presión es mayor, en este punto la presión está entre 
            #el integrando elemento y elemento+1
            if presion_PsiaTablas[elemento] >= dato_conocido:
                #Hacemos un early return para no tener que iterar más
                return interpolacion(dato_conocido, presion_PsiaTablas[elemento],presion_PsiaTablas[elemento-1], tempertaura_FarenheitTablas[elemento], tempertaura_FarenheitTablas[elemento-1])

def obtener_DatoPresionSaturacionTablaTemperatura(dato_conocido, sistema_Medida = "SI"):
    if sistema_Medida == "SI":
        for elemento in range(0, len(tempertaura_CelsiusTablas)):
            if tempertaura_CelsiusTablas[elemento] >= dato_conocido:
                valor_interpolacion = interpolacion (dato_conocido, tempertaura_CelsiusTablas[elemento], tempertaura_CelsiusTablas[elemento-1], presion_BarTablas[elemento], presion_BarTablas[elemento-1] )
                return valor_interpolacion
    if sistema_Medida == "I":
        for elemento in range(0, len(tempertaura_FarenheitTablas)):
            if tempertaura_FarenheitTablas[elemento] >= dato_conocido:
                valor_interpolacion = interpolacion (dato_conocido, tempertaura_FarenheitTablas[elemento], tempertaura_FarenheitTablas[elemento-1], presion_PsiaTablas[elemento], presion_PsiaTablas[elemento-1])
                return valor_interpolacion
            
def entalpia_Mezcla( temperatura_Mezcla, humedad_especifica , sistema = "SI"):
    if sistema == "SI":
        h_m = 1.005*temperatura_Mezcla + humedad_especifica*(2501.7 + 1.82*(temperatura_Mezcla))
        return h_m #Unidades en KJ/Kg
    if sistema == "I":
        h_m = 0.240*temperatura_Mezcla + humedad_especifica*(1061.5 + 0.435*(temperatura_Mezcla))
        return h_m #Unidades en BTU/lbm
    
def phi_a_humedad_especifica(phi, Temperatura, presion_total, sistema_Medida ="SI"):
    presion_saturacion = obtener_DatoPresionSaturacionTablaTemperatura(Temperatura,sistema_Medida)
    humedad_especifica = 0.622 * phi*presion_saturacion /(presion_total-phi*presion_saturacion)
    return humedad_especifica
    
def tanteo( temperatura_BulboSeco_Inicial, humedad_Especifica_Inicial, phi_final ,temperatura_inicio_tanteo, presion_total, sistema ="SI"):
    '''Esta función se encarga de hacer el tanteo para hallar la temperatura de bulbo húmedo'''
    condicion = True
    if sistema == "SI":
        h_m = entalpia_Mezcla(temperatura_BulboSeco_Inicial, humedad_Especifica_Inicial)
        numeracion_tanteo = 1
        while condicion:
            print("Iteración ", numeracion_tanteo, "del tanteo")
            humedad_tanteo = (h_m-1.005*temperatura_inicio_tanteo)/(2501.7+1.82*temperatura_inicio_tanteo)
            print("Humedad Específica parcial del tanteo: ", humedad_tanteo, " kgv/kga")
            presion_SaturadaTanteo = presion_total*humedad_tanteo/(phi_final*0.622+phi_final*humedad_tanteo)
            print("Presión Saturada parcial del tanteo: ", presion_SaturadaTanteo, "bar")
            temperatura_BulboHumedo = obtener_DatoTemperaturaSaturacionTablaTemperatura(presion_SaturadaTanteo, "SI")
            print("Temperatura Parcial del tanteo: ", temperatura_BulboHumedo, "°C")
            numeracion_tanteo+=1
            print("Tanteo no exitoso")
            if abs(temperatura_BulboHumedo - temperatura_inicio_tanteo) <= 0.01:
                # Se repite el tanteo para dar la respuesta, con la temperatura de bulbo húmedo inmediatamente anterior a la que hallamos
                print("Iteración ", numeracion_tanteo, " del tanteo")
                humedad_tanteo = (h_m-1.005*temperatura_BulboHumedo)/(2501.7+1.82*temperatura_BulboHumedo)
                print("Humedad Específica final del tanteo: ", humedad_tanteo, "kgv/kga")
                presion_SaturadaTanteo = presion_total*humedad_tanteo/(phi_final*0.622+phi_final*humedad_tanteo)
                print("Presión Saturada final del tanteo: ", presion_SaturadaTanteo, "bar")
                temperatura_BulboHumedo = obtener_DatoTemperaturaSaturacionTablaTemperatura(presion_SaturadaTanteo, "SI")
                condicion = False
                print("Temperatura Final del tanteo: ", temperatura_BulboHumedo, "°C")
                print("Tanteo Exitoso")
                return temperatura_BulboHumedo
            else:
                temperatura_inicio_tanteo = temperatura_BulboHumedo

    if sistema == "I":
        numeracion_tanteo = 1
        h_m = entalpia_Mezcla(temperatura_BulboSeco_Inicial,humedad_Especifica_Inicial, "I")
        while condicion:
            print("Iteración ", numeracion_tanteo, " del tanteo")
            humedad_tanteo = (h_m-0.240*temperatura_inicio_tanteo)/(1061.5+0.435*(temperatura_inicio_tanteo))
            print("Humedad Específica parcial del tanteo: ", humedad_tanteo, "lbv/lba")
            presion_SaturadaTanteo = presion_total*humedad_tanteo/(phi_final*(0.622+humedad_tanteo))
            print("Presión Saturada parcial del tanteo: ", presion_SaturadaTanteo, "psia")
            temperatura_BulboHumedo = obtener_DatoTemperaturaSaturacionTablaTemperatura(presion_SaturadaTanteo, "I")
            print("Temperatura Parcial del Tanteo: ", temperatura_BulboHumedo, "°F")
            numeracion_tanteo+=1
            if (temperatura_BulboHumedo - temperatura_inicio_tanteo) <= 0.01:
                # Se repite el tanteo para dar la respuesta
                print("Iteración ", numeracion_tanteo, " del tanteo")
                humedad_tanteo = (h_m -0.240*temperatura_BulboHumedo)/(1061.5+0.435*(temperatura_BulboHumedo))
                print("Humedad Específica final del tanteo: ", humedad_tanteo, "lbv/lba")
                presion_SaturadaTanteo = presion_total*humedad_tanteo/(phi_final*(0.622+humedad_tanteo))
                print("Presión Saturada final del tanteo: ", presion_SaturadaTanteo, "psia")
                temperatura_BulboHumedo = obtener_DatoTemperaturaSaturacionTablaTemperatura(presion_SaturadaTanteo, "I")
                condicion = False
                print("Temperatura Final del tanteo: ", temperatura_BulboHumedo, " °F")
                return temperatura_BulboHumedo
            else:
                temperatura_inicio_tanteo = temperatura_BulboHumedo
                
###########################
#En esta sección van a poner los datos que sean necesarios para su situación particular:
Temperatura_de_la_Mezcla_Inicial = 50 
phi_Inicial = 0 #Solo hace falta si van a calcular la humedad específica en función de la humedad realtiva
Presion_Sistema = 0.8533 #bar, la de medallo
Humedad_Especifica_Inicial = 0.0044859 #phi_a_humedad_especifica(phi_Inicial, Temperatura_de_la_Mezcla_Inicial, Presion_Sistema)}
#Humedad_Especifica_Inicial = phi_a_humedad_especifica(phi_Inicial, Temperatura_de_la_Mezcla_Inicial, Presion_Sistema)
sistema = "SI"  # "SI" para métrico y "I" para inglés
Temperatura_de_Inicio_del_Tanteo = 22 # Esta la deben definir ustedes jejeje
phi_final = 0.95    #Esta es igual a 1 si es bulbo húmedo, si no, debe ser cambiada

#Esta llamada a la función devolverá los resultados del proceso, por favor, úsenlo como guía, deben hacer todo el procedimiento escrito adecuadamente
#Esto solo es una ayuda para guiarse en los resultados parciales y final para que me les vaya bien en el parcial
tanteo(Temperatura_de_la_Mezcla_Inicial, Humedad_Especifica_Inicial, phi_final, Temperatura_de_Inicio_del_Tanteo, Presion_Sistema, "SI")

#print(obtener_DatoPresionSaturacionTablaTemperatura(22,"SI"))