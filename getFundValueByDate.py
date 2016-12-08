import urllib2

def getFundValueByDate(fundId, date):
    URL='http://fund.eastmoney.com/f10/F10DataApi.aspx?' \
        'type=lsjz&code={0}&sdate={1}&edate={1}'.format(fundId, date)
    content = urllib2.urlopen(URL).read()
    bodyStart = content.find('<tbody>')
    bodyEnd = content.find('</tbody>')
    body = content[bodyStart+len('<tbody>') : bodyEnd]
    e = body.split('</td>')[1]
    idx = e.find('>')
    value = e[idx+1:]
    print fundId, date, value
    return date, value



getFundValueByDate('000831', '2016-12-08')
getFundValueByDate('000831', '2015-12-31')

# print (1.3110 - 1.6440) * 100 / 1.6440
