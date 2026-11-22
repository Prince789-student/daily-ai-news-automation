import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

leaders = [
    ("Elon Musk", "Elon Musk"),
    ("Mark Zuckerberg", "Mark Zuckerberg"),
    ("Sam Altman", "Sam Altman"),
    ("Jensen Huang", "Jensen Huang"),
    ("Sundar Pichai", "Sundar Pichai")
]

for name, query_name in leaders:
    query = f'"{query_name}" (tweet OR posted OR announced OR x.com OR thread) when:1d'
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            root = ET.fromstring(r.read())
            items = root.findall(".//item")[:2]
            print(f"=== {name} ({len(items)} items) ===")
            for item in items:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                print(f"  • {title}")
    except Exception as e:
        print(f"  Error for {name}: {e}")
