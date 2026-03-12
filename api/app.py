import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# --- CONFIGURAÇÃO DE CAMINHOS PARA VERCEL ---
# Isso resolve o erro 500 ao localizar a pasta templates na raiz
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
CORS(app)

# --- SEU BANCO DE DADOS ---
NIVEIS_INFO = {
    0: {
        "nome": "Nível 1: Potências Simples",
        "materia": "Aqui focamos na regra fundamental: ∫ x^n dx = (x^(n+1))/(n+1).",
        "dica_estudo": "DICA: Olhe para o expoente da função. O resultado sempre terá um expoente a mais e será dividido por esse novo valor!"
    },
    1: {
        "nome": "Nível 2: Potências Maiores",
        "materia": "A regra da potência continua a mesma, mas os denominadores crescem!",
        "dica_estudo": "DICA: Não se assuste com frações. Se a função é x^4, procure pela carta que divide por 5."
    },
    2: {
        "nome": "Nível 3: Trigonométricas (Seno)",
        "materia": "Introdução às funções circulares. A integração exige atenção aos sinais.",
        "dica_estudo": "DICA: Lembre-se que integrar é o oposto de derivar. Se a derivada do cosseno é -seno, a integral do seno deve devolver o sinal negativo!"
    },
    3: {
        "nome": "Nível 4: Trigonométricas (Cosseno)",
        "materia": "Diferenciando a integral do seno da integral do cosseno.",
        "dica_estudo": "DICA: A integral do cosseno é o seno positivo. É o par mais 'limpo' da trigonometria básica."
    }
}

CARDS_DB = {
    "p1": {"display": "x^2", "type": "function", "match": "p1_res", "chips": 10},
    "p1_res": {"display": "(x^3)/3", "type": "result", "chips": 20},
    "p2": {"display": "x^4", "type": "function", "match": "p2_res", "chips": 15},
    "p2_res": {"display": "(x^5)/5", "type": "result", "chips": 25},
    "t1": {"display": "sen(x)", "type": "function", "match": "t1_res", "chips": 20},
    "t1_res": {"display": "-cos(x)", "type": "result", "chips": 30},
    "t2": {"display": "cos(x)", "type": "function", "match": "t2_res", "chips": 20},
    "t2_res": {"display": "sen(x)", "type": "result", "chips": 30},
    "c1": {"display": "+C", "type": "modifier", "mult_bonus": 2}
}

BOSSES = {
    2: {"q": "Qual a integral de 4x^3?", "opts": [{"t": "x^4 + C", "c": True}, {"t": "4x^4 + C", "c": False}, {"t": "12x^2 + C", "c": False}]},
    4: {"q": "Resolva: integral de 2.sen(x)", "opts": [{"t": "-2.cos(x) + C", "c": True}, {"t": "2.cos(x) + C", "c": False}, {"t": "-cos(x) + C", "c": False}]}
}

game_state = {"level": 0, "score": 0, "hands": 4, "hints": 10, "jokers": []}

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    lvl = min(game_state["level"], len(NIVEIS_INFO)-1)
    return jsonify({
        "state": game_state,
        "info": NIVEIS_INFO.get(lvl),
        "cards": CARDS_DB,
        "boss": BOSSES.get(game_state["level"] + 1)
    })

@app.route('/validate', methods=['POST'])
def validate():
    global game_state
    data = request.json
    selected = data.get('ids', [])
    chips, mult = 0, 1
    for cid in selected:
        c = CARDS_DB.get(cid)
        if c and c.get('type') == 'function' and c['match'] in selected:
            chips += c['chips'] + CARDS_DB[c['match']]['chips']
        if c and c.get('type') == 'modifier': mult += c['mult_bonus']

    game_state["score"] += (chips * mult)
    game_state["hands"] -= 1

    status = "CONTINUE"
    target = 100 + (game_state["level"] * 50)
    if game_state["score"] >= target:
        status = "BOSS_TIME" if (game_state["level"] + 1) % 2 == 0 else "NEXT_LEVEL"
        if status == "NEXT_LEVEL": game_state["level"] += 1; game_state["score"] = 0; game_state["hands"] = 4
    elif game_state["hands"] <= 0: status = "GAME_OVER"
    return jsonify({"state": game_state, "status": status, "target": target})

@app.route('/use_hint', methods=['POST'])
def use_hint():
    global game_state
    if game_state["hints"] > 0:
        game_state["hints"] -= 1
        lvl = min(game_state["level"], len(NIVEIS_INFO)-1)
        return jsonify({"success": True, "tip": NIVEIS_INFO[lvl]["dica_estudo"], "remaining": game_state["hints"]})
    return jsonify({"success": False, "msg": "Acabaram suas dicas!"})

@app.route('/solve_boss', methods=['POST'])
def solve_boss():
    global game_state
    if request.json.get('correct'):
        game_state["level"] += 1; game_state["score"] = 0; game_state["hands"] = 4
        return jsonify({"success": True})
    game_state = {"level": 0, "score": 0, "hands": 4, "hints": 10, "jokers": []}
    return jsonify({"success": False})

# Importante para a Vercel reconhecer o objeto 'app'
if __name__ == '__main__':
    app.run(debug=True)