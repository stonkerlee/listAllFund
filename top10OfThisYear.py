# coding=utf-8

import urllib2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

TYPE_STR_MAPPING = {'hh':'混合型基金',
                    'gp':'股票型基金'}

def top10OfThisYear(type):
    result = []
    URL = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={0}&sc=jnzf&st=desc&pi=1&pn=10&dx=1'.format(type)
    content = urllib2.urlopen(URL).read()
    start = content.find('[')
    end = content.find(']')
    data = content[start+2 : end-1]
    L = data.split('","')
    for e in L:
        r = e.split(',')
        result.append((r[0], r[14], r[3], r[1]))
    return (type, result)

def display_by_text(data):
    type = data[0]
    print('-'*10 + TYPE_STR_MAPPING[type] + '-'*10)
    data_list = data[1]
    msg = ''
    for d in data_list:
        msg += '{0} {1:>7}% {2} {3}\n'.format(d[0], d[1], d[2], d[3])
    print msg

def display_by_matplotlib(data):
    type = data[0]
    data_list = data[1]
    date = data_list[0][2]
    earning_list = [float(d[1]) for d in data_list]
    earning_max = earning_list[0]
    name_list = [unicode(d[3], encoding='utf-8') for d in data_list]

    plt.title(unicode(date) + u' top10 ' + unicode(TYPE_STR_MAPPING[type], encoding='utf-8'))
    plt.ylabel('Percent')
    plt.ylim(ymax=earning_max+5)
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(range(1, 11)))
    gap = 0.5 if earning_max > 50 else 0.2

    for i in range(len(earning_list)):
        plt.text(i+0.77, earning_list[i] + gap,
                 unicode(earning_list[i]) + u'%\n' + name_list[i],
                 fontsize=9)

    plt.bar(range(1, 11), earning_list, align='center', width=0.5)
    plt.show()


if __name__ == '__main__':
    # display_by_text(top10OfThisYear('hh'))
    # display_by_text(top10OfThisYear('gp'))
    display_by_matplotlib(top10OfThisYear('hh'))
    # display_by_matplotlib(top10OfThisYear('gp'))
