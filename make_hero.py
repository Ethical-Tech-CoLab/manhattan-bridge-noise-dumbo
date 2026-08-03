"""Build the site's photographic assets from the two files in assets/source/.

Outputs
    assets/hero-composite.jpg        2400 x 1000, the index page hero band
    assets/hero-composite-1200.jpg   small-screen variant
    assets/carousel/bridge-underside.jpg
                                     the HAER plate, border trimmed, for the
                                     noise-canyon carousel

Inputs and their provenance
    assets/source/haer-ny-127-7.jpg
        Historic American Engineering Record survey NY-127, photograph 7,
        Jack E. Boucher for the National Park Service. Library of Congress
        item ny0980, digital id 119135. The Library states "No known
        restrictions on images made by the U.S. Government." The 1024 px
        derivative is the largest that exists at the predictable LOC paths:
        the p.tif, pd.jpg and pw.jpg masters all return 404 for this item.

    assets/source/model-t1-under.png
        A canvas render taken from this repository's own visual-review/
        model-3d.html at tier T1, view Under, with callouts and sightlines
        turned off. It is therefore a picture of inferred geometry, which is
        why it is composited as a wireframe dissolving out of the photograph
        rather than presented as a depiction of the structure.

The output is deliberately grayscale-neutral so the page can tint it with
the theme accent in CSS instead of baking a colour into a JPEG.

Run:  python make_hero.py
"""
import os

from PIL import Image, ImageChops, ImageFilter, ImageOps

W, H = 2400, 1000
OUT = "assets"
SRC = os.path.join("assets", "source")
PHOTO = os.path.join(SRC, "haer-ny-127-7.jpg")
RENDER = os.path.join(SRC, "model-t1-under.png")


def content_box(im, dark=34, light=228, frac=0.78, limit=0.25):
    """Trim the scan furniture from a HAER plate.

    The plate is nested: a white page margin, then a black negative border
    carrying the hand-lettered survey number, then the photograph. Two earlier
    versions of this got it wrong in instructive ways.

    Testing only for near-black stopped immediately at the white page margin
    and trimmed nine pixels while reporting success. Testing for "uniformly
    black OR uniformly white" then stopped at the TRANSITION rows where the
    margin meets the border and neither test passes on its own.

    So the test is that a band is EXTREME - near-black plus near-white together
    account for most of it - and rather than peeling until the test fails, each
    edge scans the outer quarter and crops just past the furthest extreme band.
    That bridges the transitions.
    """
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    xs = list(range(0, w, 2))
    ys = list(range(0, h, 2))

    def extreme(vals):
        n = len(vals)
        return (sum(1 for v in vals if v <= dark or v >= light) / n) >= frac

    def scan(n, band, forward):
        far = -1
        for k in range(int(n * limit)):
            i = k if forward else n - 1 - k
            if extreme(band(i)):
                far = k
        return far + 1

    top = scan(h, lambda y: [px[x, y] for x in xs], True)
    bot = h - 1 - scan(h, lambda y: [px[x, y] for x in xs], False)
    left = scan(w, lambda x: [px[x, y] for y in ys], True)
    right = w - 1 - scan(w, lambda x: [px[x, y] for y in ys], False)
    pad = max(2, int(0.004 * min(w, h)))
    return (left + pad, top + pad, right + 1 - pad, bot + 1 - pad)


def geom_box(im, floor=30):
    """Tight bounding box of drawn geometry on the model's flat background."""
    g = im.convert("L")
    bg = g.getpixel((4, 4))
    mask = g.point(lambda v: 255 if abs(v - bg) > floor else 0)
    return mask.getbbox() or (0, 0, im.size[0], im.size[1])


def _ramp(n, stops):
    stops = sorted(stops)
    out = []
    for i in range(n):
        fr = i / (n - 1)
        v = stops[-1][1] if fr > stops[-1][0] else stops[0][1]
        for j in range(len(stops) - 1):
            a, va = stops[j]
            b, vb = stops[j + 1]
            if a <= fr <= b:
                t = 0.0 if b == a else (fr - a) / (b - a)
                v = va + (vb - va) * t
                break
        out.append(int(round(v)))
    return out


def hgrad(size, stops):
    w, h = size
    row = Image.new("L", (w, 1))
    d = row.load()
    for x, v in enumerate(_ramp(w, stops)):
        d[x, 0] = v
    return row.resize((w, h), Image.BILINEAR)


