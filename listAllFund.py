# coding=utf-8

import urllib2

# dt = Data Type?  kf = '开放式基金'?
# ft = Fund Type?
# st=asc 升序排序
# sd=2015-12-08&ed=2016-12-08
# URL='http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&st=asc&pi=1&pn=1'

def parse(content, result):
    start = content.find('[')
    end = content.find(']')
    wholeData = content[start+2:end-1]
    L = wholeData.split('","')
    for e in L:
        l = e.split(',')
        print l[0], l[1]
        result.append((l[0], l[1]))


def listAllFund():
    result = []
    URL = 'http://fund.eastmoney.com/data/rankhandler.aspx?' \
          'op=ph&dt=kf&ft=all&st=asc&pi=1&pn=5000'
    content = urllib2.urlopen(URL).read()
    parse(content, result)
    print('Total number: ' + str(len(result)))
    return result


listAllFund()