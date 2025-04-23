from models import huevos_collection, ventas_collection
from datetime import datetime

def registrar_huevos(tipo, tamaño, cantidad):
    huevos_collection.update_one(
        {"tipo": tipo, "tamaño": tamaño},
        {"$inc": {"cantidad": cantidad}},
        upsert=True
    )

def verificar_stock(tipo, tamaño, cantidad):
    huevo = huevos_collection.find_one({"tipo": tipo, "tamaño": tamaño})
    if not huevo or huevo["cantidad"] < cantidad:
        return False
    return True

def registrar_venta(tipo_cliente, unidad, tipo, tamaño, cantidad):
    huevos_por_unidad = 30 if unidad == "cubeta" else 12
    cantidad_huevos = int(cantidad) * huevos_por_unidad

    # Regla de negocio
    if tipo_cliente == "juridico" and unidad != "cubeta":
        return {"error": "Una persona jurídica solo puede comprar por cubeta."}

    # Validar stock
    if not verificar_stock(tipo, tamaño, cantidad):
        return {"error": "Stock insuficiente."}

    # Descontar stock
    huevos_collection.update_one(
        {"tipo": tipo, "tamaño": tamaño},
        {"$inc": {"cantidad": -cantidad}}
    )

    # Registrar venta
    venta = {
        "tipo_cliente": tipo_cliente,
        "unidad": unidad,
        "tipo": tipo,
        "tamaño": tamaño,
        "cantidad": cantidad,
        "fecha": datetime.now()
    }
    ventas_collection.insert_one(venta)

    # Generar factura
    generar_factura(venta)
    return {"message": "Venta registrada exitosamente."}

def generar_factura(venta):
    PRECIOS_CUBETA = {
        "rojo": {
            "A": 12000,
            "AA": 13500,
            "B": 11000,
            "EXTRA": 15000
        },
        "blanco": {
            "A": 10000,
            "AA": 11500,
            "B": 9500,
            "EXTRA": 14000
        }
    }

    tipo = venta["tipo"].lower()
    tamaño = venta["tamaño"].upper()
    unidad = venta["unidad"]

    if unidad != "cubeta":
        return {"error": "Por ahora solo se permite venta por cubeta."}

    if tipo not in PRECIOS_CUBETA or tamaño not in PRECIOS_CUBETA[tipo]:
        return {"error": "Tipo o tamaño de huevo no válido."}

    valor_unitario = PRECIOS_CUBETA[tipo][tamaño]
    subtotal = venta["cantidad"] * valor_unitario
    iva = subtotal * 0.05
    total = subtotal + iva

    with open("factura.txt", "w") as f:
        f.write("Granja Huevos del Campo\n")
        f.write("NIT: 870545489-0\n")
        f.write("******** FACTURA DE VENTA ********\n")
        f.write(f"Cliente: {venta['tipo_cliente'].capitalize()}\n")
        f.write(f"Cantidad: {venta['cantidad']} ({venta['unidad']})\n")
        f.write(f"Tipo de huevo: {venta['tipo']} Tamaño: {venta['tamaño']}\n")
        f.write(f"Subtotal: ${subtotal}\n")
        f.write(f"IVA (5%): ${iva}\n")
        f.write(f"Total con IVA: ${total}\n")
        f.write("***********************************\n")
        f.write("       .==;=.                            \n")
        f.write("      / _  _ \                           \n")
        f.write("     |  o  o  |                          \n")
        f.write("     \   /\   /             ,            \n")
        f.write("    ,/'-=\/=-'\,    |\   /\/ \/|   ,_    \n")
        f.write("   / /        \ \   ; \/`     '; , \_',  \n")
        f.write("  | /          \ |   \        /          \n")
        f.write("  \/ \        / \/    '.    .'    /`.    \n")
        f.write("      '.    .'          `~~` , /\ ``     \n")
        f.write("      _|`~~`|_              .  `         \n")
        f.write("      /|\  /|\                           \n")
