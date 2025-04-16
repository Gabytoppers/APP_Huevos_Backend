from flask import Flask, request, jsonify
from services import registrar_huevos, registrar_venta, verificar_stock
from models import huevos_collection

app = Flask(__name__)

@app.route('/registro_huevos', methods=['POST'])
def registrar():
    data = request.json
    tipo = data.get("tipo_huevo")
    tamaño = data.get("tamaño")
    cantidad = data.get("cantidad")
    if not tipo or not tamaño or not cantidad:
        return jsonify({"error": "Faltan datos"}), 400

    registrar_huevos(tipo, tamaño, cantidad)
    return jsonify({"message": "Huevos registrados exitosamente"}), 200

@app.route('/venta_huevos', methods=['POST'])
def venta():
    data = request.json
    tipo_cliente = data.get("tipo_cliente")
    unidad = data.get("unidad")
    tipo = data.get("tipo_huevo")
    tamaño = data.get("tamaño")
    cantidad = data.get("cantidad")

    if not tipo_cliente or not unidad or not tipo or not tamaño or not cantidad:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = registrar_venta(tipo_cliente, unidad, tipo, tamaño, cantidad)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

@app.route('/venta_huevos_juridica', methods=['POST'])
def venta_juridica():
    data = request.json
    tipo_cliente = data.get("tipo_cliente")
    unidad = data.get("unidad")
    tipo = data.get("tipo_huevo")
    tamaño = data.get("tamaño")
    cantidad = data.get("cantidad")

    if not tipo_cliente or not unidad or not tipo or not tamaño or not cantidad:
        return jsonify({"error": "Faltan datos"}), 400

    # Validar que el tipo de cliente es persona jurídica
    if tipo_cliente.lower() != "juridica":
        return jsonify({"error": "Solo se puede vender a persona jurídica"}), 400

    # Validar que la venta sea por cubeta
    if unidad.lower() != "cubeta":
        return jsonify({"error": "Solo se pueden vender cubetas a persona jurídica"}), 400

    resultado = registrar_venta(tipo_cliente, unidad, tipo, tamaño, cantidad)
    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@app.route('/consultar_stock', methods=['GET'])
def stock():
    tipo = request.args.get("tipo_huevo")
    tamaño = request.args.get("tamaño")
    huevo = huevos_collection.find_one({"tipo": tipo, "tamaño": tamaño})
    if not huevo:
        return jsonify({"message": "No hay stock para ese tipo y tamaño"}), 404
    return jsonify({"stock": huevo["cantidad"]})

if __name__ == '__main__':
    app.run(debug=True)
