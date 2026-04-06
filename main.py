"""
Script principal de ejemplo para el Sistema de Gestión de Pedidos - TechShop
Demuestra el uso de los tres módulos: Producto, Pedido y ProcesadorDePedidos
"""

from producto import Producto
from pedido import Pedido
from procesador_pedido import ProcesadorDePedidos


def mostrar_separador():
    """Imprime un separador visual"""
    print("\n" + "=" * 70 + "\n")


def ejemplo_pedido_exitoso():
    """Ejemplo 1: Procesamiento exitoso de un pedido"""
    print("📦 EJEMPLO 1: Procesamiento Exitoso de Pedido")
    mostrar_separador()
    
    # Crear productos con stock suficiente
    laptop = Producto("P001", "Laptop Dell XPS 15", 1200.00, 10)
    mouse = Producto("P002", "Mouse Logitech MX Master", 85.00, 50)
    teclado = Producto("P003", "Teclado Mecánico RGB", 120.00, 30)
    
    print("📋 Productos disponibles:")
    print(f"  • {laptop}")
    print(f"  • {mouse}")
    print(f"  • {teclado}")
    
    # Crear pedido
    pedido = Pedido("PED001", "Juan Pérez")
    pedido.agregar_producto(laptop, 2)
    pedido.agregar_producto(mouse, 3)
    pedido.agregar_producto(teclado, 1)
    
    print(f"\n🛒 Pedido creado: {pedido}")
    print(f"   Total a pagar: ${pedido.calcular_total():.2f}")
    
    # Procesar pedido
    procesador = ProcesadorDePedidos()
    resultado = procesador.procesar_pedido(pedido)
    
    if resultado['exito']:
        print(f"\n✅ {resultado['mensaje']}")
        print("\n📊 Stock actualizado:")
        print(f"  • {laptop}")
        print(f"  • {mouse}")
        print(f"  • {teclado}")
    
    mostrar_separador()


def ejemplo_pedido_rechazado():
    """Ejemplo 2: Pedido rechazado por falta de stock"""
    print("🚫 EJEMPLO 2: Pedido Rechazado por Falta de Stock")
    mostrar_separador()
    
    # Crear productos con stock limitado
    monitor = Producto("P004", "Monitor 4K LG 27''", 450.00, 2)
    webcam = Producto("P005", "Webcam Logitech C920", 95.00, 1)
    
    print("📋 Productos disponibles:")
    print(f"  • {monitor}")
    print(f"  • {webcam}")
    
    # Crear pedido que excede el stock
    pedido = Pedido("PED002", "María García")
    pedido.agregar_producto(monitor, 5)  # Solo hay 2 disponibles
    pedido.agregar_producto(webcam, 1)
    
    print(f"\n🛒 Pedido creado: {pedido}")
    print(f"   Total solicitado: ${pedido.calcular_total():.2f}")
    
    # Procesar pedido
    procesador = ProcesadorDePedidos()
    resultado = procesador.procesar_pedido(pedido)
    
    if not resultado['exito']:
        print(f"\n❌ {resultado['mensaje']}")
        print("\n⚠️  Productos sin stock suficiente:")
        for item in resultado['productos_sin_stock']:
            print(f"  • {item['nombre']}")
            print(f"    - Stock disponible: {item['stock_disponible']}")
            print(f"    - Cantidad solicitada: {item['cantidad_solicitada']}")
        
        print(f"\n📊 Estado del pedido: {pedido.estado.upper()}")
        print(f"   Stock no modificado:")
        print(f"  • {monitor}")
        print(f"  • {webcam}")
    
    mostrar_separador()


