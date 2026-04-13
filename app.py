from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Banco de dados de questões (Níveis 1 a 10)
QUESTIONS = [
    # NÍVEL 1-3: IMEDIATAS E POLINÔMIOS
    {"q": "∫ x² dx", "options": ["x³/3", "2x", "x³", "x²/2"], "ans": "x³/3", "level": 1},
    {"q": "∫ 5 dx", "options": ["5x", "5", "0", "x⁵"], "ans": "5x", "level": 1},
    {"q": "∫ (x³ + 2x) dx", "options": ["x⁴/4 + x²", "3x² + 2", "x⁴ + x²", "x³/4 + x"], "ans": "x⁴/4 + x²", "level": 1},
    {"q": "∫ sec²(x) dx", "options": ["tan(x)", "sec(x)", "-tan(x)", "cos(x)"], "ans": "tan(x)", "level": 2},
    {"q": "∫ √x dx", "options": ["(2/3)x^(3/2)", "x^(1/2)", "(1/2)x^(-1/2)", "2√x"], "ans": "(2/3)x^(3/2)", "level": 2},
    {"q": "∫ 1/x² dx", "options": ["-1/x", "1/x", "ln(x²)", "-2/x³"], "ans": "-1/x", "level": 2},
    {"q": "∫ 2x dx", "options": ["x²", "2", "x²/2", "2x²"], "ans": "x²", "level": 3},
    {"q": "∫ cos(x) dx", "options": ["sin(x)", "-sin(x)", "cos²(x)", "1"], "ans": "sin(x)", "level": 3},

    # NÍVEL 4-6: SUBSTITUIÇÃO (u-sub)
    {"q": "∫ e^(5x) dx", "options": ["e^(5x)/5", "5e^(5x)", "e^(5x)", "e⁵/x"], "ans": "e^(5x)/5", "level": 4},
    {"q": "∫ x sin(x²) dx", "options": ["-cos(x²)/2", "cos(x²)/2", "-cos(x)", "sin(x²)/2"], "ans": "-cos(x²)/2", "level": 4},
    {"q": "∫ (ln x / x) dx", "options": ["(ln x)²/2", "ln(ln x)", "1/x²", "ln x"], "ans": "(ln x)²/2", "level": 5},
    {"q": "∫ cos(x) sin³(x) dx", "options": ["sin⁴(x)/4", "cos⁴(x)/4", "sin²(x)/2", "sin⁴(x)"], "ans": "sin⁴(x)/4", "level": 5},
    {"q": "∫ 1/(3x + 2) dx", "options": ["ln|3x+2|/3", "3 ln|3x+2|", "ln|3x+2|", "1/3"], "ans": "ln|3x+2|/3", "level": 6},
    {"q": "∫ x² e^(x³) dx", "options": ["e^(x³)/3", "x³e^x", "e^(x³)", "3e^(x³)"], "ans": "e^(x³)/3", "level": 6},

    # NÍVEL 7-8: INTEGRAÇÃO POR PARTES
    {"q": "∫ x cos(x) dx", "options": ["x sin(x) + cos(x)", "x sin(x) - cos(x)", "-x sin(x)", "cos(x)"], "ans": "x sin(x) + cos(x)", "level": 7},
    {"q": "∫ x eˣ dx", "options": ["(x-1)eˣ", "xeˣ", "eˣ(x+1)", "x²eˣ/2"], "ans": "(x-1)eˣ", "level": 7},
    {"q": "∫ ln(x) dx", "options": ["x ln(x) - x", "1/x", "x ln(x)", "ln²(x)/2"], "ans": "x ln(x) - x", "level": 8},
    {"q": "∫ x² ln(x) dx", "options": ["(x³/3)ln(x) - x³/9", "x² ln(x)", "x³/3", "ln(x)/x"], "ans": "(x³/3)ln(x) - x³/9", "level": 8},

    # NÍVEL 9-10: FRAÇÕES PARCIAIS / TRIGONOMÉTRICA (BOSS)
    {"q": "∫ 1/(x² + 1) dx", "options": ["arctan(x)", "arcsin(x)", "ln(x²+1)", "tan(x)"], "ans": "arctan(x)", "level": 9},
    {"q": "∫ sin²(x) dx", "options": ["x/2 - sin(2x)/4", "cos²(x)", "sin³(x)/3", "x - cos(x)"], "ans": "x/2 - sin(2x)/4", "level": 9},
    {"q": "∫ dx / √(4 - x²)", "options": ["arcsin(x/2)", "arctan(x/2)", "1/2 arcsin(x)", "ln|x|"], "ans": "arcsin(x/2)", "level": 10},
    {"q": "∫ 1/(x(x+1)) dx", "options": ["ln|x/(x+1)|", "ln|x+1| - ln|x|", "arctan(x)", "1/x"], "ans": "ln|x/(x+1)|", "level": 10},
]

