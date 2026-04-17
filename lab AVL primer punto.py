class Nodo:
    """Nodo del árbol AVL, similar a un nodo de lista enlazada pero con dos hijos."""
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None
        self.altura = 1   # hoja = altura 1


class AVL:
    def __init__(self):
        self.raiz = None

    # ---------- Métodos auxiliares simples ----------
    def altura(self, nodo):
        """Devuelve la altura de un nodo (0 si es None)."""
        return nodo.altura if nodo else 0

    def factor_balance(self, nodo):
        """Factor de balance = altura izq - altura der."""
        if not nodo:
            return 0
        return self.altura(nodo.izq) - self.altura(nodo.der)

    def actualizar_altura(self, nodo):
        """Recalcula la altura a partir de las alturas de los hijos."""
        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    # ---------- Rotaciones (similares a reordenar punteros en listas) ----------
    def rotar_derecha(self, y):
        x = y.izq
        temp = x.der

        # Rotación
        x.der = y
        y.izq = temp

        # Actualizar alturas (primero el que quedó abajo)
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        return x

    def rotar_izquierda(self, x):
        y = x.der
        temp = y.izq

        y.izq = x
        x.der = temp

        self.actualizar_altura(x)
        self.actualizar_altura(y)
        return y

    # ---------- Balanceo automático ----------
    def balancear(self, nodo):
        """Aplica la rotación que corresponda si el nodo está desbalanceado."""
        fb = self.factor_balance(nodo)

        # Caso izquierda - izquierda
        if fb > 1 and self.factor_balance(nodo.izq) >= 0:
            return self.rotar_derecha(nodo)

        # Caso derecha - derecha
        if fb < -1 and self.factor_balance(nodo.der) <= 0:
            return self.rotar_izquierda(nodo)

        # Caso izquierda - derecha
        if fb > 1 and self.factor_balance(nodo.izq) < 0:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)

        # Caso derecha - izquierda
        if fb < -1 and self.factor_balance(nodo.der) > 0:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)

        return nodo

    # ---------- Inserción (recursiva, como en un BST) ----------
    def insertar(self, dato):
        """Inserta un nuevo dato y mantiene el balance."""
        self.raiz = self._insertar(self.raiz, dato)

    def _insertar(self, nodo, dato):
        if not nodo:
            return Nodo(dato)

        if dato < nodo.dato:
            nodo.izq = self._insertar(nodo.izq, dato)
        elif dato > nodo.dato:
            nodo.der = self._insertar(nodo.der, dato)
        else:
            return nodo   # no duplicados

        self.actualizar_altura(nodo)
        return self.balancear(nodo)

    # ---------- Eliminación sencilla ----------
    def eliminar(self, dato):
        self.raiz = self._eliminar(self.raiz, dato)

    def _minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def _eliminar(self, nodo, dato):
        if not nodo:
            return None

        if dato < nodo.dato:
            nodo.izq = self._eliminar(nodo.izq, dato)
        elif dato > nodo.dato:
            nodo.der = self._eliminar(nodo.der, dato)
        else:
            # Nodo encontrado
            if not nodo.izq:
                return nodo.der
            elif not nodo.der:
                return nodo.izq
            else:
                sucesor = self._minimo(nodo.der)
                nodo.dato = sucesor.dato
                nodo.der = self._eliminar(nodo.der, sucesor.dato)

        self.actualizar_altura(nodo)
        return self.balancear(nodo)

    # ---------- Recorrido in-order (como lista ordenada) ----------
    def in_order(self):
        elementos = []
        self._in_order(self.raiz, elementos)
        return elementos

    def _in_order(self, nodo, lista):
        if nodo:
            self._in_order(nodo.izq, lista)
            lista.append(nodo.dato)
            self._in_order(nodo.der, lista)

    # ---------- Visualización simple ----------
    def mostrar(self):
        """Imprime el árbol de lado (rotado 90°) para ver su estructura."""
        self._mostrar(self.raiz, 0)

    def _mostrar(self, nodo, nivel):
        if nodo:
            self._mostrar(nodo.der, nivel + 1)
            print("    " * nivel + f"{nodo.dato} (h={nodo.altura})")
            self._mostrar(nodo.izq, nivel + 1)


# ---------- Prueba rápida ----------
if __name__ == "__main__":
    arbol = AVL()
    datos = [15, 10, 20, 8, 12, 25, 5]

    print("Insertando:", datos)
    for num in datos:
        arbol.insertar(num)

    arbol.mostrar()
    print("In-order:", arbol.in_order())

    print("\nEliminando 10...")
    arbol.eliminar(10)
    arbol.mostrar()
    print("In-order:", arbol.in_order())  