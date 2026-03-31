import requests
from config import COOKIES, HEADERS


def search_products(query="пальто из натуральной шерсти"):
    params = {
        'ab_testid': 'pmb_01',
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'hide_vflags': '4294967296',
        'inheritFilters': 'false',
        'lang': 'ru',
        'query': query,
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': '30',
        'suppressSpellcheck': 'false',
    }

    response = requests.get(
        'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search',
        params=params,
        cookies=COOKIES,
        headers=HEADERS,
    )

    print(f"Статус: {response.status_code}")

    if response.status_code != 200:
        print(f"Ошибка: статус {response.status_code}")
        return []

    data = response.json()
    products = data.get("products", [])

    print(f"Найдено товаров: {len(products)}")
    return products