def ejemplo_multiples_pedidos():
    """Ejemplo 3: Procesamiento de múltiples pedidos secuenciales"""
    print("📊 EJEMPLO 3: Procesamiento de Múltiples Pedidos")
    mostrar_separador()
    
    # Crear producto compartido
    auriculares = Producto("P006", "Auriculares Sony WH-1000XM5", 350.00, 20)
    
    print(f"📋 Producto inicial: {auriculares}")
    
    # Crear tres pedidos
    pedido1 = Pedido("PED003", "Carlos López")
    pedido1.agregar_producto(auriculares, 6)
    
    pedido2 = Pedido("PED004", "Ana Martínez")
    pedido2.agregar_producto(auriculares, 8)
    
    pedido3 = Pedido("PED005", "Luis Rodríguez")
    pedido3.agregar_producto(auriculares, 10)
    
    # Procesar pedidos secuencialmente
    procesador = ProcesadorDePedidos()
    
    print("\n🔄 Procesando pedidos...\n")
    
    # Pedido 1
    resultado1 = procesador.procesar_pedido(pedido1)
    print(f"Pedido 1 ({pedido1.cliente}): ", end="")
    print(f"✅ Procesado - Stock restante: {auriculares.stock}")
    
    # Pedido 2
    resultado2 = procesador.procesar_pedido(pedido2)
    print(f"Pedido 2 ({pedido2.cliente}): ", end="")
    print(f"✅ Procesado - Stock restante: {auriculares.stock}")
    
    # Pedido 3 (debería fallar)
    resultado3 = procesador.procesar_pedido(pedido3)
    print(f"Pedido 3 ({pedido3.cliente}): ", end="")
    print(f"❌ Rechazado - Stock insuficiente ({auriculares.stock} disponibles)")
    
    # Mostrar estadísticas
    stats = procesador.obtener_estadisticas()
    print("\n📈 Estadísticas del procesador:")
    print(f"  • Total de pedidos: {stats['total_pedidos']}")
    print(f"  • Pedidos procesados: {stats['pedidos_procesados']}")
    print(f"  • Pedidos rechazados: {stats['pedidos_rechazados']}")
    print(f"  • Monto total procesado: ${stats['monto_total_procesado']:.2f}")
    print(f"  • Tasa de éxito: {stats['tasa_exito']:.2f}%")
    
    mostrar_separador()


def ejemplo_detalles_pedido():
    """Ejemplo 4: Visualización detallada de un pedido"""
    print("📋 EJEMPLO 4: Detalles Completos de un Pedido")
    mostrar_separador()
    
    # Crear productos
    tablet = Producto("P007", "iPad Air 2024", 650.00, 15)
    funda = Producto("P008", "Funda Protective Case", 45.00, 50)
    stylus = Producto("P009", "Apple Pencil", 130.00, 30)
    
    # Crear y procesar pedido
    pedido = Pedido("PED006", "Sofia Hernández")
    pedido.agregar_producto(tablet, 1)
    pedido.agregar_producto(funda, 2)
    pedido.agregar_producto(stylus, 1)
    
    procesador = ProcesadorDePedidos()
    procesador.procesar_pedido(pedido)
    
    # Obtener y mostrar detalles
    detalles = pedido.obtener_detalles()
    
    print(f"🆔 Número de pedido: {detalles['numero_pedido']}")
    print(f"👤 Cliente: {detalles['cliente']}")
    print(f"📊 Estado: {detalles['estado'].upper()}")
    print(f"\n🛍️  Productos en el pedido:")
    
    for i, item in enumerate(detalles['items'], 1):
        print(f"\n  {i}. {item['nombre']} (Código: {item['codigo']})")
        print(f"     • Precio unitario: ${item['precio_unitario']:.2f}")
        print(f"     • Cantidad: {item['cantidad']}")
        print(f"     • Subtotal: ${item['subtotal']:.2f}")
    
    print(f"\n💰 TOTAL A PAGAR: ${detalles['total']:.2f}")
    
    mostrar_separador()


def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🏪 SISTEMA DE GESTIÓN DE PEDIDOS - TECHSHOP")
    print("=" * 70 + "\n")
    
    # Ejecutar ejemplos
    ejemplo_pedido_exitoso()
    ejemplo_pedido_rechazado()
    ejemplo_multiples_pedidos()
    ejemplo_detalles_pedido()
    
    print("✨ Ejemplos completados exitosamente!\n")
    print("💡 Tip: Ejecuta 'pytest tests/ -v' para ver las pruebas de integración\n")


if __name__ == "__main__":
    main()