"""Generates the Billow landing page in five languages into billow-site/."""
import hashlib
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from theme_css import theme_aware

SITE = pathlib.Path(sys.argv[1])
STYLE = theme_aware(pathlib.Path(sys.argv[2]).read_text())
BASE = "https://billow-app.org/"
DEMO_VER = hashlib.sha1((SITE / "demo.js").read_bytes()).hexdigest()[:8]
THEME_VER = hashlib.sha1((SITE / "theme.js").read_bytes()).hexdigest()[:8]
CONTACT_VER = hashlib.sha1((SITE / "contact.js").read_bytes()).hexdigest()[:8]
GALLERY_VER = hashlib.sha1((SITE / "gallery.js").read_bytes()).hexdigest()[:8]

LANGS = ["en", "de", "es", "it", "sq"]
NAMES = {"en": "English", "de": "Deutsch", "es": "Español", "it": "Italiano", "sq": "Shqip"}
OG = {"en": "en_US", "de": "de_DE", "es": "es_ES", "it": "it_IT", "sq": "sq_AL"}

T = {
"en": dict(
  title="Billow — Subscription Tracker",
  desc="Track every subscription, renewal and free trial on your iPhone. Know what leaves your account before payday. No account, no bank login, private in your iCloud.",
  og="Know what leaves your account before payday.",
  nav_features="Features", nav_privacy="Privacy", nav_support="Support", lang_label="Language",
  h1a="Know what leaves your account", h1b="before payday.",
  lead="Billow tracks every subscription, renewal and free trial, and warns you before money goes out.",
  badge="Coming soon to the App Store",
  pills=["No account", "No bank login", "Private in iCloud", "No ads or tracking"],
  alt_home="Billow home screen with monthly total, upcoming renewals and attention cards",
  s1=("Every detail", "See exactly what each one costs you.",
      "Every subscription shows its real cost per day and per year, a price-history chart that flags every increase, and the full billing history.",
      ["Cost per day, month and year, in your home currency", "Price history with every increase marked", "Mark paid, pause, snooze or cancel in one tap"],
      "Disney+ detail with price history showing a rise from $13.99 to $16.99"),
  s2=("Payday planner", "Plan around the day you get paid.",
      "The calendar shows daily totals, marks your payday and tells you exactly what leaves your account before the next one, with 3, 6 and 12-month forecasts.",
      ["Month grid with daily totals", "“Before payday” total that updates as charges land", "Forecasts for the months ahead"],
      "Calendar with daily totals and payday marker"),
  s3=("Trials & price hikes", "Never pay for a trial you forgot.",
      "Add a free trial and Billow sets a {tag} deadline a day before it converts, with a Live Activity countdown on your Lock Screen. Price changes and forgotten subscriptions get flagged too.",
      ["Time Sensitive reminders before a trial converts", "Alerts when a price goes up", "“Still using this?” check-ins and duplicate detection"],
      "Billow welcome screen"),
  tag="cancel by",
  s4=("Add in seconds", "Share a receipt. Billow does the rest.",
      "Search 500+ known services, or share a receipt, screenshot, PDF or bank statement. Billow finds the recurring charges on your iPhone and explains why it thinks each one repeats.",
      ["500+ services with logos, plans and billing cycles", "Import from receipts and bank statements, on device", "Home Screen, Lock Screen and StandBy widgets"],
      "Adding a subscription from the merchant catalog"),
  gallery="A closer look", caps=["Welcome", "Home", "Calendar", "Detail", "Add"],
  priv_h="Private by design",
  priv_sub="Billow has no account, no server and no analytics. Your subscriptions stay on your iPhone and in your own iCloud.",
  tiles=[("No account", "Open the app and start. Nothing to sign up for."),
         ("No bank login", "Statements you share are read on your iPhone."),
         ("Your iCloud", "Synced through your private iCloud database."),
         ("No tracking", "No ads, no analytics, no third-party SDKs.")],
  langs_h="Made for five languages and every currency",
  logos_by="Merchant logos by", privacy_policy="Privacy Policy",
),
"de": dict(
  title="Billow — Abo-Tracker",
  desc="Behalte jedes Abo, jede Verlängerung und jede Testphase auf deinem iPhone im Blick. Wisse vor dem Zahltag, was von deinem Konto abgeht. Kein Konto, kein Bank-Login, privat in deiner iCloud.",
  og="Wisse vor dem Zahltag, was von deinem Konto abgeht.",
  nav_features="Funktionen", nav_privacy="Datenschutz", nav_support="Support", lang_label="Sprache",
  h1a="Wisse, was von deinem Konto abgeht –", h1b="vor dem Zahltag.",
  lead="Billow behält jedes Abo, jede Verlängerung und jede Testphase im Blick und warnt dich, bevor Geld abgebucht wird.",
  badge="Bald im App Store",
  pills=["Kein Konto", "Kein Bank-Login", "Privat in iCloud", "Keine Werbung, kein Tracking"],
  alt_home="Billow-Startbildschirm mit Monatssumme, anstehenden Verlängerungen und Hinweiskarten",
  s1=("Jedes Detail", "Sieh genau, was dich jedes Abo kostet.",
      "Jedes Abo zeigt seine echten Kosten pro Tag und Jahr, einen Preisverlauf, der jede Erhöhung markiert, und den kompletten Abbuchungsverlauf.",
      ["Kosten pro Tag, Monat und Jahr in deiner Hauptwährung", "Preisverlauf mit jeder Erhöhung markiert", "Als bezahlt markieren, pausieren, verschieben oder kündigen – mit einem Tipp"],
      "Disney+-Details mit Preisverlauf von 13,99 $ auf 16,99 $"),
  s2=("Zahltag-Planer", "Plane rund um deinen Zahltag.",
      "Der Kalender zeigt Tagessummen, markiert deinen Zahltag und sagt dir genau, was vor dem nächsten von deinem Konto abgeht – mit Prognosen für 3, 6 und 12 Monate.",
      ["Monatsansicht mit Tagessummen", "Summe „vor dem Zahltag“, die sich mit jeder Abbuchung aktualisiert", "Prognosen für die kommenden Monate"],
      "Kalender mit Tagessummen und Zahltag-Markierung"),
  s3=("Testphasen & Preiserhöhungen", "Zahl nie wieder für eine vergessene Testphase.",
      "Füge eine Testphase hinzu und Billow setzt einen Tag vor der Umwandlung eine Frist „{tag}“ – mit Live-Activity-Countdown auf deinem Sperrbildschirm. Auch Preisänderungen und vergessene Abos werden markiert.",
      ["Dringende Erinnerungen, bevor eine Testphase umgewandelt wird", "Hinweise, wenn ein Preis steigt", "„Nutzt du das noch?“-Abfragen und Duplikaterkennung"],
      "Billow-Willkommensbildschirm"),
  tag="Kündigen bis",
  s4=("In Sekunden hinzugefügt", "Beleg teilen. Billow erledigt den Rest.",
      "Durchsuche über 500 bekannte Dienste oder teile einen Beleg, Screenshot, ein PDF oder einen Kontoauszug. Billow findet die wiederkehrenden Abbuchungen auf deinem iPhone und erklärt, warum es sie für wiederkehrend hält.",
      ["Über 500 Dienste mit Logos, Tarifen und Abrechnungszyklen", "Import aus Belegen und Kontoauszügen, direkt auf dem Gerät", "Widgets für Home-Bildschirm, Sperrbildschirm und StandBy"],
      "Abo aus dem Händlerkatalog hinzufügen"),
  gallery="Ein genauerer Blick", caps=["Willkommen", "Start", "Kalender", "Details", "Hinzufügen"],
  priv_h="Datenschutz von Anfang an",
  priv_sub="Billow hat kein Konto, keinen Server und keine Analyse-Tools. Deine Abos bleiben auf deinem iPhone und in deiner eigenen iCloud.",
  tiles=[("Kein Konto", "App öffnen und loslegen. Keine Registrierung."),
         ("Kein Bank-Login", "Geteilte Kontoauszüge werden auf deinem iPhone gelesen."),
         ("Deine iCloud", "Synchronisiert über deine private iCloud-Datenbank."),
         ("Kein Tracking", "Keine Werbung, keine Analyse, keine Drittanbieter-SDKs.")],
  langs_h="Gemacht für fünf Sprachen und jede Währung",
  logos_by="Händlerlogos von", privacy_policy="Datenschutzerklärung",
),
"es": dict(
  title="Billow — Control de suscripciones",
  desc="Controla cada suscripción, renovación y prueba gratuita en tu iPhone. Sabe qué sale de tu cuenta antes del día de cobro. Sin cuenta, sin acceso bancario, privado en tu iCloud.",
  og="Sabe qué sale de tu cuenta antes del día de cobro.",
  nav_features="Funciones", nav_privacy="Privacidad", nav_support="Soporte", lang_label="Idioma",
  h1a="Sabe qué sale de tu cuenta", h1b="antes del día de cobro.",
  lead="Billow controla cada suscripción, renovación y prueba gratuita, y te avisa antes de que salga el dinero.",
  badge="Próximamente en el App Store",
  pills=["Sin cuenta", "Sin acceso bancario", "Privado en iCloud", "Sin anuncios ni rastreo"],
  alt_home="Pantalla de inicio de Billow con el total mensual, próximas renovaciones y avisos",
  s1=("Cada detalle", "Mira exactamente cuánto te cuesta cada una.",
      "Cada suscripción muestra su coste real por día y por año, un gráfico de historial de precios que marca cada subida y el historial completo de cobros.",
      ["Coste por día, mes y año en tu moneda principal", "Historial de precios con cada subida marcada", "Marca como pagada, pausa, pospón o cancela con un toque"],
      "Detalle de Disney+ con historial de precios de 13,99 $ a 16,99 $"),
  s2=("Planificador del día de cobro", "Organízate en torno al día en que cobras.",
      "El calendario muestra los totales diarios, marca tu día de cobro y te dice exactamente qué sale de tu cuenta antes del siguiente, con previsiones a 3, 6 y 12 meses.",
      ["Vista mensual con totales diarios", "Total «antes del cobro» que se actualiza con cada cargo", "Previsiones para los próximos meses"],
      "Calendario con totales diarios y marca del día de cobro"),
  s3=("Pruebas y subidas de precio", "No vuelvas a pagar por una prueba que olvidaste.",
      "Añade una prueba gratuita y Billow fija un plazo «{tag}» un día antes de que se convierta, con una cuenta atrás en Actividad en vivo en tu pantalla bloqueada. También marca los cambios de precio y las suscripciones olvidadas.",
      ["Recordatorios urgentes antes de que una prueba se convierta", "Avisos cuando sube un precio", "Preguntas «¿Aún lo usas?» y detección de duplicados"],
      "Pantalla de bienvenida de Billow"),
  tag="cancelar antes del",
  s4=("Añade en segundos", "Comparte un recibo. Billow hace el resto.",
      "Busca entre más de 500 servicios conocidos o comparte un recibo, una captura, un PDF o un extracto bancario. Billow encuentra los cobros recurrentes en tu iPhone y explica por qué cree que se repiten.",
      ["Más de 500 servicios con logos, planes y ciclos de cobro", "Importa recibos y extractos bancarios en el propio dispositivo", "Widgets para la pantalla de inicio, la pantalla bloqueada y StandBy"],
      "Añadir una suscripción desde el catálogo"),
  gallery="Un vistazo más de cerca", caps=["Bienvenida", "Inicio", "Calendario", "Detalle", "Añadir"],
  priv_h="Privado por diseño",
  priv_sub="Billow no tiene cuenta, ni servidor, ni analíticas. Tus suscripciones se quedan en tu iPhone y en tu propio iCloud.",
  tiles=[("Sin cuenta", "Abre la app y empieza. Sin registros."),
         ("Sin acceso bancario", "Los extractos que compartes se leen en tu iPhone."),
         ("Tu iCloud", "Sincronizado con tu base de datos privada de iCloud."),
         ("Sin rastreo", "Sin anuncios, sin analíticas, sin SDK de terceros.")],
  langs_h="Hecho para cinco idiomas y cualquier moneda",
  logos_by="Logos de comercios de", privacy_policy="Política de privacidad",
),
"it": dict(
  title="Billow — Gestione abbonamenti",
  desc="Tieni traccia di ogni abbonamento, rinnovo e prova gratuita sul tuo iPhone. Sappi cosa esce dal tuo conto prima dello stipendio. Nessun account, nessun accesso bancario, privato nel tuo iCloud.",
  og="Sappi cosa esce dal tuo conto prima dello stipendio.",
  nav_features="Funzioni", nav_privacy="Privacy", nav_support="Assistenza", lang_label="Lingua",
  h1a="Sappi cosa esce dal tuo conto", h1b="prima dello stipendio.",
  lead="Billow tiene traccia di ogni abbonamento, rinnovo e prova gratuita, e ti avvisa prima che i soldi escano.",
  badge="Presto su App Store",
  pills=["Nessun account", "Nessun accesso bancario", "Privato in iCloud", "Niente pubblicità né tracciamento"],
  alt_home="Schermata Home di Billow con totale mensile, prossimi rinnovi e avvisi",
  s1=("Ogni dettaglio", "Scopri quanto ti costa davvero ognuno.",
      "Ogni abbonamento mostra il costo reale al giorno e all'anno, un grafico dello storico prezzi che segnala ogni aumento e lo storico completo degli addebiti.",
      ["Costo al giorno, al mese e all'anno nella tua valuta", "Storico prezzi con ogni aumento evidenziato", "Segna come pagato, metti in pausa, posticipa o disdici con un tocco"],
      "Dettaglio Disney+ con storico prezzi da 13,99 $ a 16,99 $"),
  s2=("Pianificatore dello stipendio", "Organizzati intorno al giorno dello stipendio.",
      "Il calendario mostra i totali giornalieri, segna il giorno dello stipendio e ti dice esattamente cosa esce dal conto prima del prossimo, con previsioni a 3, 6 e 12 mesi.",
      ["Vista mensile con totali giornalieri", "Totale «prima dello stipendio» che si aggiorna a ogni addebito", "Previsioni per i prossimi mesi"],
      "Calendario con totali giornalieri e giorno dello stipendio"),
  s3=("Prove e aumenti di prezzo", "Non pagare mai più una prova dimenticata.",
      "Aggiungi una prova gratuita e Billow imposta una scadenza «{tag}» il giorno prima della conversione, con un conto alla rovescia in Attività Live sulla schermata di blocco. Segnala anche aumenti di prezzo e abbonamenti dimenticati.",
      ["Promemoria urgenti prima che una prova si converta", "Avvisi quando un prezzo aumenta", "Domande «Lo usi ancora?» e rilevamento dei doppioni"],
      "Schermata di benvenuto di Billow"),
  tag="disdici entro",
  s4=("Aggiungi in pochi secondi", "Condividi una ricevuta. Al resto pensa Billow.",
      "Cerca tra oltre 500 servizi noti oppure condividi una ricevuta, uno screenshot, un PDF o un estratto conto. Billow trova gli addebiti ricorrenti sul tuo iPhone e spiega perché pensa che si ripetano.",
      ["Oltre 500 servizi con loghi, piani e cicli di fatturazione", "Importa ricevute ed estratti conto direttamente sul dispositivo", "Widget per Home, schermata di blocco e StandBy"],
      "Aggiunta di un abbonamento dal catalogo"),
  gallery="Uno sguardo più da vicino", caps=["Benvenuto", "Home", "Calendario", "Dettaglio", "Aggiungi"],
  priv_h="Privato per scelta",
  priv_sub="Billow non ha account, server né strumenti di analisi. I tuoi abbonamenti restano sul tuo iPhone e nel tuo iCloud.",
  tiles=[("Nessun account", "Apri l'app e inizia. Nessuna registrazione."),
         ("Nessun accesso bancario", "Gli estratti conto che condividi vengono letti sul tuo iPhone."),
         ("Il tuo iCloud", "Sincronizzato tramite il tuo database iCloud privato."),
         ("Nessun tracciamento", "Niente pubblicità, analisi o SDK di terze parti.")],
  langs_h="Pensato per cinque lingue e ogni valuta",
  logos_by="Loghi dei servizi di", privacy_policy="Informativa sulla privacy",
),
"sq": dict(
  title="Billow — Ndjekja e abonimeve",
  desc="Ndiqni çdo abonim, rinovim dhe provë falas në iPhone. Dijeni çfarë del nga llogaria juaj para ditës së rrogës. Pa llogari, pa hyrje në bankë, privat në iCloud-in tuaj.",
  og="Dijeni çfarë del nga llogaria juaj para ditës së rrogës.",
  nav_features="Veçoritë", nav_privacy="Privatësia", nav_support="Ndihma", lang_label="Gjuha",
  h1a="Dijeni çfarë del nga llogaria juaj", h1b="para ditës së rrogës.",
  lead="Billow ndjek çdo abonim, rinovim dhe provë falas, dhe ju paralajmëron para se të dalin paratë.",
  badge="Së shpejti në App Store",
  pills=["Pa llogari", "Pa hyrje në bankë", "Privat në iCloud", "Pa reklama dhe pa gjurmim"],
  alt_home="Ekrani kryesor i Billow me totalin mujor, rinovimet e ardhshme dhe njoftimet",
  s1=("Çdo detaj", "Shihni saktësisht sa ju kushton secili.",
      "Çdo abonim tregon koston e vërtetë për ditë dhe për vit, një grafik të historikut të çmimit që shënon çdo rritje dhe historikun e plotë të pagesave.",
      ["Kosto për ditë, muaj dhe vit në monedhën tuaj", "Historiku i çmimit me çdo rritje të shënuar", "Shënojeni të paguar, pezulloni, shtyjeni ose anulojeni me një prekje"],
      "Detajet e Disney+ me historikun e çmimit nga 13,99 $ në 16,99 $"),
  s2=("Planifikuesi i rrogës", "Planifikoni sipas ditës kur merrni rrogën.",
      "Kalendari tregon totalet ditore, shënon ditën e rrogës dhe ju tregon saktësisht çfarë del nga llogaria para rrogës së ardhshme, me parashikime për 3, 6 dhe 12 muaj.",
      ["Pamje mujore me totalet ditore", "Totali «para rrogës» që përditësohet me çdo pagesë", "Parashikime për muajt në vijim"],
      "Kalendari me totalet ditore dhe ditën e rrogës"),
  s3=("Provat dhe rritjet e çmimit", "Mos paguani më për një provë që e harruat.",
      "Shtoni një provë falas dhe Billow vendos afatin «{tag}» një ditë para se të kalojë në pagesë, me numërim mbrapsht në Live Activity në ekranin e kyçjes. Shënohen gjithashtu ndryshimet e çmimit dhe abonimet e harruara.",
      ["Kujtesa urgjente para se prova të kalojë në pagesë", "Njoftime kur rritet një çmim", "Pyetje «Ende e përdorni?» dhe zbulim i dyfishimeve"],
      "Ekrani i mirëseardhjes në Billow"),
  tag="anuloni deri më",
  s4=("Shtoni në pak sekonda", "Ndani një faturë. Pjesën tjetër e bën Billow.",
      "Kërkoni mes mbi 500 shërbimeve të njohura ose ndani një faturë, pamje ekrani, PDF ose pasqyrë bankare. Billow gjen pagesat e përsëritura në iPhone dhe shpjegon pse mendon se përsëriten.",
      ["Mbi 500 shërbime me logo, plane dhe cikle pagese", "Importim nga faturat dhe pasqyrat bankare, në pajisje", "Widget-e për ekranin kryesor, ekranin e kyçjes dhe StandBy"],
      "Shtimi i një abonimi nga katalogu"),
  gallery="Një vështrim më nga afër", caps=["Mirëseardhja", "Kreu", "Kalendari", "Detajet", "Shto"],
  priv_h="Privatësi që në projektim",
  priv_sub="Billow nuk ka llogari, server apo analitikë. Abonimet tuaja qëndrojnë në iPhone dhe në iCloud-in tuaj.",
  tiles=[("Pa llogari", "Hapni aplikacionin dhe filloni. Pa regjistrim."),
         ("Pa hyrje në bankë", "Pasqyrat që ndani lexohen në iPhone."),
         ("iCloud-i juaj", "Sinkronizohet përmes bazës suaj private të të dhënave në iCloud."),
         ("Pa gjurmim", "Pa reklama, pa analitikë, pa SDK të palëve të treta.")],
  langs_h="Krijuar për pesë gjuhë dhe çdo monedhë",
  logos_by="Logot e shërbimeve nga", privacy_policy="Politika e privatësisë",
),
}

