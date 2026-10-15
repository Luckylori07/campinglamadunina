# Camping La Madunina — demo di restyling (Tramontis)

Proposta dimostrativa del nuovo sito di **Camping La Madunina** (Via dei Martiri 12, 21020 Varano Borghi, VA), sulla
sponda del Lago di Comabbio. **Non è la versione ufficiale e non è ancora online**: ogni pagina mostra un banner demo
sticky, una filigrana «DEMO» e la dicitura «proposta di sito realizzata da Tramontis».

Sito originale analizzato: <https://www.campinglamadunina.com/> (sito a frame, con testi in IT/EN/DE/FR, un listino PDF e due cartine).

## Cosa c'è

- **11 pagine × 4 lingue = 44 pagine HTML statiche**: home, il campeggio, sistemazioni, servizi, galleria, prezzi,
  cartina e come arrivare, contatti, FAQ, privacy, note legali.
- Lingue: **italiano (radice `/`), inglese (`/en/`), tedesco (`/de/`), francese (`/fr/`)**, tutte complete.
- Nessuna dipendenza né framework: HTML + CSS + JavaScript nativo, compatibile con GitHub Pages.
- Direzione grafica: palette del lago (verde bosco, salvia, avorio, azzurro acqua, sabbia, accento zafferano),
  titoli in Fraunces e interfaccia in Manrope (auto-ospitati), motivo a «isobate» (curve di livello) e onde.
- Funzioni: header sticky con selettore lingua e CTA, menu mobile animato, hero panoramico, galleria con filtri e
  lightbox accessibile (dialog nativo, tastiera, swipe), listino in tabella accessibile con link al PDF originale,
  FAQ, cartine ufficiali con link alle indicazioni, modulo contatti che **non finge di inviare nulla**
  (prepara un'email nel programma di posta dell'utente), animazioni con `prefers-reduced-motion` rispettato.

## Struttura dei file

```
index.html, campeggio.html, sistemazioni.html, servizi.html, galleria.html,
prezzi.html, cartina.html, contatti.html, faq.html, privacy.html, note-legali.html   ← italiano
en/  de/  fr/                                  ← stesse 11 pagine, stessi nomi di file
assets/
  css/style.css            design system e componenti
  js/main.js               menu, lightbox, filtri, form, lingua preferita
  img/site/                foto autentiche del campeggio (WebP) e cartine ingrandite
  img/lake/                foto del Lago di Comabbio (WebP, 960 e 1920 px)
  img/originals/           file originali scaricati dal sito ufficiale + logo
  img/IMAGE_SOURCES.md     fonti e licenze di ogni immagine
  docs/listino-originale.pdf   copia identica del listino PDF ufficiale
  fonts/                   Fraunces e Manrope (OFL)
tools/
  i18n.py                  TUTTI i testi (una sezione per lingua, stesse chiavi)
  build.py                 genera le 44 pagine da componenti condivisi
  prepare_images.py        ottimizzazione immagini
  check.py, linkcheck.py   controlli: chiavi di traduzione, link/ancore/risorse
```

Le pagine HTML sono **generate**: per cambiare un testo modifica `tools/i18n.py` (o il template in `tools/build.py`)
e rilancia la build. Banner, filigrana, header, footer e sprite icone sono componenti condivisi in `build.py`.

## Esecuzione locale

```bash
python3 -m http.server 8000      # poi apri http://localhost:8000/
# dopo aver modificato testi o template:
python3 -I tools/check.py        # stesse chiavi in tutte le lingue
python3 -I tools/build.py        # rigenera le pagine (serve Pillow: pip install pillow)
python3 -I tools/linkcheck.py    # link interni, ancore, id duplicati, alt, hreflang
```

Il sito funziona anche aprendo i file direttamente, ma il reindirizzamento alla lingua preferita e alcune risorse
si verificano meglio con un server locale.

## Pubblicazione su GitHub Pages (solo dopo autorizzazione)

1. Repository → *Settings → Pages* → *Build and deployment* → *Deploy from a branch* → branch scelto, cartella `/ (root)`.
2. Il file `.nojekyll` è già presente. I percorsi sono relativi, quindi il sito funziona anche in un sotto-percorso
   (`https://utente.github.io/campinglamadunina/`).
3. Facoltativo: `SITE_URL=https://dominio python3 -I tools/build.py` scrive URL assoluti in `hreflang` e Open Graph.

## Banner, filigrana e noindex

La demo è protetta da tre elementi, tutti disattivabili **solo dopo l'approvazione del cliente**:

| Elemento | Come rimuoverlo |
|---|---|
| Banner demo sticky + filigrana «DEMO» | `DEMO=0 python3 -I tools/build.py` (non genera più né banner né filigrana) |
| `<meta name="robots" content="noindex, nofollow">` | `NOINDEX=0 python3 -I tools/build.py`. Da fare **solo alla pubblicazione ufficiale** sul dominio del cliente |
| Dicitura «proposta di sito realizzata da Tramontis» | resta nel footer finché non viene concordato diversamente: chiave `footer.made` in `tools/i18n.py` |

Con `DEMO=0` vanno anche rivisti i testi che parlano di demo: `form.demo`, `gal.note1`, `legal.draft.*`,
`privacy.s6`, `note-legali.s2`, `demo.label`. Se pubblichi online, aggiungi anche un `robots.txt`/sitemap adeguati.

## Stato delle traduzioni

| Lingua | Stato |
|---|---|
| Italiano | completo (testo di riferimento) |
| Inglese | completo: menu, pulsanti, form e messaggi di errore, banner, footer, FAQ, legali |
| Tedesco | completo, come sopra |
| Francese | completo, come sopra |

