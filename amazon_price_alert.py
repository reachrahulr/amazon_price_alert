#Install all the packages using pip(windows terminal)
from bs4 import BeautifulSoup
import requests, time, smtplib
from notify_run import Notify
from datetime import datetime

#Product url link
url = 'https://www.amazon.in/boAt-BassHeads-100-Headphones-Black/dp/B071Z8M4KX' #[Product link]
#Desired Price, the price you want ot buy the product
desired_price = 370

pnmsg = "Below Rs. " + str(desired_price) + " you can get your Boat Headphone."

def check_price():
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')

    # with open('amazon_price_alert.txt', 'wb') as new_file:
    #     new_file.write(soup.prettify().encode("utf-8"))

    heading = soup.find('span', id='productTitle').text.strip()

    price = soup.find('span', id='priceblock_ourprice').text
    price = float(price[2:])
    price = int(price)


    #VARIABLES FOR SENDING MAIL AND PUSH NOTIFICATION---------------------------------------

    print("NAME : " + heading)
    print("CURRENT PRICE : " + str(price))
    print("DESIRED PRICE : " + str(desired_price))


    # Lets send the mail-----------------------------------------------------------------
    #Go to https://myaccount.google.com/security and change Allow less secure apps to turn OFF

    def send_mail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('senderemailaddress', 'emailpassword')
        subject = "Price of Boat Headphone has fallen down below Rs. " + str(desired_price)
        body = "Hey Rahul! \n The price of Boat Headphone on AMAZON has fallen down below Rs." + str(
            desired_price) + ".\n So, hurry up & check the amazon link right now : " + url
        msg = f"Subject: {subject} \n\n {body} "
        server.sendmail(
            'senderemailaddress',
            'recieveremailaddress', msg
        )
        print("HEY Rahul, EMAIL HAS BEEN SENT SUCCESSFULLY.")
        server.quit()

    #Now lets send the push notification-------------------------------------------------
    #Check how push notifications work: https://qr.ae/TWoIb4

    def push_notification():
        notify = Notify()
        notify.send(pnmsg)
        print("HEY Rahul, PUSH NOTIFICATION HAS BEEN SENT SUCCESSFULLY.")

        print("Check again after an hour.")


    count = 0
    if desired_price >= price:
        send_mail()
        push_notification()

    else:
        count+= 1
        print("Rechecking... Last checked at " + str(datetime.now()))
        print(count)


count = 0
while(True):
  count += 1
  print("Count : "+str(count))
  check_price()
  # next alert in 3600 secs
  time.sleep(3600)

