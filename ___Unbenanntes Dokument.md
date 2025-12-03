Erkläre mir einfach wie ich Punkt 1 mit Puppet mache

Alles klar – dann machen wir es **so einfach und praxisnah wie möglich**, Schritt für Schritt, wie du **Punkt 1 – Configuration Management – mit Puppet** umsetzt. Keine Theorie, nur das, was du wirklich brauchst.

---

# **Schritt 1: Puppet installieren**

### **Auf dem Server (z. B. Ubuntu/Debian)**

`sudo apt update`  
`sudo apt install puppet-agent`

Auf RedHat/CentOS:

`sudo yum install puppet-agent`

* **Puppet-Agent** ist das Programm, das den Server konfigurieren kann.

* Optional: **Puppet Master** für zentrale Verwaltung, aber für kleine Setups reicht **Standalone Puppet Apply**.

---

# **Schritt 2: Erstelle ein Manifest**

Ein **Manifest** beschreibt den gewünschten Zustand des Systems.  
 Dateiname z. B.: `site.pp`

Beispiel – Nginx installieren und starten:

`package { 'nginx':`  
  `ensure => installed,`  
`}`

`service { 'nginx':`  
  `ensure => running,`  
  `enable => true,`  
`}`

**Erklärung:**

* `package { 'nginx': ensure => installed }` → Paket muss installiert sein.

* `service { 'nginx': ensure => running, enable => true }` → Dienst muss laufen und automatisch starten.

* **Idempotenz:** egal wie oft du das ausführt → System endet immer im selben Zustand.

---

# **Schritt 3: Manifest anwenden**

Mit Puppet-Standalone:

`sudo puppet apply site.pp`

* Puppet vergleicht *Ist-Zustand* mit *Soll-Zustand*.

* Nur die notwendigen Änderungen werden ausgeführt.

* Logs zeigen, was verändert wurde.

---

# **Schritt 4: Optional – Variablen und Bedingungen**

Du kannst dein Manifest anpassen, je nach System:

`if $facts['os']['family'] == 'Debian' {`  
  `package { 'apache2': ensure => installed }`  
`}`

* `$facts['os']['family']` wird automatisch vom Puppet-Agent gesammelt.

* So kannst du dieselben Konfigurationen für verschiedene Systeme wiederverwenden.

---

# **Schritt 5: Prüfen, dass alles stimmt**

`sudo puppet resource package nginx`  
`sudo puppet resource service nginx`

* Prüft, ob Pakete installiert und Dienste aktiv sind.

* Bestätigt, dass Puppet Punkt 1 korrekt umgesetzt hat: **System ist im gewünschten Zustand**.

---

# **Die Essenz von Punkt 1 mit Puppet**

1. Installiere Puppet-Agent

2. Schreibe ein Manifest (`site.pp`) → definiert den *Soll-Zustand*

3. Führe `puppet apply` aus → Puppet bringt den Ist-Zustand in Einklang mit dem Soll-Zustand

4. Prüfe mit `puppet resource` → alles korrekt?

Perfekt – dann erstelle ich ein **komplettes, einfaches Puppet-Manifest**, das **alle wichtigen Basiskonfigurationen für einen frischen Server** übernimmt. Damit siehst du **direkt Punkt 1 (Configuration Management) in Aktion**.

---

# **Mini-Manifest für einen frischen Server**

Dateiname: `base.pp`

`# 1. Updates und Paketmanagement`  
`exec { 'update-system':`  
  `command => '/usr/bin/apt-get update && /usr/bin/apt-get upgrade -y',`  
  `path    => ['/usr/bin', '/usr/sbin'],`  
`}`

`# 2. Basis-Pakete installieren`  
`package { ['vim', 'curl', 'git', 'htop', 'ufw']:`  
  `ensure => installed,`  
`}`

`# 3. Benutzer anlegen`  
`user { 'deploy':`  
  `ensure     => present,`  
  `managehome => true,`  
  `shell      => '/bin/bash',`  
  `password   => '!!changeme!!', # Passwort später ändern`  
`}`

