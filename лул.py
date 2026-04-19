import os

# Данные для вписывания (на основе твоего файла)
parks_data = [
    {"name": "Ботанический сад", "address": "просп. Кабанбай батыра", "rating": 4.8, "reviews": 14200},
    {"name": "Президентский парк", "address": "ул. Байтурсынова", "rating": 4.8, "reviews": 5600},
    {"name": "Парк Жетісу", "address": "ул. Сарайшык", "rating": 4.7, "reviews": 3100},
    {"name": "Триатлон Парк Астана", "address": "трасса Астана-Караганда", "rating": 4.8, "reviews": 2800},
    {"name": "Парк им. Бауыржана Момышулы", "address": "просп. Б. Момышулы", "rating": 4.6, "reviews": 1900},
    {"name": "Парк Ғашықтар (Влюбленных)", "address": "просп. Туран", "rating": 4.5, "reviews": 4200},
    {"name": "Корейский сад", "address": "внутри парка Жетісу", "rating": 4.8, "reviews": 850},
    {"name": "Парк Жерұйық", "address": "ул. Магжана Жумабаева", "rating": 4.6, "reviews": 1200},
    {"name": "Парк Ататүрік", "address": "ул. Ташенова", "rating": 4.5, "reviews": 900},
]

html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ParkCheck Astana - Тестовая панель</title>
    <style>
        :root {{
            --primary: #2ecc71;
            --dark: #2c3e50;
            --light: #f8f9fa;
            --glass: rgba(255, 255, 255, 0.9);
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e0eafc, #cfdef3);
            margin: 0;
            padding: 20px;
            color: var(--dark);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        h1 {{
            color: var(--dark);
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .search-box {{
            width: 100%;
            padding: 15px 25px;
            font-size: 18px;
            border: none;
            border-radius: 50px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            outline: none;
            transition: 0.3s;
            background: var(--glass);
        }}

        .search-box:focus {{
            box-shadow: 0 10px 30px rgba(46, 204, 113, 0.3);
            transform: translateY(-2px);
        }}

        .park-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .park-card {{
            background: var(--glass);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.05);
            transition: 0.3s;
            border: 1px solid rgba(255,255,255,0.3);
            display: block;
        }}

        .park-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0,0,0,0.1);
        }}

        .park-name {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 8px;
            color: #27ae60;
        }}

        .park-address {{
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-bottom: 15px;
        }}

        .stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}

        .rating {{
            background: #f1c40f;
            color: white;
            padding: 2px 10px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.9rem;
        }}

        .reviews {{
            font-size: 0.8rem;
            color: #95a5a6;
        }}

        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>🌳 Оценка локации: Парки Астаны</h1>
        <p>Тестовый интерфейс для фильтрации объектов</p>
        <input type="text" id="search" class="search-box" placeholder="Начните вводить название парка...">
    </header>

    <div class="park-grid" id="parkGrid">
        {"".join([f'''
        <div class="park-card" data-name="{p['name'].lower()}">
            <div class="park-name">{p['name']}</div>
            <div class="park-address">📍 {p['address']}</div>
            <div class="stats">
                <span class="rating">⭐ {p['rating']}</span>
                <span class="reviews">{p['reviews']} отзывов</span>
            </div>
        </div>
        ''' for p in parks_data])}
    </div>
</div>

<script>
    const searchInput = document.getElementById('search');
    const parkCards = document.querySelectorAll('.park-card');

    searchInput.addEventListener('input', (e) => {{
        const value = e.target.value.toLowerCase();

        parkCards.forEach(card => {{
            const name = card.getAttribute('data-name');
            if (name.includes(value)) {{
                card.classList.remove('hidden');
            }} else {{
                card.classList.add('hidden');
            }}
        }});
    }});
</script>

</body>
</html>
"""

with open("astana_parks_test.html", "w", encoding="utf-8") as f:
    f.write(html_content)
