#!/usr/bin/env python3
# generate_name_pages.py
# Generate static SEO-friendly name pages, sitemap, robots, index, and category pages.
# Usage:
#  - Put a CSV at names.csv with header: name,meaning,origin,gender,traits,pronunciation
#  - Edit SITE_URL below to your real site URL
#  - Run: python generate_name_pages.py

import csv
import json
import html
import os
import re
from pathlib import Path
from datetime import datetime
from random import choice, randint
from collections import defaultdict

# ---------------- CONFIG ----------------
ROOT = Path(__file__).parent.resolve()
PUBLIC_DIR = ROOT / "public"
NAMES_DIR = PUBLIC_DIR / "names"
SITEMAP_FILE = PUBLIC_DIR / "sitemap.xml"
ROBOTS_FILE = PUBLIC_DIR / "robots.txt"
CSV_FILE = ROOT / "names.csv"

# Change this to your Vercel URL (including https://)
SITE_URL = "https://name-meaning-site.vercel.app"  # <-- SET YOUR SITE URL HERE
SITE_NAME = "Name Meaning Finder"
AUTHOR = SITE_NAME
DEFAULT_LOCALE = "en-IN"
# ----------------------------------------

# Ensure directories
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
NAMES_DIR.mkdir(parents=True, exist_ok=True)

