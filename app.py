from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Banco de dados de questões (Níveis 1 a 10)
QUESTIONS = [
    {"q": "∫ x dx", "options": ["x²/2", "x", "x²", "1"], "ans": "x²/2", "level": 1},
    {"q": "∫ sin(x) dx", "options": ["-cos(x)", "cos(x)", "sec(x)", "tan(x)"], "ans": "-cos(x)", "level": 2},
    {"q": "∫ eˣ dx", "options": ["eˣ", "xeˣ", "eˣ⁺¹", "ln(x)"], "ans": "eˣ", "level": 3},
    {"q": "∫ 1/x dx", "options": ["ln|x|", "-1/x²", "eˣ", "x"], "ans": "ln|x|", "level": 4},
    {"q": "∫ cos(x) dx", "options": ["sin(x)", "-sin(x)", "cos²(x)", "1"], "ans": "sin(x)", "level": 5},
    {"q": "∫ sec²(x) dx", "options": ["tan(x)", "sec(x)", "cot(x)", "sin(x)"], "ans": "tan(x)", "level": 6},
    {"q": "∫ 2x dx", "options": ["x²", "2", "x²/2", "2x²"], "ans": "x²", "level": 7},
    {"q": "∫ 1/(1+x²) dx", "options": ["arctan(x)", "arcsin(x)", "ln(x²)", "tan(x)"], "ans": "arctan(x)", "level": 8},
    {"q": "∫ ln(x) dx", "options": ["x ln(x) - x", "1/x", "x ln(x)", "eˣ"], "ans": "x ln(x) - x", "level": 9},
    {"q": "∫ x eˣ dx", "options": ["(x-1)eˣ", "xeˣ", "eˣ", "x²eˣ"], "ans": "(x-1)eˣ", "level": 10}
]

BOSSES = {2: "Girotto", 4: "Casseb", 6: "Daniel", 8: "Isaac", 10: "ALESSANDRA"}

# Adicione isso logo acima da rota @app.route('/')
JOKERS_DB = [
    {"id": 1, "name": "Calc. Quebrada", "desc": "Mult x2, mas Mãos -1.", "mult": 2.0, "type": "hand_penalty", "price": 6},
    {"id": 2, "name": "Teorema de Gauss", "desc": "Mult x3, mas Erro = MORTE.", "mult": 3.0, "type": "death_risk", "price": 10},
    {"id": 3, "name": "Regra da Cadeia", "desc": "Mult x1.5 para cada acerto.", "mult": 1.5, "type": "chain", "price": 8},
    {"id": 4, "name": "Série Divergente", "desc": "Mult x4, mas Alvo sobe 50%.", "mult": 4.0, "type": "target_up", "price": 9},
    {"id": 5, "name": "Monitor Amigo", "desc": "Ignora +C, mas ganha 0.5x.", "type": "no_c_req", "price": 8},
    {"id": 6, "name": "Café do C.A.", "desc": "+500 Pts, mas +C vale 0.25x.", "bonus": 500, "type": "c_nerf", "price": 4},
    {"id": 7, "name": "Tabela do Girotto", "desc": "+300 Pts fixos por acerto.", "bonus": 300, "type": "flat_bonus", "price": 5},
    {"id": 8, "name": "Integral de Polinômio", "desc": "+100 Pts por cada 'x' na tela.", "type": "x_bonus", "price": 4},
    {"id": 9, "name": "Área sob a Curva", "desc": "+1000 Pts em Integral Definida.", "type": "def_bonus", "price": 7},
    {"id": 10, "name": "Substituição em U", "desc": "+2 Mãos extras agora.", "type": "instant_hands", "price": 5},
    {"id": 11, "name": "Constante K", "desc": "Sempre considera que o +C está ativo.", "type": "auto_c", "price": 11},
    {"id": 12, "name": "Bolsa FAPESPA", "desc": "Ganha $3 extra por vitória.", "type": "money_buff", "price": 6},
    {"id": 13, "name": "Dependência Química", "desc": "Ganha $15 agora, perde 300 pts/round.", "type": "debt", "price": 0},
    {"id": 14, "name": "O Corretor", "desc": "Itens na loja ficam 50% mais baratos.", "type": "sale", "price": 5},
    {"id": 15, "name": "Derivada Inversa", "desc": "Se errar, não perde mão (50% chance).", "type": "save_chance", "price": 7},
    {"id": 16, "name": "Teorema Fundamental", "desc": "Dobra o score se acertar em < 5 seg.", "type": "speedrun", "price": 9},
    {"id": 17, "name": "Frações Parciais", "desc": "Divide o Alvo do Boss por 2.", "type": "easy_boss", "price": 12},
    {"id": 18, "name": "Limite Fundamental", "desc": "Sempre ganha ao menos 100 pontos.", "type": "pity_points", "price": 5},
    {"id": 19, "name": "Munguba Tech", "desc": "Soma o nível atual ao Multiplicador.", "type": "lvl_scale", "price": 8},
    {"id": 20, "name": "Alessandra's Blessing", "desc": "Dobra todos os bônus de outros Jokers.", "type": "synergy", "price": 15}
]

@app.route('/get_jokers')
def get_jokers():
    # Retorna 2 coringas aleatórios para a "loja" entre níveis
    return jsonify(random.sample(JOKERS_POOL, 2))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_level/<int:lvl>')
def get_level(lvl):
    question = QUESTIONS[lvl-1]
    boss = BOSSES.get(lvl, "Monitor")
    # Simula a "mão" do Balatro: a resposta certa + 3 erradas embaralhadas
    options = question['options']
    random.shuffle(options)
    return jsonify({
        "question": question['q'],
        "options": options,
        "boss": boss,
        "target_score": lvl * 500
    })

if __name__ == '__main__':
    app.run(debug=True)