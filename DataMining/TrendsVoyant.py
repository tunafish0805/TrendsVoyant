from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import re
import json
import time
import threading
import datetime

ckey = ''
csecret = ''
atoken = ''
asecret = ''

class listener(StreamListener):

    def __init__(self):
        self.half_hr = ''
        self.save_half_hr()

    def on_data(self, data):

        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        A = decoded['created_at'].encode('ascii', 'ignore')
        B = decoded['user']['screen_name']
        C = decoded['user']['id']
        D = decoded['in_reply_to_user_id_str']
        E = decoded['text'].encode('ascii', 'ignore')

        self.half_hr += str(A)+' '+str(B)+' '+str(C)+' '+str(D)+' '+str(E)+' '

        return True

    def save_half_hr(self):
        
        self.update_chart(self.half_hr)

        self.half_hr = ''

        threading.Timer(1800, self.save_half_hr).start()

    def on_error(self, status):

        print status

    def update_chart(self, dta):

        pos, neg, tim = self.get_current_chart()
        positiveList = self.file_To_List('/var/www/FlaskApp/FlaskApp/templates/positive.txt', '\n')
        negativeList = self.file_To_List('/var/www/FlaskApp/FlaskApp/templates/negative.txt', '\n')

        data_list = dta.split()
        numPos = len([item for item in data_list if item in positiveList])
        numNeg = len([item for item in data_list if item in negativeList])
        cur_time = self.parse_date(str(datetime.datetime.now()))

        pos.pop(0)
        neg.pop(0)
        tim.pop(0)

        pos.append(numPos)
        neg.append(numNeg)
        tim.append(cur_time)

        pos_str = ' '.join([str(i) for i in pos])
        neg_str = ' '.join([str(i) for i in neg])
        tim_str = ' '.join([str(i) for i in tim])

        write_file = open('/var/www/FlaskApp/FlaskApp/templates/_data_.txt', 'w')
        
        write_file.write(pos_str+'\n'+neg_str+'\n'+tim_str)


    def get_current_chart(self):

        read_file = read_file = open('/var/www/FlaskApp/FlaskApp/templates/_data_.txt', 'r')

        lists = [string.split() for string in read_file.read().split('\n')]

        read_file.close()

        return lists[0], lists[1], lists[2]

    def file_To_List(self, fileName, splitBy = None):
        if splitBy is None:
            data = open(fileName, 'r')
            dataList = data.read().split()
            data.close()
            return dataList
        else:
            data = open(fileName, 'r')
            dataList = data.read().split(splitBy)
            clean_data = [word.strip() for word in dataList]
            data.close()
            return clean_data

    def parse_date(self, date_string):
        T = date_string.split()[1].split('.')[0].split(':')

        if int(T[0]) > 12:
            sufix = 'PM'
        else:
            sufix = 'AM'

        U = int(T[0]) % 12

	if U == 0: U = 12

        return str(U)+':'+T[1]+sufix

while True: 

    try:

        auth = OAuthHandler(ckey, csecret)

        auth.set_access_token(atoken, asecret)

        twitterStream = Stream(auth, listener())

        twitterStream.filter(track=["bitcoin","btc"])

    except ValueError as e:

        continue
