"""
Módulo ProcesadorDePedidos
Procesa pedidos validando stock y actualizando el inventario.
"""

from pedido import Pedido

class ProcesadorDePedidos:
    """
    Procesa pedidos validando disponibilidad de stock y actualizando el inventario.
    
    Atributos:
        pedidos_procesados (list): Lista de pedidos procesados exitosamente
        pedidos_rechazados (list): Lista de pedidos rechazados
    """
    
    def __init__(self):
        """Inicializa el procesador de pedidos."""
        self.pedidos_procesados = []
        self.pedidos_rechazados = []
    
    def procesar_pedido(self, pedido):
        """
        Procesa un pedido validando stock y actualizando el inventario.
        
        El flujo es el siguiente:
        1. Valida que todos los productos tengan stock suficiente
        2. Si hay stock suficiente, descuenta el stock de cada producto
        3. Marca el pedido como procesado o rechazado según corresponda
        
        Args:
            pedido (Pedido): Pedido a procesar
        
        Returns:
            dict: Resultado del procesamiento con 'exito' (bool), 'mensaje' (str), 
                  y 'productos_sin_stock' (list) si aplica
        
        Raises:
            TypeError: Si el pedido no es una instancia de Pedido
        """
        if not isinstance(pedido, Pedido):
            raise TypeError("El objeto debe ser una instancia de Pedido")
        
        # Validar que el pedido tenga items
        if not pedido.items:
            pedido.marcar_como_rechazado()
            self.pedidos_rechazados.append(pedido)
            return {
                'exito': False,
                'mensaje': 'El pedido no contiene productos',
                'productos_sin_stock': []
            }
        
        # Paso 1: Validar stock de todos los productos
        productos_sin_stock = []
        for producto, cantidad in pedido.items:
            if not producto.verificar_disponibilidad(cantidad):
                productos_sin_stock.append({
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'stock_disponible': producto.stock,
                    'cantidad_solicitada': cantidad
                })
        
        # Si algún producto no tiene stock, rechazar el pedido
        if productos_sin_stock:
            pedido.marcar_como_rechazado()
            self.pedidos_rechazados.append(pedido)
            return {
                'exito': False,
                'mensaje': f'Stock insuficiente para {len(productos_sin_stock)} producto(s)',
                'productos_sin_stock': productos_sin_stock
            }
        
        # Paso 2: Todos los productos tienen stock, actualizar inventario
        for producto, cantidad in pedido.items:
            producto.actualizar_stock(cantidad)
        
        # Paso 3: Marcar el pedido como procesado
        pedido.marcar_como_procesado()
        self.pedidos_procesados.append(pedido)
        
        return {
            'exito': True,
            'mensaje': f'Pedido #{pedido.numero_pedido} procesado exitosamente',
            'productos_sin_stock': []
        }
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del procesador de pedidos.
        
        Returns:
            dict: Diccionario con estadísticas de procesamiento
        """
        total_procesados = len(self.pedidos_procesados)
        total_rechazados = len(self.pedidos_rechazados)
        total = total_procesados + total_rechazados
        
        monto_total_procesado = sum(
            pedido.calcular_total() for pedido in self.pedidos_procesados
        )
        
        return {
            'total_pedidos': total,
            'pedidos_procesados': total_procesados,
            'pedidos_rechazados': total_rechazados,
            'monto_total_procesado': monto_total_procesado,
            'tasa_exito': (total_procesados / total * 100) if total > 0 else 0
        }
    
    def __str__(self):
        """Representación en string del procesador."""
        stats = self.obtener_estadisticas()
        return f"ProcesadorDePedidos(Procesados: {stats['pedidos_procesados']}, Rechazados: {stats['pedidos_rechazados']})"
    
    def __repr__(self):
        """Representación para debugging."""
        return self.__str__()