from flask import Flask, escape, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

@app.route('/api/v1/transaction', methods=['GET'])
def index():
    data = mongo.db.transaction.find({})
    if request.args:
        data = request.args.get("data")
        valor = request.args.get("valor")
        if not valor:
            d = mongo.db.transaction.find(
                {"Data": data}
            )
            return dumps(d)
        if not data:
            d = mongo.db.transaction.find(
                {"Valor": {"$lt": int(valor)}}
            )
            return dumps(d)
        d = mongo.db.transaction.find(
            {"Data": data, "Valor": {"$lt": int(valor)}}
        )
        return dumps(d)
    return dumps(data)

@app.route('/api/v1/transaction/create', methods=['POST'])
def create_transaction():
    _json_dados = request.json
    _data = _json_dados['Data']
    _hora = _json_dados['Hora']
    _ctnini = _json_dados['ContaInicial']
    _ctnfin = _json_dados['ContaFinal']
    _valor = _json_dados['Valor']
    if _data and _hora and _ctnfin and _ctnini and _valor and request.method == "POST":
        mongo.db.transaction.insert_one({
            "Data": _data,
            "Hora": _hora,
            "ContaInicial": _ctnini,
            "ContaFinal": _ctnfin,
            "Valor": _valor
        })
        return jsonify({'ok': True, 'message': 'Transação adicionada com sucesso'})
    else:
        return jsonify({'ok': False, 'message': 'Transação não foi adicionada com sucesso, falta dados'})

@app.route('/api/v1/transaction/update', methods=['PUT'])
def update_transaction():
    _json_dados = request.json
    _id = _json_dados['_id']
    _data = _json_dados['Data']
    _hora = _json_dados['Hora']
    _ctnini = _json_dados['ContaInicial']
    _ctnfin = _json_dados['ContaFinal']
    _valor = _json_dados['Valor']
    if _data and _hora and _ctnfin and _ctnini and _valor and request.method == "POST":
        mongo.db.transaction.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {
                "Data": _data,
                "Hora": _hora,
                "ContaInicial": _ctnini,
                "ContaFinal": _ctnfin,
                "Valor": _valor
            }
        )
        return jsonify({'ok': True, 'message': 'Transação alterada com sucesso'})
    else:
        return jsonify({'ok': False, 'message': 'Transação não foi alterada com sucesso'})

@app.route('/api/v1/transaction/delete', methods=['DELETE'])
def delete_transaction():
    _json_dados = request.json
    _id = _json_dados['id']
    mongo.db.transaction.delete_one({'_id': ObjectId(_id)})
    return jsonify({'ok': True, 'message': 'Transação deletada com sucesso'})
