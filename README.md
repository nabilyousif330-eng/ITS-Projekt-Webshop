# Vulnerable Webshop System - ITS Projekt

Dieses Projekt implementiert eine Online-Shop-Anwendung auf Basis von Python und Flask, die bewusst mit kritischen Sicherheitslücken aus den OWASP Top 10 ausgestattet wurde. Zudem enthält das Projekt ein automatisiertes Python-Exploit-Skript (`exploit.py`), das alle eingebauten Lücken nacheinander angreift, vollautomatisch ausnutzt und die erfolgreiche Kompromittierung dokumentiert.

## Technologie-Stack
* **Backend:** Python / Flask
* **Datenbank:** SQLite3
* **Frontend:** HTML5 / CSS3
* **Exploit-Framework:** Python Requests

---

## Die 8 implementierten Sicherheitslücken (OWASP Top 10)

Das System verfügt über zwei Modi: **Vulnerable** (Schwachstellen aktiv) und **Secure** (Schutzmaßnahmen aktiv). Im unsicheren Modus können folgende 8 Schwachstellen ausgenutzt werden:

1. **SQL Injection (SQLi):** Unsanitierte Benutzereingaben in der Produktsuche ermöglichen das Auslesen der gesamten Datenbank inklusive Benutzer-Credentials.
2. **Reflected Cross-Site Scripting (XSS):** Dynamische Fehlermeldungen spiegeln unbereinigten JavaScript-Code direkt im Browser des Opfers wider.
3. **Stored Cross-Site Scripting (Stored XSS):** Schadcode kann permanent in den Produktbewertungen hinterlassen werden und wird bei jedem Aufruf der Produktseite ausgeführt.
4. **Insecure Direct Object References (IDOR):** Durch einfache Manipulation der Bestell-ID in der URL können unbefugt die Bestelldaten und Rechnungen anderer Kunden eingesehen werden.
5. **Path Traversal / Local File Inclusion (LFI):** Über den Datei-Download-Pfad können sensible Systemdateien oder Konfigurationsdateien des Servers (z. B. `app.py`) ausgelesen werden.
6. **Broken Authentication (Schwache Passwort-Hashes):** Passwörter werden in der Datenbank im Klartext oder mit unsicheren MD5-Hashes ohne Salt gespeichert, was Brute-Force-Angriffe erleichtert.
7. **Security Misconfiguration (Debug-Modus aktiv):** Der Flask-Debug-Modus ist aktiviert. Bei Fehlern wird ein interaktiver Stack-Trace angezeigt, der zur Remotecodeausführung (RCE) missbraucht werden kann.
8. **Insecure Deserialization / Missing Rate Limiting:** Fehlende Ratenbegrenzung bei Login-Versuchen ermöglicht automatisierte Credential-Stuffing-Angriffe über das Exploit-Skript.

---

## Automatisiertes Exploit-Framework (`exploit.py`)

Das mitgelieferte Skript `exploit.py` dient zur sequentiellen Validierung aller 8 Sicherheitslücken. 

### Ablauf des Scripts:
* Es sendet automatisierte Payloads an die jeweiligen Endpunkte der Webapplikation.
* Es validiert die HTTP-Antworten (Statuscodes und Keywords) auf eine erfolgreiche Kompromittierung.
* **Ergebnis-Dokumentation:** Im Terminal wird farblich dokumentiert, ob der Angriff erfolgreich war (`[+] Exploit Successful`) oder fehlschlug (`[-] Exploit Failed`), wenn der Schutzmodus aktiviert ist.

---

## Geplanter Demo-Ablauf (10 Min. Lightning Talk)
* **Einführung (2 Min.):** Vorstellung der Webarchitektur und Übersicht der 8 Schwachstellen.
* **Live-Demo - Manuelle Ausnutzung (3 Min.):** Demonstration von SQL-Injection in der Produktsuche sowie Reflected XSS.
* **Live-Demo - Automatisiertes Framework (3 Min.):** Ausführung des Skripts `exploit.py` zur sequentiellen Validierung.
* **Fazit & Diskussion (2 Min.):** Zusammenfassung der Erkenntnisse aus der Offensiv-Perspektive.

Sicherer Code-Ausschnitt für app.py:
# Sichere Implementierung mit Parameterized Queries
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
Durch diese Anpassung werden Benutzereingaben strikt als Daten und nicht als ausführbarer SQL-Code behandelt, wodurch jegliche Form von SQL-Injection unmöglich gemacht wird.
