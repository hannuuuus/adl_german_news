# -*- coding: utf-8 -*-

# Scrapy settings for news_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = "news_crawler"

SPIDER_MODULES = ["news_crawler.spiders"]
NEWSPIDER_MODULE = "news_crawler.spiders"

# Run spider until item count or timeout
CLOSESPIDER_ITEMCOUNT = 1000
CLOSESPIDER_TIMEOUT = 3600 * 24 * 3

# Project-specific variables
TOPIC = "all"


START_DATE = "01.01.2019"


END_DATE = "19.10.2024"

ARTICLE_LENGTH = 100
KEYWORDS_MIN_FREQUENCY = 2
KEYWORDS_MIN_DISTANCE = 5  # must be geq 1

KEYWORDS = [
    "klimawandel",
    "klimaveränderung",
    "klimaschutz",
    "klimaziel",
    "klimapolitik",
    "klimakrise",
    "klimaneutral",
    "klimafreundlich",
    "erderwärmung",
    "globale erwärmung",
    "treibhauseffekt",
    "kohlenstoffbudget",
    "ipcc",
    "weltklima",
    "un-klima",
    "climate-engineering",
    "fridays for future",
    "klimastreik",
    "cop26",
    "glasgow climate conference",
    "kyoto-protokoll",
    "übereinkommen von paris",
    "greta thunberg",
    "kohleausstieg",
    "energiewende",
    "erneuerbare energien",
    "fossile brennstoffe",
    "elektromobilität",
    "verkehrswende",
    "grüner strom",
    "solarenergie",
    "windkraft",
    "windenergie",
    "photovoltaik",
    "klimakatastrophe",
    "klimagerechtigkeit",
    "nutzenergie",
    "co2-neutrales europa",
    "grüner deal",
    "eu green deal",
    "wasserstoffstrategie",
    "klimadividende",
    "olaf scholz",
    "angela merkel",
    "annalena baerbock",
    "robert habeck",
    "christian lindner",
    "armin laschet",
    "markus söder",
    "saskia esken",
    "norbert walter-borjans",
    "friedrich merz",
    "sahra wagenknecht",
    "dietmar bartsch",
    "janine wissler",
    "alice weidel",
    "tino chrupalla",
    "flüchtlingskrise",
    "migration",
    "zuwanderung",
    "integration",
    "asylpolitik",
    "eu-asylpolitik",
    "migrationpakt",
    "immigration",
    "migrationspolitik",
    "einwanderung",
    "grenzen",
    "deutschlandpakt",
    "ausländerpolitik",
    "fluchtursachen",
    "abschiebung",
    "dublin-verfahren",
    "globaler süden",
    "wohnungsnot",
    "mietpreisdeckel",
    "soziale gerechtigkeit",
    "armutsgrenze",
    "wohlstandskluft",
    "inflation",
    "wirtschaftswachstum",
    "steuerreform",
    "corona",
    "pandemie",
    "lockdown",
    "impfpflicht",
    "impfstoff",
    "rki",
    "coronaschutzverordnung",
    "kontaktbeschränkungen",
    "homeoffice",
    "digitalisierung",
    "datenschutz",
    "cybersicherheit",
    "5g-netzausbau",
    "netzpolitik",
    "gesundheitsversorgung",
    "gesundheitsreform",
    "pflegekrise",
    "pflegenotstand",
    "pflegereform",
    "krankenkassenreform",
    "bürgerversicherung",
    "rentenreform",
    "grundrente",
    "arbeitsmarkt",
    "arbeitslosigkeit",
    "arbeitsmarktpolitik",
    "arbeitsplatzsicherung",
    "lohngerechtigkeit",
    "frauenquote",
    "gender pay gap",
    "klimaflüchtlinge",
    "kindergrundsicherung",
    "familienpolitik",
    "bildungspolitik",
    "kita-gebühren",
    "schulpolitik",
    "digitalpakt schule",
    "corona-bonus",
    "corona-hilfen",
    "wirtschaftshilfen",
    "kleinunternehmer",
    "mittelstand",
    "green finance",
    "grüne technologie",
    "umweltpolitik",
    "plastikmüll",
    "einwegplastik-verbot",
    "ressourcenschonung",
    "kreislaufwirtschaft",
    "ökodesign-richtlinie",
    "landwirtschaftspolitik",
    "agrarreform",
    "biodiversität",
    "artenschutz",
    "waldsterben",
    "ozeanverschmutzung",
    "bodendegradation",
    "tierwohl",
    "massentierhaltung",
    "veganismus",
    "ökologische landwirtschaft",
    "biolandwirtschaft",
    "umweltschutz",
    "naturschutz",
    "cdu",
    "csu",
    "spd",
    "fdp",
    "die grünen",
    "linke",
    "afd",
    "bundestagswahl",
    "europa-wahl",
    "rechtsextremismus",
    "rechtspopulismus",
    "linksextremismus",
    "klimaskeptiker",
    "verschwörungstheorien",
    "querdenker",
    "antifa",
    "anti-semitismus",
    "islamfeindlichkeit",
    "rassismus",
    "feminismus",
    "equal pay",
    "gleichberechtigung",
    "israel",
    "nahost",
    "terror",
    "isis",
    "islamisch",
    "muslimisch",
    "muslim",
    "christ",
    "hamas",
    "tesla",
    "demo",
    "sebastian kurz",
    "strache",
    "kogler",
    "gruene",
    "fpoe",
    "oesterreich",
    "spoe",
    "naturschutz",
    "schi",
    "ischgl",
    "ukraine",
    "krieg",
    "klima",
    "leiche",
    "mrna",
    "rna",
    "ns",
    "nazi",
    "hitler",
    "ss",
    "amnesty",
    "europa",
    "asien",
    "afrika",
    "amerika",
    "usa",
    "us",
    "frankreich",
    "alexander van der bellen",
    "karl nehammer",
    "werner kogler",
    "herbert kickl",
    "norbert hofer",
    "Assad" "pamela rendi-wagner",
    "christian kern",
    "maria theresia fischer",
    "natascha strobl",
    "oevp",
    "fpoe",
    "spo",
    "gruene",
    "neos",
    "fpö",
    "övp",
    "ibiza-affäre",
    "ibiza-video",
    "strache",
    "strache-skandal",
    "rücktritt sebastian kurz",
    "basti-fantasti",
    "korruptionsaffäre",
    "chatprotokolle",
    "postenschacher",
    "kaufhaus oesterreich",
    "asylpolitik österreich",
    "migrationspolitik",
    "schwarz-blaue koalition",
    "türkise koalition",
    "schwarz-grüne koalition",
    "flüchtlingskrise",
    "österreichische neutralität",
    "wehrpflicht",
    "bundesheer",
    "impfpflicht österreich",
    "corona-maßnahmen österreich",
    "lockdown österreich",
    "österreichischer wirtschaftsaufschwung",
    "wirtschaftshilfen corona",
    "grenzkontrollen österreich",
    "klimapolitik österreich",
    "klimaneutralität 2040",
    "erneuerbare energien",
    "energiepolitik österreich",
    "österreichische wirtschaftspolitik",
    "steuerpolitik",
    "mindestsicherung",
    "sozialpolitik",
    "arbeitsmarktpolitik",
    "corona",
    "pandemie",
    "politik",
    "pensionen",
    "rentenreform",
    "arbeitslosigkeit österreich",
    "rechtsstaatlichkeit",
    "freiheitliche grundordnung",
    "bsw",
    "freiheitliche",
    "sparen",
    "rechtsruck österreich",
    "rechtspopulismus",
    "sozialpartnerschaft",
    "frauenpolitik",
    "gleichstellung",
    "bildungspolitik",
    "universitätsreform",
    "studiengebühren",
    "österreichische eu-politik",
    "eu-beitritt",
    "austritt fpoe",
    "öxit",
    "österreichische außenpolitik",
    "westbalkan-konferenz",
    "europäische union",
    "österreich in der eu",
    "schengen-raum",
    "unhcr",
    "unesco",
    "vereinte nationen",
    "nato-partnerschaft",
    "österreichische neutralität",
    "klimastreik wien",
    "fridays for future wien",
    "erneuerbare energie förderung",
    "guy parmelin",
    "ignazio cassis",
    "alain berset",
    "viola amherd",
    "uli maurer",
    "simonetta sommaruga",
    "svp",
    "sp",
    "fdp",
    "cvp",
    "grüne schweiz",
    "glp",
    "evp",
    "schweizerischer bundesrat",
    "schweizer bundesversammlung",
    "direkte demokratie",
    "volksabstimmung",
    "eidgenössische wahlen",
    "schweizer neutralität",
    "neutralität schweiz",
    "schweizer asylpolitik",
    "flüchtlingspolitik schweiz",
    "migrationspolitik schweiz",
    "zuwanderung schweiz",
    "masseneinwanderungsinitiative",
    "fremdenfeindlichkeit",
    "minarettverbot",
    "ehe für alle",
    "volksinitiative",
    "rentenreform schweiz",
    "pensionskassenreform",
    "altersvorsorge 2020",
    "bilaterale abkommen eu",
    "rahmenabkommen schweiz eu",
    "eu-beitritt schweiz",
    "schweizer eu-beziehungen",
    "schweizer wirtschaftspolitik",
    "freihandelsabkommen schweiz",
    "steueroase",
    "bankgeheimnis",
    "steuerpolitik schweiz",
    "klimapolitik schweiz",
    "co2-gesetz",
    "klimaneutralität 2050",
    "energiegesetz schweiz",
    "energiewende schweiz",
    "kernenergie schweiz",
    "ausstieg aus der kernenergie",
    "erneuerbare energien schweiz",
    "wasserkraft schweiz",
    "swissness",
    "covid-19 schweiz",
    "corona-pandemie schweiz",
    "corona-maßnahmen schweiz",
    "corona-impfungen schweiz",
    "gesundheitspolitik schweiz",
    "krankenkassenreform schweiz",
    "spitäler schweiz",
    "bildungsvergleich schweiz",
    "arbeitsmarkt schweiz",
    "arbeitslosigkeit schweiz",
    "sozialpolitik schweiz",
    "schweizerische volkspartei",
    "rechtspopulismus schweiz",
    "feminismus schweiz",
    "gleichstellung der geschlechter",
    "geschlechterparität schweiz",
    "jugendpolitik schweiz",
    "bildungspolitik schweiz",
    "wissenschaftsförderung schweiz",
    "digitalisierung schweiz",
    "cybersicherheit schweiz",
    "5g-ausbau schweiz",
    "verkehrspolitik schweiz",
    "alpentransit",
    "schweizer tourismuspolitik",
    "alpeninitiative",
    "sbb",
    "postauto-skandal",
    "syrienkonferenz schweiz",
    "genfer konvention",
    "uno schweiz",
    "humanitäre hilfe schweiz",
    "helvetismus",
    "swiss army",
    "wehrpflicht schweiz",
    "milizarmee schweiz",
    "gdp",
    "bip",
    "bruttoinlandsprodukt",
    "familie",
    "regierung",
    "syrien",
    "waffenruhe",
    "5g",
    "afd",
    "asyl",
    "kriminell",
    "ampel",
    "leitkultur",
    "kultur",
    "nazi",
    "greta",
    "trump",
    "xi",
]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'news_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'news_crawler.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "news_crawler.middlewares.RotateUserAgentMiddleware": 110,
}

# User agents used for rotation (most common agents)
USER_AGENT_CHOICES = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
    "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.42 (KHTML, like Gecko) Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.42",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
]

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
PERSIST_STATS_ENABLED = True
EXTENSIONS = {
    "scrapy.extensions.closespider.CloseSpider": 500,
    "news_crawler.extensions.PersistStatsExtension": 500,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "news_crawler.pipelines.HtmlWriterPipeline": 100,
    "news_crawler.pipelines.JsonWriterPipeline": 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enableand configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