# Helper utilities
def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[’'`\".,:;!@#$%^&*()_+=\[\]{}<>?/\\]+", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-") or "name"

def slugify_simple(s: str) -> str:
    return re.sub(r'[^a-z0-9\-]+', '-', (s or "").strip().lower()).strip('-') or "unknown"

def safe_text(s: str) -> str:
    return html.escape((s or "").strip())

# Small variety templates
OPENING_TEMPLATES = [
    "The name {name} means {meaning}.",
    "{name} is a name that means {meaning}.",
    "Meaning of {name}: {meaning}.",
    "{name} — meaning: {meaning}.",
]
ORIGIN_TEMPLATES = [
    "Origin: {origin}.",
    "This name comes from {origin}.",
    "Rooted in {origin} culture.",
    "A name with {origin} origins.",
]
PERSONALITY_TEMPLATES = [
    "{name} is often associated with qualities like {traits}.",
    "People with the name {name} are believed to be {traits}.",
    "Those named {name} tend to be {traits}.",
    "{name} often suggests a personality that is {traits}.",
]
DEFAULT_TRAITS = [
    "kind and compassionate", "confident and ambitious", "creative and thoughtful",
    "calm and wise", "energetic and curious", "practical and hardworking",
    "adventurous and bold", "loyal and reliable"
]

# ---- Safe CSV reader ----
def read_csv(path: Path):
    rows = []
    if not path.exists():
        print(f"ERROR: CSV file not found at {path}. Create a CSV with columns: name,meaning,origin,gender,traits,pronunciation")
        return rows
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            safe_row = {}
            for k, v in (r.items()):
                if k is None:
                    continue
                key = (k or "").strip().lower()
                val = (v or "").strip()
                safe_row[key] = val
            # skip rows that are completely empty
            if any(value for value in safe_row.values()):
                rows.append(safe_row)
    return rows

# ---- Page generation ----
def generate_description(row):
    name = row.get("name", "").strip()
    meaning = row.get("meaning", "").strip() or "Meaning not available"
    origin = row.get("origin", "").strip() or "Unknown origin"
    gender = row.get("gender", "").strip()
    traits = row.get("traits", "").strip() or choice(DEFAULT_TRAITS)

    parts = []
    parts.append(OPENING_TEMPLATES[randint(0, len(OPENING_TEMPLATES)-1)].format(name=name, meaning=meaning))
    parts.append(ORIGIN_TEMPLATES[randint(0, len(ORIGIN_TEMPLATES)-1)].format(origin=origin))
    parts.append(PERSONALITY_TEMPLATES[randint(0, len(PERSONALITY_TEMPLATES)-1)].format(name=name, traits=traits))
    if row.get("pronunciation"):
        parts.append(f"Pronunciation: {row.get('pronunciation')}.")
    if row.get("popularity"):
        parts.append(f"Popularity: {row.get('popularity')}.")
    if gender:
        parts.append(f"Commonly used for: {gender}.")
    paragraphs = "".join(f"<p>{safe_text(p)}</p>" for p in parts)
    return paragraphs

def build_html(row):
    name = (row.get("name") or "").strip()
    if not name:
        return None
    slug = slugify(name)
    meaning = row.get("meaning", "").strip() or "Meaning not available"
    origin = row.get("origin", "").strip() or "Unknown"
    gender = (row.get("gender") or "").strip().capitalize() or "Unspecified"
    traits = row.get("traits", "").strip() or choice(DEFAULT_TRAITS)
    pronunciation = (row.get("pronunciation") or "").strip()

    # Meta title + description (kept concise and SEO-friendly)
    title = f"{name} Meaning — {meaning} | {SITE_NAME}"
    # meta description target ~120-155 chars
    meta_desc_short = f"{name} meaning: {meaning}. Origin: {origin}. Traits: {traits}."
    if len(meta_desc_short) > 155:
        meta_desc = meta_desc_short[:152].rsplit(" ",1)[0] + "..."
    else:
        meta_desc = meta_desc_short

    page_url = f"{SITE_URL}/names/{slug}.html"
    lastmod = datetime.utcnow().date().isoformat()

    # richer JSON-LD: WebPage + DefinedTerm + BreadcrumbList
    jsonld_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": page_url,
                "name": name,
                "description": re.sub(r"\s+", " ", meaning)[:197],
                "url": page_url,
                "inLanguage": DEFAULT_LOCALE,
                "author": {"@type": "Organization", "name": AUTHOR}
            },
            {
                "@type": "DefinedTerm",
                "name": name,
                "description": meaning,
                "inDefinedTermSet": SITE_URL
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Names", "item": SITE_URL + "/names/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": page_url}
                ]
            }
        ]
    }
    # produce valid JSON-LD (raw JSON, not HTML-escaped)
    json_ld = json.dumps(jsonld_obj, ensure_ascii=False, indent=2)
    json_ld_block = f'<script type="application/ld+json">\n{json_ld}\n</script>'

    # Small internal links to categories (gender + origin + length)
    gender_slug = slugify_simple(gender)
    origin_slug = slugify_simple(origin)
    nlen = len(name.replace(" ", ""))
    if nlen <= 4:
        length_label = "Short (1-4)"
    elif nlen <= 7:
        length_label = "Medium (5-7)"
    else:
        length_label = "Long (8+)"
    length_slug = slugify_simple(length_label)

    # Category URLs
    cat_gender_url = f"{SITE_URL}/categories/{gender_slug}.html"
    cat_origin_url = f"{SITE_URL}/categories/origin-{origin_slug}.html"
    cat_length_url = f"{SITE_URL}/categories/length-{length_slug}.html"

    # Build content HTML
    description_html = generate_description(row)
    cat_links_html = f'''
    <p>Categories:
      <a href="{cat_gender_url}">{html.escape(gender)}</a> |
      <a href="{cat_origin_url}">{html.escape(origin)}</a> |
      <a href="{cat_length_url}">{html.escape(length_label)}</a>
    </p>
    '''

    og_image = f"{SITE_URL}/og-default.png"

    html_template = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{safe_text(title)}</title>
  <meta name="description" content="{safe_text(meta_desc)}" />
  <link rel="canonical" href="{page_url}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{safe_text(SITE_NAME)}" />
  <meta property="og:title" content="{safe_text(title)}" />
  <meta property="og:description" content="{safe_text(meta_desc)}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{safe_text(title)}" />
  <meta name="twitter:description" content="{safe_text(meta_desc)}" />
{json_ld_block}
{html.escape(str(jsonld_obj)).replace("&quot;", '"')}
  </script>
  <style>
    body{{font-family: system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;max-width:820px;margin:28px auto;padding:0 18px;color:#111;line-height:1.6}}
    header h1{{font-size:28px;margin:8px 0 4px}}
    .meta{{color:#666;font-size:14px;margin-bottom:14px}}
    .content p{{margin:0 0 14px}}
    footer{{margin-top:36px;font-size:13px;color:#666}}
    a.button{{display:inline-block;padding:8px 12px;border-radius:6px;border:1px solid #ddd;text-decoration:none;color:inherit}}
  </style>
</head>
<body>
  <header>
    <a href="{SITE_URL}" class="button">← Home</a>
    <h1>{safe_text(name)}</h1>
    <div class="meta">Meaning: <strong>{safe_text(meaning)}</strong> • Origin: {safe_text(origin)} • Pronunciation: {safe_text(pronunciation)}</div>
  </header>
  <main class="content">
    {description_html}
    {cat_links_html}
    <h3>Quick facts</h3>
    <ul>
      <li><strong>Name:</strong> {safe_text(name)}</li>
      <li><strong>Meaning:</strong> {safe_text(meaning)}</li>
      <li><strong>Origin:</strong> {safe_text(origin)}</li>
      <li><strong>URL:</strong> <a href="{page_url}">{page_url}</a></li>
    </ul>
  </main>
  <footer>
    <p>© {datetime.utcnow().year} {safe_text(SITE_NAME)} — <a href="{SITE_URL}/privacy">Privacy</a> • <a href="{SITE_URL}/contact">Contact</a></p>
  </footer>
</body>
</html>
"""
    return slug, html_template, lastmod

# ---- Sitemap & robots ----
def update_sitemap(add_entries):
    existing = {}
    if SITEMAP_FILE.exists():
        txt = SITEMAP_FILE.read_text(encoding='utf-8')
        blocks = re.findall(r"<url>(.*?)</url>", txt, flags=re.S)
        for b in blocks:
            mloc = re.search(r"<loc>(.*?)</loc>", b)
            mlast = re.search(r"<lastmod>(.*?)</lastmod>", b)
            if mloc:
                existing[mloc.group(1).strip()] = mlast.group(1).strip() if mlast else ""
    # merge
    for url, lastmod in add_entries.items():
        existing[url] = lastmod
    items = []
    for loc, last in sorted(existing.items()):
        items.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{last or datetime.utcnow().date().isoformat()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>""")
    sitemap_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
                      "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(items) + "\n</urlset>\n"
    SITEMAP_FILE.write_text(sitemap_content, encoding='utf-8')
    print(f"[sitemap] Updated {SITEMAP_FILE} with {len(items)} URLs")

def ensure_robots():
    content = ROBOTS_FILE.read_text(encoding='utf-8') if ROBOTS_FILE.exists() else ""
    if "Sitemap:" not in content:
        content = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
        ROBOTS_FILE.write_text(content, encoding='utf-8')
        print(f"[robots] Wrote {ROBOTS_FILE}")
    else:
        print("[robots] robots.txt already contains Sitemap line (left unchanged)")

# ---- Names index ----
def generate_index_page(pages):
    rows_html = "\n".join(f'<li><a href="{url}">{html.escape(title)}</a></li>' for url,title in pages)
    index_html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Names index — {safe_text(SITE_NAME)}</title>
<meta name="description" content="Index of generated name meaning pages" />
</head><body>
<h1>Names index</h1>
<ul>
{rows_html}
</ul>
<p><a href="{SITE_URL}">Back to Home</a></p>
</body></html>"""
    (NAMES_DIR / "index.html").write_text(index_html, encoding='utf-8')
    print(f"[index] Wrote index with {len(pages)} entries to {NAMES_DIR / 'index.html'}")

# ---- Category generation (auto) ----
CATEGORIES_DIR = PUBLIC_DIR / "categories"
CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)

def write_html(path: Path, html_str: str):
    path.write_text(html_str, encoding='utf-8')
    print(f"[write] {path.relative_to(ROOT)}")

def render_category_page(title: str, description: str, items: list):
    rows = "\n".join(f'<li><a href="{u}">{html.escape(l)}</a></li>' for u,l in items)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}"/>
</head><body>
<header><a href="{SITE_URL}">Home</a> › <strong>{html.escape(title)}</strong></header>
<main>
<h1>{html.escape(title)}</h1>
<p>{html.escape(description)}</p>
<ul>
{rows}
</ul>
<p><a href="{SITE_URL}/categories/index.html">All categories</a></p>
</main>
<footer>© {datetime.utcnow().year} {html.escape(SITE_NAME)}</footer>
</body></html>"""

def generate_categories(csv_rows, pages):
    # Build lookup: name_lower -> (url,label)
    lookup = {}
    for url,label in pages:
        lookup[label.strip().lower()] = (url, label)

    by_gender = defaultdict(list)
    by_origin = defaultdict(list)
    by_length = defaultdict(list)

    for r in csv_rows:
        name = (r.get("name") or "").strip()
        if not name:
            continue
        key = name.lower()
        if key in lookup:
            url, label = lookup[key]
        else:
            slug = slugify(name)
            url = f"{SITE_URL}/names/{slug}.html"
            label = name

        gender = (r.get("gender") or "").strip().lower()
        if gender in ("male","m"):
            by_gender["Male"].append((url, label))
        elif gender in ("female","f"):
            by_gender["Female"].append((url, label))
        else:
            by_gender["Unisex/Unknown"].append((url, label))

        origin = (r.get("origin") or "Unknown").strip()
        by_origin[origin].append((url, label))

        nlen = len(name.replace(" ", ""))
        if nlen <= 4:
            by_length["Short (1-4)"].append((url, label))
        elif nlen <= 7:
            by_length["Medium (5-7)"].append((url, label))
        else:
            by_length["Long (8+)"].append((url, label))

    # Write gender pages
    for gender_label, items in sorted(by_gender.items()):
        title = f"{gender_label} Names"
        desc = f"{len(items)} {gender_label.lower()} names from the site."
        out = CATEGORIES_DIR / f"{slugify_simple(gender_label)}.html"
        write_html(out, render_category_page(title, desc, sorted(items, key=lambda x: x[1].lower())))

    # Write origin pages
    for origin_label, items in sorted(by_origin.items(), key=lambda x: (-len(x[1]), x[0].lower())):
        safe_slug = slugify_simple(origin_label)
        title = f"{origin_label} Names"
        desc = f"{len(items)} names with origin: {origin_label}."
        out = CATEGORIES_DIR / f"origin-{safe_slug}.html"
        write_html(out, render_category_page(title, desc, sorted(items, key=lambda x: x[1].lower())))

    # Write length pages
    for label, items in sorted(by_length.items()):
        title = f"{label} Names"
        desc = f"{len(items)} names of length category: {label}."
        out = CATEGORIES_DIR / f"length-{slugify_simple(label)}.html"
        write_html(out, render_category_page(title, desc, sorted(items, key=lambda x: x[1].lower())))

    # Build categories index
    index_rows = []
    for gender_label, items in sorted(by_gender.items()):
        slug = slugify_simple(gender_label)
        index_rows.append((f"{SITE_URL}/categories/{slug}.html", f"{gender_label} ({len(items)})"))
    for origin_label, items in sorted(by_origin.items(), key=lambda x: (-len(x[1]), x[0].lower())):
        slug = f"origin-{slugify_simple(origin_label)}"
        index_rows.append((f"{SITE_URL}/categories/{slug}.html", f"{origin_label} ({len(items)})"))
    for label, items in sorted(by_length.items(), key=lambda x: x[0]):
        slug = f"length-{slugify_simple(label)}"
        index_rows.append((f"{SITE_URL}/categories/{slug}.html", f"{label} ({len(items)})"))

    index_html = render_category_page("Categories", "Browse name categories by gender, origin, and length.", index_rows)
    write_html(CATEGORIES_DIR / "index.html", index_html)

# ---- Main ----
def main():
    rows = read_csv(CSV_FILE)
    if not rows:
        print("No rows found in CSV. Exiting.")
        return

    sitemap_additions = {}
    index_pages = []
    created = 0
    overwritten = 0

    for row in rows:
        built = build_html(row)
        if not built:
            continue
        slug, html_content, lastmod = built
        out_file = NAMES_DIR / f"{slug}.html"
        was_exist = out_file.exists()
        out_file.write_text(html_content, encoding='utf-8')
        if was_exist:
            overwritten += 1
        else:
            created += 1
        url = f"{SITE_URL}/names/{slug}.html"
        sitemap_additions[url] = lastmod
        index_pages.append((url, row.get("name","").strip()))

    update_sitemap(sitemap_additions)
    ensure_robots()
    generate_index_page(index_pages)

    # generate category pages using CSV rows and index_pages
    generate_categories(rows, index_pages)
    # add category pages to sitemap automatically
    # iterate generated category html files and add to sitemap_additions
    for f in CATEGORIES_DIR.glob("*.html"):
        url = f"{SITE_URL}/categories/{f.name}"
        sitemap_additions[url] = datetime.utcnow().date().isoformat()
    print(f"[done] Created: {created}, Overwritten: {overwritten}, Total processed: {len(rows)}")
    print("Next steps: git add public/names/*.html public/sitemap.xml public/robots.txt public/categories && git commit && git push")

if __name__ == "__main__":
    main()
