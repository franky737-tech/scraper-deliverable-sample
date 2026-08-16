# Quotes Monitoring — Datenlieferung vom 2026-08-17

**Kunde:** MUSTER (Portfolio-Beispiel — alle Daten von quotes.toscrape.com, einer offiziellen Scraping-Testseite) · **Zeitraum:** 2026-08-17 · **Lauf:** RUN-001

## Inhalt dieses Pakets

| Datei | Inhalt |
|---|---|
| `data/quotes_monitoring.csv` / `.xlsx` | Datensatz (30 Datensätze, davon 30 neu) |
| `CHANGELOG.csv` | Änderungsverlauf je Lauf |
| `RUN_LOG.txt` | Zeitstempel & Ergebnis je Lauf |
| `code/` | Scraper (`scraper.py`) + `requirements.txt` + Scheduling-Anleitung |

## Quellen & Methode

- **Quelle:** siehe Spalte `source_url` (jeder Datensatz einzeln auditierbar)
- **Erfasst am:** 2026-08-17 06:02
- **Methode:** Öffentliche Daten, robots.txt respektiert, max. 1 Anfrage/Sekunde, eigener User-Agent

## Feldverzeichnis

| Spalte | Bedeutung | Beispiel |
|---|---|---|
| `quote_text` | Erfasster Textinhalt des Eintrags | The world as we have created it … |
| `author` | Zugeordnete Person/Quelle des Eintrags | Albert Einstein |
| `source_url` | Exakte Herkunfts-URL (Auditierbarkeit je Datensatz) | http://quotes.toscrape.com/page/1/ |
| `scraped_at` | Zeitstempel der Erfassung | 2026-08-17 06:02:18 |
| `is_new` | `Y` = seit letztem Lauf neu hinzugekommen (Delta-Markierung) | Y |

## Qualitätssicherung

- 10 Datensätze stichprobenartig manuell gegen die Quellseite geprüft — OK
- Duplikate entfernt über den Primärschlüssel `author` + `quote_text` (erste 60 Zeichen)
- `is_new = Y` markiert Datensätze, die seit dem letzten Lauf neu sind

## Neu ausführen / wöchentlicher Lauf

`cd code && python3 scraper.py` — wöchentlich automatisiert via cron:
`0 6 * * 1 /usr/bin/python3 /pfad/code/scraper.py` (Ergebnis landet in `new_items.csv`; Google-Sheets-Push aktivierbar)

## Hinweise & Grenzen

Verifikation stichprobenartig durchgeführt. Vollständigkeit hängt von der Quelle ab; bei Strukturänderungen der Zielseite kann ein Adapter-Fix nötig werden (im Wartungsangebot enthalten).
