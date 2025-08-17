import os
import requests
from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
from datetime import datetime

# Correspondance des champs de l'API Météo-Concept (prévisions)

WEATHER_CODES = {
    0: "Soleil",
    1: "Peu nuageux",
    2: "Ciel voilé",
    3: "Nuageux",
    4: "Très nuageux",
    5: "Couvert",
    6: "Brouillard",
    7: "Brouillard givrant",
    10: "Pluie faible",
    11: "Pluie modérée",
    12: "Pluie forte",
    13: "Pluie faible verglaçante",
    14: "Pluie modérée verglaçante",
    15: "Pluie forte verglaçante",
    16: "Bruine",
    20: "Neige faible",
    21: "Neige modérée",
    22: "Neige forte",
    30: "Pluie et neige mêlées faibles",
    31: "Pluie et neige mêlées modérées",
    32: "Pluie et neige mêlées fortes",
    40: "Averses de pluie locales et faibles",
    41: "Averses de pluie locales",
    42: "Averses locales et fortes",
    43: "Averses de pluie faibles",
    44: "Averses de pluie",
    45: "Averses de pluie fortes",
    46: "Averses de pluie faibles et fréquentes",
    47: "Averses de pluie fréquentes",
    48: "Averses de pluie fortes et fréquentes",
    60: "Averses de neige localisées et faibles",
    61: "Averses de neige localisées",
    62: "Averses de neige localisées et fortes",
    63: "Averses de neige faibles",
    64: "Averses de neige",
    65: "Averses de neige fortes",
    66: "Averses de neige faibles et fréquentes",
    67: "Averses de neige fréquentes",
    68: "Averses de neige fortes et fréquentes",
    70: "Averses de pluie et neige mêlées localisées et faibles",
    71: "Averses de pluie et neige mêlées localisées",
    72: "Averses de pluie et neige mêlées localisées et fortes",
    73: "Averses de pluie et neige mêlées faibles",
    74: "Averses de pluie et neige mêlées",
    75: "Averses de pluie et neige mêlées fortes",
    76: "Averses de pluie et neige mêlées faibles et nombreuses",
    77: "Averses de pluie et neige mêlées fréquentes",
    78: "Averses de pluie et neige mêlées fortes et fréquentes",
    100: "Orages faibles et locaux",
    101: "Orages locaux",
    102: "Orages fort et locaux",
    103: "Orages faibles",
    104: "Orages",
    105: "Orages forts",
    106: "Orages faibles et fréquents",
    107: "Orages fréquents",
    108: "Orages forts et fréquents",
    120: "Orages faibles et locaux de neige ou grésil",
    121: "Orages locaux de neige ou grésil",
    122: "Orages locaux de neige ou grésil",
    123: "Orages faibles de neige ou grésil",
    124: "Orages de neige ou grésil",
    125: "Orages de neige ou grésil",
    126: "Orages faibles et fréquents de neige ou grésil",
    127: "Orages fréquents de neige ou grésil",
    128: "Orages fréquents de neige ou grésil",
    130: "Orages faibles et locaux de pluie et neige mêlées ou grésil",
    131: "Orages locaux de pluie et neige mêlées ou grésil",
    132: "Orages fort et locaux de pluie et neige mêlées ou grésil",
    133: "Orages faibles de pluie et neige mêlées ou grésil",
    134: "Orages de pluie et neige mêlées ou grésil",
    135: "Orages forts de pluie et neige mêlées ou grésil",
    136: "Orages faibles et fréquents de pluie et neige mêlées ou grésil",
    137: "Orages fréquents de pluie et neige mêlées ou grésil",
    138: "Orages forts et fréquents de pluie et neige mêlées ou grésil",
    140: "Pluies orageuses",
    141: "Pluie et neige mêlées à caractère orageux",
    142: "Neige à caractère orageux",
    210: "Pluie faible intermittente",
    211: "Pluie modérée intermittente",
    212: "Pluie forte intermittente",
    220: "Neige faible intermittente",
    221: "Neige modérée intermittente",
    222: "Neige forte intermittente",
    230: "Pluie et neige mêlées",
    231: "Pluie et neige mêlées",
    232: "Pluie et neige mêlées",
    235: "Averses de grêle"
}
load_dotenv()

API_KEY = os.getenv("API_KEY_METEO")              
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")            
INSEE_CODE = "75056"    

if not API_KEY or not TELEGRAM_TOKEN or not CHAT_ID:
    raise RuntimeError("Variables manquantes: API_KEY_METEO / TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID")

bot = Bot(TELEGRAM_TOKEN)

def job():
    try:
        url = f"https://api.meteo-concept.com/api/forecast/daily?token={API_KEY}&insee={INSEE_CODE}&start=0&end=0"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        meteo = data["forecast"][0]

        weather = WEATHER_CODES.get(meteo["weather"], f"Code météo {meteo['weather']}")
        rain = meteo["probarain"]
        tmin = meteo["tmin"]
        tmax = meteo["tmax"]

        paris = timezone("Europe/Paris")
        date_fr = datetime.now(paris).strftime("%d/%m/%Y")

        message = (
            f"Date : {date_fr}\n"
            f"Température : {tmin}° ➜ {tmax}°\n"
            f"Temps : {weather}\n"
            f"Probabilité de pluie : {rain}%"
        )

        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        # En cas d'erreur, envoie un message pour prévenir (optionnel)
        try:
            bot.send_message(chat_id=CHAT_ID, text=f"[ERREUR] {e}")
        except Exception:
            pass
        #Log dans la console
        print("Erreur job():", e)

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone=timezone("Europe/Paris"))
    # Tous les jours à 08:00 Europe/Paris
    scheduler.add_job(job, "cron", hour=7, minute=0)
    print("Bot météo démarré. Envoi quotidien à 08:00 Europe/Paris.")
    scheduler.start()


