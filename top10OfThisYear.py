# coding=utf-8

import urllib2

msg = ''

def top10OfThisYear(type):
    global msg
    URL = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={0}&sc=jnzf&st=desc&pi=1&pn=10&dx=1'.format(type)
    content = urllib2.urlopen(URL).read()
    start = content.find('[')
    end = content.find(']')
    data = content[start+2 : end-1]
    L = data.split('","')
    for e in L:
        r = e.split(',')
        msg += '{0} {1:>7}% {2} {3}\n'.format(r[0], r[14], r[3], r[1])


if __name__ == '__main__':
    msg += '-'*10 + 'top10 混合型' + '-'*10 + '\n'
    top10OfThisYear('hh')
    msg += '-' * 10 + 'top10 股票型' + '-' * 10 + '\n'
    top10OfThisYear('gp')
    print(msg)
