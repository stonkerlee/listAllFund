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
    result = []
    for e in L:
        r = e.split(',')
        result.append((r[0], r[18], r[1]))
    return (year, result)

def display_by_text(data):
    year = data[0]
    data_list = data[1]
    print('-' * 10 + 'top10 of {0}'.format(year) + '-' * 10)
    for d in data_list:
        print('{0} {1:>8}% {2}'.format(d[0], d[1], d[2]))


if __name__ == '__main__':
    display_by_text(top10OfYear('2015'))
    display_by_text(top10OfYear('2014'))
    display_by_text(top10OfYear('2013'))
    display_by_text(top10OfYear('2012'))
