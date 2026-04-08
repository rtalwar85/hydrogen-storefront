import csv
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / 'public' / 'generated-shopify-products'
CSV_PATH = ROOT / 'generated-shopify-products.csv'

HEADERS = [
    'Title','URL handle','Description','Vendor','Product category','Type','Tags',
    'Published on online store','Status','SKU','Barcode','Option1 name','Option1 value',
    'Option1 Linked To','Option2 name','Option2 value','Option2 Linked To','Option3 name',
    'Option3 value','Option3 Linked To','Price','Compare-at price','Cost per item',
    'Charge tax','Tax code','Unit price total measure','Unit price total measure unit',
    'Unit price base measure','Unit price base measure unit','Inventory tracker',
    'Inventory quantity','Continue selling when out of stock','Weight value (grams)',
    'Weight unit for display','Requires shipping','Fulfillment service','Product image URL',
    'Image position','Image alt text','Variant image URL','Gift card','SEO title',
    'SEO description','Color (product.metafields.shopify.color-pattern)',
    'Google Shopping / Google product category','Google Shopping / Gender',
    'Google Shopping / Age group','Google Shopping / Manufacturer part number (MPN)',
    'Google Shopping / Ad group name','Google Shopping / Ads labels',
    'Google Shopping / Condition','Google Shopping / Custom product',
    'Google Shopping / Custom label 0','Google Shopping / Custom label 1',
    'Google Shopping / Custom label 2','Google Shopping / Custom label 3',
    'Google Shopping / Custom label 4',
]

