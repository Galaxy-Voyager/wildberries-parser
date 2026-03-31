import requests
from config import COOKIES, HEADERS

# Кэш для таблицы basket
_BASKET_TABLE = None


def get_basket_table():
    """Загружает актуальную таблицу basket из API Wildberries"""
    global _BASKET_TABLE
    if _BASKET_TABLE is not None:
        return _BASKET_TABLE

    url = "https://cdn.wbbasket.ru/api/v3/upstreams"
    response = requests.get(url, timeout=5)
    data = response.json()

    table = []
    for route in data.get("recommend", {}).get("mediabasket_route_map", []):
        for host_info in route.get("hosts", []):
            table.append({
                "from": host_info.get("vol_range_from", 0),
                "to": host_info.get("vol_range_to", 0),
                "host": host_info.get("host", "")
            })

    _BASKET_TABLE = sorted(table, key=lambda x: x["from"])
    return _BASKET_TABLE


def get_basket_by_vol(vol):
    """Определяет basket по значению vol"""
    table = get_basket_table()
    for entry in table:
        if entry["from"] <= vol <= entry["to"]:
            return entry["host"]
    return "basket-28.wbbasket.ru"


def get_product_card(nm_id):
    """Получение карточки товара"""
    vol = nm_id // 100000
    part = nm_id // 1000
    basket_host = get_basket_by_vol(vol)

    url = f"https://{basket_host}/vol{vol}/part{part}/{nm_id}/info/ru/card.json"

    try:
        response = requests.get(url, headers={'User-Agent': HEADERS['user-agent']}, timeout=10)
        if response.status_code == 200:
            return response.json(), basket_host
    except:
        pass

    return None, None


def get_product_stocks(nm_id):
    """Получение остатков через API cards/detail"""
    url = "https://www.wildberries.ru/__internal/u-card/cards/v4/detail"

    params = {
        "appType": 1,
        "curr": "rub",
        "dest": "-1257786",
        "spp": 30,
        "hide_vflags": "4294967296",
        "ab_testing": "false",
        "lang": "ru",
        "nm": nm_id
    }

    try:
        response = requests.get(url, params=params, cookies=COOKIES, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            if products:
                total = 0
                for size in products[0].get("sizes", []):
                    for stock in size.get("stocks", []):
                        total += stock.get("qty", 0)
                return total
    except:
        pass

    return 0


def get_image_urls(nm_id, basket_host, count=5):
    """Формирование ссылки на изображения товара"""
    vol = nm_id // 100000
    part = nm_id // 1000

    images = [f"https://{basket_host}/vol{vol}/part{part}/{nm_id}/images/big/{i}.webp" for i in range(1, count + 1)]
    return ", ".join(images)
