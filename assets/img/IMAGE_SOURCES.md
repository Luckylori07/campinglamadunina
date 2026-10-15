# Fonti e licenze delle immagini

Ultimo controllo: 15 ottobre 2026. Le immagini originali sono state scaricate e ottimizzate (WebP) con `tools/prepare_images.py`.

## 1. Fotografie del campeggio (sito ufficiale)

Provenienza: <https://www.campinglamadunina.com/> (cartelle `imm/` e `imm/piccole/`). Sono le uniche fotografie
autentiche della struttura che il sito ufficiale pubblica. **Condizioni d'uso: non dichiarate dal sito.** Sono usate
in questa demo solo per mostrare al titolare come potrebbe apparire il nuovo sito; prima della pubblicazione serve il
suo consenso e, meglio, la fornitura degli originali ad alta risoluzione.

**Limite tecnico:** gli originali sono molto piccoli (da 179×120 a 386×257 px) e quattro hanno una cornice blu
sfumata, che è stata ritagliata. Le versioni in `assets/img/site/` sono state ingrandite 2–4× (Lanczos + nitidezza
leggera) senza aggiungere dettagli: restano visibilmente morbide se mostrate in grande.

| File usato | Originale (in `assets/img/originals/`) | Didascalia del sito | Note |
|---|---|---|---|
| `site/ingresso.webp` | `ingresso.jpg` (386×257) | L'Ingresso | |
| `site/piazzetta.webp` | `thumbs/la-piazzetta.jpg` (179×119) | La Piazzetta | |
| `site/piazzole.webp` | `thumbs/Le-piazzole.jpg` (179×119) | Le Piazzole | |
| `site/piscina.webp` | `la-Piscina.jpg` (249×150) | La Piscina | cornice ritagliata |
| `site/ristorante.webp` | `thumbs/Il-ristorante.jpg` (179×120) | Il Ristorante | cornice ritagliata |
| `site/servizi-igienici.webp` | `thumbs/bagno.jpg` (179×120) | I Servizi | cornice ritagliata |
| `site/serata-pista.webp` | `thumbs/giochi.jpg` (179×119) | Discoteca | didascalia del sito: «Discoteca»; mostrata come «Serata sulla pista da ballo» |
| `site/pista-ciclabile.webp` | `thumbs/Il-lago.jpg` (170×120) | Pista ciclabile | |
| `site/tramonto.webp` | `tramonto-su-lago.jpg` (249×150) | Tramonto sul Lago | cornice ritagliata |
| `site/cartina-zona.webp` | `cartina.gif` (380×380) | cartina ufficiale | ingrandita 2× |
| `site/cartina-dettaglio.webp` | `cartina2p.jpg` (215×180) | schema stradale ufficiale | ingrandito 3× |

Il logo `logo-camp.jpg` (fornito nella repository, 128×94) e `imm/logo.gif` (logotipo originale) sono conservati
in `assets/img/originals/`. L'header della demo usa un marchio ridisegnato (tenda + onde, SVG) come proposta di
restyling: l'uso del logo originale va deciso con il cliente.

## 2. Fotografie del Lago di Comabbio (Wikimedia Commons)

Immagini **illustrative**: mostrano il lago, non la struttura, e nel sito sono sempre etichettate come tali.
Licenze verificate sulle pagine dei file il 15/10/2026 (CC0, CC BY, CC BY-SA, pubblico dominio). Le licenze
CC BY / CC BY-SA richiedono l'indicazione dell'autore (presente in didascalia e in «Note legali»); CC BY-SA
richiede inoltre che eventuali opere derivate (ridimensionamenti/ritagli inclusi) siano rilasciate con la stessa
licenza.

| File | Titolo su Commons | Autore | Licenza | Fonte | Uso |
|---|---|---|---|---|---|
| `assets/img/lake/veduta-aerea-{960,1920}.webp` | Aerial photograph of Lago di Comabbio.jpg | Yair-haklai | CC BY-SA 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Aerial_photograph_of_Lago_di_Comabbio.jpg) | Hero cartina, «Il campeggio», galleria |
| `assets/img/lake/passerella-lago-{960,1920}.webp` | Boardwalk on Lago di Comabbio.jpg | Kaitu | CC0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Boardwalk_on_Lago_di_Comabbio.jpg) | Home (natura), galleria |
| `assets/img/lake/canne-ninfee-{960,1920}.webp` | CANNE E NINFEE NEL LAGO DI COMABBIO.jpg | Monica Rondoni | CC0 | [pagina del file](https://commons.wikimedia.org/wiki/File:CANNE_E_NINFEE_NEL_LAGO_DI_COMABBIO.jpg) | Hero prezzi |
| `assets/img/lake/cigni-pontile-{960,1920}.webp` | Cigni sul Lago di Comabbio.jpg | Riccardo Ortelli | CC BY-SA 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Cigni_sul_Lago_di_Comabbio.jpg) | Hero contatti, galleria |
| `assets/img/lake/riflesso-colline-{960,1920}.webp` | Lago Comabbio - riflesso 1.jpg | Riccardo Ortelli | CC BY-SA 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Lago_Comabbio_-_riflesso_1.jpg) | Hero «Il campeggio», galleria |
| `assets/img/lake/salice-lago-{960,1920}.webp` | Lago di Comabbio (4882917585).jpg | Grzegorz Jereczek from Gdańsk, Poland | CC BY-SA 2.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Lago_di_Comabbio_(4882917585).jpg) | Hero sistemazioni, galleria |
| `assets/img/lake/lago-sponda-fiorita-{960,1920}.webp` | Lago di Comabbio (4882918177).jpg | Grzegorz Jereczek from Gdańsk, Poland | CC BY-SA 2.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Lago_di_Comabbio_(4882918177).jpg) | Home (hero), galleria |
| `assets/img/lake/alba-lago-{960,1920}.webp` | Lago di Comabbio.JPG | No machine-readable author provided. Bol2030 assumed (based on copyright claims). | Public domain | [pagina del file](https://commons.wikimedia.org/wiki/File:Lago_di_Comabbio.JPG) | Hero galleria |
| `assets/img/lake/ninfee-lago-{960,1920}.webp` | Lake Comabbio.jpg | Mangled Cab | CC BY-SA 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Lake_Comabbio.jpg) | Hero servizi, galleria |
| `assets/img/lake/tramonto-cigno-{960,1920}.webp` | Queen of the Lake - regina del lago al tramonto.jpg | Mikartphotographer | CC BY-SA 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Queen_of_the_Lake_-_regina_del_lago_al_tramonto.jpg) | CTA finale, galleria |
| `assets/img/lake/passerella-ternate-{960,1920}.webp` | Ternate - Lago di Comabbio.jpg | Mario Falcetti | CC BY 4.0 | [pagina del file](https://commons.wikimedia.org/wiki/File:Ternate_-_Lago_di_Comabbio.jpg) | Hero FAQ, galleria |

## 3. Altro

- Font: Fraunces e Manrope (SIL Open Font License 1.1), in `assets/fonts/` (build da `@fontsource-variable`).
- Icone: SVG disegnate per questo progetto (sprite inline), nessuna libreria.
- Motivo «isobate» (`assets/img/contour.svg`) e favicon: generati per il progetto.

## 4. Fonti cercate e non utilizzate

Portali turistici (Camping.it, Campeggi.com, park4night, Tripadvisor) e Google Immagini mostrano foto di terzi o
del campeggio con licenza non chiara: non sono state scaricate né riutilizzate.