Le traduzioni sono state scritte per questa demo a partire dai testi ufficiali IT/EN/DE/FR e **vanno riviste da un
madrelingua prima della pubblicazione**, soprattutto le pagine legali. Le voci del listino usano i termini presenti
nel PDF quadrilingue (Adulti/Adult/Erwachsene/Adultes, Piazzola/Platz/Place, ecc.). Il footer e il banner sono
tradotti nelle altre lingue (la dicitura esatta in italiano compare nelle pagine italiane).

## Provenienza dei contenuti e listino

- **Testi su servizi e posizione**: pagine ufficiali IT/EN/DE/FR («main.html»), listino PDF, informazioni e cartina.
- **Listino**: `listino.pdf` (1 pagina A4, creato il 21/02/2024; `listino_eu.pdf` è identico). Voci riportate
  fedelmente: Adulti 8,00 · Bambini 0-12 anni 7,00 · Piazzola 10,00 · Cane 3,00 · Tassa di soggiorno per persona al
  giorno 0,50 · Ospiti (adulti o bambini, oltre 1 ora di campeggio) 7,00 · Docce calde gratuite · piscina compresa
  nelle tariffe · aperto tutto l'anno tranne dal 7 gennaio al 6 febbraio · convenzioni semestrali e annuali · listino
  forfettario a richiesta. **Non è stato possibile verificare che sia ancora in vigore**: la pagina Prezzi lo dichiara
  «da confermare», non aggiunge prezzi, sconti o stagioni e rimanda al PDF originale (copia locale + link ufficiale).
- **Servizi da portali di terzi** (Camping.it, verifica del 16/02/2024; Campeggi.com): camper service, bagni per
  disabili, cani al guinzaglio e solo sulle piazzole, tipologie tenda/camper/roulotte. Sono mostrati con etichetta
  «Portale di terzi · da confermare».
- **Territorio**: Wikipedia (lago di ~3,4 km², ~9 km di rive, 5 comuni, percorso ciclopedonale di ~12 km; la voce è
  priva di fonti) e Wikimedia Commons. **Indirizzo**: confermato su OpenStreetMap (campeggio mappato in Via dei
  Martiri 12).
- **Fonti immagini e licenze**: vedi [`assets/img/IMAGE_SOURCES.md`](assets/img/IMAGE_SOURCES.md).

## Informazioni da confermare con il campeggio

1. **Apertura**: il sito dice «aperto tutto l'anno», il listino «tranne dal 7 gennaio al 6 febbraio».
2. **Tariffe aggiornate**; valuta e unità del listino (il PDF non indica «€» né «a notte»).
3. **Spiaggia riservata sul lago** (citata nei testi ufficiali): accesso, orari, condizioni.
4. **Tipologie di piazzola** (tende/camper/roulotte), numero di piazzole (150 secondo un portale), dimensioni,
   **allacciamenti elettrici** e dotazioni: nessuna fonte ufficiale → omessi.
5. **Bungalow o altri alloggi**: la parola compare solo nelle meta-keywords del vecchio sito; non presentati.
6. Camper service, accessibilità, regole sui cani (solo portali di terzi, dati 2024).
7. Ragione sociale, P. IVA, REA, titolare del trattamento: da inserire in privacy e note legali.
8. Consenso all'uso di nome, logo e fotografie; **originali ad alta risoluzione** delle foto.
9. Logo: la demo propone un marchio ridisegnato; il logo originale è in `assets/img/originals/`.
10. Il fax citato nella cartina ufficiale (0332 960361, stesso numero del telefono) non è stato pubblicato.

## Limitazioni note

- **Foto del campeggio a bassa risoluzione** (max 386×257 px): ingrandite ma morbide. Le foto del lago sono
  illustrative e non mostrano la struttura.
- Nessuna fotografia autentica di tende/camper/roulotte: le categorie usano illustrazioni grafiche dichiarate come tali.
- Nessun sistema di prenotazione né backend: il modulo apre il programma di posta (`mailto:`).
- Nessuna mappa incorporata: si usano le cartine ufficiali + link a Google Maps/OpenStreetMap (nessuna coordinata
  non verificata, nessun cookie di terzi caricato).
- Il selettore lingua porta alla pagina equivalente; la lingua scelta viene ricordata (`localStorage`) e, a una nuova
  visita, si viene portati alla lingua preferita (aggiungendo `?nolang` si disattiva).
- Le skill indicate nel brief sono in `.claude/skills/` (non `claude/skills/`): `frontend-design` è stata applicata;
  per `ui-ux-pro-max` nella repository c'è solo il file `.md` senza lo script `search.py` e i dataset, quindi ne sono
  state applicate le regole (accessibilità, touch target, performance, reduced motion, form) senza interrogare il motore.
  Non sono state trovate altre immagini «titolate» oltre a `logo-camp.jpg`.

## Test eseguiti (Chromium headless con Playwright)

Vedi il report finale in conversazione; sintesi: 220 verifiche pagina×viewport (44 pagine × 375/390/768/1280/1920 px)
senza overflow orizzontale, errori in console, richieste fallite o immagini non caricate; banner, filigrana,
footer Tramontis, `noindex`, `lang` e un solo `h1` presenti ovunque; 50 controlli di interazione (menu mobile,
lingua, galleria/lightbox, form, tastiera, no-JS, reduced motion) superati; `tools/linkcheck.py` senza link rotti.
Non eseguiti: audit Lighthouse, screen reader reali, test su Safari/Firefox e dispositivi fisici.
