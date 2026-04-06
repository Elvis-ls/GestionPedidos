"""
Pruebas unitarias para el módulo Pedido
"""

import pytest

from producto import Producto
from pedido import Pedido


class TestPedido:
    """Clase de pruebas para el módulo Pedido"""
    
    def test_crear_pedido_vacio(self):
        """Prueba la creación de un pedido vacío"""
        pedido = Pedido("PED001", "Juan Pérez")
        
        assert pedido.numero_pedido == "PED001"
        assert pedido.cliente == "Juan Pérez"
        assert pedido.items == []
        assert pedido.estado == 'pendiente'
    
    def test_agregar_producto_valido(self):
        """Prueba agregar un producto válido al pedido"""
        pedido = Pedido("PED002", "María García")
        producto = Producto("P001", "Laptop", 1200.00, 10)
        
        pedido.agregar_producto(producto, 2)
        
        assert len(pedido.items) == 1
        assert pedido.items[0] == (producto, 2)
    
    def test_agregar_multiples_productos(self):
        """Prueba agregar múltiples productos al pedido"""
        pedido = Pedido("PED003", "Carlos López")
        producto1 = Producto("P001", "Laptop", 1200.00, 10)
        producto2 = Producto("P002", "Mouse", 25.00, 50)
        producto3 = Producto("P003", "Teclado", 75.00, 30)
        
        pedido.agregar_producto(producto1, 1)
        pedido.agregar_producto(producto2, 3)
        pedido.agregar_producto(producto3, 2)
        
        assert len(pedido.items) == 3
    
    def test_agregar_producto_cantidad_invalida(self):
        """Prueba agregar un producto con cantidad inválida"""
        pedido = Pedido("PED004", "Ana Martínez")
        producto = Producto("P004", "Monitor", 300.00, 15)
        
        with pytest.raises(ValueError, match="La cantidad debe ser mayor a 0"):
            pedido.agregar_producto(producto, 0)
        
        with pytest.raises(ValueError, match="La cantidad debe ser mayor a 0"):
            pedido.agregar_producto(producto, -5)
    
    def test_agregar_objeto_no_producto(self):
        """Prueba agregar un objeto que no es un Producto"""
        pedido = Pedido("PED005", "Luis Rodríguez")
        
        with pytest.raises(TypeError, match="El objeto debe ser una instancia de Producto"):
            pedido.agregar_producto("No es un producto", 1)
    
    def test_calcular_total_pedido_vacio(self):
        """Prueba calcular el total de un pedido vacío"""
        pedido = Pedido("PED006", "Sofia Hernández")
        
        total = pedido.calcular_total()
        
        assert total == 0
    
    def test_calcular_total_un_producto(self):
        """Prueba calcular el total con un solo producto"""
        pedido = Pedido("PED007", "Diego Torres")
        producto = Producto("P005", "Webcam", 80.00, 5)
        
        pedido.agregar_producto(producto, 3)
        total = pedido.calcular_total()
        
        assert total == 240.00
    
    def test_calcular_total_multiples_productos(self):
        """Prueba calcular el total con múltiples productos"""
        pedido = Pedido("PED008", "Elena Vargas")
        producto1 = Producto("P006", "Auriculares", 50.00, 20)
        producto2 = Producto("P007", "Cable HDMI", 15.00, 30)
        producto3 = Producto("P008", "Mouse Pad", 10.00, 40)
        
        pedido.agregar_producto(producto1, 2)  # 100.00
        pedido.agregar_producto(producto2, 4)  # 60.00
        pedido.agregar_producto(producto3, 5)  # 50.00
        
        total = pedido.calcular_total()
        
        assert total == 210.00
    
    def test_marcar_como_procesado(self):
        """Prueba marcar un pedido como procesado"""
        pedido = Pedido("PED009", "Roberto Díaz")
        
        pedido.marcar_como_procesado()
        
        assert pedido.estado == 'procesado'
    
    def test_marcar_como_rechazado(self):
        """Prueba marcar un pedido como rechazado"""
        pedido = Pedido("PED010", "Patricia Ruiz")
        
        pedido.marcar_como_rechazado()
        
        assert pedido.estado == 'rechazado'
    
    def test_obtener_detalles_pedido(self):
        """Prueba obtener los detalles completos de un pedido"""
        pedido = Pedido("PED011", "Fernando Gómez")
        producto1 = Producto("P009", "SSD 500GB", 120.00, 12)
        producto2 = Producto("P010", "RAM 16GB", 80.00, 25)
        
        pedido.agregar_producto(producto1, 2)
        pedido.agregar_producto(producto2, 1)
        
        detalles = pedido.obtener_detalles()
        
        assert detalles['numero_pedido'] == "PED011"
        assert detalles['cliente'] == "Fernando Gómez"
        assert detalles['estado'] == 'pendiente'
        assert detalles['total'] == 320.00
        assert len(detalles['items']) == 2
        assert detalles['items'][0]['codigo'] == "P009"
        assert detalles['items'][0]['cantidad'] == 2
        assert detalles['items'][0]['subtotal'] == 240.00
    
    def test_str_representation(self):
        """Prueba la representación en string del pedido"""
        pedido = Pedido("PED012", "Laura Castro")
        producto = Producto("P011", "Tablet", 450.00, 8)
        pedido.agregar_producto(producto, 1)
        
        str_pedido = str(pedido)
        
        assert "PED012" in str_pedido
        assert "Laura Castro" in str_pedido
        assert "pendiente" in str_pedido
        assert "$450.00" in str_pedido