# Datasommer-2024

Repo som skal brukes som demo for å innføre datastudentene i datariggen de skal bruke i sommer. Utfyllende informasjon om temaene i denne demoen kan man finne på https://docs.knada.io/

## Innhold

### BigQuery
**Hva er BigQuery?**
[BigQuery](https://console.cloud.google.com/bigquery) er den tilhørende databaseløsningen til Google Cloud Platform (GCP) og er den som oftes brukes for å dele dataprodukter internt eller på tvers av team. BigQuery fungerer sømløst med tilgangsstyringen i CGP og sørger for at du kan kjøre SQL-spørringer mot databasene du har tilgang til. Du kan enten gjøre spørringer direkte i [konsollen](https://console.cloud.google.com/bigquery), eller du kan koble deg til BigQuery med en database-connection i for eksempel Python.

### KnadaVM / GCP VM
**Hva er KnadaVM?**
Fordi vi ofte jobber med sensitiv data som ikke skal leve på enkeltes lokalmaskiner eller fordi vi trenger mer utregningsressurser enn det vi har lokalt, så utvikler vi mest i KnadaVM. KnadaVM er en virtuell maskin som hostes av GCP. Vm-en har begrensede tilganger til adresser på nettet, men hvor det er mulig å be om åpninger til det man anser som viktig for å få gjort det man skal. KnadaVM har for eksempel åpning mot databasene vi bruker, mot pypi, mot github og flere andre kilder som man finner i dokumentasjonen på [Nada sin docs](https://docs.knada.io/analyse/allowlisting/).

Private VM-er for bruk til individuell utforskning og utvikling opprettes på [Knorten](https://knorten.knada.io/oversikt). For å opprette en kraftigere maskin for kjøring av maskinlæring kan man ta kontakt med leder, NADA eller opprette det selv i GCP. Pass på at du har tillatelse til det fra team eller leder før du oppretter det selv, da det er kostnad knyttet til å opprette kraftigere VM-er.

#### Spilleregler på KnadaVM
- Opprett og bruk virtuelle maskiner eller databaser med lokasjonen **europe-north1**. Dette er fordi vi ikke kan lagre data i alle land, for eksempel USA.
- Hold VM-et oppdatert. 
```
aptitude update

aptitude full-upgrade
```
- Hold python-pakker oppdatert. Bruk gjerne en requirements.txt fil sammen med [Dependabot](https://docs.github.com/en/code-security/dependabot).
```
pip list --outdated
pip install [package_name] --upgrade
```
- Både kjøring av kode og det å ha en VM slått på koster penger. Vær bevisst på dette ved kjøring av tunge beregninger og ved lengre opphold uten bruk av VM-en. Lag deg en vane for å slå av VM-en på slutten av dagen eller i helgen hvis den ikke trenger å stå på for å kjøre kode. Det kan gjøres i [Google Cloud Console](https://console.cloud.google.com/compute).


### Secret Manager
**Hva er secret manager?**
En secret manager brukes for å lagre brukernavn, passord og api-nøkler, enten personlig eller på tvers av teamet. Bruk av en secret manager hindrer at slike ting lever utrygt i koden. Vi bruker secret manager for å logge inn på databaser eller for autentisere oss opp mot forskjellige api-er eller mot datamarkedsplassen. Secret manager kan også spore bruk av hemmeligheter slik at man har oversikt over hvem som har gjort spørringer eller tatt i bruk api.

I NAV er det vanligst å bruke [Google Cloud Secret Manager](https://console.cloud.google.com/security/secret-manager).



### Datafortellinger
**Hva er en datafortelling?**
I NAV bruker vi datafortellinger for å formidle innsikt vi finner i daten slik at verdien eller kunnskapen vi finner blir delt med andre. Datafortellinger er enkle statiske nettsider som kan inneholde interaktive komponenter som plott og kode sammen med forklarende tekst. Her kan du finne den mest hensiktsmessige måten å formidle dine data og funn. Når en datafortelling er klar for å deles med NAV kan den publiseres til [datamarkedsplassen](https://data.ansatt.nav.no/). Det finnes mange enkle verktøy for å produsere nettsider som kan publiseres som datafortellinger, men det vanligste er programmet [Quarto](https://quarto.org/).

#### Quarto
Quarto kan produsere nettsider, dashboards og presentasjoner ved å bruke jupyter notebooks eller ved hjelp av pandoc markdown og kodesnutter. Du kan skrive kode for å lage dynamisk innhold i enten python, R, Julia eller Observable JS. Quarto kan integreres med VS Code ved hjelp av en extension.

For å laste ned Quarto, gå til https://quarto.org/docs/download/tarball.html

### Airflow
**Hva er airflow?**
Datafortellinger er statiske html-nettsted, som vil si at koden for å generer html-en, kun kjøres før nettstedet blir publisert. Det går ann å ha kodesnutter som kjører når nettstedet blir åpnet, men av sikkerhetsårsaker er det ikke mulig å for eksempel hente ny data fra NAV sine databaser. Airflow er et verktøy som kan brukes for å sørge for at tall og grafer, eller dataen de er basert på, kan oppdateres jevnlig. Airflow brukes for å skedulere en kjøring av koden som brukes for å hente dataen og oppdatere grafene slik at vi alltid kan få de nyeste tallene. Ved hjelp av airflow kan man bestemme selv hvor ofte man skal oppdatere datafortellingene.

Rent praktisk fungerer airflow veldig likt som en VM. Airflow spinner opp en kjøring av koden din i en pod som genererer html-siden på nytt. Dette fører til at spørringene og plottene dine henter og baserer seg på den nyeste dataen tilgjengelig. 
