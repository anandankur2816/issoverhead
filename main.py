from datetime import datetime
import requests
import smtplib as smt
from email_desc import *
import time

my_lat = 23.344101
my_long = 85.309563


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    # print(data)
    iss_location = (data["iss_position"]["longitude"], data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])
    iss_lat = float(data["iss_position"]["latitude"])
    # print(iss_location)
    response.close()
    print(f"Look in the sky{abs(iss_lat - my_lat)} and {abs(iss_lng - my_long)}")
    if abs(iss_lat - my_lat) <= 5 and abs(iss_lng - my_long) <= 5:
        return True


parameter = {
    "lat": my_lat,
    "lng": my_long,
    "formatted": 0
}


def is_night():
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    # print(sunrise)
    # print(sunset)
    curr_time = datetime.now().hour
    # print(curr_time.hour)
    if sunset <= curr_time <= sunrise:
        return True


def send_mail():
    with smt.SMTP("smtp.gmail.com", port=587) as conn:
        conn.starttls()
        conn.login(user=my_email, password=my_pass)
        conn.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="subject:ISS is overhead\n\n Look up in the sky it's time"
        )
        print("Mail sent")


mail_sent = False
while not mail_sent:
    if is_iss_overhead() and is_night():
        send_mail()
        mail_sent = True
        break
    time.sleep(5)
