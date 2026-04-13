# 🚀 INTEGRAL-TRO: The Balatro Edition
### *A Roguelike Deck-Builder for Mastering Calculus II*

**INTEGRAL-TRO** is an educational strategy game inspired by the hit roguelike *Balatro*. Developed as a final project for Computer Science, it gamifies the complexities of **Calculus II**—specifically integration techniques—by combining academic rigor with deep resource management.

## 🎯 Project Overview
Most educational tools are simple quizzes. **INTEGRAL-TRO** is a full-scale game engine. It challenges students to not only solve integrals but to manage a complex system of **Jokers** and **Tarots** to manipulate score multipliers. It turns a "math problem" into a "strategic decision-making" challenge.

## 🛠️ Technical Stack
* **Backend:** Python 3.x / **Flask**
    * Dynamic question sampling and level-based filtering.
    * API-driven shop logic with randomized item pools.
* **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3
    * Custom-built game engine for state management.
    * CRT/Scanline retro-future aesthetic.
    * Distributed logic: The server acts as the "Source of Truth," while the client handles the real-time scoring engine.

## 🃏 Core Game Mechanics

### 1. The Scoring Equation
The game uses a "Chips vs. Mult" system. To beat a round, your score must exceed the Boss Target:

$$Score = (Base Points + Chip Bonuses) \times (Base Mult \times Joker Multipliers)$$

### 2. Strategic Layers
* **Jokers (50 Unique Cards):** Permanent passive buffs that stay with you across rounds.
    * *Example:* **"Gauss's Theorem"** – Grants a massive x3 Mult, but a single wrong answer results in an immediate **Game Over**.
* **Tarots (50 Unique Consumables):** Manual-use items stored in a **3-slot inventory**.
    * *Example:* **"Professor's Folder"** – Reveals the correct answer but reduces your remaining "hands" to one.
* **The "+C" Rule:** A tribute to the most common student mistake. Forgetting to toggle the **[+C]** button results in a **50% score penalty**.

## 📈 Academic Curriculum
The question bank (50+ problems) covers the essential syllabus of Calculus II:
1.  **Levels 1-3:** Power Rule and Immediate Integrals.
2.  **Levels 4-6:** $u$-Substitution and Trigonometric Identities.
3.  **Levels 7-8:** Integration by Parts ($udv$).
4.  **Levels 9-10:** Partial Fractions and Advanced Trig Substitution.

## 👩‍💻 Development Context
This project was developed at **CESUPA** (Centro Universitário do Estado do Pará) as an innovative tool for engineering students. It features 10 difficulty tiers with "Bosses" named after real faculty members, culminating in the final challenge against **Professor Alessandra**.

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/integral-tro.git](https://github.com/your-username/integral-tro.git)
    cd integral-tro
    ```
2.  **Install Dependencies**
    ```bash
    pip install flask
    ```
3.  **Run the Server**
    ```bash
    python app.py
    ```
4.  **Play**
    Navigate to `http://localhost:5000` in your preferred browser.


### 📄 License
This project is for educational purposes. Feel free to fork and adapt it for other subjects like Physics or Statistics!
