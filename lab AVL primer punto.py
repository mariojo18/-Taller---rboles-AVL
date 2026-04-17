import sys

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None
        self.altura = 1 

def obtenerAltura(nodo):
    if not nodo:
        return 0
    return nodo.altura

def obtenerBalance(nodo):
    if not nodo:
        return 0
    return obtenerAltura(nodo.izq) - obtenerAltura(nodo.der)

def actualizarAltura(nodo):
    if nodo:
        nodo.altura = 1 + max(obtenerAltura(nodo.izq), obtenerAltura(nodo.der))

def rotar_derecha(y):
    x = y.izq
    T2 = x.der

    x.der = y
    y.izq = T2

    actualizarAltura(y)
    actualizarAltura(x)

    return x

def rotar_izquierda(x):
    y = x.der
    T2 = y.izq

    y.izq = x
    x.der = T2

    actualizarAltura(x)
    actualizarAltura(y)

    return y

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        self.raiz = self.insertar_recursivo(self.raiz, dato)

    def insertar_recursivo(self, nodo, dato):
        if not nodo:
            return Nodo(dato)

        if dato < nodo.dato:
            nodo.izq = self.insertar_recursivo(nodo.izq, dato)
        elif dato > nodo.dato:
            nodo.der = self.insertar_recursivo(nodo.der, dato)
        else:
            return nodo

        actualizarAltura(nodo)
        balance = obtenerBalance(nodo)

        # Izquierda-Izquierda
        if balance > 1 and obtenerBalance(nodo.izq) >= 0:
            return rotar_derecha(nodo)
        
        # Izquierda-Derecha
        if balance > 1 and obtenerBalance(nodo.izq) < 0:
            nodo.izq = rotar_izquierda(nodo.izq)
            return rotar_derecha(nodo)
        
        # Derecha-Derecha
        if balance < -1 and obtenerBalance(nodo.der) <= 0:
            return rotar_izquierda(nodo)
        
        # Derecha-Izquierda
        if balance < -1 and obtenerBalance(nodo.der) > 0:
            nodo.der = rotar_derecha(nodo.der)
            return rotar_izquierda(nodo)
        
        return nodo

    # Eliminación
    def eliminar(self, dato):
        self.raiz = self.eliminar_recursivo(self.raiz, dato)

    def eliminar_recursivo(self, nodo, dato):
        # 1. Eliminación BST estándar
        if not nodo:
            return nodo

        if dato < nodo.dato:
            nodo.izq = self.eliminar_recursivo(nodo.izq, dato)
        elif dato > nodo.dato:
            nodo.der = self.eliminar_recursivo(nodo.der, dato)
        else:
            if not nodo.izq:
                return nodo.der
            elif not nodo.der:
                return nodo.izq
            else:
                # Nodo con dos hijos: obtener el sucesor in-order (el menor del subárbol derecho)
                sucesor = self.nodo_valor_minimo(nodo.der)
                nodo.dato = sucesor.dato
                nodo.der = self.eliminar_recursivo(nodo.der, sucesor.dato)
        
        if not nodo:
            return nodo
            
        actualizarAltura(nodo)
        balance = obtenerBalance(nodo)

        # Izquierda-Izquierda
        if balance > 1 and obtenerBalance(nodo.izq) >= 0:
            return rotar_derecha(nodo)
        # Izquierda-Derecha
        if balance > 1 and obtenerBalance(nodo.izq) < 0:
            nodo.izq = rotar_izquierda(nodo.izq)
            return rotar_derecha(nodo)
        # Derecha-Derecha
        if balance < -1 and obtenerBalance(nodo.der) <= 0:
            return rotar_izquierda(nodo)
        # Derecha-Izquierda
        if balance < -1 and obtenerBalance(nodo.der) > 0:
            nodo.der = rotar_derecha(nodo.der)
            return rotar_izquierda(nodo)
        
        return nodo

    def nodo_valor_minimo(self, nodo):
        """Encuentra el nodo con el valor mínimo en un subárbol (el más a la izquierda)."""
        actual = nodo
        while actual.izq:
            actual = actual.izq
        return actual

    # Recorrido In-Orden
    def inorden(self):
        """Devuelve una lista con los valores en orden ascendente."""
        resultado = []
        self.inorden_recursivo(self.raiz, resultado)
        return resultado

    def inorden_recursivo(self, nodo, lista):
        if nodo:
            self.inorden_recursivo(nodo.izq, lista)
            lista.append(nodo.dato)
            self.inorden_recursivo(nodo.der, lista)

    # Visualización simple
    def mostrar(self):
        """Imprime el árbol girado 90° a la izquierda para ver su estructura."""
        self.mostrar_recursivo(self.raiz, 0)

    def mostrar_recursivo(self, nodo, nivel):
        if nodo:
            # Imprime primero el subárbol derecho
            self.mostrar_recursivo(nodo.der, nivel + 1)
            # Imprime el nodo actual con indentación
            print("    " * nivel + f"{nodo.dato} (h={nodo.altura}, bf={obtenerBalance(nodo)})")
            # Imprime el subárbol izquierdo
            self.mostrar_recursivo(nodo.izq, nivel + 1)


avl = ArbolAVL()
valores_a_insertar = [10, 20, 30, 40, 50, 25]

print("Insertando valores:", valores_a_insertar)
for val in valores_a_insertar:
    avl.insertar(val)

print("\n--- Árbol después de las inserciones ---")
avl.mostrar()
print("\nRecorrido in-order:", avl.inorden())

print("\nEliminando el valor 20...")
avl.eliminar(20)
avl.mostrar()
print("\nIn-order después de eliminar 20:", avl.inorden())

print("\nEliminando el valor 30...")
avl.eliminar(30)
avl.mostrar()
print("\nIn-order después de eliminar 30:", avl.inorden())
