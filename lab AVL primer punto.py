import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 

# ---------- Funciones auxiliares (igual que tenías) ----------
def getHeight(node):
    if not node:
        return 0
    return node.height

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

# ---------- Rotaciones (igual que tenías) ----------
def rotate_right(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x

def rotate_left(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y

# ---------- Clase AVLTree ----------
class AVLTree:
    def __init__(self):
        self.root = None

    # ========== INSERCIÓN ==========
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # 1. Inserción BST normal
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node   # no se permiten duplicados
        
        # 2. Actualizar altura de este nodo ancestro
        updateHeight(node)
        
        # 3. Obtener el factor de balance y rebalancear si es necesario
        balance = getBalance(node)

        # Caso Izquierda-Izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)
        
        # Caso Izquierda-Derecha
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        
        # Caso Derecha-Derecha
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        
        # Caso Derecha-Izquierda
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)
        
        return node   # ya estaba balanceado

    # ========== ELIMINACIÓN ==========
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        # 1. Eliminación BST estándar
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Nodo encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Nodo con dos hijos: obtener el sucesor in-order (el menor del subárbol derecho)
                sucesor = self._min_value_node(node.right)
                node.value = sucesor.value
                node.right = self._delete_recursive(node.right, sucesor.value)
        
        if not node:
            return node   # si el nodo fue eliminado y no hay reemplazo

        # 2. Actualizar altura
        updateHeight(node)
        
        # 3. Rebalancear
        balance = getBalance(node)

        # Caso Izquierda-Izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)
        # Caso Izquierda-Derecha
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        # Caso Derecha-Derecha
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        # Caso Derecha-Izquierda
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)
        
        return node

    def _min_value_node(self, node):
        """Encuentra el nodo con el valor mínimo en un subárbol (el más a la izquierda)."""
        current = node
        while current.left:
            current = current.left
        return current

    # ========== RECORRIDO IN-ORDER ==========
    def inorder(self):
        """Devuelve una lista con los valores en orden ascendente."""
        resultado = []
        self._inorder_recursive(self.root, resultado)
        return resultado

    def _inorder_recursive(self, node, lista):
        if node:
            self._inorder_recursive(node.left, lista)
            lista.append(node.value)
            self._inorder_recursive(node.right, lista)

    # ========== VISUALIZACIÓN SIMPLE ==========
    def display(self):
        """Imprime el árbol girado 90° a la izquierda para ver su estructura."""
        self._display_recursive(self.root, 0)

    def _display_recursive(self, node, level):
        if node:
            # Imprime primero el subárbol derecho (aparecerá arriba en pantalla)
            self._display_recursive(node.right, level + 1)
            # Imprime el nodo actual con indentación
            print("    " * level + f"{node.value} (h={node.height}, bf={getBalance(node)})")
            # Imprime el subárbol izquierdo (aparecerá abajo)
            self._display_recursive(node.left, level + 1)


# ========== PRUEBA RÁPIDA ==========
if __name__ == "__main__":
    avl = AVLTree()
    values_to_insert = [10, 20, 30, 40, 50, 25]

    print("Insertando valores:", values_to_insert)
    for val in values_to_insert:
        avl.insert(val)

    print("\n--- Árbol después de las inserciones ---")
    avl.display()
    print("\nRecorrido in-order:", avl.inorder())

    # Probamos eliminación
    print("\nEliminando el valor 20...")
    avl.delete(20)
    avl.display()
    print("\nIn-order después de eliminar 20:", avl.inorder())

    print("\nEliminando el valor 30...")
    avl.delete(30)
    avl.display()
    print("\nIn-order después de eliminar 30:", avl.inorder())
