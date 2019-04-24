import scrapy
import datetime

class QuotesSpider(scrapy.Spider):
    name = "nasdaq3"
    letter = 'A'
    start_urls = []
    while ord(letter) <= ord('Z'):
    start_urls.append('http://www.advfn.com/nasdaq/nasdaq.asp?companies=' + letter)
        letter = chr(ord(letter) + 1)
        
    def parse(self, response):
        ftxt = response.css('tr.ts0 a::text').getall()
        stxt = response.css('tr.ts1 a::text').getall()
        fu = response.css('tr.ts0 a::attr(href)').getall()
        su = response.css('tr.ts1 a::attr(href)').getall()
        furl = fu[::6]
        surl = su[::6]
        txt = []
        url = []

        i = 0
        while i < len(ftxt):
            txt.append(ftxt[i])
            if i + 1 < len(ftxt):
                    txt.append(ftxt[i+1])
            if i < len(stxt):
                    txt.append(stxt[i])
            if i + 1 < len(stxt):
                    txt.append(stxt[i+1])
            i = i + 2
    
        i = 0
        while i < len(furl):
            url.append(furl[i])
            if i < len(surl):
                    url.append(surl[i])
            i = i + 1
            
        i = 0
        while (i + 1 < len(txt)) and (i//2 < len(url)):
            if url[i//2] is not None:
                link = response.urljoin(url[i//2])
            request = response.follow(link, self.findprice)
            request.meta['Equity'] = txt[i]
            request.meta['Symbol'] = txt[i + 1]
            yield request
            i = i + 2

    def findprice(self, response):
        equity = response.meta['Equity']
        symbol = response.meta['Symbol']
        sp = ""
        if not response.css('span#quoteElementPiece6.PriceTextUp::text'):
            if not response.css('span#quoteElementPiece6.PriceTextDown::text'):
                sp = response.css('span#quoteElementPiece6.PriceTextUnchanged::text').get()
            else:
                sp = response.css('span#quoteElementPiece6.PriceTextDown::text').get()
        else:          
            sp = response.css('span#quoteElementPiece6.PriceTextUp::text').get()
                
        if sp is not None: 
            yield {
                'Equity': equity,
                'Symbol': symbol,
                'Time': datetime.datetime.now().strftime("%I:%M %p on %B %d"),
                'Stock Price': float(sp),
            }
        else:
            yield {
                'Equity': equity,
                'Symbol': symbol,
                'Time': datetime.datetime.now().strftime("%I:%M %p on %B %d"),
                'Stock Price': None,
            }
