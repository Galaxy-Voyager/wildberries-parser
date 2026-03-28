import requests


def get_product_card(nm_id):
    """
    Получение детальной карточки товара по артикулу
    """
    nm_str = str(nm_id)
    vol = nm_str[:4]
    part = nm_str[:6]

    url = f"https://basket-28.wbbasket.ru/vol{vol}/part{part}/{nm_id}/info/ru/card.json"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def get_image_urls(nm_id, count=5):
    """
    Формирование ссылки на изображения товара
    """
    nm_str = str(nm_id)
    vol = nm_str[:4]
    part = nm_str[:3]

    images = []
    for i in range(1, count + 1):
        img_url = f"https://basket-01.wb.ru/vol{vol}/part{part}/{nm_id}/images/big/{i}.jpg"
        images.append(img_url)

    return ", ".join(images)