S5 = {
  "en": (("Insights", "See where a year of subscriptions goes.",
          "A 12-month chart shows what you spent, what it costs per day and which months peak. Billow flags forgotten subscriptions and counts what you saved by cancelling.",
          ["12-month trend with your cost per day", "Possibly forgotten and saved-this-year totals", "Your most expensive subscriptions, ranked"],
          "Insights with a 12-month spending chart"), "Insights"),
  "de": (("Einblicke", "Sieh, wohin ein Jahr Abos geht.",
          "Ein 12-Monats-Diagramm zeigt, was du ausgegeben hast, was es pro Tag kostet und in welchen Monaten es Spitzen gibt. Billow markiert vergessene Abos und zählt, was du durch Kündigungen gespart hast.",
          ["12-Monats-Verlauf mit deinen Kosten pro Tag", "Summen für vermutlich vergessene Abos und die Ersparnis dieses Jahres", "Deine teuersten Abos im Ranking"],
          "Einblicke mit 12-Monats-Ausgabendiagramm"), "Einblicke"),
  "es": (("Análisis", "Mira a dónde va un año de suscripciones.",
          "Un gráfico de 12 meses muestra cuánto gastaste, cuánto cuesta al día y qué meses son los más caros. Billow marca las suscripciones olvidadas y cuenta lo que ahorraste al cancelar.",
          ["Tendencia de 12 meses con tu coste diario", "Totales de posibles olvidos y del ahorro de este año", "Tus suscripciones más caras, ordenadas"],
          "Análisis con gráfico de gasto de 12 meses"), "Análisis"),
  "it": (("Analisi", "Scopri dove va un anno di abbonamenti.",
          "Un grafico di 12 mesi mostra quanto hai speso, quanto costa al giorno e quali mesi sono i più cari. Billow segnala gli abbonamenti dimenticati e conta quanto hai risparmiato disdicendo.",
          ["Andamento di 12 mesi con il costo al giorno", "Totali dei possibili dimenticati e del risparmio di quest'anno", "I tuoi abbonamenti più cari, in classifica"],
          "Analisi con grafico della spesa di 12 mesi"), "Analisi"),
  "sq": (("Analiza", "Shihni ku shkon një vit abonimesh.",
          "Një grafik 12-mujor tregon sa keni shpenzuar, sa kushton në ditë dhe cilët muaj janë më të shtrenjtët. Billow shënon abonimet e harruara dhe numëron sa keni kursyer duke anuluar.",
          ["Ecuria 12-mujore me koston tuaj ditore", "Totalet e abonimeve ndoshta të harruara dhe të kursimeve të këtij viti", "Abonimet tuaja më të shtrenjta, të renditura"],
          "Analiza me grafikun e shpenzimeve 12-mujore"), "Analiza"),
}
for _l, (_s5, _cap) in S5.items():
    T[_l]["s5"] = _s5
    T[_l]["caps"] = T[_l]["caps"][:3] + [_cap] + T[_l]["caps"][3:]
