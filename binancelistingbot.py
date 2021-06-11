from binance.client import Client
from binance.enums import *
from decimal import *
import keyboard
from datetime import datetime, time
from time import sleep
import time

api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

listingsymbol = 'TLMUSDT'
print(f"BOT IS SETUP FOR {listingsymbol} LISTING IN BINANCE AT 2021-04-13 6:00:00 UTC")

balance = float(client.get_asset_balance(asset='USDT')["free"])
usdtprice = float(client.get_ticker(symbol='BUSDUSDT')['lastPrice'])
balancevisual = balance / usdtprice
print(f" {balance} USDT are available, ca correspond a {balancevisual}$ (USD)")

quantityvisual = float(input('How much you wanna put in the LISTING in $ (USD)'))
quantity = quantityvisual * usdtprice
print(f"{quantity} USDT or {quantityvisual} $ (usd) will be in the LISTING")

def dateDiffInSeconds(date1, date2):
  timedelta = date2 - date1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def daysHoursMinutesSecondsFromSeconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)

listingdatetime = datetime.strptime('2021-04-13 1:59:58', '%Y-%m-%d %H:%M:%S')
now = datetime.now()

while listingdatetime>now:
    print("%dd %dh %dm %ds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, listingdatetime)))
    sleep(1)
    now = datetime.now()

#DES QU'ON ARRIVE A LA DATE DU LISTING (LISTINGDATETIME) ON ÉXÉCUTE CETTE BOUCLE
#CETTE BOUCLE ÉXECUTE DES BUY, TANT QU'IL Y A DES ERREURS CA RECOMMENCE, DES QU'ON LE BUY EST UN SUCCÈS, CA S'ARRETE ET PASSE A LA SUITE

done = False
while not done:
    try:
        monnaieprice = float(client.get_ticker(symbol=listingsymbol)['lastPrice'])
        quantitybuy = int(quantity / monnaieprice)

        order = client.order_market_buy(
            symbol=listingsymbol,
            quantity=quantitybuy) 
        done = True
    except Exception:
        print("erreur")
        time.sleep(0.1)

firstlimitquantity = 50
secondlimitquantity = 20
thirdlimitquantity = 20

firstsellquantity = int(quantitybuy/100 * firstlimitquantity)
secondsellquantity = int(quantitybuy/100 * secondlimitquantity)
thirdsellquantity = int(quantitybuy/100 * thirdlimitquantity)

order = client.order_limit_sell(
    symbol=listingsymbol,
    quantity=firstsellquantity,
    price='12.0000')

order2 = client.order_limit_sell(
    symbol=listingsymbol,
    quantity=secondsellquantity,
    price='15.0000')

order3 = client.order_limit_sell(
    symbol=listingsymbol,
    quantity=secondsellquantity,
    price='20.0000')

print('SUCCESFULLY BOUGHT AND PUT 3 SELL LIMITS')

panicsell = str(input('Would you like to panic sell (answer Yes or No)')) 
if panicsell.lower() == 'yes':
    client.cancel_orders(symbol=listingsymbol)
    order = client.order_market_sell(
            symbol=listingsymbol,
            quantity=quantitybuy)
    print('Cancelled all orders and sold')
else:
    print('DIDNT Cancelled all orders and sold')