BOSSES = {2: "Girotto", 4: "Casseb", 6: "Daniel", 8: "Isaac", 10: "ALESSANDRA"}

# Adicione isso logo acima da rota @app.route('/')
JOKERS_DB = [
    # --- GRUPO 1: OS CLÁSSICOS (1-10) ---
    {"id": 1, "name": "Calc. Quebrada", "desc": "Mult x2, mas Mãos -1.", "mult": 2.0, "type": "hand_penalty", "price": 6},
    {"id": 2, "name": "Teorema de Gauss", "desc": "Mult x3, mas Erro = MORTE.", "mult": 3.0, "type": "death_risk", "price": 10},
    {"id": 3, "name": "Regra da Cadeia", "desc": "Mult x1.5 acumulativo, mas Alvo +10%.", "mult": 1.5, "type": "target_up", "price": 8},
    {"id": 4, "name": "Série Divergente", "desc": "Mult x4, mas Alvo do Boss sobe 50%.", "mult": 4.0, "type": "target_up", "price": 9},
    {"id": 5, "name": "Monitor Amigo", "desc": "Ignora +C, mas Pontos Base x0.5.", "type": "no_c_req", "price": 8},
    {"id": 6, "name": "Café do C.A.", "desc": "+500 Pts, mas +C vale apenas x0.2.", "bonus": 500, "type": "c_nerf", "price": 4},
    {"id": 7, "name": "Tabela do Girotto", "desc": "+300 Pts fixos, mas saca -1 carta.", "bonus": 300, "type": "draw_penalty", "price": 5},
    {"id": 8, "name": "Integral de Polinômio", "desc": "+150 Pts por 'x', mas Mult x0.8.", "type": "x_bonus", "price": 4},
    {"id": 9, "name": "Área sob a Curva", "desc": "+1500 Pts em Definitas, 0 Pts em Indefinitas.", "type": "def_only", "price": 7},
    {"id": 10, "name": "Substituição em U", "desc": "+2 Mãos agora, mas perde $5.", "type": "instant_hands", "price": 5},

    # --- GRUPO 2: VIDA NO CESUPA (11-20) ---
    {"id": 11, "name": "X-Burguer da Esquina", "desc": "Mult x2, mas diminui sua visão das cartas.", "mult": 2.0, "type": "blindness", "price": 5},
    {"id": 12, "name": "Ar-Condicionado no 15", "desc": "Mult x3 se responder em < 10s, senão Mult x0.5.", "type": "timer", "price": 7},
    {"id": 13, "name": "Chuva de Belém", "desc": "Ganha $10, mas embaralha sua mão a cada 5s.", "type": "shuffle", "price": 0},
    {"id": 14, "name": "Trabalho em Grupo", "desc": "Mult x2 se tiver outro Joker, senão Mult x0.5.", "type": "synergy", "price": 6},
    {"id": 15, "name": "Açaí com Peixe", "desc": "Dobra o Score do Round, mas desativa no próximo.", "type": "recharge", "price": 8},
    {"id": 16, "name": "Voucher da Cantina", "desc": "Itens da loja -50%, mas -200 Pts por round.", "type": "sale", "price": 4},
    {"id": 17, "name": "Estacionamento Loteado", "desc": "+1 slot de Joker, mas Alvo do Boss +100%.", "type": "slot_up", "price": 12},
    {"id": 18, "name": "WI-FI do CESUPA", "desc": "50% de chance de Mult x5 ou Mult x0.", "type": "lag", "price": 6},
    {"id": 19, "name": "Biblioteca Silenciosa", "desc": "Mult x2 se não usar descartes.", "type": "no_discard_buff", "price": 7},
    {"id": 20, "name": "Formatura Antecipada", "desc": "Pula o Boss atual, mas reseta seu dinheiro para $0.", "type": "skip", "price": 15},

    # --- GRUPO 3: PURA MATEMÁTICA (21-35) ---
    {"id": 21, "name": "Zero da Alessandra", "desc": "Mult x10, mas Erro = Perde todos os Jokers.", "type": "extreme_risk", "price": 13},
    {"id": 22, "name": "Derivada Parcial", "desc": "Mult x1.5, mas ignora bônus de +C.", "type": "no_c", "price": 5},
    {"id": 23, "name": "Logaritmo Neperiano", "desc": "Diminui o Alvo em 300, mas Mult x0.9.", "type": "target_down", "price": 6},
    {"id": 24, "name": "Seno e Cosseno", "desc": "Mult oscila entre x1 e x4 a cada turno.", "type": "oscillation", "price": 8},
    {"id": 25, "name": "Fatorial de Estresse", "desc": "Mult cresce por nível, mas Mãos caem por nível.", "type": "scaling", "price": 10},
    {"id": 26, "name": "Matriz Identidade", "desc": "Mantém seu Mult do round passado, mas reseta Score.", "type": "carry_over", "price": 9},
    {"id": 27, "name": "Assíntota Vertical", "desc": "Score infinito se acertar 5 vezes, senão 0 Pts.", "type": "infinite_goal", "price": 14},
    {"id": 28, "name": "Frações Parciais", "desc": "Divide o Alvo por 2, mas tira -2 descartes.", "type": "easy_boss", "price": 11},
    {"id": 29, "name": "Constante de Euler", "desc": "Mult x2.71, mas perde $1 por turno.", "mult": 2.71, "type": "drain", "price": 9},
    {"id": 30, "name": "Vetor Gradiente", "desc": "+Score na direção do acerto, mas -Mãos.", "type": "vector", "price": 8},
    {"id": 31, "name": "Integral Tripla", "desc": "Mult x3, mas exige acertar 3 vezes para validar.", "type": "triple", "price": 12},
    {"id": 32, "name": "Cálculo Numérico", "desc": "Sempre dá 80% do Score necessário, nunca 100%.", "type": "approx", "price": 5},
    {"id": 33, "name": "Teorema de Stokes", "desc": "Converte dinheiro em Mult (10 para 1x).", "type": "money_to_mult", "price": 10},
    {"id": 34, "name": "Jacobiano", "desc": "Muda a pergunta se você não gostar, custa $2.", "type": "reroll_q", "price": 6},
    {"id": 35, "name": "Série de Taylor", "desc": "Acertos sucessivos dão +0.5x ao Mult total.", "type": "taylor_scale", "price": 11},

    # --- GRUPO 4: CAOS E META (36-50) ---
    {"id": 36, "name": "DP de Cálculo I", "desc": "Mult x5, mas você volta 1 nível.", "type": "backwards", "price": 9},
    {"id": 37, "name": "Greve Acadêmica", "desc": "Não ganha pontos, mas ganha $5 por turno.", "type": "passive_income", "price": 4},
    {"id": 38, "name": "Sistema fora do Ar", "desc": "Esconde o Alvo do Boss, mas Mult x3.", "type": "blind_bet", "price": 7},
    {"id": 39, "name": "Munguba Tech v2", "desc": "Dobra o efeito do seu primeiro Joker.", "type": "copy_first", "price": 12},
    {"id": 40, "name": "Pasta do Professor", "desc": "Revela a resposta, mas tira -3 mãos.", "type": "cheat", "price": 10},
    {"id": 41, "name": "Café Gelado", "desc": "Mult x1.2 fixo, sem penalidades.", "mult": 1.2, "type": "flat_mult", "price": 3},
    {"id": 42, "name": "PROVA FINAL", "desc": "Mult x10 no último round, mas Mão = 1.", "type": "last_stand", "price": 15},
    {"id": 43, "name": "Cópia do Colega", "desc": "Copia o efeito do Joker à direita.", "type": "mimic", "price": 11},
    {"id": 44, "name": "Lattes do Mal", "desc": "Ganha Mult por cada $5 que você tem.", "type": "rich_mult", "price": 9},
    {"id": 45, "name": "Bolsa Permanência", "desc": "Não pode descer de $10, mas Mult x0.9.", "type": "min_money", "price": 6},
    {"id": 46, "name": "Teorema de Pappus", "desc": "Mult x2 se o resultado tiver frações.", "type": "fraction_buff", "price": 7},
    {"id": 47, "name": "Análise Real", "desc": "O jogo fica em preto e branco, mas Mult x3.", "type": "hard_mode", "price": 8},
    {"id": 48, "name": "Curva de Gauss", "desc": "Mult x4 se seu score estiver na média.", "type": "average_buff", "price": 9},
    {"id": 49, "name": "Algoritmo de Busca", "desc": "Sempre saca a resposta certa, custa $10.", "type": "auto_win", "price": 14},
    {"id": 50, "name": "Alessandra's Mercy", "desc": "Dobra todos os bônus e remove penalidades.", "type": "god_mode", "price": 20}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_level/<int:lvl>')
def get_level(lvl):
    # 1. Filtramos apenas as questões que pertencem ao nível atual
    # Ou, para dar mais variedade, questões de níveis anteriores também:
    possible_questions = [q for q in QUESTIONS if q['level'] == lvl]

    # Caso não existam muitas questões do nível exato, pegamos as "até" aquele nível
    if not possible_questions:
        possible_questions = [q for q in QUESTIONS if q['level'] <= lvl]

    # 2. O PULO DO GATO: Sorteamos uma questão aleatória da lista filtrada
    question = random.choice(possible_questions)

    boss = BOSSES.get(lvl, "Monitor")

    # 3. Embaralhamos as opções para a resposta não ficar sempre na mesma posição
    options = list(question['options'])
    random.shuffle(options)

    return jsonify({
        "question": question['q'],
        "options": options,
        "boss": boss,
        "target_score": lvl * 500,
        "ans": question['ans']
    })

@app.route('/get_shop_items')
def get_shop():
    return jsonify(random.sample(JOKERS_DB, 3))


if __name__ == '__main__':
    app.run(debug=True)