S6 = {
  "en": ("Email receipts", "Find subscriptions in your inbox.",
         "Connect Gmail, iCloud Mail or any IMAP mailbox and Billow finds the receipts for your subscriptions. Mail is read on your iPhone with read-only access, only the merchant, amount, date and billing cycle are kept, and nothing is ever uploaded. Disconnect any time. {privacy}",
         ["Gmail, iCloud Mail and other IMAP mailboxes", "Only receipt emails from the last 18 months, read-only", "Message text is discarded right after reading"],
         "Mailboxes screen with a connected iCloud Mail account and its last scan", "How Billow handles your email"),
  "de": ("E-Mail-Belege", "Finde Abos in deinem Posteingang.",
         "Verbinde Gmail, iCloud Mail oder ein IMAP-Postfach und Billow findet die Belege deiner Abos. Mails werden auf deinem iPhone nur lesend gelesen, gespeichert werden nur Anbieter, Betrag, Datum und Abrechnungszyklus, und nichts wird hochgeladen. Jederzeit trennbar. {privacy}",
         ["Gmail, iCloud Mail und andere IMAP-Postfächer", "Nur Beleg-Mails der letzten 18 Monate, nur lesend", "Der Mailtext wird direkt nach dem Lesen verworfen"],
         "Postfächer-Bildschirm mit verbundenem iCloud-Mail-Konto und letzter Prüfung", "Wie Billow mit deinen E-Mails umgeht"),
  "es": ("Recibos por email", "Encuentra suscripciones en tu bandeja de entrada.",
         "Conecta Gmail, el correo de iCloud o cualquier buzón IMAP y Billow encuentra los recibos de tus suscripciones. El correo se lee en tu iPhone en solo lectura, solo se guardan el comercio, el importe, la fecha y el ciclo de cobro, y nunca se sube nada. Desconéctalo cuando quieras. {privacy}",
         ["Gmail, correo de iCloud y otros buzones IMAP", "Solo emails de recibos de los últimos 18 meses, en solo lectura", "El texto del mensaje se descarta justo después de leerlo"],
         "Pantalla de buzones con una cuenta de correo de iCloud conectada y su último análisis", "Cómo trata Billow tu correo"),
  "it": ("Ricevute email", "Trova gli abbonamenti nella tua posta.",
         "Collega Gmail, la posta di iCloud o qualsiasi casella IMAP e Billow trova le ricevute dei tuoi abbonamenti. La posta viene letta sul tuo iPhone in sola lettura, si conservano solo esercente, importo, data e ciclo di fatturazione e non viene caricato nulla. Puoi disconnetterti quando vuoi. {privacy}",
         ["Gmail, posta di iCloud e altre caselle IMAP", "Solo email di ricevute degli ultimi 18 mesi, in sola lettura", "Il testo del messaggio viene eliminato subito dopo la lettura"],
         "Schermata delle caselle con un account di posta iCloud collegato e l'ultima analisi", "Come Billow tratta la tua posta"),
  "sq": ("Faturat me email", "Gjeni abonimet në kutinë tuaj postare.",
         "Lidhni Gmail, iCloud Mail ose çdo kuti IMAP dhe Billow gjen faturat e abonimeve tuaja. Posta lexohet në iPhone-in tuaj vetëm për lexim, ruhen vetëm tregtari, shuma, data dhe cikli i pagesës, dhe asgjë nuk ngarkohet kurrë. Mund të shkëputeni në çdo kohë. {privacy}",
         ["Gmail, iCloud Mail dhe kuti të tjera IMAP", "Vetëm email-et e faturave të 18 muajve të fundit, vetëm për lexim", "Teksti i mesazhit fshihet menjëherë pas leximit"],
         "Ekrani i kutive postare me një llogari iCloud Mail të lidhur dhe kontrollin e fundit", "Si e trajton Billow postën tuaj"),
}
TERMS = {"en": "Terms of Use", "de": "Nutzungsbedingungen", "es": "Términos de uso", "it": "Termini d'uso", "sq": "Kushtet e përdorimit"}
for _l, _s6 in S6.items():
    T[_l]["s6"] = _s6[:5]
    T[_l]["privacy_link"] = _s6[5]
GALLERY = ["onboarding", "home", "calendar", "insights", "detail", "add"]

APPLE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.78-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-3-.79-1.54.02-2.96.9-3.76 2.28-1.6 2.78-.41 6.9 1.15 9.16.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.23-.02 2.01-1.12 2.76-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.4-.92-2.42-3.66l.04-.03zM14.1 5.86c.63-.77 1.06-1.83.94-2.89-.91.04-2.01.61-2.66 1.37-.58.67-1.09 1.75-.96 2.79 1.02.08 2.05-.52 2.68-1.27z"/></svg>'
ICONS = [
  '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/><path d="M3 3l18 18"/>',
  '<path d="M3 10h18L12 4 3 10z"/><path d="M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18"/>',
  '<path d="M7 18a5 5 0 0 1-.5-9.97A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z"/>',
  '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
]
EXTRA_CSS = ""
# Root page only: send first-time visitors to their language once; never override a choice they made.
DETECT = """<script>
(function () {
  var supported = ["de", "es", "it", "sq"], key = "billow-lang";
  try {
    if (localStorage.getItem(key)) return;
    var l = (navigator.languages || [navigator.language || ""]).map(function (x) { return x.slice(0, 2).toLowerCase(); });
    for (var i = 0; i < l.length; i++) {
      if (l[i] === "en") break;
      if (supported.indexOf(l[i]) >= 0) { localStorage.setItem(key, l[i]); location.replace(l[i] + "/"); return; }
    }
  } catch (e) {}
})();
</script>"""
REMEMBER = """<script>
document.getElementById("lang").addEventListener("change", function (e) {
  try { localStorage.setItem("billow-lang", e.target.value); } catch (err) {}
  location.href = e.target.options[e.target.selectedIndex].dataset.href;
});
(function () {
  var els = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) { els.forEach(function (el) { el.classList.add("in"); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  els.forEach(function (el) { io.observe(el); });
})();
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var raw = en.target.getAttribute("data-count"), m = raw.match(/^([0-9]+)(.*)$/);
        if (!m) return;
        var target = parseInt(m[1], 10), suffix = m[2], start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min(1, (ts - start) / 1400), eased = 1 - Math.pow(1 - p, 3);
          en.target.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }
})();
</script>"""

e = html.escape



JS_FLAG = '<script>document.documentElement.classList.add("js");try{var t=localStorage.getItem("billow-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>'
SPARK = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></svg>'
CARD_ICONS = [
  ('teal',  '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'),
  ('amber', '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg>'),
  ('mint',  '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>'),
]
# Floating cards beside the hero phone: (label, value) x3, matching CARD_ICONS.
HERO_CARDS = {
  "en": [("Before payday", "$84.97"), ("Trial ends", "in 2 days"), ("Price went up", "+$3.00")],
  "de": [("Vor dem Zahltag", "84,97 €"), ("Testphase endet", "in 2 Tagen"), ("Preis gestiegen", "+3,00 €")],
  "es": [("Antes del día de pago", "84,97 €"), ("La prueba termina", "en 2 días"), ("Subida de precio", "+3,00 €")],
  "it": [("Prima dello stipendio", "84,97 €"), ("La prova finisce", "tra 2 giorni"), ("Prezzo aumentato", "+3,00 €")],
  "sq": [("Para pagës", "84,97 €"), ("Prova mbaron", "pas 2 ditësh"), ("Çmimi u rrit", "+3,00 €")],
}
SERVICES = ["Netflix", "Spotify", "Disney+", "iCloud+", "YouTube Premium", "Apple Music", "Amazon Prime", "ChatGPT", "Adobe Creative Cloud", "Microsoft 365", "Dropbox", "Strava", "Duolingo", "The New York Times", "PlayStation Plus", "Canva", "Notion", "HBO Max"]
# Stats strip under the hero: (value, label) x3.
STATS = {
  "en": [("500+", "services with logos"), ("5", "languages, every currency"), ("0", "accounts, servers or trackers")],
  "de": [("500+", "Dienste mit Logos"), ("5", "Sprachen, jede Währung"), ("0", "Konten, Server oder Tracker")],
  "es": [("500+", "servicios con logos"), ("5", "idiomas, cualquier moneda"), ("0", "cuentas, servidores o rastreadores")],
  "it": [("500+", "servizi con logo"), ("5", "lingue, ogni valuta"), ("0", "account, server o tracker")],
  "sq": [("500+", "shërbime me logo"), ("5", "gjuhë, çdo monedhë"), ("0", "llogari, serverë apo gjurmues")],
}

