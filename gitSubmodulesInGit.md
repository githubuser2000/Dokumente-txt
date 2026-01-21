---
generator: Aspose.Words for Java 23.4.0;
---

**Leitfaden: Git Submodules effektiv nutzen**

**​. Einleitung**

​Git Submodules ermöglichen es, ein Git-Repository als Unterverzeichnis
eines anderen Git-Repositorys zu verwalten. Dies ist ideal, um externe
Bibliotheken oder getrennte Projektkomponenten einzubinden, ohne deren
Historie mit der des Hauptprojekts zu vermischen.

**​. Erstellung eines Submodules**

​Um ein neues Submodule hinzuzufügen, nutzt man den Befehl git submodule
add.

\# Syntax: git submodule add \<URL\> \<Pfad\>

git submodule add https://github.com/user/beispiel-repo.git lib/extern

\# Syntax: git submodule add \<URL\> \<Pfad\>

git submodule add https://github.com/user/beispiel-repo.git lib/extern

**Was dabei im Hintergrund passiert:**

- ​**Klonen:** Das Repository wird in den Ordner lib/extern geladen.

- ​**.gitmodules:** Eine Konfigurationsdatei wird erstellt/aktualisiert,
  die Pfad und URL speichert.

- ​**Index:** Das Hauptprojekt registriert den aktuellen Commit-Hash des
  Submodules.

​**Wichtig:** Danach müssen die Änderungen im Hauptprojekt committet
werden:

git add .

git commit -m \"Add submodule in lib/extern\"

**3. Klonen eines Projekts mit Submodules**

​Standardmäßig lädt ein einfaches git clone die Submodule-Inhalte nicht
herunter (die Ordner bleiben leer).

**​Methode A: Direkt beim Klonen**

git clone \--recursive \<URL-Hauptprojekt\>

**Methode B: Nachträglich initialisieren**

​Falls das Projekt bereits ohne die Flags geklont wurde:

git submodule update \--init \--recursive

**4. Workflow im Alltag**

**​Updates vom Submodule-Server beziehen**

​Wenn im entfernten Submodule-Repository neue Commits vorhanden sind:

\# Alle Submodules auf den Stand bringen, der im Hauptprojekt
registriert ist

git submodule update \--remote

**Änderungen im Submodule vornehmen**

​Wenn du Code innerhalb des Submodules bearbeitest, beachte die
**\"Detached HEAD\"** Falle.

1.  ​Wechsel in den Ordner: cd lib/extern

2.  ​Branch auschecken: git checkout main

3.  ​Änderungen vornehmen, committen und **pushen**.

4.  ​Zurück ins Hauptprojekt wechseln und den neuen Stand dort committen.

**​. Wichtige Befehle & Tipps**

|                                      |                                                               |
|--------------------------------------|---------------------------------------------------------------|
| **Befehl**                           | **Beschreibung**                                              |
|                                      |                                                               |
| git submodule status                 | Zeigt den aktuellen Commit-Hash und Status der Submodules.    |
|                                      |                                                               |
| git diff \--submodule                | Zeigt detaillierte Änderungen innerhalb der Submodules an.    |
|                                      |                                                               |
| git submodule foreach \'\<befehl\>\' | Führt einen Befehl (z.B. git status) in allen Submodules aus. |
|                                      |                                                               |

**Die Goldene Regel**

​**Pushe das Submodule immer vor dem Hauptprojekt.** Wenn du im
Hauptprojekt einen Commit-Pointer auf einen Hash setzt, den du im
Submodule noch nicht gepusht hast, können deine Kollegen das Submodule
nicht aktualisieren (Error: \"Reference not found\").

**​. Ein Submodule entfernen**

​Da Git hier sehr gründlich ist, erfolgt das Löschen in mehreren
Schritten:

1.  ​git rm -f \<pfad_zum_submodule\>

2.  ​Den entsprechenden Abschnitt in der .gitmodules löschen.

3.  ​Den entsprechenden Abschnitt in .git/config löschen.

4.  ​Den internen Cache löschen: rm -rf .git/modules/\<name\>

5.  ​Änderungen committen.

​Möchtest du, dass ich dir zusätzlich ein praktisches Bash-Skript
erstelle, das diese Schritte zum Entfernen oder Massen-Update
automatisiert?