PRODUCTS = [
    ('Aurora Glass Candle', 'Sage Mist', ['#DCE8DE', '#91A88B', '#F6EFE7']),
    ('Aurora Glass Candle', 'Coastal Linen', ['#D9E8F5', '#6F93B7', '#F5F8FB']),
    ('Aurora Glass Candle', 'Amber Fig', ['#E8D3B8', '#A36B3F', '#FBF5EE']),
    ('Aurora Glass Candle', 'Rose Sandalwood', ['#F0D4DA', '#B36A78', '#FFF5F6']),
    ('Aurora Glass Candle', 'Midnight Plum', ['#D9D1E8', '#5F4C7A', '#F8F6FB']),
    ('Terra Ceramic Candle', 'Cedar Grove', ['#E1D8CF', '#8A7768', '#F9F6F2']),
    ('Terra Ceramic Candle', 'Vanilla Birch', ['#EEE2C8', '#B69A65', '#FCFAF4']),
    ('Terra Ceramic Candle', 'Citrus Bloom', ['#F9DE9C', '#E39A24', '#FFF9EC']),
    ('Terra Ceramic Candle', 'Lavender Smoke', ['#DDD8EE', '#8779B3', '#F9F8FD']),
    ('Terra Ceramic Candle', 'Wild Jasmine', ['#F1E9D7', '#A5956D', '#FFFCF4']),
    ('Solstice Reed Diffuser', 'Sea Salt Neroli', ['#D8EEF0', '#4F9AA3', '#F2FBFB']),
    ('Solstice Reed Diffuser', 'White Tea', ['#ECE8DC', '#99896B', '#FBFAF5']),
    ('Solstice Reed Diffuser', 'Bergamot Moss', ['#DDE5D4', '#6A8358', '#F7FAF4']),
    ('Solstice Reed Diffuser', 'Peony Rain', ['#F1DCE5', '#B4748B', '#FFF7FA']),
    ('Solstice Reed Diffuser', 'Spiced Tonka', ['#E7D5C7', '#9E6C48', '#FCF7F3']),
    ('Luna Hand Wash', 'Mineral Water', ['#D9EBF3', '#6A9EB5', '#F5FBFD']),
    ('Luna Hand Wash', 'White Sage', ['#E2E8DE', '#7C9674', '#F7FAF6']),
    ('Luna Hand Wash', 'Blush Peony', ['#F3DDE3', '#B87B89', '#FFF7F8']),
    ('Luna Hand Wash', 'Green Mandarin', ['#EEF0C9', '#98A53C', '#FBFDEE']),
    ('Luna Hand Wash', 'Cashmere Oud', ['#E9DDD5', '#9B7464', '#FCF8F6']),
    ('Marina Throw Pillow', 'Harbor Blue', ['#D7E7F3', '#4E7FA7', '#F5FAFD']),
    ('Marina Throw Pillow', 'Terracotta Clay', ['#EED4C7', '#B5694C', '#FFF7F3']),
    ('Marina Throw Pillow', 'Olive Weave', ['#DDE3D6', '#6F7E58', '#F7FAF5']),
    ('Marina Throw Pillow', 'Sunset Coral', ['#F6D7CE', '#D97962', '#FFF8F5']),
    ('Marina Throw Pillow', 'Fog Linen', ['#EAE7E1', '#A09A8F', '#FDFCF9']),
    ('Atelier Mug', 'Cloud White', ['#F4F2EC', '#B7B2A7', '#FFFEFC']),
    ('Atelier Mug', 'Stone Blue', ['#D8E2EC', '#6D89A6', '#F5F9FC']),
    ('Atelier Mug', 'Dusty Rose', ['#EFDCE0', '#B47A87', '#FFF8F8']),
    ('Atelier Mug', 'Forest Clay', ['#DCE2D7', '#718163', '#F7FAF5']),
    ('Atelier Mug', 'Honey Sand', ['#F5E5C6', '#C69C59', '#FFF9EF']),
    ('Canvas Tote', 'Market Stripe', ['#EFE9DE', '#8E795B', '#FCFBF7']),
    ('Canvas Tote', 'Olive Shore', ['#DDE3D8', '#6B7D60', '#F7FAF5']),
    ('Canvas Tote', 'Berry Check', ['#F0D9DF', '#A96375', '#FFF8FA']),
    ('Canvas Tote', 'Sky Grid', ['#DDEAF5', '#6A90B0', '#F7FBFD']),
    ('Canvas Tote', 'Sun Wash', ['#F7E1B8', '#D19B38', '#FFF9EE']),
    ('Desk Journal', 'Moonstone Gray', ['#E6E5E3', '#8D8A84', '#FCFBFA']),
    ('Desk Journal', 'Botanical Green', ['#DDE6D9', '#6D8662', '#F7FAF6']),
    ('Desk Journal', 'Rose Dune', ['#EFDCE0', '#B57B89', '#FFF8F8']),
    ('Desk Journal', 'Ocean Ink', ['#DAE6F0', '#587D9A', '#F5FAFD']),
    ('Desk Journal', 'Golden Hour', ['#F6E4BE', '#CC9E4C', '#FFF9EF']),
    ('Meadow Soap Set', 'Fresh Basil', ['#DFE8D9', '#729163', '#F7FAF6']),
    ('Meadow Soap Set', 'Apricot Bloom', ['#F6DFD4', '#D58B6A', '#FFF8F5']),
    ('Meadow Soap Set', 'Pear Nectar', ['#EEF1D0', '#A1AD54', '#FBFDEE']),
    ('Meadow Soap Set', 'Blue Chamomile', ['#DDE8F2', '#6B90B6', '#F6FBFD']),
    ('Meadow Soap Set', 'Sandal Cream', ['#EFE4D5', '#B49269', '#FDF9F4']),
    ('Woven Table Runner', 'Drift Beige', ['#F0E7DB', '#AA9472', '#FCFAF7']),
    ('Woven Table Runner', 'Sea Glass', ['#D8ECEB', '#649E9A', '#F3FBFB']),
    ('Woven Table Runner', 'Ochre Line', ['#F4E0B9', '#C58E36', '#FFF9EE']),
    ('Woven Table Runner', 'Fern Stripe', ['#DCE5D8', '#6B825C', '#F7FAF5']),
    ('Woven Table Runner', 'Clay Rose', ['#F2DDD9', '#B97972', '#FFF8F7']),
]


def slugify(text: str) -> str:
    cleaned = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return re.sub(r'-{2,}', '-', cleaned)


def wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines = []
    current = []
    current_length = 0
    for word in words:
        next_length = current_length + len(word) + (1 if current else 0)
        if next_length > width and current:
            lines.append(' '.join(current))
            current = [word]
            current_length = len(word)
        else:
            current.append(word)
            current_length = next_length
    if current:
        lines.append(' '.join(current))
    return lines


