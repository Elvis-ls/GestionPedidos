
"""
Módulo Pedido
Representa una orden de compra realizada por un cliente.
"""

from producto import Producto

class Pedido:
    """
    Representa un pedido de productos realizado por un cliente.
    
    Atributos:
        numero_pedido (str): Identificador único del pedido
        cliente (str): Nombre del cliente
        items (list): Lista de tuplas (Producto, cantidad)
        estado (str): Estado del pedido ('pendiente', 'procesado', 'rechazado')
    """
    
    def __init__(self, numero_pedido, cliente):
        """
        Inicializa un pedido vacío.
        
        Args:
            numero_pedido (str): Identificador único del pedido
            cliente (str): Nombre del cliente
        """
        self.numero_pedido = numero_pedido
        self.cliente = cliente
        self.items = []  # Lista de tuplas (Producto, cantidad)
        self.estado = 'pendiente'
    
    def agregar_producto(self, producto, cantidad):
        """
        Agrega un producto al pedido con la cantidad especificada.
        
        Args:
            producto (Producto): Producto a agregar
            cantidad (int): Cantidad solicitada
        
        Raises:
            ValueError: Si la cantidad es menor o igual a 0
            TypeError: Si el producto no es una instancia de Producto
        """
        if not isinstance(producto, Producto):
            raise TypeError("El objeto debe ser una instancia de Producto")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        self.items.append((producto, cantidad))
    
    def calcular_total(self):
        """
        Calcula el costo total del pedido sumando el precio de todos los productos.
        
        Returns:
            float: Costo total del pedido
        """
        total = 0
        for producto, cantidad in self.items:
            total += producto.precio * cantidad
        return total
    
    def marcar_como_procesado(self):
        """Marca el pedido como procesado."""
        self.estado = 'procesado'
    
    def marcar_como_rechazado(self):
        """Marca el pedido como rechazado."""
        self.estado = 'rechazado'
    
    def obtener_detalles(self):
        """
        Obtiene un resumen detallado del pedido.
        
        Returns:
            dict: Diccionario con los detalles del pedido
        """
        detalles = {
            'numero_pedido': self.numero_pedido,
            'cliente': self.cliente,
            'estado': self.estado,
            'items': [],
            'total': self.calcular_total()
        }
        
        for producto, cantidad in self.items:
            detalles['items'].append({
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio_unitario': producto.precio,
                'subtotal': producto.precio * cantidad
            })
        
        return detalles
    
    def __str__(self):
        """Representación en string del pedido."""
        return f"Pedido #{self.numero_pedido} - Cliente: {self.cliente} - Estado: {self.estado} - Total: ${self.calcular_total():.2f}"
    
    def __repr__(self):
        """Representación para debugging."""
        return self.__str__()