# ---- "And there's more" section: strings reused from the app's own String Catalog (Localizable.xcstrings).
APP_STRINGS = {
 "guide.everywhere.title": {
  "en": "Widgets, Siri and Spotlight",
  "de": "Widgets, Siri und Spotlight",
  "es": "Widgets, Siri y Spotlight",
  "it": "Widget, Siri e Spotlight",
  "sq": "Widget-e, Siri dhe Spotlight"
 },
 "guide.everywhere.body": {
  "en": "Home and Lock Screen widgets with Mark paid, “What's due this week?” in Siri, and every subscription in Spotlight.",
  "de": "Home- und Sperrbildschirm-Widgets mit „Als bezahlt markieren“, „Was wird diese Woche fällig?“ in Siri und jedes Abo in Spotlight.",
  "es": "Widgets de inicio y pantalla de bloqueo con Marcar como pagado, “¿Qué vence esta semana?” en Siri y cada suscripción en Spotlight.",
  "it": "Widget per Home e schermata di blocco con Segna come pagato, “Cosa scade questa settimana?” in Siri e ogni abbonamento in Spotlight.",
  "sq": "Widget-e për ekranin kryesor dhe të kyçur me Shëno si të paguar, “Çfarë ka afat këtë javë?” në Siri, dhe çdo abonim në Spotlight."
 },
 "guide.cancel.title": {
  "en": "Cancel in two taps",
  "de": "In zwei Tipps kündigen",
  "es": "Cancela con dos toques",
  "it": "Disdici con due tocchi",
  "sq": "Anuloni me dy prekje"
 },
 "guide.cancel.body": {
  "en": "Routed to the right place for App Store, Google Play, PayPal, Amazon or the merchant, with guided steps, letters for five countries and a signature on device.",
  "de": "Zum richtigen Ort für App Store, Google Play, PayPal, Amazon oder den Anbieter, mit Schritt-für-Schritt-Anleitung, Schreiben für fünf Länder und Unterschrift am Gerät.",
  "es": "Dirigido al lugar correcto para App Store, Google Play, PayPal, Amazon o el proveedor, con pasos guiados, cartas para cinco países y firma en el dispositivo.",
  "it": "Instradato al posto giusto per App Store, Google Play, PayPal, Amazon o il fornitore, con passi guidati, lettere per cinque paesi e firma sul dispositivo.",
  "sq": "Drejtuar në vendin e duhur për App Store, Google Play, PayPal, Amazon ose tregtarin, me hapa të udhëzuar, letra për pesë vende dhe nënshkrim në pajisje."
 },
 "guide.insights.title": {
  "en": "Insights and a yearly recap",
  "de": "Einblicke und ein Jahresrückblick",
  "es": "Análisis y un resumen anual",
  "it": "Analisi e un recap annuale",
  "sq": "Analiza dhe një përmbledhje vjetore"
 },
 "guide.insights.body": {
  "en": "Spend by category and payment method, a 12-month trend, what you saved, and a shareable recap each December.",
  "de": "Ausgaben nach Kategorie und Zahlungsmethode, 12-Monats-Trend, Ersparnisse und ein teilbarer Rückblick jeden Dezember.",
  "es": "Gasto por categoría y método de pago, tendencia de 12 meses, lo ahorrado y un resumen para compartir cada diciembre.",
  "it": "Spesa per categoria e metodo di pagamento, trend a 12 mesi, quanto hai risparmiato e un recap condivisibile ogni dicembre.",
  "sq": "Shpenzimet sipas kategorisë dhe mënyrës së pagesës, trendi 12-mujor, çfarë kursyet, dhe një përmbledhje për ndarje çdo dhjetor."
 },
 "guide.prices.title": {
  "en": "Price rises, explained",
  "de": "Preiserhöhungen, erklärt",
  "es": "Subidas de precio, explicadas",
  "it": "Aumenti di prezzo, spiegati",
  "sq": "Rritjet e çmimeve, të shpjeguara"
 },
 "guide.prices.body": {
  "en": "Old price, new price and the yearly impact, with cheaper tiers, annual plans and your rights in Germany and Italy.",
  "de": "Alter Preis, neuer Preis und die Jahreswirkung, mit günstigeren Tarifen, Jahresabos und deinen Rechten in Deutschland und Italien.",
  "es": "Precio anterior, nuevo e impacto anual, con planes más baratos, planes anuales y tus derechos en Alemania e Italia.",
  "it": "Prezzo vecchio, nuovo e impatto annuo, con piani più economici, piani annuali e i tuoi diritti in Germania e Italia.",
  "sq": "Çmimi i vjetër, i riu dhe ndikimi vjetor, me plane më të lira, plane vjetore dhe të drejtat tuaja në Gjermani dhe Itali."
 },
 "household.intro.title": {
  "en": "Share subscriptions with your household",
  "de": "Abos mit deinem Haushalt teilen",
  "es": "Comparte suscripciones con tu hogar",
  "it": "Condividi gli abbonamenti con la tua famiglia",
  "sq": "Ndani abonimet me familjen"
 },
 "household.intro.body": {
  "en": "Invite up to 5 people by link. Everyone joins with their own Apple ID and keeps their own list private; only the subscriptions you share are visible.",
  "de": "Lade bis zu 5 Personen per Link ein. Alle treten mit ihrer eigenen Apple-ID bei und ihre eigene Liste bleibt privat; sichtbar sind nur die Abos, die geteilt werden.",
  "es": "Invita hasta a 5 personas con un enlace. Cada persona se une con su propio Apple ID y su lista sigue siendo privada; solo se ven las suscripciones compartidas.",
  "it": "Invita fino a 5 persone con un link. Ognuno entra con il proprio Apple ID e la propria lista resta privata; si vedono solo gli abbonamenti condivisi.",
  "sq": "Ftoni deri në 5 persona me një lidhje. Secili hyn me Apple ID-në e vet dhe lista e tij mbetet private; shihen vetëm abonimet që ndani."
 },
 "paywall.feature.family": {
  "en": "Shared with your family via Family Sharing",
  "de": "Mit der Familie über Familienfreigabe geteilt",
  "es": "Compartido con tu familia mediante En familia",
  "it": "Condiviso con la famiglia tramite In famiglia",
  "sq": "Ndahet me familjen përmes Family Sharing"
 },
 "widget.next.title": {
  "en": "Next charge",
  "de": "Nächste Abbuchung",
  "es": "Próximo cobro",
  "it": "Prossimo addebito",
  "sq": "Pagesa e radhës"
 },
 "widget.inline.month": {
  "en": "This month %@",
  "de": "Diesen Monat %@",
  "es": "Este mes %@",
  "it": "Questo mese %@",
  "sq": "Këtë muaj %@"
 },
 "widget.inDays.placeholder": {
  "en": "in 3 days",
  "de": "in 3 Tagen",
  "es": "en 3 días",
  "it": "tra 3 giorni",
  "sq": "pas 3 ditësh"
 },
 "guide.price": {
  "en": "Free to start; no fees on what you save, ever",
  "de": "Kostenlos zum Start; nie eine Gebühr auf deine Ersparnis",
  "es": "Gratis para empezar; nunca una comisión sobre lo que ahorras",
  "it": "Gratis per iniziare; mai una commissione su ciò che risparmi",
  "sq": "Falas për të filluar; asnjë tarifë mbi atë që kurseni, kurrë"
 }
}
MORE = {
  "en": ("And there's more", "Share bills with your household, see everything from your Lock Screen, and cancel without the runaround.", "Family Sharing", "You", "Pro"),
  "de": ("Und da ist noch mehr", "Teile Rechnungen mit deinem Haushalt, sieh alles vom Sperrbildschirm aus und kündige ohne Umwege.", "Familienfreigabe", "Du", "Pro"),
  "es": ("Y hay más", "Comparte gastos con tu hogar, mira todo desde la pantalla bloqueada y cancela sin rodeos.", "En familia", "Tú", "Pro"),
  "it": ("E c'è di più", "Dividi le spese con chi vive con te, vedi tutto dalla schermata di blocco e disdici senza giri di parole.", "In famiglia", "Tu", "Pro"),
  "sq": ("Dhe ka më shumë", "Ndani faturat me familjen, shihni gjithçka nga ekrani i kyçur dhe anuloni pa rrugë të gjata.", "Family Sharing", "Ju", "Pro"),
}
MORE_ICONS = {
  "household": '<path d="M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0z"/><path d="M4 21c1.2-3.5 4-5.5 8-5.5s6.8 2 8 5.5"/><path d="M19 8a3 3 0 1 0-2.2-5"/><path d="M5 8a3 3 0 1 1 2.2-5"/>',
  "family": '<path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.4-7 10-7 10z"/>',
  "widgets": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/>',
  "cancel": '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
  "insights": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  "prices": '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
}

# ---- "Try it now" section and the in-page demo app.
TRY = {
  "en": dict(hint="It's interactive, tap around", live="Live demo", eyebrow="Interactive demo", h="Try Billow right here.", sub="A small simulation of the app in your browser. Add a service, set your payday, start a trial. Nothing is saved and nothing leaves this page.", steps=["Add a subscription from the catalog", "Set your payday and watch the “before payday” total", "Mark one as a free trial to get a cancel-by deadline"], reset="Start over", nav="Try it"),
  "de": dict(hint="Es ist interaktiv, tipp dich durch", live="Live-Demo", eyebrow="Interaktive Demo", h="Probiere Billow gleich hier aus.", sub="Eine kleine Simulation der App in deinem Browser. Füge einen Dienst hinzu, setze deinen Zahltag, starte eine Testphase. Nichts wird gespeichert, nichts verlässt diese Seite.", steps=["Füge ein Abo aus dem Katalog hinzu", "Setze deinen Zahltag und sieh die Summe „vor dem Zahltag“", "Markiere eines als Testphase und erhalte eine „Kündigen bis“-Frist"], reset="Neu starten", nav="Ausprobieren"),
  "es": dict(hint="Es interactivo, toca y prueba", live="Demo en vivo", eyebrow="Demo interactiva", h="Prueba Billow aquí mismo.", sub="Una pequeña simulación de la app en tu navegador. Añade un servicio, fija tu día de cobro, empieza una prueba. No se guarda nada y nada sale de esta página.", steps=["Añade una suscripción del catálogo", "Fija tu día de cobro y mira el total «antes del día de pago»", "Marca una como prueba gratis para obtener un plazo «cancelar antes del»"], reset="Empezar de nuevo", nav="Pruébalo"),
  "it": dict(hint="È interattivo, tocca e prova", live="Demo dal vivo", eyebrow="Demo interattiva", h="Prova Billow qui.", sub="Una piccola simulazione dell'app nel tuo browser. Aggiungi un servizio, imposta il giorno dello stipendio, avvia una prova. Niente viene salvato e niente lascia questa pagina.", steps=["Aggiungi un abbonamento dal catalogo", "Imposta il giorno dello stipendio e guarda il totale «prima dello stipendio»", "Segna uno come prova gratuita per avere una scadenza «disdici entro»"], reset="Ricomincia", nav="Provalo"),
  "sq": dict(hint="Është interaktiv, prekeni dhe provoni", live="Demo e drejtpërdrejtë", eyebrow="Demo interaktive", h="Provoni Billow këtu.", sub="Një simulim i vogël i aplikacionit në shfletuesin tuaj. Shtoni një shërbim, caktoni ditën e pagës, nisni një provë. Asgjë nuk ruhet dhe asgjë nuk del nga kjo faqe.", steps=["Shtoni një abonim nga katalogu", "Caktoni ditën e pagës dhe shihni totalin “para pagës”", "Shënoni një si provë falas për të marrë afatin “anuloni deri”"], reset="Filloni nga e para", nav="Provojeni"),
}
DEMO_UI = {
  "en": dict(this_month="This month", per_month="/month", per_year="/year", trials_add="Trials would add {x}/month", attention_one="1 thing needs your attention", attention_many="{n} things need your attention", all_good="Everything is under control", before_payday="Before payday", payday="Payday", next7="Next 7 days", all_subs="All subscriptions", empty="Nothing yet. Add your first subscription.", home="Home", add="Add", calendar="Calendar", search="Search 500+ services", price="Price", billing="Billing", monthly="Monthly", yearly="Yearly", next_charge="Next charge", trial="Free trial", trial_hint="14 days free, then {x}", add_btn="Add subscription", back="Back", added="{name} added", trial_ends_in="Trial ends in {n} days", trial_ends_today="Trial ends today", cancel_by="Cancel by {d} or pay {x}", price_up="Price went up", price_up_body="{old} → {new} · +{diff}/month", converts="converts to {x}", today="Today", tomorrow="Tomorrow", in_days="in {n} days", trial_tag="TRIAL", remove="Remove", day="day"),
  "de": dict(this_month="Diesen Monat", per_month="/Monat", per_year="/Jahr", trials_add="Testphasen würden {x}/Monat hinzufügen", attention_one="1 Sache braucht deine Aufmerksamkeit", attention_many="{n} Dinge brauchen deine Aufmerksamkeit", all_good="Alles unter Kontrolle", before_payday="Vor dem Zahltag", payday="Zahltag", next7="Nächste 7 Tage", all_subs="Alle Abos", empty="Noch nichts. Füge dein erstes Abo hinzu.", home="Start", add="Hinzufügen", calendar="Kalender", search="500+ Dienste durchsuchen", price="Preis", billing="Abrechnung", monthly="Monatlich", yearly="Jährlich", next_charge="Nächste Abbuchung", trial="Testphase", trial_hint="14 Tage gratis, dann {x}", add_btn="Abo hinzufügen", back="Zurück", added="{name} hinzugefügt", trial_ends_in="Testphase endet in {n} Tagen", trial_ends_today="Testphase endet heute", cancel_by="Kündigen bis {d} oder {x} zahlen", price_up="Preis gestiegen", price_up_body="{old} → {new} · +{diff}/Monat", converts="wird zu {x}", today="Heute", tomorrow="Morgen", in_days="in {n} Tagen", trial_tag="TEST", remove="Entfernen", day="Tag"),
  "es": dict(this_month="Este mes", per_month="/mes", per_year="/año", trials_add="Las pruebas añadirían {x}/mes", attention_one="1 cosa necesita tu atención", attention_many="{n} cosas necesitan tu atención", all_good="Todo bajo control", before_payday="Antes del día de pago", payday="Día de pago", next7="Próximos 7 días", all_subs="Todas las suscripciones", empty="Nada todavía. Añade tu primera suscripción.", home="Inicio", add="Añadir", calendar="Calendario", search="Busca entre 500+ servicios", price="Precio", billing="Cobro", monthly="Mensual", yearly="Anual", next_charge="Próximo cobro", trial="Prueba gratis", trial_hint="14 días gratis, luego {x}", add_btn="Añadir suscripción", back="Atrás", added="{name} añadido", trial_ends_in="La prueba termina en {n} días", trial_ends_today="La prueba termina hoy", cancel_by="Cancela antes del {d} o paga {x}", price_up="Subida de precio", price_up_body="{old} → {new} · +{diff}/mes", converts="pasa a {x}", today="Hoy", tomorrow="Mañana", in_days="en {n} días", trial_tag="PRUEBA", remove="Quitar", day="día"),
  "it": dict(this_month="Questo mese", per_month="/mese", per_year="/anno", trials_add="Le prove aggiungerebbero {x}/mese", attention_one="1 cosa richiede attenzione", attention_many="{n} cose richiedono attenzione", all_good="Tutto sotto controllo", before_payday="Prima dello stipendio", payday="Stipendio", next7="Prossimi 7 giorni", all_subs="Tutti gli abbonamenti", empty="Ancora niente. Aggiungi il primo abbonamento.", home="Home", add="Aggiungi", calendar="Calendario", search="Cerca tra 500+ servizi", price="Prezzo", billing="Fatturazione", monthly="Mensile", yearly="Annuale", next_charge="Prossimo addebito", trial="Prova gratuita", trial_hint="14 giorni gratis, poi {x}", add_btn="Aggiungi abbonamento", back="Indietro", added="{name} aggiunto", trial_ends_in="La prova finisce tra {n} giorni", trial_ends_today="La prova finisce oggi", cancel_by="Disdici entro il {d} o paghi {x}", price_up="Prezzo aumentato", price_up_body="{old} → {new} · +{diff}/mese", converts="diventa {x}", today="Oggi", tomorrow="Domani", in_days="tra {n} giorni", trial_tag="PROVA", remove="Rimuovi", day="giorno"),
  "sq": dict(this_month="Këtë muaj", per_month="/muaj", per_year="/vit", trials_add="Provat do të shtonin {x}/muaj", attention_one="1 gjë ka nevojë për vëmendje", attention_many="{n} gjëra kanë nevojë për vëmendje", all_good="Gjithçka nën kontroll", before_payday="Para pagës", payday="Dita e pagës", next7="7 ditët e ardhshme", all_subs="Të gjitha abonimet", empty="Asgjë ende. Shtoni abonimin e parë.", home="Kreu", add="Shto", calendar="Kalendari", search="Kërkoni në 500+ shërbime", price="Çmimi", billing="Faturimi", monthly="Mujor", yearly="Vjetor", next_charge="Pagesa e ardhshme", trial="Provë falas", trial_hint="14 ditë falas, pastaj {x}", add_btn="Shto abonimin", back="Prapa", added="{name} u shtua", trial_ends_in="Prova mbaron pas {n} ditësh", trial_ends_today="Prova mbaron sot", cancel_by="Anuloni deri më {d} ose paguani {x}", price_up="Çmimi u rrit", price_up_body="{old} → {new} · +{diff}/muaj", converts="bëhet {x}", today="Sot", tomorrow="Nesër", in_days="pas {n} ditësh", trial_tag="PROVË", remove="Hiq", day="dita"),
}
CURRENCY = {"en": "USD", "de": "EUR", "es": "EUR", "it": "EUR", "sq": "EUR"}

