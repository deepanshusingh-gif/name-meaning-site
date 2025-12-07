import os

# ---------- SETTINGS ----------
BASE_URL = "https://mynamefinder.netlify.app"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
NAMES_FILE = os.path.join(PROJECT_DIR, "names_master.txt")
NAMES_DIR = os.path.join(PROJECT_DIR, "names")
SITEMAP_FILE = os.path.join(PROJECT_DIR, "sitemap.txt")


def generate_meaning(name: str) -> str:
    """Return a meaning string for a given name."""
    key = name.strip().lower()

    meanings = {
        "arjun": "Arjun means bright, shining, or white. Symbolizes courage, heroism, and intelligence.",
        "aarav": "Aarav means peace, calmness, and wisdom. Associated with a peaceful and intelligent personality.",
        "vivaan": "Vivaan means full of life, energy, and vibrance. Represents enthusiasm and freshness.",
        "krish": "Krish is short for Krishna, meaning one who attracts. Represents charm, love, and positivity.",
        "shivansh": "Shivansh means a part of Lord Shiva. Symbolizes strength, spirituality, and deep inner power.",
        "keshav": "Keshav is a name of Krishna, meaning one with beautiful hair. Represents love and kindness.",
        "rudra": "Rudra is a form of Shiva, symbolizing power, storm, and transformation.",
        "arnav": "Arnav means ocean or sea, symbolizing depth, vastness, and emotional strength.",
        "yash": "Yash means fame, success, and glory. Represents achievement and recognition.",
        "lakshay": "Lakshay means target or aim. Symbolizes ambition, focus, and direction.",
        "priya": "Priya means beloved, dear one. Symbolizes affection, warmth, and kindness.",
        "diya": "Diya means lamp or light. Represents brightness, hope, and positivity.",
        "advika": "Advika means unique or one of a kind. Symbolizes individuality and uniqueness.",
        "ishika": "Ishika means paintbrush or sacred arrow. Represents creativity and purpose.",
        "anvi": "Anvi is a name of Goddess Lakshmi, meaning kind and compassionate.",
        "radha": "Radha symbolizes devotion, love, and purity as the consort of Lord Krishna.",
        "charvi": "Charvi means beautiful and charming. Represents grace and inner beauty.",
        "tanvi": "Tanvi means delicate and beautiful girl. Represents elegance and softness.",
        "nidhi": "Nidhi means treasure or wealth. Represents abundance and prosperity.",
        "manya": "Manya means worthy of honor and respect.",
        "ali": "Ali means high, elevated, or champion. Symbolizes strength and honor.",
        "yusuf": "Yusuf means God increases. Represents blessings, growth, and prosperity.",
        "ahmed": "Ahmed means highly praised or one who constantly thanks God.",
        "imran": "Imran means prosperity or exaltation. A respected and traditional name.",
        "omar": "Omar means flourishing, long-lived, or eloquent speaker.",
        "kabir": "Kabir means great or noble. Symbolizes wisdom and spiritual strength.",
        "ayaan": "Ayaan means gift of God or blessing. Symbolizes good fortune and protection.",
        "rehan": "Rehan means sweet basil, fragrance, or kingly. Represents freshness and grace.",
        "faisal": "Faisal means decisive, strong judge, or one who settles arguments.",
        "muhammad": "Muhammad means the praised one. The name of the Prophet, symbolizing high respect.",
        "zara": "Zara means princess, flower, or shining star. Represents elegance and brightness.",
        "ayesha": "Ayesha means lively, prosperous, or life. A respected Islamic name.",
        "noor": "Noor means light or radiance. Represents guidance and illumination.",
        "sara": "Sara means princess or noblewoman. Represents purity and grace.",
        "maryam": "Maryam means beloved, pure, or elevated. The mother of Isa (Jesus).",
        "sana": "Sana means brilliance, radiance, or praise.",
        "meera": "Meera symbolizes devotion to Lord Krishna. Represents love and spirituality.",
        "ira": "Ira means earth or speech. Associated with Goddess Saraswati in some traditions.",
        "kavya": "Kavya means poetry. Represents artistic talent and creativity.",
        "saanvi": "Saanvi is a name of Goddess Lakshmi, symbolizing beauty and prosperity.",
        "myra": "Myra means beloved, admirable, or sweet.",
        "anika": "Anika means graceful and brilliant. Linked to Goddess Durga.",
        "riya": "Riya means singer or graceful. Represents charm and expression.",
        "tara": "Tara means star. Represents guidance, light, and hope.",
        "samaira": "Samaira means enchanting or protected.",
        "arohi": "Arohi means ascending or musical tune.",
        "isha": "Isha is another name of Goddess Parvati, meaning protector or supreme.",
        "aditi": "Aditi means boundless and motherly. Associated with freedom.",
        "shruti": "Shruti means musical note or sound. Represents knowledge.",
        "divya": "Divya means divine or heavenly.",
        "tejas": "Tejas means brilliance, sharpness, or glow.",
        "aryan": "Aryan means noble or honorable.",
        "ansh": "Ansh means portion or part of.",
        "dev": "Dev means god or divine.",
        "vihaan": "Vihaan means dawn or beginning of a new era.",
        "ishaan": "Ishaan means sun or Lord Shiva.",
        "shaurya": "Shaurya means bravery or heroism.",
        "dhruv": "Dhruv means pole star, symbolizing stability.",
        "atharv": "Atharv means wise or learned.",
        "raghav": "Raghav means descendant of King Raghu.",
        "rohan": "Rohan means ascending or sandalwood.",
        "manav": "Manav means human or humane.",
        "naman": "Naman means salutation or respect.",
        "varun": "Varun means lord of water.",
        "kartik": "Kartik is associated with Lord Murugan.",
        "gautam": "Gautam means bright or enlightened (Gautam Buddha).",
        "siddharth": "Siddharth means one who has attained enlightenment.",
        "nikhil": "Nikhil means complete or whole.",
        "kunal": "Kunal means lotus.",
        "simran": "Simran means remembrance (of God).",
        "neha": "Neha means love, rain, or affection.",
        "ritika": "Ritika means movement or stream.",
        "parth": "Parth means warrior prince (Arjuna).",
        "reyansh": "Reyansh means ray of light or part of Lord Vishnu.",
        "ishita": "Ishita means mastery, excellence.",
        "jhanvi": "Jhanvi means Ganga river.",
        "kritika": "Kritika means star or creativity.",
        "tanisha": "Tanisha means ambitious or desire.",
        "harsh": "Harsh means happiness or joy.",
        "aditya": "Aditya means sun or son of Aditi.",
        "samar": "Samar means battle or companion in war.",
        "ranveer": "Ranveer means brave warrior.",
        "rahul": "Rahul means conqueror of miseries.",
        "harshit": "Harshit means joyous or happy.",
        "devansh": "Devansh means part of God.",
        "hridaan": "Hridaan means great heart or kind-hearted.",
        "ayaan": "Ayaan means blessing or gift of God.",
        }


    if key in meanings:
        return meanings[key]

    # fallback for unknown names
    proper = name.strip().capitalize()
    return (
        f"The name {proper} is associated with positivity, individuality, and a strong personality. "
        f"It reflects confidence and a unique identity."
    )


