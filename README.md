# Kleiner Docker Service zum überwachen der Netzwerk Latenz

## Setup
1. Docker und Docker Compose installieren.
2. Repository klonen
3. In das Verzeichnis wechseln
4. ggf. Konfiguration in der `docker-compose.yml` anpassen
5. `docker-compose up -d` ausführen
6. Grafana Setup

## Grafana Setup
### Data Source InfluxDB einrichten
1. Im Browser `http://<deine-server-ip>:3000` öffnen
2. Standard Login: admin / admin
3. Neues Passwort setzen
4. Datenquelle hinzufügen:
   - Connections: Data sources: InfluxDB
   - Query Language: Flux
   - URL: `http://influxdb:8086`
   - Schalte Basic Auth aus
   - Bei Organisation, Org-Name aus der `docker-compose.yml` eintragen (`MeineFirma`)
   - Bei Token, den Token aus der `docker-compose.yml` eintragen (`DeinSuperGeheimerAdminTokenFuerDenPinger`)
   - Bei Bucket, den Bucket aus der `docker-compose.yml` eintragen (`latenzmessung`)

### Dashboard importieren
1. Im Browser `http://<deine-server-ip>:3000` öffnen
2. Links im Menü auf Dashboards
3. Dann New -> Import
4. JSON Datei `util/dashboard.json` auswählen und hochladen oder Inhalt der Datei in das Textfeld kopieren
5. Load drücken
6. Bei influxdb die zuvor eingerichtete Data Source auswählen
7. Auf Import drücken

