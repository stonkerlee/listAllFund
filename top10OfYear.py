import urllib2

def top10OfYear(year):
    URL = 'http://fund.eastmoney.com/data/rankhandler.aspx?' \
          'op=ph&dt=kf&ft=all&sc=qjzf&st=desc' \
          '&sd={0}-12-31&ed={1}-12-31&pi=1&pn=10&dx=1'.format(int(year)-1, year)
    content = urllib2.urlopen(URL).read()
    start = content.find('[')
    end = content.find(']')
    data = content[start + 2: end - 1]
    L = data.split('","')
    for e in L:
        # print e
        r = e.split(',')
        print('{0} {1}% {2}'.format(r[0], r[18], r[1]))


print('-'*10 + 'top10 of 2015' + '-'*10)
top10OfYear('2015')
print('-'*10 + 'top10 of 2014' + '-'*10)
top10OfYear('2014')
print('-'*10 + 'top10 of 2013' + '-'*10)
top10OfYear('2013')
print('-'*10 + 'top10 of 2012' + '-'*10)
top10OfYear('2012')
