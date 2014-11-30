import coinmarketcap
import time

def update_lists(price, date):

    prices, date_times = get_lists()

    prices.pop(0)
    date_times.pop(0)
    
    prices.append(price)
    date_times.append(date)
    
    lists_file = open('/var/www/FlaskApp/FlaskApp/templates/price_list.txt', 'w')

    W = ' '.join([str(i) for i in prices]) + '\n' + ' '.join(date_times)

    lists_file.write(W)

    lists_file.close()
    

def get_lists():

    list_file = open('/var/www/FlaskApp/FlaskApp/templates/price_list.txt', 'r')

    lists = list_file.read().split('\n')

    prices = [float(i) for i in lists[0].split()]

    date_times = [i for i in lists[1].split()]

    list_file.close()

    return prices, date_times


while 1:

    price = float(coinmarketcap.price('bitcoin')[2:])

    date_time = ''.join(coinmarketcap.last_updated().split()[5:7])

    update_lists(price, date_time)

    time.sleep(1800)