def more_section(lang, root):
    a = lambda k: e(APP_STRINGS[k][lang])
    h, sub, family_title, you, pro = MORE[lang]
    ico = lambda k: f'<div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{MORE_ICONS[k]}</svg></div>'
    return f"""<section class="more" id="more">
  <div class="wrap">
    <div class="reveal head">
      <h2>{e(h)}</h2>
      <p class="sub">{e(sub)}</p>
    </div>
    <div class="bento">
      <div class="tile wide reveal">
        {ico("household")}<strong>{a("household.intro.title")}</strong><span>{a("household.intro.body")}</span>
        <div class="split" aria-hidden="true">
          <div class="row sum"><b>Netflix</b><b>17,99 €</b></div>
          <div class="row"><i style="background:#0E7490">{e(you[:1])}</i><span>{e(you)}</span><b>6,00 €</b></div>
          <div class="row"><i style="background:#D97706">A</i><span>Ana</span><b>6,00 €</b></div>
          <div class="row"><i style="background:#059669">L</i><span>Luca</span><b>5,99 €</b></div>
        </div>
      </div>
      <div class="tile reveal d1">{ico("family")}<strong>{e(family_title)}</strong><span>{a("paywall.feature.family")}</span></div>
      <div class="tile reveal d2">{ico("cancel")}<strong>{a("guide.cancel.title")}</strong><span>{a("guide.cancel.body")}</span></div>
      <div class="tile wide reveal">
        {ico("widgets")}<strong>{a("guide.everywhere.title")}</strong><span>{a("guide.everywhere.body")}</span>
        <div class="widgets" aria-hidden="true">
          <div class="w small"><small>{a("widget.next.title")}</small><b>Spotify</b><em>{a("widget.inDays.placeholder")}</em></div>
          <div class="w inline"><i></i>{e(APP_STRINGS["widget.inline.month"][lang].replace("%@", "108,88 €"))}</div>
        </div>
      </div>
      <div class="tile reveal d1">{ico("insights")}<strong>{a("guide.insights.title")}</strong><span>{a("guide.insights.body")}</span></div>
      <div class="tile reveal d2">{ico("prices")}<strong>{a("guide.prices.title")}</strong><span>{a("guide.prices.body")}</span></div>
    </div>
    <p class="note reveal">{a("guide.price")}.</p>
  </div>
</section>"""

def try_section(lang, root):
    t = TRY[lang]
    steps = "\n        ".join(f"<li><span>{i + 1}</span>{e(s)}</li>" for i, s in enumerate(t["steps"]))
    cfg = json.dumps({"lang": lang, "currency": CURRENCY[lang], "t": DEMO_UI[lang]}, ensure_ascii=False)
    return f"""<section class="try" id="try">
  <div class="wrap">
    <div class="text reveal">
      <div class="eyebrow">{e(t["eyebrow"])}</div>
      <h2>{e(t["h"])}</h2>
      <p>{e(t["sub"])}</p>
      <ol class="steps">
        {steps}
      </ol>
      <button type="button" class="reset" id="demo-reset">{e(t["reset"])}</button>
    </div>
    <div class="hint reveal d2" aria-hidden="true">
      <span class="hint-label">{e(t["hint"])}</span>
      <svg class="hint-arrow" viewBox="0 0 220 120" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path class="line" d="M8 14 C 70 -4, 150 18, 200 86"/><path class="head" d="M176 80 L 202 88 L 198 62"/></svg>
      <svg class="hint-arrow-down" viewBox="0 0 60 120" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path class="line" d="M30 8 C 10 40, 50 70, 30 108"/><path class="head" d="M16 94 L 30 110 L 44 94"/></svg>
    </div>
    <div class="demo reveal d1">
      <div class="phone"><div class="live"><i></i>{e(t["live"])}</div><div class="screen"><div class="app" id="demo" lang="{lang}" role="region" aria-label="{e(t["eyebrow"])}"></div></div></div>
      <div id="demo-live" class="visually-hidden" aria-live="polite"></div>
    </div>
  </div>
</section>
<script>window.BILLOW_DEMO = {cfg};</script>
<script src="{root}demo.js?v={DEMO_VER}" defer></script>"""

# ---- Contact form: posts to the owner's own relay (Google Apps Script web app, source in tools/contact-relay.gs), which emails CONTACT_EMAIL.
CONTACT_EMAIL = "ecapi88@gmail.com"
CONTACT_RELAY = "https://script.google.com/macros/s/AKfycbwyyLMU7Jk-GYlnWHQQom6_0QEGJDzTC4GAfF0sRChL-YQVGXAbD-aO3emt8ghBGWHNZA/exec"
CONTACT = {
  "en": dict(open_mail="Open in your mail app", eyebrow="Contact", h="Get in touch.", sub="A question, an idea or a bug? Write to me and I'll reply within two working days.", name="Your name", email="Your email", message="Message", send="Send message", sending="Sending…", sent="Thanks, your message is on its way.", error="Couldn't send. Email me directly at {mail}.", direct="Or email", note="Goes straight to my inbox and is used only to reply to you.", nav="Contact", subject="Message from billow-app.org"),
  "de": dict(open_mail="In deiner Mail-App öffnen", eyebrow="Kontakt", h="Schreib mir.", sub="Eine Frage, eine Idee oder ein Fehler? Schreib mir und ich antworte innerhalb von zwei Werktagen.", name="Dein Name", email="Deine E-Mail", message="Nachricht", send="Nachricht senden", sending="Wird gesendet…", sent="Danke, deine Nachricht ist unterwegs.", error="Senden fehlgeschlagen. Schreib mir direkt an {mail}.", direct="Oder per E-Mail", note="Landet direkt in meinem Postfach und wird nur für die Antwort verwendet.", nav="Kontakt", subject="Nachricht von billow-app.org"),
  "es": dict(open_mail="Abrir en tu app de correo", eyebrow="Contacto", h="Escríbeme.", sub="¿Una pregunta, una idea o un error? Escríbeme y te responderé en dos días laborables.", name="Tu nombre", email="Tu correo", message="Mensaje", send="Enviar mensaje", sending="Enviando…", sent="Gracias, tu mensaje está en camino.", error="No se pudo enviar. Escríbeme directamente a {mail}.", direct="O por correo", note="Llega directamente a mi bandeja y se usa solo para responderte.", nav="Contacto", subject="Mensaje desde billow-app.org"),
  "it": dict(open_mail="Apri nella tua app di posta", eyebrow="Contatti", h="Scrivimi.", sub="Una domanda, un'idea o un bug? Scrivimi e ti rispondo entro due giorni lavorativi.", name="Il tuo nome", email="La tua email", message="Messaggio", send="Invia messaggio", sending="Invio in corso…", sent="Grazie, il tuo messaggio è in arrivo.", error="Invio non riuscito. Scrivimi direttamente a {mail}.", direct="Oppure via email", note="Arriva direttamente nella mia casella e serve solo per risponderti.", nav="Contatti", subject="Messaggio da billow-app.org"),
  "sq": dict(open_mail="Hape në aplikacionin e postës", eyebrow="Kontakt", h="Më shkruani.", sub="Një pyetje, një ide apo një gabim? Më shkruani dhe do t'ju përgjigjem brenda dy ditësh pune.", name="Emri juaj", email="Email-i juaj", message="Mesazhi", send="Dërgo mesazhin", sending="Po dërgohet…", sent="Faleminderit, mesazhi juaj është rrugës.", error="Dërgimi dështoi. Më shkruani drejtpërdrejt në {mail}.", direct="Ose me email", note="Shkon drejt në postën time dhe përdoret vetëm për t'ju përgjigjur.", nav="Kontakt", subject="Mesazh nga billow-app.org"),
}

def contact_form(lang, root, next_url):
    c = CONTACT[lang]
    mail_link = f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
    return f"""<form id="contact-form" class="contact-form" action="{CONTACT_RELAY}" method="POST" data-to="{CONTACT_EMAIL}" data-sending="{e(c["sending"])}" data-sent="{e(c["sent"])}" data-error="{e(c["error"]).replace("{mail}", e(mail_link))}" data-open="{e(c["open_mail"])}">
        <input type="hidden" name="_subject" value="{e(c["subject"])}">
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div class="two">
          <label><span>{e(c["name"])}</span><input type="text" name="name" required autocomplete="name" maxlength="120"></label>
          <label><span>{e(c["email"])}</span><input type="email" name="email" required autocomplete="email" maxlength="200"></label>
        </div>
        <label><span>{e(c["message"])}</span><textarea name="message" required rows="5" maxlength="4000"></textarea></label>
        <div class="actions">
          <button type="submit" class="send">{e(c["send"])}</button>
          <span class="direct">{e(c["direct"])} {mail_link}</span>
        </div>
        <p class="status" role="status" aria-live="polite"></p>
        <p class="note">{e(c["note"])}</p>
      </form>"""

def contact_section(lang, root):
    c = CONTACT[lang]
    page = BASE if lang == "en" else f"{BASE}{lang}/"
    return f"""<section class="contact" id="contact">
  <div class="wrap">
    <div class="text reveal">
      <div class="eyebrow">{e(c["eyebrow"])}</div>
      <h2>{e(c["h"])}</h2>
      <p>{e(c["sub"])}</p>
    </div>
    <div class="reveal d1">
      {contact_form(lang, root, page + "#contact")}
    </div>
  </div>
</section>
<script src="{root}contact.js?v={CONTACT_VER}" defer></script>
<script src="{root}theme.js?v={THEME_VER}" defer></script>
<script src="{root}gallery.js?v={GALLERY_VER}" defer></script>"""