def render_svg(path: Path, title: str, scent: str, palette: list[str], product_type: str) -> None:
    title_lines = wrap_text(title, 16)[:2]
    title_svg = []
    for index, line in enumerate(title_lines):
        title_svg.append(
            f'<text x="70" y="{495 + index * 42}" font-size="34" font-family="Georgia, serif" fill="#1f1f1f">{html.escape(line)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="{palette[0]}"/>
      <stop offset="100%" stop-color="{palette[2]}"/>
    </linearGradient>
    <linearGradient id="card" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f6f1ea"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="1200" fill="url(#bg)"/>
  <circle cx="210" cy="230" r="120" fill="{palette[2]}" opacity="0.8"/>
  <circle cx="975" cy="275" r="170" fill="{palette[0]}" opacity="0.6"/>
  <rect x="70" y="70" width="1060" height="1060" rx="56" fill="url(#card)" opacity="0.94"/>
  <rect x="150" y="180" width="900" height="170" rx="18" fill="{palette[0]}"/>
  <rect x="350" y="280" width="500" height="420" rx="36" fill="{palette[1]}" opacity="0.16"/>
  <ellipse cx="600" cy="720" rx="250" ry="40" fill="#d8d1c9"/>
  <rect x="455" y="330" width="290" height="330" rx="32" fill="#fbf8f4" stroke="{palette[1]}" stroke-width="8"/>
  <rect x="495" y="285" width="210" height="64" rx="18" fill="{palette[1]}"/>
  <rect x="520" y="390" width="160" height="180" rx="18" fill="{palette[0]}"/>
  <rect x="495" y="610" width="210" height="26" rx="13" fill="{palette[1]}" opacity="0.45"/>
  <text x="600" y="462" text-anchor="middle" font-size="30" font-family="Georgia, serif" fill="#2e2e2e">{html.escape(scent)}</text>
  <text x="600" y="502" text-anchor="middle" font-size="18" font-family="Arial, sans-serif" letter-spacing="2" fill="#666">CURATED HOME GOODS</text>
  <text x="600" y="548" text-anchor="middle" font-size="20" font-family="Arial, sans-serif" fill="{palette[1]}">{html.escape(product_type)}</text>
  {''.join(title_svg)}
  <text x="70" y="590" font-size="24" font-family="Arial, sans-serif" letter-spacing="2" fill="{palette[1]}">{html.escape(scent.upper())}</text>
  <text x="70" y="628" font-size="18" font-family="Arial, sans-serif" letter-spacing="3" fill="#6f6f6f">{html.escape(product_type.upper())}</text>
</svg>
'''
    path.write_text(svg, encoding='utf-8')


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (title, scent, palette) in enumerate(PRODUCTS, start=1):
        full_title = f'{title} - {scent}'
        handle = slugify(full_title)
        sku = f'SA-{index:03d}'
        barcode = f'880000{index:07d}'
        price = round(18.0 + (index % 7) * 3.25, 2)
        compare_at = round(price + 8.0, 2)
        cost = round(price * 0.45, 2)
        inventory = 20 + (index % 11) * 3
        weight = 220 + (index % 6) * 45
        image_name = f'{handle}.svg'
        product_type = title.split(' ', 1)[1]

        render_svg(OUTPUT_DIR / image_name, title, scent, palette, product_type)

        row = {header: '' for header in HEADERS}
        row.update({
            'Title': full_title,
            'URL handle': handle,
            'Description': f'{full_title} is a thoughtfully styled {product_type.lower()} designed for modern homes. It pairs a refined palette with gift-ready presentation and everyday practicality.',
            'Vendor': 'Southern Aura Studio',
            'Product category': 'Home & Garden > Decor',
            'Type': product_type,
            'Tags': f"{title.split(' ', 1)[0]}, {product_type}, {scent}, Home Decor, Gift Idea",
            'Published on online store': 'TRUE',
            'Status': 'Active',
            'SKU': sku,
            'Barcode': barcode,
            'Option1 name': 'Title',
            'Option1 value': 'Default Title',
            'Price': f'{price:.2f}',
            'Compare-at price': f'{compare_at:.2f}',
            'Cost per item': f'{cost:.2f}',
            'Charge tax': 'TRUE',
            'Inventory tracker': 'shopify',
            'Inventory quantity': str(inventory),
            'Continue selling when out of stock': 'DENY',
            'Weight value (grams)': str(weight),
            'Weight unit for display': 'g',
            'Requires shipping': 'TRUE',
            'Fulfillment service': 'manual',
            'Product image URL': image_name,
            'Image position': '1',
            'Image alt text': f'{full_title} product image',
            'Gift card': 'FALSE',
            'SEO title': f'{full_title} | Southern Aura Studio',
            'SEO description': f'Shop {full_title}, a beautifully designed {product_type.lower()} with a soft, elevated aesthetic.',
            'Color (product.metafields.shopify.color-pattern)': '; '.join(palette),
            'Google Shopping / Google product category': 'Home & Garden > Decor',
            'Google Shopping / Age group': 'Adult',
            'Google Shopping / Manufacturer part number (MPN)': sku,
            'Google Shopping / Ad group name': title,
            'Google Shopping / Ads labels': scent,
            'Google Shopping / Condition': 'New',
            'Google Shopping / Custom product': 'FALSE',
            'Google Shopping / Custom label 0': 'Generated Catalog',
            'Google Shopping / Custom label 1': product_type,
        })
        rows.append(row)

    with CSV_PATH.open('w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Wrote {CSV_PATH}')
    print(f'Created {len(rows)} images in {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
