from classes.interface.interface import InterfaceComands
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
import os
path = os.path.join(os.path.join(os.path.abspath(__name__).split("proj_banco_dados")[0], "proj_banco_dados"), "files")
path_file = os.path.join(path, "words_alpha.txt")


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

interface: InterfaceComands = None

@app.route('/')
@cross_origin()
def Hello():
    return "Hello world!"

@app.route('/init', methods=['POST'])
@cross_origin()
def init_interface_object():
    global interface
    
    dados = request.get_json()
    if not dados or "rpp" not in dados:
        return jsonify({"erro":"Parâmetro 'rpp' é obrigatório"}), 400

    registers_per_page = dados["rpp"]
    interface = InterfaceComands(
        path_file, rpp=registers_per_page
    )

    return jsonify({"status":"Interface incializada com sucesso",
        "pages":len(interface.listPages.list_pages), # número de páginas
        "buckets" : int(interface.buckets.qunt), # número de buckets
        "regiBucket" : int(interface.buckets.lim), # número de tuplas por buket
        "colision_rate":f"{interface.colison_rate():.2%}", # taxa de colisão
        "overflow_rate":f"{interface.overflow_rate():.2%}", # taxa de overflow
        "rpp":int(registers_per_page), # registro por página
        "regi": int(interface.listPages.get_num_regis())} # Quantidade de registros
        ), 200
    
# retornar primeira e ultima página
@app.route('/getPages', methods=['GET'])
@cross_origin()
def first_last_page():
    global interface
    
    if interface is None:
        return jsonify({"error" : "Interface nao foi inicializada"}), 400
    
    first_page = interface.listPages[0]
    last_page = interface.listPages[-1]

    first_page_list = [str(item) for item in first_page]
    last_page_list = [str(item) for item in last_page]
    
    # número da página e registros de cada uma
    response = {
        "first": {"idx":0, "page":first_page_list},
        "last" : {"idx":interface.listPages.num_pages - 1,"page": last_page_list}
    }
    return jsonify(response), 200
    

@app.route('/tablescan', methods=['GET'])
@cross_origin()
def table_scan():
    global interface
    
    key = request.args.get('key')
    
    if interface is None:
        return jsonify({"error" : "Interface nao foi inicializada"}), 400
    

    # realizar table scan a partir da key passada pelo usuário

    inicio = time.time()
    
    result = interface.table_scan(key)

    scan_time = time.time() - inicio
    
    if result is None:
        return jsonify({"erro":"Chave nao esta na lista de paginas"}), 400
    
    item, idx = result
    
    
    return jsonify({"status":"Table Scan concluido",
        "time":f"{scan_time}",
        "cost":f"{interface.last_table_search_cost}",
        "key":item,
        "idx":idx,
        "page": [str(item) for item in interface.listPages[idx]]}), 200

# realisar procura com hash
@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    global interface
    
    key = request.args.get('key')
    
    if interface is None:
        return jsonify({"error" : "Interface nao foi inicializada"}), 400
    
    
    inicio = time.time()
    
    result = interface.get_page_by_key(key)

    scan_time = time.time() - inicio
    
    if result is None:
        return jsonify({"erro":"Chave nao esta na lista de paginas"}), 400
    
    item, idx = result

    return jsonify({"status":"Hash Scan concluido",
        "time":f"{scan_time}",
        "cost":f"{interface.last_hash_consult_cost}",
        "key":item,
        "idx":idx,
        "page": [str(item) for item in interface.listPages[idx]]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)