# ---- Pricing: plan names, Pro features and the Free/Pro split come from the app's String Catalog; prices from App/Billow.storekit.
PAYWALL = {
 "paywall.badge": {
  "en": "BILLOW PRO",
  "de": "BILLOW PRO",
  "es": "BILLOW PRO",
  "it": "BILLOW PRO",
  "sq": "BILLOW PRO"
 },
 "paywall.feature.family": {
  "en": "Shared with your family via Family Sharing",
  "de": "Mit der Familie über Familienfreigabe geteilt",
  "es": "Compartido con tu familia mediante En familia",
  "it": "Condiviso con la famiglia tramite In famiglia",
  "sq": "Ndahet me familjen përmes Family Sharing"
 },
 "paywall.feature.letters": {
  "en": "Cancellation letters for your country",
  "de": "Kündigungsschreiben für dein Land",
  "es": "Cartas de baja para tu país",
  "it": "Lettere di disdetta per il tuo paese",
  "sq": "Letra anulimi për vendin tuaj"
 },
 "paywall.feature.trials": {
  "en": "Trial countdowns and price-change alerts",
  "de": "Testphasen-Countdown und Preiswarnungen",
  "es": "Cuenta atrás de pruebas y alertas de precio",
  "it": "Conto alla rovescia prove e avvisi prezzi",
  "sq": "Numërim mbrapsht për provat dhe njoftime për çmimet"
 },
 "paywall.feature.unlimited": {
  "en": "Unlimited subscriptions",
  "de": "Unbegrenzt viele Abos",
  "es": "Suscripciones ilimitadas",
  "it": "Abbonamenti illimitati",
  "sq": "Abonime të pakufizuara"
 },
 "paywall.feature.widgets": {
  "en": "All widgets, export, household sharing",
  "de": "Alle Widgets, Export, Haushalt teilen",
  "es": "Todos los widgets, exportación, uso compartido en casa",
  "it": "Tutti i widget, esportazione, condivisione familiare",
  "sq": "Të gjitha widget-et, eksporti, ndarja familjare"
 },
 "paywall.plan.lifetime": {
  "en": "Lifetime",
  "de": "Lebenslang",
  "es": "De por vida",
  "it": "A vita",
  "sq": "Përgjithmonë"
 },
 "paywall.plan.monthly": {
  "en": "Monthly",
  "de": "Monatlich",
  "es": "Mensual",
  "it": "Mensile",
  "sq": "Mujor"
 },
 "paywall.plan.yearly": {
  "en": "Yearly",
  "de": "Jährlich",
  "es": "Anual",
  "it": "Annuale",
  "sq": "Vjetor"
 },
 "paywall.lifetime": {
  "en": "Pay once, no subscription",
  "de": "Einmal zahlen, kein Abo",
  "es": "Pagas una vez, sin suscripción",
  "it": "Paghi una volta, nessun abbonamento",
  "sq": "Paguani një herë, pa abonim"
 },
 "paywall.monthly": {
  "en": "Billed monthly, cancel anytime",
  "de": "Monatlich abgerechnet, jederzeit kündbar",
  "es": "Cobro mensual, cancela cuando quieras",
  "it": "Addebito mensile, disdici quando vuoi",
  "sq": "Faturohet çdo muaj, anuloni kurdo"
 },
 "paywall.sub": {
  "en": "Free tracks 7. Pro tracks all of them and watches trials and prices for you.",
  "de": "Kostenlos verwaltet 7. Pro verwaltet alle und behält Testphasen und Preise für dich im Blick.",
  "es": "Gratis controla 7. Pro las controla todas y vigila pruebas y precios por ti.",
  "it": "Gratis ne segue 7. Pro li segue tutti e tiene d'occhio prove e prezzi per te.",
  "sq": "Falas ndjek 7. Pro i ndjek të gjitha dhe vëzhgon provat dhe çmimet për ju."
 },
 "paywall.cta.trial": {
  "en": "Start 14-day free trial",
  "de": "14 Tage kostenlos testen",
  "es": "Empezar prueba gratis de 14 días",
  "it": "Inizia la prova gratuita di 14 giorni",
  "sq": "Filloni provën 14-ditore falas"
 },
 "paywall.redeem": {
  "en": "Redeem code",
  "de": "Code einlösen",
  "es": "Canjear código",
  "it": "Riscatta codice",
  "sq": "Përdor kodin"
 },
 "paywall.yearly.trial": {
  "en": "14 days free, then %@/year · %@/month",
  "de": "14 Tage kostenlos, dann %@/Jahr · %@/Monat",
  "es": "14 días gratis, luego %@/año · %@/mes",
  "it": "14 giorni gratis, poi %@/anno · %@/mese",
  "sq": "14 ditë falas, pastaj %@/vit · %@/muaj"
 }
}
PRICES = {"monthly": "$2.99", "yearly": "$19.99", "yearly_month": "$1.67", "lifetime": "$49.99"}
PRICING = {
  "en": dict(nav="Pricing", eyebrow="Pricing", h="Free to start. Pro when you want it all.", free="Free", free_desc="Everything you need to stop forgetting.", free_feats=["Track up to 7 subscriptions", "Calendar, payday view and 3-month forecast", "Receipt and statement import, on device", "iCloud sync between your devices"], plus="Everything in Free, plus", per_month="/month", per_year="/year", once="one-time", popular="Most popular", trial="14 days free", save="Save 44%", lifetime_hint="Yours forever, every future update", no_fees="No fees on what you save, ever. Cancel in your Apple account at any time.", prices_note="Prices in US dollars; the App Store shows your local price.", codes_h="Discount codes", codes_soon="Coming soon", codes_body="Launch offers and promo codes are on the way. You'll redeem them in the app under Billow Pro › Redeem code.", codes_hint="Follow the site or the App Store page for the first codes."),
  "de": dict(nav="Preise", eyebrow="Preise", h="Kostenlos starten. Pro, wenn du alles willst.", free="Kostenlos", free_desc="Alles, was du brauchst, um nichts mehr zu vergessen.", free_feats=["Bis zu 7 Abos verwalten", "Kalender, Zahltag-Ansicht und 3-Monats-Prognose", "Import aus Belegen und Kontoauszügen, auf dem Gerät", "iCloud-Sync zwischen deinen Geräten"], plus="Alles aus Kostenlos, plus", per_month="/Monat", per_year="/Jahr", once="einmalig", popular="Am beliebtesten", trial="14 Tage kostenlos", save="44 % sparen", lifetime_hint="Für immer deins, inklusive aller Updates", no_fees="Nie eine Gebühr auf deine Ersparnis. Jederzeit in deinem Apple-Konto kündbar.", prices_note="Preise in US-Dollar; der App Store zeigt deinen lokalen Preis.", codes_h="Rabattcodes", codes_soon="Bald verfügbar", codes_body="Startangebote und Promo-Codes sind unterwegs. Du löst sie in der App unter Billow Pro › Code einlösen ein.", codes_hint="Die ersten Codes erscheinen hier und auf der App-Store-Seite."),
  "es": dict(nav="Precios", eyebrow="Precios", h="Gratis para empezar. Pro cuando lo quieras todo.", free="Gratis", free_desc="Todo lo que necesitas para dejar de olvidar.", free_feats=["Controla hasta 7 suscripciones", "Calendario, vista del día de pago y previsión a 3 meses", "Importación de recibos y extractos, en el dispositivo", "Sincronización iCloud entre tus dispositivos"], plus="Todo lo de Gratis, más", per_month="/mes", per_year="/año", once="pago único", popular="El más popular", trial="14 días gratis", save="Ahorra un 44 %", lifetime_hint="Tuyo para siempre, con todas las actualizaciones", no_fees="Nunca una comisión sobre lo que ahorras. Cancela en tu cuenta de Apple cuando quieras.", prices_note="Precios en dólares; el App Store muestra tu precio local.", codes_h="Códigos de descuento", codes_soon="Próximamente", codes_body="Las ofertas de lanzamiento y los códigos promocionales están en camino. Los canjearás en la app en Billow Pro › Canjear código.", codes_hint="Los primeros códigos aparecerán aquí y en la página del App Store."),
  "it": dict(nav="Prezzi", eyebrow="Prezzi", h="Gratis per iniziare. Pro quando vuoi tutto.", free="Gratis", free_desc="Tutto ciò che serve per smettere di dimenticare.", free_feats=["Fino a 7 abbonamenti", "Calendario, vista stipendio e previsione a 3 mesi", "Import da ricevute ed estratti conto, sul dispositivo", "Sincronizzazione iCloud tra i tuoi dispositivi"], plus="Tutto di Gratis, più", per_month="/mese", per_year="/anno", once="una tantum", popular="Il più scelto", trial="14 giorni gratis", save="Risparmi il 44%", lifetime_hint="Tuo per sempre, con tutti gli aggiornamenti", no_fees="Mai una commissione su ciò che risparmi. Disdici dal tuo account Apple quando vuoi.", prices_note="Prezzi in dollari USA; l'App Store mostra il prezzo locale.", codes_h="Codici sconto", codes_soon="In arrivo", codes_body="Offerte di lancio e codici promozionali sono in arrivo. Li riscatterai nell'app in Billow Pro › Riscatta codice.", codes_hint="I primi codici compariranno qui e sulla pagina dell'App Store."),
  "sq": dict(nav="Çmimet", eyebrow="Çmimet", h="Falas për të filluar. Pro kur doni gjithçka.", free="Falas", free_desc="Gjithçka që ju duhet për të mos harruar më.", free_feats=["Ndiqni deri në 7 abonime", "Kalendari, pamja e ditës së pagës dhe parashikimi 3-mujor", "Import nga faturat dhe pasqyrat bankare, në pajisje", "Sinkronizim iCloud mes pajisjeve tuaja"], plus="Gjithçka nga Falas, plus", per_month="/muaj", per_year="/vit", once="pagesë e vetme", popular="Më i zgjedhuri", trial="14 ditë falas", save="Kurseni 44%", lifetime_hint="I juaji përgjithmonë, me çdo përditësim", no_fees="Asnjë tarifë mbi atë që kurseni, kurrë. Anuloni nga llogaria juaj Apple në çdo kohë.", prices_note="Çmimet në dollarë amerikanë; App Store tregon çmimin tuaj lokal.", codes_h="Kodet e zbritjes", codes_soon="Së shpejti", codes_body="Ofertat e nisjes dhe kodet promocionale janë rrugës. Do t'i përdorni në aplikacion te Billow Pro › Përdor kodin.", codes_hint="Kodet e para do të shfaqen këtu dhe në faqen e App Store."),
}

