# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + a quote (zenquotes.io)
# Runs: every day at 8 AM IST via GitHub Actions
# APIs: both free, no API keys needed

import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import date

# -- FUNCTION 1: Weather ---------------------------------------
def get_weather(city="Trivandrum"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip() # remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather unavailable ({e})"

def send_alert_email(weather_text):
    """Send email alert for extreme weather"""
    sender = "diyarajesh05diya@gmail.com" # CHANGE THIS to your Gmail
    receiver = "diyarajesh05diya@gmail.com" # CHANGE THIS to your Gmail
    password = os.getenv("GMAIL_APP_PASSWORD")

    body = f"Weather Alert for Talipparamba\n\n{weather_text}\n\nSent by Pulse Bot"
    msg = MIMEText(body)
    msg['Subject'] = f"Weather Alert: {weather_text}"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("Alert email sent successfully")
    except Exception as e:
        print(f"Email failed: {e}")

# -- FUNCTION 2: Quote ---------------------------------------
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

# -- MAIN FUNCTION ---------------------------------------
def main():
    today = date.today().strftime("%B %d, %Y")
    weather = get_weather()
    quote = get_quote()

    # Task 1: Send email alert if temp > 35°C or Rain
    if "°C" in weather:
        temp_str = weather.split("°C")[0].split()[-1].replace("+","")
        try:
            temp = int(temp_str)
            if temp > 35 or "Rain" in weather:
                send_alert_email(weather)
        except:
            pass

    # Create the daily briefing
    briefing = f"""
Pulse Daily Briefing - {today}

Weather: {weather}

Quote of the Day:
{quote}

Have a great day!
"""

    # Save to file for GitHub Actions artifact
    with open("briefing.txt", "w", encoding="utf-8") as f:
        f.write(briefing.strip())

    print(briefing.strip())

if __name__ == "__main__":
    main()