def vgrad(size, stops):
    w, h = size
    col = Image.new("L", (1, h))
    d = col.load()
    for y, v in enumerate(_ramp(h, stops)):
        d[0, y] = v
    return col.resize((w, h), Image.BILINEAR)


def build_carousel_plate(photo):
    """The photograph on its own, trimmed, for use as a carousel slide."""
    d = os.path.join(OUT, "carousel")
    os.makedirs(d, exist_ok=True)
    im = ImageOps.autocontrast(photo, cutoff=1)
    w, h = im.size
    s = 1400.0 / max(w, h)
    if s < 1.0:
        im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
    p = os.path.join(d, "bridge-underside.jpg")
    im.convert("RGB").save(p, "JPEG", quality=88, optimize=True, progressive=True)
    print("wrote", p, os.path.getsize(p), "bytes", im.size)


def main():
    os.makedirs(OUT, exist_ok=True)

    photo = Image.open(PHOTO).convert("L")
    box = content_box(photo)
    print("photo", photo.size, "content box", box)
    photo = photo.crop(box)
    build_carousel_plate(photo)

    base = Image.new("L", (W, H), 16)
    pw, ph = photo.size
    scale = 1.42 * H / ph
    photo = photo.resize((int(pw * scale), int(ph * scale)), Image.LANCZOS)
    pw, ph = photo.size

    # Window on the tower and the deck soffit.
    top = int(ph * 0.10)
    photo = photo.crop((0, top, pw, top + H))
    pw, ph = photo.size

    px0 = W - pw + int(pw * 0.06)
    photo = ImageOps.autocontrast(photo, cutoff=1)
    photo = photo.point(lambda v: int(min(255, (v / 255.0) ** 1.18 * 255 * 0.92)))

    # Feather the photograph's left edge into the wireframe zone.
    fade = int(pw * 0.42)
    pmask = hgrad((pw, ph), [(0.0, 0), (fade / pw * 0.55, 40),
                             (fade / pw, 255), (1.0, 255)])
    base.paste(photo, (px0, 0), pmask)

    # The model render, screened over the plate so its lines read as light.
    ren = Image.open(RENDER).convert("L")
    gb = geom_box(ren)
    print("render", ren.size, "geom box", gb)
    ren = ren.crop(gb)
    ren = ImageChops.subtract(ren, Image.new("L", ren.size, 34))
    rw, rh = ren.size
    rs = (H * 0.86) / rh
    ren = ren.resize((int(rw * rs), int(rh * rs)), Image.LANCZOS)
    rw, rh = ren.size

    plate = Image.new("L", (W, H), 0)
    plate.paste(ren, (int(W * 0.235), int((H - rh) / 2)))
    bloom = plate.filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * 0.55))
    plate = ImageChops.lighter(plate, bloom)
    plate = ImageChops.multiply(plate, hgrad(
        (W, H), [(0.0, 0), (0.20, 150), (0.50, 255), (0.78, 195), (1.0, 55)]))
    base = ImageChops.screen(base, plate.point(lambda v: int(min(255, v * 0.92))))

    # Readability scrim, darkest at the left where the headline sits.
    scrim = hgrad((W, H), [(0.0, 250), (0.30, 175), (0.55, 62), (1.0, 0)])
    base = ImageChops.subtract(base, scrim.point(lambda v: int(v * 0.58)))

    # Top and bottom falloff so the band sits into the page.
    vs = vgrad((W, H), [(0.0, 90), (0.12, 0), (0.86, 0), (1.0, 120)])
    base = ImageChops.subtract(base, vs.point(lambda v: int(v * 0.6)))

    out = base.convert("RGB")
    p = os.path.join(OUT, "hero-composite.jpg")
    out.save(p, "JPEG", quality=86, optimize=True, progressive=True)
    print("wrote", p, os.path.getsize(p), "bytes", out.size)

    small = out.resize((1200, 500), Image.LANCZOS)
    ps = os.path.join(OUT, "hero-composite-1200.jpg")
    small.save(ps, "JPEG", quality=84, optimize=True, progressive=True)
    print("wrote", ps, os.path.getsize(ps), "bytes", small.size)


if __name__ == "__main__":
    main()
