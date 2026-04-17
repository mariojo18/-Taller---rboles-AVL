import sys
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    # --- Funciones Auxiliares ---
    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # --- Rotaciones ---
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    # --- Inserción ---
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node # No se permiten duplicados

        self._update_height(node)
        return self._rebalance(node)

    # --- Eliminación ---
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if not node:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Nodo encontrado: Caso con uno o ningún hijo
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Caso con dos hijos: Obtener el sucesor (mínimo en el subárbol derecho)
            temp = self._get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        if not node:
            return node

        self._update_height(node)
        return self._rebalance(node)

    # --- Lógica de Rebalanceo ---
    def _rebalance(self, node):
        balance = self._get_balance(node)

        # Caso Izquierda-Izquierda o Izquierda-Derecha
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left) # Rotación doble
            return self._rotate_right(node)

        # Caso Derecha-Derecha o Derecha-Izquierda
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right) # Rotación doble
            return self._rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # --- Recorrido In-order ---
    def in_order(self):
        elements = []
        self._in_order_recursive(self.root, elements)
        return elements

    def _in_order_recursive(self, node, elements):
        if node:
            self._in_order_recursive(node.left, elements)
            elements.append(node.value)
            self._in_order_recursive(node.right, elements)

    # --- Visualización ---
    def display(self, node=None, level=0, prefix="Raíz: "):
        if node is None and level == 0:
            node = self.root
        if node:
            print(" " * (level * 4) + prefix + f"[{node.value}] (Alt:{node.height}, Bal:{self._get_balance(node)})")
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.display(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")

# --- Pruebas del sistema ---
avl = AVLTree()
valores =  [15, 10, 20, 8, 12, 25, 5]

print("Insertando valores:", valores)
for val in valores:
    avl.insert(val)

print("\nEstructura del árbol después de inserciones:")
avl.display()

print("\nRecorrido In-order (ordenado):", avl.in_order())

print("\nEliminando el valor 30...")
avl.delete(30)
avl.display()
