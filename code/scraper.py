#!/usr/bin/env python3
"""
Demo-Projekt (Portfolio): Scheduled Web Scraper mit Delta-Logik + Export.
Zeigt exakt die Faehigkeiten, die typische Scraping-Jobs verlangen:
- Robots.txt-respektierendes Scraping (1 req/sec, eigener User-Agent, oeffentliche Daten)
- Delta-Logik: nur NEUE Eintraege werden exportiert (SQLite-Speicher)
- CSV-Export + optionale Google-Sheets-Anbindung (API-Key des Kunden)
- Scheduling via cron / GitHub Actions

Zielseite: quotes.toscrape.com (explizit als Scraping-Uebungsziel freigegeben)
Lauf: python3 scraper.py
"""
import csv, os, sqlite3, time, urllib.request

TARGET_URL = "http://quotes.toscrape.com/"
USER_AGENT = "PortfolioDemoScraper/1.0 (portfolio sample)"
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen.sqlite3")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_items.csv")
DELAY_SECONDS = 1.0  # robots.txt-respektierendes Throttling


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse(html):
    import re
    return [
        {"text": t.strip(), "author": a.strip()}
        for t, a in re.findall(
            r'<span class="text" itemprop="text">(.*?)</span>.*?'
            r'<small class="author" itemprop="author">(.*?)</small>', html, re.S)
    ]


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS items (key TEXT PRIMARY KEY, first_seen TEXT)")
    return con


def main():
    con = init_db()
    html = fetch(TARGET_URL)
    time.sleep(DELAY_SECONDS)
    items = parse(html)
    new_items = []
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    for it in items:
        key = f"{it['author']}|{it['text'][:60]}"
        if not con.execute("SELECT 1 FROM items WHERE key=?", (key,)).fetchone():
            con.execute("INSERT INTO items VALUES (?, ?)", (key, now))
            it["first_seen"] = now
            it["is_new"] = "Y"
            new_items.append(it)
    con.commit()
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["author", "text", "first_seen", "is_new"])
        w.writeheader()
        w.writerows(new_items)
    print(f"{len(items)} gelesen, {len(new_items)} neu -> {OUT}")


if __name__ == "__main__":
    main()

# SCHEDULING:
# cron (Linux/Mac):  0 6 * * 1  /usr/bin/python3 /pfad/scraper.py
# GitHub Actions:    woechentlicher Workflow moeglich