`# 4. SSH-Keys für Benutzer`  
`file { '/home/deploy/.ssh':`  
  `ensure  => directory,`  
  `owner   => 'deploy',`  
  `group   => 'deploy',`  
  `mode    => '0700',`  
`}`

`file { '/home/deploy/.ssh/authorized_keys':`  
  `ensure  => present,`  
  `owner   => 'deploy',`  
  `group   => 'deploy',`  
  `mode    => '0600',`  
  `content => "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...yourkeyhere...",`  
`}`

`# 5. Firewall (UFW) konfigurieren`  
`exec { 'enable-ufw':`  
  `command => '/usr/sbin/ufw allow ssh && /usr/sbin/ufw enable',`  
  `path    => ['/usr/bin', '/usr/sbin'],`  
  `unless  => '/usr/sbin/ufw status | grep -q "Status: active"',`  
`}`

`# 6. Nginx installieren und starten`  
`package { 'nginx':`  
  `ensure => installed,`  
`}`

`service { 'nginx':`  
  `ensure => running,`  
  `enable => true,`  
`}`

`# 7. Zeitzone setzen`  
`exec { 'set-timezone':`  
  `command => '/usr/bin/timedatectl set-timezone Europe/Berlin',`  
  `path    => ['/usr/bin', '/usr/sbin'],`  
  `unless  => '/usr/bin/timedatectl | grep -q "Europe/Berlin"',`  
`}`

---

# **So wendest du das Manifest an**

1. Manifest auf den Server kopieren:

`scp base.pp user@server:/tmp/base.pp`

2. Manifest ausführen:

`sudo puppet apply /tmp/base.pp`

3. Puppet prüft **alle Ressourcen** und bringt den Server in den gewünschten Zustand.

---

# **Was dieses Manifest abdeckt (Punkt 1\)**

* Systemupdates & Paketmanagement ✅

* Basis-Tools installieren ✅

* Benutzerverwaltung & SSH-Zugang ✅

* Firewall aktivieren ✅

* Webserver (Nginx) starten ✅

* Zeitzone korrekt einstellen ✅

Alles ist **idempotent** – wenn du das Manifest nochmal ausführst, passiert nichts Neues, der Zustand bleibt konsistent.

# **1\. Multi-Server Setup mit Puppet Apply (Agentless / Bolt-Style)**

Wenn du keinen Puppet Master nutzen willst, kannst du **`puppet apply`** auf jedem Server ausführen.

* Erstelle eine **Liste deiner Server**:

`servers=("server1.example.com" "server2.example.com" "server3.example.com")`

* Kopiere das Manifest auf alle Server:

`for s in "${servers[@]}"; do`  
    `scp base.pp user@$s:/tmp/base.pp`  
`done`

* Führe das Manifest auf allen Servern aus:

`for s in "${servers[@]}"; do`  
    `ssh user@$s "sudo puppet apply /tmp/base.pp"`  
`done`

**Erklärung:**

* Jeder Server wird **unabhängig auf den gewünschten Zustand gebracht**.

* Idempotenz sorgt dafür, dass **keine Konflikte oder Duplikate** entstehen.

* Du hast damit eine **Mini-Orchestrierung**, die Punkt 1 auf Cluster-Ebene abdeckt.

---

# **2\. Mit Puppet Bolt – einfacher und professioneller**

Puppet Bolt ist ein **agentenloses Tool**, ideal für kleine Multi-Server-Szenarien.

1. Installiere Bolt:

`sudo apt install puppet-bolt`

2. Erstelle ein **Inventory** (z. B. `inventory.yaml`):

`targets:`  
  `- server1.example.com`  
  `- server2.example.com`  
  `- server3.example.com`  
`config:`  
  `ssh:`  
    `user: deploy`  
    `password: 'changeme'`

3. Führe das Manifest auf allen Servern aus:

`bolt apply /tmp/base.pp --targets all`

**Vorteile:**

* Keine Agenten notwendig

* Parallele Ausführung

* Einfache Inventarverwaltung

* Rollouts auf beliebig viele Server

---

# **3\. Skalierbare Struktur**

Wenn du viele Server hast:

* **Modularisiere dein Manifest**:

`manifests/`  
  `base.pp        # Basis-System`  
  `nginx.pp       # Webserver`  
  `users.pp       # Benutzer & SSH`  
  `firewall.pp    # Firewall`  
`site.pp          # inkludiert alle Module`

*   
* **site.pp**

`include base`  
`include nginx`  
`include users`  
`include firewall`

* Puppet übernimmt dann **alle Abhängigkeiten automatisch**.

# **4\. Zusammenfassung Multi-Server Punkt 1**

* Manifest \= *Soll-Zustand definieren*

* Puppet Apply / Bolt \= *Ist-Zustand angleichen*

* Idempotent \= *wiederholbar, ohne Schaden*

* Modular \= *leicht erweiterbar auf viele Server*

* Ergebnis \= **alle Server im gewünschten Zustand, automatisch verwaltet**

# **1\. Idee der Pipeline**

* Neue Server kommen ins Netzwerk / Cloud

* Pipeline erkennt neue Hosts (oder wird manuell getriggert)

* Manifest wird automatisch auf den Servern ausgeführt

* Idempotenz sorgt für sicheren, wiederholbaren Rollout

**Tools:**

* Git (für Versionierung der Puppet-Manifest-Dateien)

* Puppet (für Configuration Management)

* Optional Puppet Bolt (für Agentless-Ausführung)

* Cron / CI-Runner (für Automatisierung)

---

# **2\. Schritt 1 – Puppet-Manifeste versionieren**

* Erstelle ein Git-Repository für deine Puppet-Manifeste:

`git init puppet-config`  
`cd puppet-config`  
`mkdir manifests`

* Verschiebe dein `base.pp` \+ Module hinein:

`manifests/base.pp`  
`manifests/nginx.pp`  
`manifests/users.pp`  
`manifests/firewall.pp`

* Erstelle `site.pp`:

`include base`  
`include nginx`  
`include users`  
`include firewall`

* Committe alles:

`git add .`  
`git commit -m "Initial Puppet Manifests"`

---

# **3\. Schritt 2 – CI/CD Runner vorbereiten**

* Auf einem **Management-Server**:

  * Installiere Puppet / Puppet Bolt

  * Installiere Git

  * Optional: Cron oder GitHub Actions / GitLab Runner

**Beispiel Cron-Job (alle 10 Minuten prüfen & anwenden):**

`*/10 * * * * cd /opt/puppet-config && git pull && bolt apply manifests/site.pp --targets all`

**Erklärung:**

* `git pull` → zieht neue Manifest-Versionen

* `bolt apply` → führt die aktuelle Konfiguration auf allen Servern aus

* Idempotent → nur neue Änderungen werden angewendet

---

# **4\. Schritt 3 – Neue Server automatisch hinzufügen**

* Bolt Inventory (`inventory.yaml`) kann dynamisch sein:

`targets:`  
  `- server1.example.com`  
  `- server2.example.com`  
  `- server3.example.com`  
`config:`  
  `ssh:`  
    `user: deploy`  
    `private-key: /home/ci/.ssh/id_rsa`

* Für neue Server:

  * IP oder Hostname ins Inventory eintragen

  * Cron/Runner führt Manifest automatisch aus

Alternativ: dynamisches Inventory aus Cloud-API (AWS, GCP, Azure) → CI/CD erkennt automatisch neue Instanzen.

---

# **5\. Schritt 4 – Rollback / Versionierung**

* Alle Manifest-Versionen sind im Git gespeichert

* Änderungen werden durch Commit nachvollziehbar

* Bei Fehlern: `git checkout <alte-version>` und Bolt erneut ausführen → Rollback funktioniert **sicher**.

---

# **6\. Schritt 5 – Optional: Notification / Logging**

* Puppet / Bolt erzeugt Logs über Änderungen

* Cron-Job kann Ergebnisse per Mail oder Slack versenden:

`bolt apply manifests/site.pp --targets all | tee /var/log/puppet-bolt.log`

* So siehst du **immer, welche Änderungen gemacht wurden**.

---

# **7\. Ergebnis**

* Neue Server → einfach ins Inventory aufnehmen

* Pipeline → automatisch Manifest anwenden

* Alle Server → immer im gewünschten Zustand

