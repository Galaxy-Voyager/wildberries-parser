import pandas as pd
import time
from search_products import search_products
from get_card_details import get_product_card, get_image_urls


def parse_wildberries(query="пальто из натуральной шерсти"):
    """
    Собирает данные о товарах и сохраняет в excel
    """

    print("=" * 50)
    print("Парсер Wildberries")
    print("=" * 50)
    print(f"Поисковый запрос: {query}")
    print()

    products = search_products(query)

    if not products:
        print("Товары не найдены")
        return

    # Ограничение до 10 товаров
    products = products[:10]
    print(f"Обработка первых {len(products)} товаров")
    print()

    time.sleep(2)

    print("Сбор информации...")
    print("-" * 50)

    items = []

    for idx, product in enumerate(products, 1):
        print(f"[{idx}/{len(products)}] Обработка товара...")

        # --- Данные из поиска ---

        # Цена
        price = product.get("sizes", [{}])[0].get("price", {}).get("product", 0) / 100

        # Размеры
        sizes_list = []
        total_quantity = 0
        for size in product.get("sizes", []):
            size_name = size.get("name")
            if size_name:
                sizes_list.append(size_name)
            total_quantity += size.get("totalQuantity", 0)
        sizes_str = ", ".join(sizes_list) if sizes_list else ""

        # Ссылка на товар
        product_link = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"

        # Селлер
        supplier_id = product.get("supplierId")
        seller_link = f"https://www.wildberries.ru/seller/{supplier_id}" if supplier_id else ""
        seller_name = product.get("supplier", product.get("brand", ""))

        # --- Данные из карточки ---

        card_data = get_product_card(nm_id)

        description = ""
        characteristics = ""

        if card_data:
            description = card_data.get("description", "")
            options = card_data.get("options", [])
            if options:
                characteristics = "; ".join([f"{o.get('name')}: {o.get('value')}" for o in options])

        # Изображения
        images_str = get_image_urls(nm_id)

        # --- Формирование записи ---

        item = {
            "Ссылка на товар": product_link,
            "Артикул": nm_id,
            "Название": product.get("name", ""),
            "Цена": price,
            "Описание": description,
            "Ссылки на изображения": images_str,
            "Характеристики": characteristics,
            "Название селлера": seller_name,
            "Ссылка на селлера": seller_link,
            "Размеры": sizes_str,
            "Остатки": total_quantity,
            "Рейтинг": product.get("rating", 0),
            "Количество отзывов": product.get("feedbacks", 0)
        }

        items.append(item)


    # Сохранение результатов
    print()
    print("Сохранение результатов...")
    print("-" * 50)

    df = pd.DataFrame(items)
    df.to_excel("catalog.xlsx", index=False)
    print(f"Сохранено {len(items)} товаров в catalog.xlsx")

    print()
    print("Готово!")


if __name__ == "__main__":
    parse_wildberries(query="пальто из натуральной шерсти")
