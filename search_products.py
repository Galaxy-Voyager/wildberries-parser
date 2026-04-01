import requests
import time
from config import COOKIES, HEADERS


def search_products(query="пальто из натуральной шерсти", max_pages=None):
    """
    Поиск всех товаров по запросу
    max_pages: ограничение на количество страниц (None = все страницы)
    """
    all_products = []
    page = 1

    while True:
        params = {
            'ab_testid': 'pmb_01',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'hide_vflags': '4294967296',
            'inheritFilters': 'false',
            'lang': 'ru',
            'page': str(page),
            'query': query,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '100',
            'suppressSpellcheck': 'false',
        }

        print(f"  Загрузка страницы {page}...", end=" ")

        response = requests.get(
            'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search',
            params=params,
            cookies=COOKIES,
            headers=HEADERS,
        )

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break

        data = response.json()
        products = data.get("products", [])

        if not products:
            print("товары не найдены")
            break

        print(f"{len(products)} товаров")
        all_products.extend(products)

        if len(products) < 100:
            break

        page += 1

        if max_pages and page > max_pages:
            break

        time.sleep(0.5)

    print(f"\nВсего найдено товаров: {len(all_products)}")
    return all_products