def pricing_section(lang, root):
    p = PRICING[lang]; w = lambda k: e(PAYWALL[k][lang])
    pro_feats = [w("paywall.feature.unlimited"), w("paywall.feature.trials"), w("paywall.feature.widgets"), w("paywall.feature.letters"), w("paywall.feature.family")]
    free_lis = "".join(f"<li>{e(x)}</li>" for x in p["free_feats"])
    pro_lis = "".join(f"<li>{x}</li>" for x in pro_feats)
    yearly_line = e(PAYWALL["paywall.yearly.trial"][lang]).replace("%@", PRICES["yearly"], 1).replace("%@", PRICES["yearly_month"], 1)
    return f"""<section class="pricing" id="pricing">
  <div class="wrap">
    <div class="head reveal">
      <div class="eyebrow">{e(p["eyebrow"])}</div>
      <h2>{e(p["h"])}</h2>
      <p class="sub">{w("paywall.sub")}</p>
    </div>
    <div class="plans">
      <div class="plan reveal">
        <h3>{e(p["free"])}</h3>
        <div class="price"><b>$0</b></div>
        <p>{e(p["free_desc"])}</p>
        <ul>{free_lis}</ul>
      </div>
      <div class="plan pro reveal d1">
        <div class="ribbon">{e(p["popular"])} · {e(p["trial"])}</div>
        <h3><span class="badge-pro">{w("paywall.badge")}</span>{w("paywall.plan.yearly")}</h3>
        <div class="price"><b>{PRICES["yearly"]}</b><span>{e(p["per_year"])}</span><em>{e(p["save"])}</em></div>
        <p>{yearly_line}</p>
        <div class="plus">{e(p["plus"])}</div>
        <ul>{pro_lis}</ul>
      </div>
      <div class="plan stack reveal d2">
        <div class="mini">
          <h3><span class="badge-pro">{w("paywall.badge")}</span>{w("paywall.plan.monthly")}</h3>
          <div class="price"><b>{PRICES["monthly"]}</b><span>{e(p["per_month"])}</span></div>
          <p>{w("paywall.monthly")}</p>
        </div>
        <div class="mini">
          <h3><span class="badge-pro">{w("paywall.badge")}</span>{w("paywall.plan.lifetime")}</h3>
          <div class="price"><b>{PRICES["lifetime"]}</b><span>{e(p["once"])}</span></div>
          <p>{w("paywall.lifetime")}. {e(p["lifetime_hint"])}.</p>
        </div>
      </div>
    </div>
    <div class="codes reveal">
      <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v3a2.5 2.5 0 0 0 0 5v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3a2.5 2.5 0 0 0 0-5z"/><path d="M9 9l6 6M15 9l-6 6"/></svg></div>
      <div class="text"><strong>{e(p["codes_h"])} <span class="soon">{e(p["codes_soon"])}</span></strong><span>{e(p["codes_body"])}</span><small>{e(p["codes_hint"])}</small></div>
    </div>
    <p class="note">{e(p["no_fees"])} {e(p["prices_note"])}</p>
  </div>
</section>"""

THEME = {
  "en": dict(name="Appearance", system="System", light="Light", dark="Dark"),
  "de": dict(name="Darstellung", system="System", light="Hell", dark="Dunkel"),
  "es": dict(name="Apariencia", system="Sistema", light="Claro", dark="Oscuro"),
  "it": dict(name="Aspetto", system="Sistema", light="Chiaro", dark="Scuro"),
  "sq": dict(name="Pamja", system="Sistemi", light="E çelët", dark="E errët"),
}
THEME_ICONS = ('<svg class="i-system" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor" stroke="none"/></svg>'
               '<svg class="i-light" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
               '<svg class="i-dark" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>')

def theme_button(lang):
    labels = json.dumps(THEME[lang], ensure_ascii=False).replace("'", "&#39;")
    return f"""<button type="button" class="theme-toggle" data-labels='{labels}' aria-label="{e(THEME[lang]["name"])}">{THEME_ICONS}</button>"""

# ---- FAQ: shown as native <details> and emitted as schema.org FAQPage JSON-LD.
FAQ = {
  "en": ("Questions, answered", "Still wondering? Ask below.", [
    ("Do I need to connect my bank?", "No. Add subscriptions from the catalog of 500+ services, type them in, or share a receipt, screenshot, PDF or bank statement. Everything is read on your iPhone; Billow never asks for bank credentials."),
    ("Where is my data stored?", "On your iPhone and in your own private iCloud database, which also syncs your other devices. Billow has no account, no server and no analytics."),
    ("What is free and what needs Pro?", "Free tracks up to 7 subscriptions with the calendar, payday view and on-device import. Pro removes the limit and adds trial countdowns, price-change alerts, all widgets, export, household sharing and cancellation letters. The yearly plan starts with 14 days free."),
    ("What happens if I stop paying for Pro?", "Nothing is deleted. Your subscriptions stay, and the Free limits apply again until you resubscribe."),
    ("How do I cancel Pro?", "In your Apple account: Settings › your name › Subscriptions › Billow. Cancel at least 24 hours before the renewal date and you won't be charged again."),
    ("Which countries and languages?", "Built for the United States, Albania, Germany, Italy and Spain, in English, Albanian, German, Italian and Spanish, with every currency and your home currency for totals."),
    ("How do free trials work in Billow?", "Mark a subscription as a trial and Billow sets a cancel-by deadline one day before it converts, reminds you at 3 days, 1 day and on the deadline, and shows a Live Activity countdown on your Lock Screen."),
    ("Can I share with my family or household?", "Yes. Household sharing lets up to 5 people join by link, each with their own Apple ID, and only the subscriptions you choose are shared. Pro yearly and lifetime also work with Apple Family Sharing."),
  ]),
  "de": ("Fragen und Antworten", "Noch Fragen? Schreib mir unten.", [
    ("Muss ich meine Bank verbinden?", "Nein. Füge Abos aus dem Katalog mit über 500 Diensten hinzu, tippe sie ein oder teile einen Beleg, Screenshot, ein PDF oder einen Kontoauszug. Alles wird auf deinem iPhone gelesen; Billow fragt nie nach Bankzugangsdaten."),
    ("Wo werden meine Daten gespeichert?", "Auf deinem iPhone und in deiner eigenen privaten iCloud-Datenbank, die auch deine anderen Geräte synchronisiert. Billow hat kein Konto, keinen Server und keine Analytik."),
    ("Was ist kostenlos und wofür brauche ich Pro?", "Kostenlos verwaltet bis zu 7 Abos mit Kalender, Zahltag-Ansicht und Import auf dem Gerät. Pro hebt das Limit auf und ergänzt Testphasen-Countdowns, Preiswarnungen, alle Widgets, Export, Haushalt-Teilen und Kündigungsschreiben. Das Jahresabo beginnt mit 14 Tagen kostenlos."),
    ("Was passiert, wenn ich Pro nicht mehr bezahle?", "Es wird nichts gelöscht. Deine Abos bleiben, und die Limits der kostenlosen Version gelten wieder, bis du erneut abonnierst."),
    ("Wie kündige ich Pro?", "In deinem Apple-Konto: Einstellungen › dein Name › Abonnements › Billow. Kündige mindestens 24 Stunden vor der Verlängerung, dann wird nichts mehr abgebucht."),
    ("Welche Länder und Sprachen?", "Gemacht für die USA, Albanien, Deutschland, Italien und Spanien, auf Deutsch, Englisch, Albanisch, Italienisch und Spanisch, mit jeder Währung und deiner Hauptwährung für Summen."),
    ("Wie funktionieren Testphasen in Billow?", "Markiere ein Abo als Testphase und Billow setzt eine „Kündigen bis“-Frist einen Tag vor der Umwandlung, erinnert dich 3 Tage, 1 Tag vorher und am Stichtag und zeigt einen Live-Activity-Countdown auf dem Sperrbildschirm."),
    ("Kann ich mit Familie oder Haushalt teilen?", "Ja. Beim Haushalt-Teilen treten bis zu 5 Personen per Link bei, jede mit eigener Apple-ID, und nur die Abos, die du auswählst, werden geteilt. Pro Jährlich und Lifetime funktionieren auch mit der Apple-Familienfreigabe."),
  ]),
  "es": ("Preguntas frecuentes", "¿Todavía tienes dudas? Pregunta abajo.", [
    ("¿Tengo que conectar mi banco?", "No. Añade suscripciones desde el catálogo de más de 500 servicios, escríbelas o comparte un recibo, una captura, un PDF o un extracto bancario. Todo se lee en tu iPhone; Billow nunca pide credenciales bancarias."),
    ("¿Dónde se guardan mis datos?", "En tu iPhone y en tu propia base de datos privada de iCloud, que también sincroniza tus otros dispositivos. Billow no tiene cuenta, ni servidor, ni analíticas."),
    ("¿Qué es gratis y qué necesita Pro?", "Gratis controla hasta 7 suscripciones con calendario, vista del día de pago e importación en el dispositivo. Pro quita el límite y añade cuentas atrás de pruebas, avisos de subidas de precio, todos los widgets, exportación, uso compartido en casa y cartas de cancelación. El plan anual empieza con 14 días gratis."),
    ("¿Qué pasa si dejo de pagar Pro?", "No se borra nada. Tus suscripciones se quedan y vuelven a aplicarse los límites de Gratis hasta que te suscribas de nuevo."),
    ("¿Cómo cancelo Pro?", "En tu cuenta de Apple: Ajustes › tu nombre › Suscripciones › Billow. Cancela al menos 24 horas antes de la renovación y no se te volverá a cobrar."),
    ("¿Qué países e idiomas?", "Pensado para Estados Unidos, Albania, Alemania, Italia y España, en español, inglés, albanés, alemán e italiano, con cualquier moneda y tu moneda principal para los totales."),
    ("¿Cómo funcionan las pruebas gratis en Billow?", "Marca una suscripción como prueba y Billow fija un plazo «cancelar antes del» un día antes de que pase a ser de pago, te recuerda a los 3 días, 1 día y en la fecha límite, y muestra una cuenta atrás en Actividad en vivo en la pantalla bloqueada."),
    ("¿Puedo compartir con mi familia o mi hogar?", "Sí. Con el uso compartido en casa, hasta 5 personas se unen con un enlace, cada una con su Apple ID, y solo se comparten las suscripciones que elijas. Pro anual y Lifetime también funcionan con En familia de Apple."),
  ]),
  "it": ("Domande frequenti", "Hai ancora dubbi? Chiedi qui sotto.", [
    ("Devo collegare la banca?", "No. Aggiungi gli abbonamenti dal catalogo di oltre 500 servizi, scrivili o condividi una ricevuta, uno screenshot, un PDF o un estratto conto. Tutto viene letto sul tuo iPhone; Billow non chiede mai credenziali bancarie."),
    ("Dove sono salvati i miei dati?", "Sul tuo iPhone e nel tuo database privato di iCloud, che sincronizza anche gli altri tuoi dispositivi. Billow non ha account, server né analytics."),
    ("Cosa è gratis e cosa richiede Pro?", "Gratis segue fino a 7 abbonamenti con calendario, vista stipendio e import sul dispositivo. Pro toglie il limite e aggiunge conto alla rovescia delle prove, avvisi sugli aumenti di prezzo, tutti i widget, esportazione, condivisione familiare e lettere di disdetta. Il piano annuale parte con 14 giorni gratis."),
    ("Cosa succede se smetto di pagare Pro?", "Non viene eliminato nulla. I tuoi abbonamenti restano e tornano a valere i limiti di Gratis finché non ti riabboni."),
    ("Come disdico Pro?", "Dal tuo account Apple: Impostazioni › il tuo nome › Abbonamenti › Billow. Disdici almeno 24 ore prima del rinnovo e non ti verrà più addebitato nulla."),
    ("Quali paesi e lingue?", "Pensato per Stati Uniti, Albania, Germania, Italia e Spagna, in italiano, inglese, albanese, tedesco e spagnolo, con ogni valuta e la tua valuta principale per i totali."),
    ("Come funzionano le prove gratuite in Billow?", "Segna un abbonamento come prova e Billow imposta una scadenza «disdici entro» un giorno prima della conversione, ti ricorda a 3 giorni, 1 giorno e alla scadenza, e mostra un conto alla rovescia in Attività Live sulla schermata di blocco."),
    ("Posso condividere con la famiglia?", "Sì. Con la condivisione familiare fino a 5 persone entrano con un link, ognuna con il proprio Apple ID, e si condividono solo gli abbonamenti che scegli. Pro annuale e Lifetime funzionano anche con In famiglia di Apple."),
  ]),
  "sq": ("Pyetje dhe përgjigje", "Keni ende pyetje? Shkruani më poshtë.", [
    ("A duhet të lidh bankën?", "Jo. Shtoni abonime nga katalogu me mbi 500 shërbime, shkruajini ose ndani një faturë, pamje ekrani, PDF ose pasqyrë bankare. Gjithçka lexohet në iPhone-in tuaj; Billow nuk kërkon kurrë kredenciale bankare."),
    ("Ku ruhen të dhënat e mia?", "Në iPhone-in tuaj dhe në bazën tuaj private të iCloud, që sinkronizon edhe pajisjet e tjera. Billow nuk ka llogari, server apo analitikë."),
    ("Çfarë është falas dhe çfarë kërkon Pro?", "Falas ndjek deri në 7 abonime me kalendarin, pamjen e ditës së pagës dhe importin në pajisje. Pro heq kufirin dhe shton numërimin mbrapsht të provave, njoftimet për rritje çmimi, të gjitha widget-et, eksportin, ndarjen familjare dhe letrat e anulimit. Plani vjetor fillon me 14 ditë falas."),
    ("Çfarë ndodh nëse ndaloj së paguari Pro?", "Asgjë nuk fshihet. Abonimet tuaja mbeten dhe kufijtë e versionit Falas zbatohen sërish derisa të riabonoheni."),
    ("Si e anuloj Pro?", "Në llogarinë tuaj Apple: Settings › emri juaj › Subscriptions › Billow. Anuloni të paktën 24 orë para rinovimit dhe nuk do të paguani më."),
    ("Cilat vende dhe gjuhë?", "Krijuar për SHBA-në, Shqipërinë, Gjermaninë, Italinë dhe Spanjën, në shqip, anglisht, gjermanisht, italisht dhe spanjisht, me çdo monedhë dhe monedhën tuaj kryesore për totalet."),
    ("Si funksionojnë provat falas në Billow?", "Shënoni një abonim si provë dhe Billow vendos afatin “anuloni deri” një ditë para se të kthehet me pagesë, ju kujton 3 ditë, 1 ditë para dhe në afat, dhe tregon numërimin mbrapsht në Live Activity në ekranin e kyçur."),
    ("A mund ta ndaj me familjen?", "Po. Me ndarjen familjare deri në 5 persona hyjnë me një lidhje, secili me Apple ID-në e vet, dhe ndahen vetëm abonimet që zgjidhni ju. Pro vjetor dhe Lifetime punojnë edhe me Family Sharing të Apple."),
  ]),
}

