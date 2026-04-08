from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime
import random
import threading
import time
import os

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Кэш для цен криптовалют
crypto_prices_cache = {}
last_update = None
UPDATE_INTERVAL = 30  # секунд

# Список отслеживаемых криптовалют
TRACKED_CRYPTOS = [
    {"symbol": "BTC", "name": "Bitcoin"},
    {"symbol": "ETH", "name": "Ethereum"},
    {"symbol": "BNB", "name": "Binance Coin"},
    {"symbol": "SOL", "name": "Solana"},
    {"symbol": "XRP", "name": "Ripple"},
    {"symbol": "ADA", "name": "Cardano"},
    {"symbol": "DOGE", "name": "Dogecoin"},
    {"symbol": "AVAX", "name": "Avalanche"}
]

def fetch_crypto_prices():
    """Получение цен с CoinGecko API"""
    global crypto_prices_cache, last_update
    try:
        symbols = ",".join([c["symbol"].lower() for c in TRACKED_CRYPTOS])
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbols}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        
        # Маппинг символов на ID CoinGecko
        id_map = {
            "btc": "bitcoin",
            "eth": "ethereum",
            "bnb": "binancecoin",
            "sol": "solana",
            "xrp": "ripple",
            "ada": "cardano",
            "doge": "dogecoin",
            "avax": "avalanche-2"
        }
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for crypto in TRACKED_CRYPTOS:
                cg_id = id_map.get(crypto["symbol"].lower())
                if cg_id and cg_id in data:
                    crypto_prices_cache[crypto["symbol"]] = {
                        "name": crypto["name"],
                        "symbol": crypto["symbol"],
                        "price": data[cg_id]["usd"],
                        "change_24h": data[cg_id].get("usd_24h_change", 0),
                        "volume_24h": data[cg_id].get("usd_24h_vol", 0)
                    }
            last_update = datetime.now()
        else:
            # Fallback - демо данные при ошибке API
            generate_demo_prices()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        generate_demo_prices()

def generate_demo_prices():
    """Генерация демо-данных при ошибке API"""
    global crypto_prices_cache, last_update
    base_prices = {
        "BTC": 65000, "ETH": 3500, "BNB": 580, "SOL": 140,
        "XRP": 0.55, "ADA": 0.65, "DOGE": 0.15, "AVAX": 35
    }
    
    for crypto in TRACKED_CRYPTOS:
        base = base_prices.get(crypto["symbol"], 100)
        variation = random.uniform(-0.05, 0.05)
        price = base * (1 + variation)
        
        crypto_prices_cache[crypto["symbol"]] = {
            "name": crypto["name"],
            "symbol": crypto["symbol"],
            "price": round(price, 2),
            "change_24h": round(random.uniform(-5, 5), 2),
            "volume_24h": round(random.uniform(1000000, 100000000), 0)
        }
    last_update = datetime.now()

def update_prices_periodically():
    """Периодическое обновление цен"""
    while True:
        fetch_crypto_prices()
        time.sleep(UPDATE_INTERVAL)

# Запуск фонового потока для обновления цен
update_thread = threading.Thread(target=update_prices_periodically, daemon=True)
update_thread.start()

# ========== НОВОСТИ БЛОГА ==========
def get_blog_news():
    """Генерация новостей блога в хронологическом порядке 2024 года"""
    return [
        {
            "id": 1,
            "title": "Строим свою ракету. Приглашаем первых соратников.",
            "content": "Мы с моим товарищем - обычные парни, без «олимпиадных» дипломов и московских родственников. У столичных ребят есть всё: хорошие вузы, связи, бюджеты. У нас — только желание и скорость.<br><br>Поэтому мы запускаем частный проект по работе с криптовалютным рынком. Никаких обещаний золотых гор. Будем разбираться, учиться читать графики, тестировать стратегии на малых суммах, фиксировать ошибки.<br><br>Сейчас мы формируем закрытый канал в Telegram для тех, кто тоже хочет пробовать, но не знает, с чего начать. Без «инфоцыган» — только обмен опытом и сделки за свой счёт. Каждый входит на свои средства.<br><br>Если надоело просто смотреть, как другие «поднимаются» — напишите. Сделаем ракету сами.<br><br>📞 Телефон / WhatsApp: 8(914)617-88-91",
            "date": "2024-09-01",
            "author": "Основатель проекта",
            "tags": ["Старт", "Набор", "Честность"]
        },
        {
            "id": 2,
            "title": "Информация для тех, с кем у нас есть действующие займы по распискам",
            "content": "Друзья, честно отчитываемся: несколько сделок, на которые мы привлекали средства по договорам займа, завершились убытком. Мы не смогли вовремя закрыть позиции.<br><br>Мы признаём обязательства по всем распискам. Часть средств уже вернули, по оставшимся — просим связаться с нами для утверждения нового графика возврата (с учётом нашей текущей платёжеспособности).<br><br>Если у вас есть основания требовать возврат — пишите, звоните 8(914)617-88-91. Мы не скрываемся, отвечаем на каждый запрос.<br><br>Важно: новые займы или инвестиции мы не привлекаем до полного погашения текущих обязательств.",
            "date": "2024-10-28",
            "author": "Команда проекта",
            "tags": ["Отчетность", "Обязательства", "Возврат"]
        },
        {
            "id": 3,
            "title": "Изменение в управлении проектом. Закрытие.",
            "content": "Я прекращаю участие в проекте с сегодняшнего дня.<br><br>По всем финансовым обязательствам, возникшим по моей инициативе (расписки, переводы, устные договорённости):<br><br>я остаюсь ответственным;<br>все обязательства действительны до полного погашения;<br>я не снимаю с себя ответственности за возврат средств.<br><br>По остальным обязательствам ответственен Артем.<br><br>Для сверки долгов и утверждения графика платежей:<br><br>по долгам, взятым Артемом: +7 (914) 617-88-91<br>по долгам, взятым мной: +7 (914) 595-44-16<br><br>Если вы не знаете, кому именно переводили деньги, — пишите мне. Я помогу идентифицировать получателя и подтвержу обязательство.<br><br>Новых привлечений средств не ведётся. Проект закрывается в текущем виде.",
            "date": "2024-11-20",
            "author": "Основатель",
            "tags": ["Закрытие", "Ликвидация", "Ответственность"]
        }
    ]

@app.route('/')
def index():
    """Главная страница - отдает index.html из корня"""
    return send_from_directory('.', 'index.html')

@app.route('/api/prices')
def get_prices():
    """API эндпоинт для получения текущих цен"""
    return jsonify({
        "prices": crypto_prices_cache,
        "last_update": last_update.isoformat() if last_update else None
    })

@app.route('/api/news')
def get_news():
    """API эндпоинт для получения новостей"""
    return jsonify(get_blog_news())

if __name__ == '__main__':
    # Начальная загрузка цен
    fetch_crypto_prices()
    print("Сервер запущен: http://localhost:5000")
    app.run(debug=True, port=5000)