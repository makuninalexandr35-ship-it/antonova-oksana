"""Generate web assets from originals. Run with Python + Pillow; no browser runtime dependencies."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'styles.css').read_text(encoding='utf-8')
sources = set(re.findall(r'src="(assets/[^\"]+\.(?:jpg|JPG|png))"', html))
sources.update(re.findall(r"url\('([^']+\.(?:jpg|png))'\)", css))
out = ROOT / 'assets' / 'optimized'
out.mkdir(exist_ok=True)
manifest_path = out / 'manifest.json'
if manifest_path.exists():
    sources.update(json.loads(manifest_path.read_text(encoding='utf-8')))
manifest = {}
for source in sorted(sources):
    original = ROOT / source
    with Image.open(original) as raw:
        im = ImageOps.exif_transpose(raw).convert('RGBA' if 'A' in raw.getbands() else 'RGB')
        logo = 'logo' in original.stem
        hero = original.stem == 'Торт-заставка'
        max_width = min(im.width, 2268 if hero else 1600)
        widths = sorted(set([min(im.width, w) for w in ([360, 720] if logo else [400, 800, max_width])]))
        variants = []
        name = hashlib.sha256(source.encode()).hexdigest()[:12]
        for width in widths:
            resized = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
            file = out / f'{name}-{width}.webp'
            resized.save(file, 'WEBP', quality=88, method=6, lossless=logo)
            variants.append({'src': file.relative_to(ROOT).as_posix(), 'width': width, 'height': resized.height, 'bytes': file.stat().st_size})
        manifest[source] = {'original_bytes': original.stat().st_size, 'variants': variants}

# Reuse the existing square-ish brand artwork, with its original proportions.
with Image.open(ROOT / 'assets/logo.jpg') as raw:
    icon = ImageOps.pad(raw.convert('RGB'), (256, 256), color='#f8f3eb')
    icon.save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    icon.resize((48, 48), Image.Resampling.LANCZOS).save(ROOT / 'assets/favicon-48.png')
    icon.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / 'assets/apple-touch-icon.png')

# JPEG is broadly supported by social preview crawlers; retain the whole photograph.
with Image.open(ROOT / 'assets/Торт-заставка.jpg') as raw:
    preview = ImageOps.exif_transpose(raw).convert('RGB')
    preview.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    preview.save(ROOT / 'assets/og-cake.jpg', quality=90, optimize=True, progressive=True)

manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Optimized {len(manifest)} images; originals preserved.')
print('Original bytes:', sum(v['original_bytes'] for v in manifest.values()))
print('Largest WebP variants:', sum(v['variants'][-1]['bytes'] for v in manifest.values()))
