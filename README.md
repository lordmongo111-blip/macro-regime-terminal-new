# Macro / Regime Terminal

Streamlit-Starterprojekt für Makroanalyse, G10-FX, Saisonalität, COT, NQ/ES und eine illustrative Regression.

## Lokal starten

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub und Streamlit Community Cloud

1. Erstelle ein GitHub-Repository.
2. Lade `app.py`, `requirements.txt` und `README.md` hoch.
3. Öffne Streamlit Community Cloud und verbinde dein GitHub-Konto.
4. Wähle das Repository und als App-Datei `app.py`.
5. Deploye die App.

## FRED API-Key

Der FRED-Key darf nicht in GitHub gespeichert werden. Für Streamlit Cloud:
- App öffnen → Settings → Secrets
- Folgendes als TOML eintragen:

```toml
FRED_API_KEY = "DEIN_FRED_API_KEY"
```

Alternativ kann der Schlüssel in der Sidebar eingegeben werden.

## Datenstatus und Einschränkungen

- USD-Makroserien sind über FRED abrufbar, wenn ein gültiger API-Key vorhanden ist.
- Das G10-Ranking zeigt die Datenabdeckung; es berechnet noch kein vollständiges relatives Live-Ranking für alle zehn Währungen.
- Saisonalität und NQ/ES verwenden historische Kursdaten über yfinance; Verfügbarkeit, Verzögerung und Lizenzbedingungen sind zu prüfen.
- Der CFTC-Test ist ein Datenquellen-Preview, keine vollständig validierte COT-Auswertung.
- Die Regression verwendet synthetische Daten.
- Keine Anlageberatung. Vor produktiver Verwendung Daten, Methodik und Signale unabhängig validieren.
