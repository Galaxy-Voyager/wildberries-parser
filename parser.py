import pandas as pd
import time
from search_products import search_products
from get_card_details import get_product_card, get_image_urls, get_product_stocks


def parse_wildberries(query="пальто из натуральной шерсти", max_pages=None):
    """
    Собирает данные о товарах и сохраняет в excel
    max_pages: ограничение на количество страниц (None = все страницы)
    """
    print("=" * 50)
    print("Парсер Wildberries")
    print("=" * 50)
    print(f"Поисковый запрос: {query}\n")

    products = search_products(query, max_pages=max_pages)
    if not products:
        print("Товары не найдены")
        return

    print(f"\nОбработка {len(products)} товаров\n")
    time.sleep(0.5)

    print("Сбор информации...")
    print("-" * 50)

    items = []

    for idx, product in enumerate(products, 1):
        print(f"[{idx}/{len(products)}] Обработка товара...")

        nm_id = product.get("id")
        if not nm_id:
            print("  Артикул не найден")
            continue

        # Данные из поиска
        price = product.get("sizes", [{}])[0].get("price", {}).get("product", 0) / 100

        sizes_list = []
        for size in product.get("sizes", []):
            if size.get("name"):
                sizes_list.append(size.get("name"))
        sizes_str = ", ".join(sizes_list) if sizes_list else ""

        product_link = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
        supplier_id = product.get("supplierId")
        seller_link = f"https://www.wildberries.ru/seller/{supplier_id}" if supplier_id else ""
        seller_name = product.get("supplier", product.get("brand", ""))

        rating = product.get("reviewRating", product.get("rating", 0))
        feedbacks = product.get("feedbacks", 0)

        # Данные из карточки
        card_data, basket = get_product_card(nm_id)

        description = ""
        characteristics = ""
        country = ""
        photo_count = 5

        if card_data:
            description = card_data.get("description", "")
            options = card_data.get("options", [])
            if options:
                characteristics = "; ".join([f"{o.get('name')}: {o.get('value')}" for o in options])
                for opt in options:
                    if opt.get("name") == "Страна производства":
                        country = opt.get("value", "")
                        break
            photo_count = card_data.get("media", {}).get("photo_count", 5)

        # Остатки
        total_quantity = get_product_stocks(nm_id)

        images_str = get_image_urls(nm_id, basket, photo_count) if basket else ""

        items.append({
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
            "Рейтинг": rating,
            "Количество отзывов": feedbacks,
            "Страна производства": country
        })

    print()
    print("Сохранение результатов...")
    print("-" * 50)

    df = pd.DataFrame(items)

    df_full = df.drop(columns=["Страна производства"])
    df_full.to_excel("catalog_full.xlsx", index=False)
    print(f"Сохранено {len(items)} товаров в catalog_full.xlsx")

    filtered_df = df[
        (df["Рейтинг"] >= 4.5) &
        (df["Цена"] <= 10000) &
        (df["Страна производства"].str.contains("Россия", na=False, case=False))
    ]
    filtered_df = filtered_df.drop(columns=["Страна производства"])
    filtered_df.to_excel("catalog_filtered.xlsx", index=False)
    print(f"Сохранено {len(filtered_df)} товаров в catalog_filtered.xlsx")

    print()
    print("Готово!")


if __name__ == "__main__":
    parse_wildberries(query="пальто из натуральной шерсти")
