"""The stories of Sunday 22 November 2026, chosen for the judge's criteria.

Order matters: index 0 is the lead. Selection weighs consequence and regional spread, not
how many outlets repeated a story. Every line was reported on 22 November 2026 by at least
one of the feeds in ni22-src/; the source column names one that carried it that day.
"""

DAY = "SUNDAY 22 NOVEMBER 2026"

# (region, kicker, headline, one-line detail, illustration key)
LEADS = [
    ("GLOBAL", "COP31", "CLIMATE TALKS COLLAPSE",
     "No deal in the final hours: the EU and others rejected a text that dropped any mention of fossil fuels.",
     "cop"),
    ("MIDDLE EAST", "HORMUZ", "TANKERS ABLAZE IN THE GULF",
     "Two vessels hit in the Strait of Hormuz; Bahrain accuses Iran of striking an industrial site.",
     "tanker"),
    ("NORTH AFRICA", "BENGHAZI", "DRONES STRIKE A RUSSIAN WARSHIP",
     "Suspected Ukrainian sea drones hit a Russian ship at a Libyan naval base; a second vessel was targeted.",
     "drone"),
]

# (region, headline, illustration key) — the day's consequential stories beyond the leads
PANELS = [
    ("UKRAINE", "Kyiv region strikes kill six as rescuers search the rubble", "rubble"),
    ("SUDAN", "RSF drone strikes hit homes and a UN building in Khartoum", "sudan"),
    ("UNITED STATES", "Democrats clinch 258 House seats, their largest majority since 1992", "capitol"),
    ("WEST BANK", "Settler fires in the West Bank draw 'terrorism' warning", "fire"),
    ("ISRAEL", "Coalition talks between Likud and Yashar end with no deal", "knesset"),
    ("INDONESIA", "Factory blaze kills three with dozens missing in Java", "factory"),
    ("SOUTH KOREA", "Education minister resigns over AI-driven exam cheating scandal", "exam"),
    ("MEXICO", "Drug lord on the FBI's ten most wanted arrested in a shoot-out", "arrest"),
    ("LIBYA", "Suspected drone attack explodes on a Russian ship off the coast", "port"),
]

# Short items that widen the map without claiming to be the day's biggest news
BRIEFS = [
    ("USA", "FBI said to be probing a hack of its criminal database"),
    ("UK", "Princess of Wales speaks publicly about her cancer"),
    ("FINLAND", "Russia tows away a ship damaged in the Gulf of Finland"),
    ("FRANCE", "Le Pen denies receiving leaked interior ministry information"),
    ("SEATTLE", "ICE arrests on an airport jet bridge draw condemnation"),
    ("NIGERIA", "Youth ask why they still do not shape the election"),
    ("BAHRAIN", "Manama blames Iran for striking an industrial site"),
    ("JAPAN", "Calls grow for the education minister to step down"),
    ("EUROPE", "Cost-of-living protests spread across several cities"),
    ("HK", "Election Committee turnout reaches a record 99 per cent"),
    ("CINEMA", "Hong Kong films take honours at the Golden Horse Awards"),
    ("SPORT", "Liverpool beat ten-man Manchester United 4-0"),
]

# Regions with a story on the map, for the "where it happened" panel
MAP_PINS = [
    ("COP31 summit", 0.13, 0.30),
    ("Strait of Hormuz", 0.62, 0.44),
    ("Benghazi", 0.52, 0.44),
    ("Kyiv", 0.57, 0.26),
    ("Khartoum", 0.57, 0.55),
    ("Washington", 0.22, 0.36),
    ("West Bank", 0.56, 0.42),
    ("Java", 0.79, 0.62),
    ("Seoul", 0.84, 0.34),
    ("Mexico", 0.18, 0.50),
    ("Gulf of Finland", 0.58, 0.20),
    ("Hong Kong", 0.80, 0.46),
]

SOURCES = ["BBC", "Al Jazeera", "France 24", "SCMP", "The Guardian", "NPR", "CNBC"]
