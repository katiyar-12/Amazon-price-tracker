import smtplib
import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv


load_dotenv()


product_url = input("Please paste your product url below : \n")


headers = {
    "User-Agent" : os.getenv("user_agent") ,
    "Accept-Language" : "en-US,en;q=0.9" ,
}
response = requests.get(url=product_url,headers=headers)

response.raise_for_status()
content = response.text

soup = BeautifulSoup(content,"html.parser")

# working with price
price = soup.select_one(".a-price-whole").getText().replace(",","").replace(".","")

if not price:
    print("❌ Price not found. Amazon might have blocked the scraper or changed the HTML.")
    exit()
formatted_price = int(price)

# working with product name
product_name = soup.title.get_text()



my_email = os.getenv("senders_email")
my_email_password = os.getenv("senders_email_password")



# setting target
target = int(input("Please enter your target price : "))

if formatted_price < target :
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(my_email,my_email_password)
    message = f"Subject:You Can Order now!!\n\nNow you can by \n{product_name}\nPrice : {price}\nlink : {product_url} "
    s.sendmail(
        from_addr=my_email,
        to_addrs="varunsinghkatiyar@gmail.com" ,
        msg=message ,
    )
    s.quit()


# to use this script
# create a .env file
# write :

# senders_email
# senders_email_password
# user_agent