* Vollständig wiederholbar & transparent

* Kleine CI/CD-Lösung ohne Master Puppet, einfach, effektiv

# **1\. Verzeichnisstruktur**

`/opt/puppet-config/`  
`├── manifests/`  
`│   ├── base.pp`  
`│   ├── nginx.pp`  
`│   ├── users.pp`  
`│   ├── firewall.pp`  
`│   └── site.pp`  
`├── inventory.yaml`  
`└── run.sh`

---

# **2\. Manifest-Beispiele**

**base.pp**

`# Updates und Basis-Pakete`  
`exec { 'update-system':`  
  `command => '/usr/bin/apt-get update && /usr/bin/apt-get upgrade -y',`  
  `path    => ['/usr/bin', '/usr/sbin'],`  
`}`

`package { ['vim', 'curl', 'git', 'htop', 'ufw']:`  
  `ensure => installed,`  
`}`

**nginx.pp**

`package { 'nginx':`  
  `ensure => installed,`  
`}`

`service { 'nginx':`  
  `ensure => running,`  
  `enable => true,`  
`}`

**users.pp**

`user { 'deploy':`  
  `ensure     => present,`  
  `managehome => true,`  
  `shell      => '/bin/bash',`  
`}`

`file { '/home/deploy/.ssh':`  
  `ensure  => directory,`  
  `owner   => 'deploy',`  
  `group   => 'deploy',`  
  `mode    => '0700',`  
`}`

`file { '/home/deploy/.ssh/authorized_keys':`  
  `ensure  => present,`  
  `owner   => 'deploy',`  
  `group   => 'deploy',`  
  `mode    => '0600',`  
  `content => "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...yourkeyhere...",`  
`}`

**firewall.pp**

`exec { 'enable-ufw':`  
  `command => '/usr/sbin/ufw allow ssh && /usr/sbin/ufw enable',`  
  `path    => ['/usr/bin', '/usr/sbin'],`  
  `unless  => '/usr/sbin/ufw status | grep -q "Status: active"',`  
`}`

**site.pp**

`include base`  
`include nginx`  
`include users`  
`include firewall`

---

# **3\. Inventory**

`inventory.yaml`

`targets:`  
  `- server1.example.com`  
  `- server2.example.com`  
  `- server3.example.com`  
`config:`  
  `ssh:`  
    `user: deploy`  
    `private-key: /home/ci/.ssh/id_rsa`

* Neue Server einfach hier hinzufügen, z. B. `server4.example.com`.

---

# **4\. Automatisches Deployment-Skript**

`run.sh`

`#!/bin/bash`  
`# Wechsle ins Repo-Verzeichnis`  
`cd /opt/puppet-config || exit`

`# Aktuellste Version aus Git ziehen`  
`git pull`

`# Puppet Bolt ausführen auf allen Servern`  
`bolt apply manifests/site.pp --targets all --no-host-key-check`

`# Ergebnis ins Log schreiben`  
`echo "$(date): Deployment completed" >> /var/log/puppet-deploy.log`

* Mach das Skript ausführbar:

`chmod +x /opt/puppet-config/run.sh`

---

# **5\. Automatisierung via Cron**

Cronjob, z. B. alle 10 Minuten prüfen:

`*/10 * * * * /opt/puppet-config/run.sh`

* Alle Änderungen werden automatisch auf allen Servern angewendet

* Idempotenz sorgt dafür, dass **keine doppelten Änderungen** passieren

---

# **6\. Vorgehensweise für neue Server**

1. Neuen Server bereitstellen (OS \+ SSH-Zugang)

2. Hostname / IP zum `inventory.yaml` hinzufügen

3. Cronjob oder manuelles `run.sh` → Manifest läuft automatisch

4. Server ist fertig konfiguriert, Nginx läuft, Firewall aktiv, Benutzer eingerichtet

---

# **✅ Ergebnis**

* Vollautomatische, wiederholbare Konfiguration (Punkt 1\)

* Unterstützt **beliebig viele Server**

* Versionierung durch Git

* Logs für Überwachung

* Einfach zu erweitern (Module hinzufügen, neue Rollen definieren)

