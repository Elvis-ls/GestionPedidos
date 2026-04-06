"""
Módulo Producto
Contiene la información básica de un producto y métodos para gestionar el stock.
"""

class Producto:
    """
    Representa un producto en el inventario de TechShop.
    
    Atributos:
        codigo (str): Código único del producto
        nombre (str): Nombre del producto
        precio (float): Precio unitario del producto
        stock (int): Cantidad disponible en inventario
    """
    
    def __init__(self, codigo, nombre, precio, stock):
        """
        Inicializa un producto con sus atributos básicos.
        
        Args:
            codigo (str): Código único del producto
            nombre (str): Nombre del producto
            precio (float): Precio unitario (debe ser >= 0)
            stock (int): Cantidad inicial en stock (debe ser >= 0)
        
        Raises:
            ValueError: Si el precio o stock son negativos
        """
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    
    def verificar_disponibilidad(self, cantidad):
        """
        Verifica si hay suficiente stock para la cantidad solicitada.
        
        Args:
            cantidad (int): Cantidad a verificar
        
        Returns:
            bool: True si hay suficiente stock, False en caso contrario
        """
        return self.stock >= cantidad
    
    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock del producto restando la cantidad especificada.
        
        Args:
            cantidad (int): Cantidad a descontar del stock
        
        Returns:
            bool: True si se actualizó correctamente, False si no hay suficiente stock
        """
        if self.verificar_disponibilidad(cantidad):
            self.stock -= cantidad
            return True
        return False
    
    def __str__(self):
        """Representación en string del producto."""
        return f"Producto({self.codigo}, {self.nombre}, ${self.precio:.2f}, Stock: {self.stock})"
    
    def __repr__(self):
        """Representación para debugging."""
        return self.__str__()