# ITS-Projekt: Vulnerable Webapp & Automatisiertes Exploit-Framework

## 📝 Projektübersicht
Dieses Repository enthält ein akademisches Demonstrationsobjekt für ein sicheres und unsicheres Webanwendungsdesign im Rahmen des ITS-Projekts. Es handelt sich um einen minimalistischen Online-Shop (Webshop), der gezielt eine kritische Sicherheitslücke enthält, um die Funktionsweise von Cyberangriffen und die Implementierung von defensiven Gegenmaßnahmen zu veranschaulichen.

Das Projekt deckt die drei Kernbereiche der Systementwicklung und IT-Sicherheit ab:
1. **Webanwendung & Datenstruktur (Person 1)**
2. **Sicherheitslücken-Implementierung (Person 2)**
3. **Exploits & Sicherheitsdokumentation (Person 3)**
## 👥 Rollenverteilung & Architektur

### 👤 Person 1: Webanwendung (Core & Frontend)
- **Komponenten:** `app.py`, `templates/base.html`, `templates/index.html`, `templates/login.html`
- **Beschreibung:** Entwicklung der grundlegenden Flask-Anwendung mit einer SQLite-Datenbankanbindung (`database.db`). Bereitstellung eines responsiven Store-Frontends und einer Benutzerverwaltung inklusive eines Login-Formulars für registrierte Kunden.

### 👤 Person 2: Sicherheitslücken (Vulnerability)
- **Komponenten:** `app.py` (Login-Injektionspunkt)
- **Beschreibung:** Gezielter Einbau einer **SQL-Injection-Schwachstelle** im Authentifizierungs-Endpunkt `/login`. Die Benutzereingaben werden ohne Validierung oder Filterung direkt in den SQL-Befehl eingebettet, was eine serverseitige Manipulation erlaubt.

### 👤 Person 3: Exploits & Dokumentation (Audit)
- **Komponenten:** `exploit.py`, `exploit_notes.txt`
- **Beschreibung:** Erstellung eines automatisierten Python-Audit-Frameworks, das die Schwachstelle mittels HTTP-POST-Anfragen verifiziert und einen erfolgreichen Login-Bypass demonstriert. Vollständige Dokumentation der Analyse im Write-up.

## 🛠️ Technische Analyse & Exploit (SQL-Injection)

### Manuelle Analyse (`exploit_notes.txt`)
Der Login-Mechanismus verwendet intern folgende unsichere SQL-Abfrage:
```sql
SELECT * FROM users WHERE username = 'USER_INPUT' AND password = 'PASSWORD_INPUT'
Der Exploit-Payload
Durch Eingabe des Payloads ' OR '1'='1 im Benutzernamen-Feld wird die logische Bedingung der Abfrage wie folgt manipuliert:
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '...'
Da '1'='1' immer wahr (true) ist, wird die Passwortüberprüfung komplett umgangen und der Zugriff auf die Anwendung gewährt.
## 🚀 Inbetriebnahme & Demo

### 1. Anwendung starten
Stellen Sie sicher, dass Flask und Requests installiert sind, und starten Sie den lokalen Webserver:
```bash
python app.py
Die Anwendung ist anschließend unter http://127.0.0.1:5000 erreichbar.

2. Automatisierten Sicherheits-Audit ausführen
Während der Webserver läuft, kann das automatisierte Exploit-Framework gestartet werden, um die Anfälligkeit der Anwendung zu überprüfen:
python exploit.py
Defensive Gegenmaßnahmen (Mitigation)
Um die SQL-Injection-Schwachstelle nachhaltig zu beseitigen, muss die Anwendung von dynamischen SQL-Queries auf Parameterized Queries (Prepared Statements) umgestellt werden.

Sicherer Code-Ausschnitt für app.py:
# Sichere Implementierung mit Parameterized Queries
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
Durch diese Anpassung werden Benutzereingaben strikt als Daten und nicht als ausführbarer SQL-Code behandelt, wodurch jegliche Form von SQL-Injection unmöglich gemacht wird.
