import re

# Función para validar una producción usando regex
def validar_produccion(produccion):
    regex = r"^[A-Z]\s*->\s*([A-Z]|[a-z]|[0-9]|\||\s|𝜀)+$"
    return re.match(regex, produccion)

# Función para mostrar la gramática actual
def mostrar_gramatica(gramatica, mensaje):
    print(f"\n{mensaje}:")
    for simbolo, producciones in gramatica.items():
        print(f"{simbolo} -> {' | '.join(producciones)}")

# Función para eliminar producciones-𝜀
def eliminar_producciones_epsilon(gramatica):
    print("\nEliminando producciones-𝜀...")
    anulables = set()
    nuevas_producciones = {}

    # Paso 1: Encontrar los símbolos anulables
    for simbolo, producciones in gramatica.items():
        for produccion in producciones:
            if produccion == '𝜀':  # Producción vacía
                anulables.add(simbolo)

    if not anulables:
        print("No hay producciones-𝜀.")
        return gramatica

    # Paso 2: Remover producciones vacías y generar nuevas producciones
    for simbolo, producciones in gramatica.items():
        nuevas_producciones[simbolo] = set()
        for produccion in producciones:
            if '𝜀' not in produccion:
                nuevas_producciones[simbolo].add(produccion)

            # Generar nuevas producciones sin los símbolos anulables
            for anulable in anulables:
                if anulable in produccion:
                    nuevas_producciones[simbolo].add(produccion.replace(anulable, ''))

    mostrar_gramatica(nuevas_producciones, "Después de eliminar producciones-𝜀")
    return nuevas_producciones

# Función para eliminar producciones unarias
def eliminar_producciones_unarias(gramatica):
    print("\nEliminando producciones unarias...")
    cambios_realizados = False
    nuevas_producciones = {}
    for simbolo, producciones in gramatica.items():
        nuevas_producciones[simbolo] = set()
        for produccion in producciones:
            if len(produccion) == 1 and produccion.isupper():  # Producción unaria
                nuevas_producciones[simbolo].update(gramatica[produccion])
                cambios_realizados = True
            else:
                nuevas_producciones[simbolo].add(produccion)
    
    if not cambios_realizados:
        print("No es necesario eliminar producciones unarias.")
        return gramatica

    mostrar_gramatica(nuevas_producciones, "Después de eliminar producciones unarias")
    return nuevas_producciones

# Función para eliminar símbolos inútiles (no alcanzables o no generadores)
def eliminar_simbolos_inutiles(gramatica):
    print("\nEliminando símbolos inútiles...")
    alcanzables = set()
    generadores = set()
    cambios_realizados = False
    
    # Paso 1: Encontrar los símbolos alcanzables desde el símbolo inicial
    alcanzables.add('S')
    cambio = True
    while cambio:
        cambio = False
        for simbolo, producciones in gramatica.items():
            if simbolo in alcanzables:
                for produccion in producciones:
                    for char in produccion:
                        if char.isupper() and char not in alcanzables:
                            alcanzables.add(char)
                            cambio = True

    # Paso 2: Encontrar los símbolos generadores (que producen terminales)
    for simbolo, producciones in gramatica.items():
        for produccion in producciones:
            if all(char.islower() or char.isdigit() for char in produccion):
                generadores.add(simbolo)

    cambio = True
    while cambio:
        cambio = False
        for simbolo, producciones in gramatica.items():
            if simbolo not in generadores:
                for produccion in producciones:
                    if all(char in generadores or char.islower() for char in produccion):
                        generadores.add(simbolo)
                        cambio = True

    # Eliminar símbolos no alcanzables o no generadores
    nuevas_producciones = {}
    for simbolo, producciones in gramatica.items():
        if simbolo in alcanzables and simbolo in generadores:
            nuevas_producciones[simbolo] = set()
            for produccion in producciones:
                if all(char in alcanzables and char in generadores or char.islower() for char in produccion):
                    nuevas_producciones[simbolo].add(produccion)
    
    if len(nuevas_producciones) == len(gramatica):
        print("No es necesario eliminar símbolos inútiles.")
        return gramatica

    mostrar_gramatica(nuevas_producciones, "Después de eliminar símbolos inútiles")
    return nuevas_producciones

# Función para convertir a Forma Normal de Chomsky (CNF)
def convertir_a_CNF(gramatica):
    print("\nConvirtiendo a Forma Normal de Chomsky (CNF)...")
    nuevas_producciones = {}
    for simbolo, producciones in gramatica.items():
        nuevas_producciones[simbolo] = set()
        for produccion in producciones:
            if len(produccion) == 1 and produccion.islower():
                # Producciones A -> a ya están en CNF
                nuevas_producciones[simbolo].add(produccion)
            else:
                # Convertir a la forma A -> BC
                while len(produccion) > 2:
                    nuevo_simbolo = f"X{len(nuevas_producciones)}"
                    nuevas_producciones[nuevo_simbolo] = {produccion[-2:]}
                    produccion = produccion[:-2] + nuevo_simbolo
                nuevas_producciones[simbolo].add(produccion)
    
    mostrar_gramatica(nuevas_producciones, "Después de convertir a CNF")
    return nuevas_producciones

# Función para cargar la gramática desde un archivo de texto
def cargar_gramatica(archivo):
    gramatica = {}
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if validar_produccion(linea):
                simbolo, producciones = linea.split('->')
                simbolo = simbolo.strip()
                producciones = [p.strip() for p in producciones.split('|')]
                gramatica[simbolo] = producciones
            else:
                print(f"Producción inválida: {linea}")
                return None
    return gramatica

# Función principal que ejecuta el programa
def main():
    archivo = 'gramatica.txt'
    
    # Cargar la gramática desde el archivo
    gramatica = cargar_gramatica(archivo)
    
    if not gramatica:
        print("Error al cargar la gramática.")
        return
    
    print("\nGramática original:")
    for simbolo, producciones in gramatica.items():
        print(f"{simbolo} -> {' | '.join(producciones)}")

    # Eliminar producciones-𝜀
    gramatica = eliminar_producciones_epsilon(gramatica)

    # Eliminar producciones unarias
    gramatica = eliminar_producciones_unarias(gramatica)

    # Eliminar símbolos inútiles
    gramatica = eliminar_simbolos_inutiles(gramatica)

    # Convertir a CNF
    gramatica = convertir_a_CNF(gramatica)

if __name__ == "__main__":
    main()
