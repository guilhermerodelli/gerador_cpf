from flask import Flask, jsonify, request
import random
import re
import numpy as np

app = Flask(__name__)


@app.route('/cpf', methods=['GET'])
def obter_cpf():
    tamanho = request.args.get('tamanho')
    if tamanho:
        try:
            tamanho = int(tamanho)
            if tamanho < 1:
                return jsonify({"error": "O tamanho deve ser um número inteiro positivo"}), 400
            cpf_gerado = ''.join(random.choices('0123456789', k=tamanho))
        except ValueError:
            return jsonify({"error": "O tamanho deve ser um número inteiro positivo"}), 400
    else:
        cpf_gerado = gerador()
    return jsonify({"cpf": cpf_gerado})


@app.route('/cpf', methods=['POST'])
def verificar_cpf():
    data = request.get_json()
    cpf = data.get('cpf')

    if not cpf:
        return jsonify({"error": "CPF não fornecido"}), 400
    
    valido = validar(cpf)

    return jsonify({"cpf": cpf, "valido": bool(valido)})

def gerador():
    def calcular_digito(cpf_parcial):
        soma = 0
        peso = len(cpf_parcial) + 1
        for digito in cpf_parcial:
            soma += int(digito) * peso
            peso -= 1
        digito = 11 - (soma % 11)
        return digito if digito < 10 else 0

    cpf = [random.randint(0, 9) for _ in range(9)]
    digito1 = calcular_digito(cpf)
    cpf.append(digito1)
    digito2 = calcular_digito(cpf)
    cpf.append(digito2)

    return '{}{}{}.{}{}{}.{}{}{}-{}{}'.format(*cpf)

def validar(cpf: str):
   cpf_gerado = re.sub("[^0-9]", "", cpf)
   cpf_numero = np.array([int(i) for i in cpf_gerado])
   numeros_10_a_2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2])
   numeros_11_a_2 = np.array([11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
   primeiro_digito_valido = sum(cpf_numero[0:9] * 10* numeros_10_a_2) % 11
   segundo_digito_valido = sum(cpf_numero[0:10] * 10* numeros_11_a_2) % 11
   return cpf_numero[9] == primeiro_digito_valido and cpf_numero[10] == segundo_digito_valido
    

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)