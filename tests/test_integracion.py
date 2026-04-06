"""
Pruebas de integración para el Sistema de Gestión de Pedidos
Verifica la interacción entre Producto, Pedido y ProcesadorDePedidos
"""

import pytest

from producto import Producto
from pedido import Pedido
from procesador_pedidos import ProcesadorDePedidos

class TestIntegracionSistemaGestionPedidos:
    """Clase de pruebas de integración para todo el sistema"""
    
    def test_procesar_pedido_valido_exitosamente(self):
        """
        Prueba de integración: Procesar un pedido válido
        Verifica que el procesador puede aceptar pedidos válidos y actualizar stock
        """
        # Configuración: Crear productos con stock suficiente
        producto1 = Producto("P001", "Laptop Dell", 1200.00, 10)
        producto2 = Producto("P002", "Mouse Logitech", 25.00, 50)
        producto3 = Producto("P003", "Teclado Mecánico", 75.00, 30)
        
        # Crear pedido
        pedido = Pedido("PED001", "Juan Pérez")
        pedido.agregar_producto(producto1, 2)
        pedido.agregar_producto(producto2, 5)
        pedido.agregar_producto(producto3, 3)
        
        # Calcular total antes de procesar
        total_esperado = (1200.00 * 2) + (25.00 * 5) + (75.00 * 3)
        assert pedido.calcular_total() == total_esperado
        
        # Guardar stock inicial
        stock_inicial_p1 = producto1.stock
        stock_inicial_p2 = producto2.stock
        stock_inicial_p3 = producto3.stock
        
        # Procesar pedido
        procesador = ProcesadorDePedidos()
        resultado = procesador.procesar_pedido(pedido)
        
        # Verificaciones
        assert resultado['exito'] == True
        assert pedido.estado == 'procesado'
        assert producto1.stock == stock_inicial_p1 - 2
        assert producto2.stock == stock_inicial_p2 - 5
        assert producto3.stock == stock_inicial_p3 - 3
        assert len(procesador.pedidos_procesados) == 1
        assert len(procesador.pedidos_rechazados) == 0
    
    def test_procesar_pedido_stock_insuficiente(self):
        """
        Prueba de integración: Procesar un pedido sin stock suficiente
        Verifica que el procesador rechaza pedidos cuando no hay stock
        """
        # Configuración: Crear productos con stock limitado
        producto1 = Producto("P004", "Monitor 4K", 450.00, 2)
        producto2 = Producto("P005", "Webcam HD", 80.00, 1)
        
        # Crear pedido que excede el stock
        pedido = Pedido("PED002", "María García")
        pedido.agregar_producto(producto1, 5)  # Solicita más de lo disponible
        pedido.agregar_producto(producto2, 1)
        
        # Guardar stock inicial
        stock_inicial_p1 = producto1.stock
        stock_inicial_p2 = producto2.stock
        
        # Procesar pedido
        procesador = ProcesadorDePedidos()
        resultado = procesador.procesar_pedido(pedido)
        
        # Verificaciones
        assert resultado['exito'] == False
        assert pedido.estado == 'rechazado'
        assert producto1.stock == stock_inicial_p1  # Stock no debe cambiar
        assert producto2.stock == stock_inicial_p2  # Stock no debe cambiar
        assert len(resultado['productos_sin_stock']) > 0
        assert len(procesador.pedidos_procesados) == 0
        assert len(procesador.pedidos_rechazados) == 1
    
    def test_procesar_multiples_pedidos_secuencialmente(self):
        """
        Prueba de integración: Procesar múltiples pedidos secuencialmente
        Verifica que el stock se actualiza correctamente entre pedidos
        """
        # Configuración: Crear producto con stock moderado
        producto = Producto("P006", "Auriculares Bluetooth", 60.00, 20)
        
        # Crear tres pedidos
        pedido1 = Pedido("PED003", "Carlos López")
        pedido1.agregar_producto(producto, 5)
        
        pedido2 = Pedido("PED004", "Ana Martínez")
        pedido2.agregar_producto(producto, 8)
        
        pedido3 = Pedido("PED005", "Luis Rodríguez")
        pedido3.agregar_producto(producto, 10)  # Este debería fallar
        
        # Procesar pedidos
        procesador = ProcesadorDePedidos()
        
        resultado1 = procesador.procesar_pedido(pedido1)
        assert resultado1['exito'] == True
        assert producto.stock == 15
        
        resultado2 = procesador.procesar_pedido(pedido2)
        assert resultado2['exito'] == True
        assert producto.stock == 7
        
        resultado3 = procesador.procesar_pedido(pedido3)
        assert resultado3['exito'] == False
        assert producto.stock == 7  # Stock no cambia
        
        # Verificar estadísticas
        assert len(procesador.pedidos_procesados) == 2
        assert len(procesador.pedidos_rechazados) == 1
    
    def test_calcular_total_pedido_correctamente(self):
        """
        Prueba de integración: Verificar que el cálculo del total es correcto
        """
        # Crear productos con diferentes precios
        producto1 = Producto("P007", "Tablet", 350.00, 15)
        producto2 = Producto("P008", "Funda", 25.00, 50)
        producto3 = Producto("P009", "Stylus", 40.00, 30)
        
        # Crear pedido
        pedido = Pedido("PED006", "Sofia Hernández")
        pedido.agregar_producto(producto1, 2)  # 700.00
        pedido.agregar_producto(producto2, 3)  # 75.00
        pedido.agregar_producto(producto3, 1)  # 40.00
        
        # Verificar cálculo
        total = pedido.calcular_total()
        assert total == 815.00
        
        # Procesar y verificar
        procesador = ProcesadorDePedidos()
        resultado = procesador.procesar_pedido(pedido)
        
        assert resultado['exito'] == True
        assert pedido.calcular_total() == 815.00
    
    def test_pedido_vacio_rechazado(self):
        """
        Prueba de integración: Verificar que un pedido vacío es rechazado
        """
        pedido = Pedido("PED007", "Diego Torres")
        # No se agregan productos
        
        procesador = ProcesadorDePedidos()
        resultado = procesador.procesar_pedido(pedido)
        
        assert resultado['exito'] == False
        assert pedido.estado == 'rechazado'
        assert 'no contiene productos' in resultado['mensaje'].lower()
    
    def test_flujo_completo_con_stock_exacto(self):
        """
        Prueba de integración: Verificar el flujo cuando se solicita exactamente el stock disponible
        """
        # Crear producto con stock exacto
        producto = Producto("P010", "Cable USB-C", 15.00, 10)
        
        # Crear pedido con la cantidad exacta
        pedido = Pedido("PED008", "Elena Vargas")
        pedido.agregar_producto(producto, 10)
        
        # Procesar
        procesador = ProcesadorDePedidos()
        resultado = procesador.procesar_pedido(pedido)
        
        # Verificar
        assert resultado['exito'] == True
        assert producto.stock == 0
        assert pedido.estado == 'procesado'
    
    def test_estadisticas_procesador(self):
        """
        Prueba de integración: Verificar las estadísticas del procesador
        """
        # Crear productos
        producto1 = Producto("P011", "SSD 1TB", 150.00, 10)
        producto2 = Producto("P012", "RAM 32GB", 200.00, 5)
        
        # Crear pedidos
        pedido1 = Pedido("PED009", "Roberto Díaz")
        pedido1.agregar_producto(producto1, 2)
        
        pedido2 = Pedido("PED010", "Patricia Ruiz")
        pedido2.agregar_producto(producto2, 3)
        
        pedido3 = Pedido("PED011", "Fernando Gómez")
        pedido3.agregar_producto(producto1, 15)  # Excede stock
        
        # Procesar
        procesador = ProcesadorDePedidos()
        procesador.procesar_pedido(pedido1)
        procesador.procesar_pedido(pedido2)
        procesador.procesar_pedido(pedido3)
        
        # Obtener estadísticas
        stats = procesador.obtener_estadisticas()
        
        assert stats['total_pedidos'] == 3
        assert stats['pedidos_procesados'] == 2
        assert stats['pedidos_rechazados'] == 1
        assert stats['monto_total_procesado'] == (150.00 * 2) + (200.00 * 3)
        assert stats['tasa_exito'] == pytest.approx(66.67, 0.01)
    
    def test_interaccion_sin_errores_entre_modulos(self):
        """
        Prueba de integración: Verificar que los tres módulos interactúan sin errores
        """
        # Crear sistema completo
        productos = [
            Producto("P013", "Impresora", 280.00, 8),
            Producto("P014", "Cartuchos (Pack)", 45.00, 20),
            Producto("P015", "Papel A4 (Resma)", 12.00, 50)
        ]
        
        pedido = Pedido("PED012", "Laura Castro")
        pedido.agregar_producto(productos[0], 1)
        pedido.agregar_producto(productos[1], 2)
        pedido.agregar_producto(productos[2], 5)
        
        procesador = ProcesadorDePedidos()
        
        # Verificar que no hay excepciones
        try:
            resultado = procesador.procesar_pedido(pedido)
            detalles = pedido.obtener_detalles()
            
            assert resultado['exito'] == True
            assert detalles['estado'] == 'procesado'
            assert detalles['total'] == pedido.calcular_total()
            
            # Todo funcionó sin errores
            assert True
        except Exception as e:
            pytest.fail(f"Los módulos no interactúan correctamente: {str(e)}")
    
    def test_procesar_pedido_con_objeto_invalido(self):
        """
        Prueba de integración: Verificar que el procesador valida el tipo de objeto
        """
        procesador = ProcesadorDePedidos()
        
        with pytest.raises(TypeError, match="El objeto debe ser una instancia de Pedido"):
            procesador.procesar_pedido("No es un pedido")