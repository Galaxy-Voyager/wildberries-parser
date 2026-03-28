import requests


def search_products(query="пальто из натуральной шерсти"):

    cookies = {
        'x_wbaas_token': '1.1000.5f0287a7d9de484dbbd47242870533a5.MTV8MmEwOTpiYWM1OjUwNjk6Mjk2OTo6NDIwOjcyfE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDYuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzc1NzU5MTcxfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3NTE1NDM3MXwx.MEUCIHiRdEKt5XapIAVwZ5Dif8h9X20ikqV0H+h1K1nrtIVmAiEArGDO9MIVgC/Bmae/pA8irUSkBq5vePsUxMJR7bcvJO0=',
        '_wbauid': '9639875131774549576',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.wildberries.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

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
        cookies=cookies,
        headers=headers,
    )

    print(f"Статус: {response.status_code}")

    if response.status_code != 200:
        print(f"Ошибка: статус {response.status_code}")
        return []

    data = response.json()
    products = data.get("products", [])

    print(f"Найдено товаров: {len(products)}")
    return products
