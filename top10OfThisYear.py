import urllib2

def top10OfThisYear():
    URL = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&sc=jnzf&st=desc&pi=1&pn=10&dx=1'
    content = urllib2.urlopen(URL).read()
    start = content.find('[')
    end = content.find(']')
    data = content[start+2 : end-1]
    L = data.split('","')
    for e in L:
        r = e.split(',')
        print('{0} {1}% {2}'.format(r[0], r[14], r[1]))


top10OfThisYear()
