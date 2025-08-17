# Telegram-MeteoBot
Bot Python qui envoie chaque matin la météo du jour (API Météo-Concept) sur un chat Telegram.

⚙️ Installation
git clone https://github.com/<user>/Telegram-MeteoBot.git
cd Telegram-MeteoBot
pip install -r requirements.txt

🔑 Configuration

Créer un fichier .env à la racine avec vos infos :

API_KEY_METEO=xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
INSEE_CODE=75056


👉 .env est ignoré par Git et reste en local.

▶️ Utilisation
python main.py


Par défaut : envoi quotidien à 07h00 Europe/Paris.

🚀 Déploiement

Compatible avec PythonAnywhere, Render, Railway, VPS, Raspberry Pi.

💡 Contributions

C’est mon premier projet fonctionnel en Python, donc je suis ouvert aux conseils, suggestions et retours.
N’hésitez pas à ouvrir une issue ou proposer une pull request !
