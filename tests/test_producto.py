"""
Pruebas unitarias para el módulo Producto
"""

import pytest

from producto import Producto


class TestProducto:
    """Clase de pruebas para el módulo Producto"""
    
    def test_crear_producto_valido(self):
        """Prueba la creación de un producto con valores válidos"""
        producto = Producto("P001", "Laptop", 1200.00, 10)
        
        assert producto.codigo == "P001"
        assert producto.nombre == "Laptop"
        assert producto.precio == 1200.00
        assert producto.stock == 10
    
    def test_crear_producto_precio_negativo(self):
        """Prueba que no se puede crear un producto con precio negativo"""
        with pytest.raises(ValueError, match="El precio no puede ser negativo"):
            Producto("P002", "Mouse", -10.00, 5)
    
    def test_crear_producto_stock_negativo(self):
        """Prueba que no se puede crear un producto con stock negativo"""
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            Producto("P003", "Teclado", 50.00, -5)
    
    def test_verificar_disponibilidad_suficiente(self):
        """Prueba verificar disponibilidad cuando hay stock suficiente"""
        producto = Producto("P004", "Monitor", 300.00, 15)
        
        assert producto.verificar_disponibilidad(10) == True
        assert producto.verificar_disponibilidad(15) == True
    
    def test_verificar_disponibilidad_insuficiente(self):
        """Prueba verificar disponibilidad cuando no hay stock suficiente"""
        producto = Producto("P005", "Webcam", 80.00, 5)
        
        assert producto.verificar_disponibilidad(6) == False
        assert producto.verificar_disponibilidad(10) == False
    
    def test_actualizar_stock_exitoso(self):
        """Prueba actualizar stock cuando hay suficiente disponibilidad"""
        producto = Producto("P006", "Auriculares", 50.00, 20)
        
        resultado = producto.actualizar_stock(5)
        
        assert resultado == True
        assert producto.stock == 15
    
    def test_actualizar_stock_fallido(self):
        """Prueba actualizar stock cuando no hay suficiente disponibilidad"""
        producto = Producto("P007", "Cable HDMI", 15.00, 3)
        
        resultado = producto.actualizar_stock(5)
        
        assert resultado == False
        assert producto.stock == 3  # El stock no debe cambiar
    
    def test_actualizar_stock_exacto(self):
        """Prueba actualizar stock con la cantidad exacta disponible"""
        producto = Producto("P008", "Mouse Pad", 10.00, 8)
        
        resultado = producto.actualizar_stock(8)
        
        assert resultado == True
        assert producto.stock == 0
    
    def test_str_representation(self):
        """Prueba la representación en string del producto"""
        producto = Producto("P009", "SSD 500GB", 120.00, 12)
        
        str_producto = str(producto)
        
        assert "P009" in str_producto
        assert "SSD 500GB" in str_producto
        assert "$120.00" in str_producto
        assert "12" in str_producto