import random
import re
import os

activarMsnDebug = False # Al activar esta variable podemos ver una impresión de las variables
testClase = False # Variable para probar el cifrado con la llave prueba usada en clase: k=casa

# ======
# Paso 1: Recibir M (mensaje) y sacar longitud (L)
# ======

def convertirMSN(mensaje):
    mensaje_number = []
    for ch in mensaje:
        if ch.isalpha():
            valor = ord(ch.upper()) - 65
            mensaje_number.append(valor)
            
    
    if(activarMsnDebug):
        print("Mensaje: ", mensaje)
        print("m: ", mensaje_number)
        
    return mensaje_number

def msnLong(mensaje):
    return len(mensaje)

# ======
# Paso 2: Con L de M calcular la llave (K)
# Paso 3: K son números aleatorios de máximo 26
# ======

def generarLlave(longitud):
    
    if(testClase):
        key = [2, 0, 18, 0] # casa
        print("Llave: Casa")
        print("k: ", key)
        return key
        
    key = [random.randint(0, 25) for _ in range(longitud)]
    
    
    if(activarMsnDebug):
        key_letras = ''.join(chr(65 + k) for k in key)  # 65 es 'A' en ASCII
        print("Llave:", key_letras)
        print("k:", key)
        
    return key

# ======
# Paso 4: Guardar Cifrado del Mensaje (C_M) [C_M = M (XOR) K mod 26] y K en un archivo
# ======

def cifrarMensaje(m, k):
    cifrado = [(mi ^ ki) for mi, ki in zip(m, k)]
        
    if(activarMsnDebug):
        cifrado_txt = ''.join(chr(65 + (c % 26)) for c in cifrado)
        print("Cifrado:", cifrado_txt)
        print("C1: ", cifrado)
    
    return cifrado

def guardarArchivo(cm, k):
    with open("cifradoANDkey.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(map(str, cm)) + "\n")
        f.write(" ".join(map(str, k)) + "\n")
    return

# ------
# Paso 5: Recibir archivos C_M y K
# ------

def recibirArchivos():
    ruta = "cifradoANDkey.txt"
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = [ln.strip() for ln in f if ln.strip() != ""]

        cm = list(map(int, lineas[0].split()))
        k  = list(map(int, lineas[1].split()))

        n = min(len(cm), len(k))
        
        if n == 0:
            raise ValueError("C_M o K están vacíos.")
            return

        mensaje = [cm[i] ^ k[i] for i in range(n)]

        if activarMsnDebug:
            print("\n=========")
            print(f"Cm = {cm}")
            print(f"k = {k}")
            print("---------")
            print(f"mensaje = {mensaje}")
            print("=========\n")
            
        return mensaje
    except Exception as e:
        print(f"Error: {e}")
        return False


# ------
# Paso 6: Obtener M en pantalla
# ------

def MostrarM(msn):
    msnTxt = ''.join(chr(65 + m) for m in msn)
    print("==========")
    print("El mensaje descifrado: ", msn)
    print("Mensaje convertido a texto: ", msnTxt)
    print("==========\n")
    return

# ------
# Paso 7: Eliminar o borrar archivo K
# ------

def borrarArchivo():
    ruta = "cifradoANDkey.txt"
    try:
        os.remove(ruta)
        print(f"Archivo '{ruta}' eliminado.")
        
        return True
    except FileNotFoundError:
        print(f"El archivo '{ruta}' no existe, nada que borrar.")
        return False
    except Exception as e:
        print(f"Error al borrar '{ruta}': {e}")
        return False

# ======
#  Aplicación
# ======

while True:
    print("==== Cifrado tipo Vernam ====")
    print("1) Cifrar mensaje")
    print("2) Descifrar (desde archivos)")
    print("3) Borrar archivo de llave")
    print("4) Opciones de texto en consola")
    print("5) Salir")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        mensaje = input("Introduzca un mensaje: ")
        L = msnLong(mensaje)
        
        if L == 0:
            print("No hay letras A-Z para cifrar.")
            break
        else:
            
            if(testClase):
                print("\n\nOpción testClase activa!\nActualizando: mensaje = hijo\n\n")
                mensaje = "hijo"
            
            if not re.fullmatch(r"[A-Za-z]+", mensaje):
                print("Error: No se pueden contener números o caracteres especiales en el mensaje. Mensaje actualizado a 'hijo'.\n")
                mensaje = "hijo"

            # Paso 1
            m = convertirMSN(mensaje) # Mensaje convertido a número
            l = msnLong(mensaje) # longitud del mensaje
            
            # Paso 2
            k = generarLlave(l) # Calculado la llave apartir de la longitud
            cm = cifrarMensaje(m, k) # Aplicando M (XOR) K mod 26
            
            guardarArchivo(cm, k)
            
            print("Mensaje cifrado con éxito!\n")

    elif opcion == "2":
        msn = recibirArchivos()
        MostrarM(msn)

    elif opcion == "3":
        borrarArchivo()

    elif opcion == "4":
        print("\nOpción protegida!\nIntroduzca la contraseña secreta (Que es 1234): ")
        con = input()
        
        if(con == "1234"):
            print("1) Activar logs de variables.")
            print("2) Activar test de clase (Key = casa, Msn = hijo)")
            print("3) Desctivar opción 1.")
            print("4) Desctivar opción 2.\n")
            
            op = input()
            
            if(op == "1"):
                print("Variable Activar Mensajes Debug: activa\n")
                activarMsnDebug = True
                
            elif(op == "2"):
                print("Variable test de clase: activa\n")
                testClase = True
                
            elif(op == "3"):
                print("Variable Activar Mensajes Debug: desactivada\n")
                activarMsnDebug = False
                
            elif(op == "4"):
                print("Variable test de clase: desactivada\n")
                testClase = False
                
            else:
                print("Ninguna opción elegida!\n")
            
        else:
            print("Contraseña equivocada!!! ??????\n")

    elif opcion == "5":
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida.\n")