def faq_section(lang, root):
    h, sub, items = FAQ[lang]
    details = "\n      ".join(f'<details class="faq-item reveal"{" open" if i == 0 else ""}><summary>{e(q)}<span class="chev" aria-hidden="true"></span></summary><div class="answer"><p>{e(a)}</p></div></details>' for i, (q, a) in enumerate(items))
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False)
    return f"""<section class="faq" id="faq">
  <div class="wrap">
    <div class="head reveal">
      <h2>{e(h)}</h2>
      <p class="sub">{e(sub)} <a href="#contact">{e(CONTACT[lang]["nav"])}</a></p>
    </div>
    <div class="faq-list">
      {details}
    </div>
  </div>
</section>
<script type="application/ld+json">{ld}</script>"""

LIGHTBOX = {
  "en": dict(close="Close", prev="Previous screen", next="Next screen", open="Open {0} full size"),
  "de": dict(close="Schließen", prev="Vorheriger Bildschirm", next="Nächster Bildschirm", open="{0} in voller Größe öffnen"),
  "es": dict(close="Cerrar", prev="Pantalla anterior", next="Pantalla siguiente", open="Abrir {0} a tamaño completo"),
  "it": dict(close="Chiudi", prev="Schermata precedente", next="Schermata successiva", open="Apri {0} a schermo intero"),
  "sq": dict(close="Mbyll", prev="Ekrani i mëparshëm", next="Ekrani tjetër", open="Hap {0} në madhësi të plotë"),
}

def page(lang):
    t = T[lang]
    root = "" if lang == "en" else "../"
    def url(l):
        return BASE if l == "en" else f"{BASE}{l}/"
    def href(l):
        return f"{root}index.html" if l == "en" else f"{root}{l}/index.html"
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in LANGS)
    options = "".join(f'<option value="{l}" data-href="{href(l)}"{" selected" if l == lang else ""}>{NAMES[l]}</option>' for l in LANGS)
    flags = "".join(f'<a href="{href(l)}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{NAMES[l]}</a>' for l in LANGS)
    pills = "".join(f'<span class="pill">{e(p)}</span>' for p in t["pills"])
    kicker = t["title"].split(" — ", 1)[-1]
    cards = "\n      ".join(
        f'<div class="card c{i + 1}"><span class="ci {cls}">{svg}</span><span><small>{e(a)}</small><strong>{e(b)}</strong></span></div>'
        for i, ((cls, svg), (a, b)) in enumerate(zip(CARD_ICONS, HERO_CARDS[lang])))
    ticker = "".join(f'<span><i>{n[0]}</i>{e(n)}</span>' for n in SERVICES)
    stats = "\n      ".join(f'<div class="stat"><b data-count="{e(v)}">{e(v)}</b><span>{e(l)}</span></div>' for v, l in STATS[lang])
    shots = {"s1": "detail", "s2": "calendar", "s5": "insights", "s3": "onboarding", "s4": "add", "s6": "mailboxes"}
    sections = []
    for i, k in enumerate(["s1", "s2", "s5", "s3", "s4", "s6"]):
        eyebrow, h2, p, items, alt = t[k]
        p = e(p).replace("{tag}", f'<span class="tag-amber">{e(t["tag"])}</span>')
        p = p.replace("{privacy}", f'<a href="{root}privacy.html">{e(t["privacy_link"])}</a>')
        lis = "\n        ".join(f"<li>{e(x)}</li>" for x in items)
        flip = " flip" if i % 2 else ""
        sections.append(f"""<section class="feature{flip}">
  <div class="wrap">
    <div class="text reveal">
      <div class="eyebrow">{e(eyebrow)}</div>
      <h2>{e(h2)}</h2>
      <p>{p}</p>
      <ul>
        {lis}
      </ul>
    </div>
    <div class="shot reveal d1"><div class="phone"><img src="{root}img/{shots[k]}.jpg" alt="{e(alt)}" loading="lazy" width="414" height="900"></div></div>
  </div>
</section>""")
    gallery = "\n    ".join(
        f'<figure><button type="button" class="shot-btn" aria-label="{e(LIGHTBOX[lang]["open"].format(c))}"><div class="phone"><img src="{root}img/{n}.jpg" alt="{e(c)}" loading="lazy" width="414" height="900"></div></button><figcaption>{e(c)}</figcaption></figure>'
        for n, c in zip(GALLERY, t["caps"]))
    lb_labels = json.dumps({k: LIGHTBOX[lang][k] for k in ("close", "prev", "next")}, ensure_ascii=False).replace("'", "&#39;")
    tiles = "\n      ".join(
        f'<div class="tile reveal d{i % 4}"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><strong>{e(a)}</strong><span>{e(b)}</span></div>'
        for i, (ico, (a, b)) in enumerate(zip(ICONS, t["tiles"])))
    style = STYLE.replace("</style>", EXTRA_CSS + "</style>")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="theme-color" content="#06202A">
<link rel="canonical" href="{url(lang)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}">
<link rel="icon" href="{root}img/icon.png">
<link rel="apple-touch-icon" href="{root}img/icon.png">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["og"])}">
<meta property="og:locale" content="{OG[lang]}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url(lang)}">
<meta property="og:site_name" content="Billow">
<meta property="og:image" content="{BASE}img/og-{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t["og"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(t["title"])}">
<meta name="twitter:description" content="{e(t["og"])}">
<meta name="twitter:image" content="{BASE}img/og-{lang}.png">
{DETECT if lang == "en" else ""}
{JS_FLAG}
{style}
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="{href(lang)}"><img src="{root}img/icon.png" alt="">Billow</a>
    <nav>
      <a class="hide-sm" href="#features">{e(t["nav_features"])}</a>
      <a class="hide-sm" href="#try">{e(TRY[lang]["nav"])}</a>
      <a class="hide-sm" href="#pricing">{e(PRICING[lang]["nav"])}</a>
      <a class="hide-sm" href="#privacy">{e(t["nav_privacy"])}</a>
      <a class="cta" href="{root}support.html">{e(t["nav_support"])}</a>
      <label class="lang"><span class="visually-hidden">{e(t["lang_label"])}</span><select id="lang" aria-label="{e(t["lang_label"])}">{options}</select></label>
      {theme_button(lang)}
    </nav>
  </div>
</header>

<section class="hero" id="hero">
  <div class="wrap">
    <div>
      <span class="kicker"><i></i>{e(kicker)}</span>
      <h1>{e(t["h1a"])} <span>{e(t["h1b"])}</span></h1>
      <p class="lead">{e(t["lead"])}</p>
      <div class="cta-row">
        <span class="badge">{APPLE}{e(t["badge"])}</span>
        <a class="ghost" href="#try">{e(TRY[lang]["nav"])}{ARROW}</a>
      </div>
      <div class="pills">{pills}</div>
    </div>
    <div class="visual">
      <div class="ring" aria-hidden="true"></div>
      <div class="glow" aria-hidden="true"></div>
      <div class="stage">
        <div class="phone"><div class="screen"><img src="{root}img/home.jpg" alt="{e(t["alt_home"])}" width="414" height="900" fetchpriority="high"><img src="{root}img/calendar.jpg" alt="" width="414" height="900" loading="lazy"><img src="{root}img/insights.jpg" alt="" width="414" height="900" loading="lazy"><img src="{root}img/detail.jpg" alt="" width="414" height="900" loading="lazy"></div></div>
        {cards}
      </div>
    </div>
  </div>
</section>

<section class="stats" aria-label="Billow in numbers">
  <div class="wrap">
    <div>
      {stats}
    </div>
  </div>
</section>

{try_section(lang, root)}

<main id="features">

{chr(10).join(sections)}

</main>

{more_section(lang, root)}

{pricing_section(lang, root)}

<section class="gallery">
  <div class="head reveal"><h2>{e(t["gallery"])}</h2></div>
  <div class="strip" data-labels='{lb_labels}'>
    {gallery}
  </div>
</section>

<section class="privacy" id="privacy">
  <div class="wrap">
    <div class="reveal">
      <h2>{e(t["priv_h"])}</h2>
      <p class="sub">{e(t["priv_sub"])}</p>
    </div>
    <div class="grid4">
      {tiles}
    </div>
  </div>
</section>

<section class="langs">
  <div class="wrap reveal">
    <h2>{e(t["langs_h"])}</h2>
    <div class="flags">{flags}</div>
  </div>
</section>

{faq_section(lang, root)}

{contact_section(lang, root)}

<section class="closing">
  <div class="wrap">
    <div class="box reveal">
      <h2>{e(t["h1a"])} <span>{e(t["h1b"])}</span></h2>
      <p>{e(t["priv_sub"])}</p>
      <div class="cta-row"><span class="badge">{APPLE}{e(t["badge"])}</span></div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <a class="brand" href="{href(lang)}"><img src="{root}img/icon.png" alt="">Billow</a>
    <nav><a href="{root}support.html">{e(t["nav_support"])}</a><a href="#faq">FAQ</a><a href="#contact">{e(CONTACT[lang]["nav"])}</a><a href="{root}privacy.html">{e(t["privacy_policy"])}</a><a href="{root}terms.html">{e(TERMS[lang])}</a></nav>
    <span>© 2026 <a class="author" href="https://www.linkedin.com/in/ervin-capi/" rel="me noopener" target="_blank">Ervin Capi<svg viewBox="0 0 24 24" aria-label="LinkedIn" role="img"><path d="M20.4 2H3.6A1.6 1.6 0 0 0 2 3.6v16.8A1.6 1.6 0 0 0 3.6 22h16.8a1.6 1.6 0 0 0 1.6-1.6V3.6A1.6 1.6 0 0 0 20.4 2zM8 19H5v-9h3zM6.5 8.7a1.7 1.7 0 1 1 0-3.4 1.7 1.7 0 0 1 0 3.4zM19 19h-3v-4.6c0-1.1 0-2.5-1.5-2.5S12.7 13 12.7 14.3V19h-3v-9h2.9v1.2a3.2 3.2 0 0 1 2.9-1.6c3.1 0 3.6 2 3.6 4.7z"/></svg></a> · {e(t["logos_by"])} <a href="https://logo.dev">Logo.dev</a></span>
  </div>
</footer>

{REMEMBER}
</body>
</html>
"""


for lang in LANGS:
    out = SITE / "index.html" if lang == "en" else SITE / lang / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page(lang))
    print(out)