def build_name_page(name: str) -> str:
    """Return HTML content for a name page."""
    name_clean = name.strip()
    title_name = name_clean
    meaning_text = generate_meaning(name_clean)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<title>{title_name} Name Meaning | Origin, Personality, Numerology</title>
<meta name="description" content="Discover the meaning of the name {title_name}, including its origin, significance, personality traits, numerology, and unique characteristics.">
<style>
    body {{
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        margin: 0;
        padding: 0;
    }}

    .container {{
        max-width: 800px;
        margin: auto;
        margin-top: 40px;
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(0,0,0,0.1);
    }}

    h1 {{
        color: #4A90E2;
        margin-bottom: 10px;
    }}

    .section {{
        margin-top: 20px;
        padding: 15px;
        background: #eef5ff;
        border-left: 4px solid #4A90E2;
        border-radius: 8px;
    }}

    a {{
        text-decoration: none;
        color: #4A90E2;
        font-size: 16px;
    }}

    a:hover {{
        text-decoration: underline;
    }}
</style>
</head>

<body>
<div class="container">
    <a href="../index.html">← Back to Home</a>
    <h1>{title_name} — Name Meaning</h1>

    <div class="section">
        <h3>Meaning of {title_name}</h3>
        <p>{meaning_text}</p>
    </div>

    <div class="section">
        <h3>Origin</h3>
        <p>Origin details for the name {title_name} will be added soon.</p>
    </div>

    <div class="section">
        <h3>Numerology</h3>
        <p>Numerology insights for the name <b>{title_name}</b> will be added.</p>
    </div>

    <div class="section">
        <h3>Related Names</h3>
        <p>Explore similar names: <a href="arjun.html">Arjun</a>, <a href="aarav.html">Aarav</a>, <a href="vivaan.html">Vivaan</a>, <a href="priya.html">Priya</a>.</p>
    </div>
</div>
</body>
</html>
"""
    return html


def load_names() -> list:
    """Load names from names_master.txt."""
    if not os.path.exists(NAMES_FILE):
        print("names_master.txt not found.")
        return []

    names = []
    with open(NAMES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                names.append(name)

    # remove duplicates while preserving order
    seen = set()
    unique = []
    for n in names:
        key = n.lower()
        if key not in seen:
            seen.add(key)
            unique.append(n)
    return unique


def slugify_name(name: str) -> str:
    """Convert name to file-friendly slug."""
    return name.strip().lower().replace(" ", "-")


def ensure_names_dir():
    if not os.path.exists(NAMES_DIR):
        os.makedirs(NAMES_DIR)


def generate_all_pages(names: list):
    """Generate HTML files for all names."""
    ensure_names_dir()
    for name in names:
        slug = slugify_name(name)
        filename = f"{slug}.html"
        filepath = os.path.join(NAMES_DIR, filename)

        html = build_name_page(name)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Generated: {filename}")


def generate_sitemap(names: list):
    """Create sitemap.txt with homepage, categories, and all name URLs."""
    lines = [f"{BASE_URL}/"]
    
        # Add static pages
    static_paths = [
        "/about.html",
        "/contact.html",
        "/privacy.html",
    ]
    for path in static_paths:
        lines.append(f"{BASE_URL}{path}")

    # Add category pages (update this list as you create more)
    category_paths = [
        "/categories/hindu-boy-names.html",
    "/categories/hindu-girl-names.html",
    "/categories/muslim-boy-names.html",
    "/categories/muslim-girl-names.html",
    "/categories/modern-names.html",
    "/categories/unique-names.html",
    "/categories/short-names.html",
    "/categories/christian-names.html",
    ]

    for path in category_paths:
        lines.append(f"{BASE_URL}{path}")

    # Add all name pages
    for name in names:
        slug = slugify_name(name)
        lines.append(f"{BASE_URL}/names/{slug}.html")

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Updated sitemap.txt")



def main():
    names = load_names()
    if not names:
        print("No names found in names_master.txt")
        return

    print(f"Loaded {len(names)} unique names.")
    generate_all_pages(names)
    generate_sitemap(names)
    print("All pages and sitemap generated successfully.")


if __name__ == "__main__":
    main()
