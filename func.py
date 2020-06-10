from urllib import request
from bs4 import BeautifulSoup as bs

def htmltotext(html):
    text = html.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def cleaning(s):
    res = ''
    punctuationordigits = ['.', ',', ':', ';', '!', '?', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "«", "»", "&"]
    for i in range(len(s)):
        if not (s[i] in punctuationordigits):
            res += s[i]
    return res.lower()

def scriptout(html):
    for script in html(["script", "style"]):
        script.extract()

def get_html(num):
    url = 'https://habr.com/ru/post/' + str(num) + '/'
    html = request.urlopen(url).read()
    html = bs(html, features="lxml")
    return html

def writing(s):
    with open('compressor.txt', 'a', encoding='UTF-8') as output:
        output.write(s + '\n')

def get_words(start, end, event_for_wait, event_for_set):
    max_page = 506123
    event_for_wait.wait()
    event_for_wait.clear()
    for i in range(start, end):
        try:
            html = get_html(i)
            scriptout(html)
            text = htmltotext(html)
            writing(cleaning(text))
        except Exception:
            pass
    event_for_set.set()