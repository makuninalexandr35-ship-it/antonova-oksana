"""Check published-page metadata, image files, and sitemap consistency (Python + Pillow)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

html = (ROOT / 'index.html').read_text(encoding='utf-8')
page = Page(html)
canonical = [a['href'] for t, a in page.tags if t == 'link' and a.get('rel') == 'canonical']
assert canonical == ['https://antonovaoksana.ru/']
assert len([t for t, a in page.tags if t == 'h1']) == 1
assert '<h1>Торты и авторские десерты на заказ в Москве</h1>' in html
assert '<title>Торты на заказ в Москве — авторские десерты | Oksana Antonova</title>' in html
og = {a['property']: a['content'] for t, a in page.tags if t == 'meta' and a.get('property', '').startswith('og:')}
assert all(og.get('og:' + k) for k in ['type', 'title', 'description', 'image', 'url'])
assert og['og:url'] == canonical[0]
schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
assert schema['@type'] == 'Organization' and schema['url'] == canonical[0]
assert not any(key in schema for key in ['address', 'openingHours', 'review', 'aggregateRating'])
socials = [a['href'] for t, a in page.tags if t == 'a' and 'social-link' in a.get('class', '')]
assert schema['sameAs'] == socials
images = [a for t, a in page.tags if t == 'img']
for attrs in images:
    assert attrs.get('alt') and attrs.get('decoding') == 'async'
    with Image.open(ROOT / attrs['src']) as im:
        assert im.size == (int(attrs['width']), int(attrs['height']))
    for variant in attrs.get('srcset', '').split(','):
        src, width = variant.strip().split()
        with Image.open(ROOT / src) as im:
            assert im.width == int(width[:-1])
    if 'hero-image' in attrs.get('class', ''):
        assert attrs.get('fetchpriority') == 'high' and attrs.get('loading') == 'eager'
    elif 'brand-logo-header' not in attrs.get('class', ''):
        assert attrs.get('loading') == 'lazy'
ids = {a['id'] for t, a in page.tags if 'id' in a}
for tag, attrs in page.tags:
    for key in ['href', 'src']:
        value = attrs.get(key, '')
        if value.startswith('#'):
            assert value[1:] in ids, value
        elif value and not urlparse(value).scheme:
            assert (ROOT / unquote(value)).exists(), value
css = (ROOT / 'styles.css').read_text(encoding='utf-8')
assert '@import' not in css
for src in re.findall(r"url\('([^']+)'\)", css):
    assert (ROOT / src).exists()
sitemap = ET.parse(ROOT / 'sitemap.xml')
assert [x.text for x in sitemap.findall('.//{*}loc')] == canonical
assert 'Sitemap: ' + canonical[0] + 'sitemap.xml' in (ROOT / 'robots.txt').read_text()
assert (ROOT / 'CNAME').read_text().strip() == urlparse(canonical[0]).hostname
print(f'PASS: metadata, Organization JSON-LD, {len(images)} images with srcset, all local links, anchors, CSS assets, sitemap, robots and CNAME.')
