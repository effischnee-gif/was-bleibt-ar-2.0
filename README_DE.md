# „Was bleibt“ – AR-Webseite

Diese kleine WebAR-Seite verwendet:

- MindAR für die Bilderkennung
- A-Frame für die 3-D-Szene
- `targets.mind` als Bild-Target
- `Muelltuete_AR_Artivive.glb` als 3-D-Modell

## Dateien

- `index.html` – die komplette AR-Webseite
- `targets.mind` – dein kompiliertes Foto-Target
- `Muelltuete_AR_Artivive.glb` – das 3-D-Modell
- `.nojekyll` – verhindert eine unnötige Jekyll-Verarbeitung bei GitHub Pages

## Veröffentlichung mit GitHub Pages

1. Bei GitHub ein kostenloses Konto anlegen bzw. anmelden.
2. Ein neues Repository erstellen, z. B. `was-bleibt-ar`.
3. Das Repository auf **Public** stellen.
4. Diese vier Dateien in das Repository hochladen.
5. Unter **Settings → Pages** bei **Build and deployment → Source**
   „Deploy from a branch“ auswählen.
6. Als Branch `main` und als Ordner `/ (root)` auswählen und speichern.
7. Nach der Veröffentlichung erscheint die Webseite unter einer Adresse
   ähnlich wie:
   `https://DEINUSERNAME.github.io/was-bleibt-ar/`

## Wichtig

Die AR-Kamera funktioniert nur über eine sichere Webadresse (HTTPS).
GitHub Pages stellt die Seite über HTTPS bereit.

Die Seite benötigt keine eigene App. Besucher öffnen einfach die Webadresse
auf ihrem Smartphone und erlauben den Kamerazugriff.

## Für die Ausstellung

Am besten liegt neben dem Foto ein kurzer Hinweis:

„Kamera auf das Bild richten.
QR-Code scannen und die Mülltüte zum Leben erwecken.“

Nach dem erfolgreichen Test kann aus der GitHub-Pages-Adresse ein QR-Code
für die Wandbeschriftung erzeugt werden.
