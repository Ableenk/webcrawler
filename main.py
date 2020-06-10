import threading
from func import get_words
from collections import Counter
from string import ascii_letters
from urllib import request

def countofmax():
    l = 500000
    r = 2000000
    while r > l:
        m = (l + r) // 2
        try:
            k = request.urlopen('https://habr.com/ru/post/' + str(m) + '/').getcode()
            l = m + 1
        except Exception:
            r = m
    return m

def topten(mas):
    for i in range(20):
        print(str(i+1)+')', mas[i][0])

def format(mas):
    pretexesnmonthes = list('без, перед, при, через, над, под, про, для, что, как, где, зачем, августа, июля, июня, сентября, октября, ноября, декабря, января, февраля, марта, апреля, мая'.split(', '))
    for i in mas:
        if (len(i) <= 2) or validate(i) or i in pretexesnmonthes:
            mas[i] = 0
    return mas.most_common(20)

def validate(nickname):
    return all(map(lambda c: c in ascii_letters, nickname))

def filezation():
    s = ''
    f = open('compressor.txt', encoding='UTF-8')
    for line in f:
        s += line
    f.close()
    open('compressor.txt', 'w')
    f.close()
    return s

maxperiod = countofmax()//3 + 2
period = 10

e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()

t1 = threading.Thread(target=get_words, args=(1, period, e1, e2))
t2 = threading.Thread(target=get_words, args=(period, 2*period, e2, e3))
t3 = threading.Thread(target=get_words, args=(2*period, 3*period, e3, e1))

t1.start()
t2.start()
t3.start()

e1.set()

t1.join()
t2.join()
t3.join()

words = Counter(filezation().split())
topten(format(words))