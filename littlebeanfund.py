# coding=utf-8

"""
dt = Data Type?  kf = '开放式基金'?
ft = Fund Type?
st=asc 升序排序
sd=2015-12-08&ed=2016-12-08
"""

import urllib2
import re
import logging


logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s]: %(message)s')


def get_fundvalue_history(fund_id):
    """
    Get history values of the specified fund
    :param fund_id: for example, '000831'
    :return: (fund_id, value_list)
    """
    url_template = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&per=100000'
    url = url_template.format(fund_id)
    content = urllib2.urlopen(url).read()

    # get total records
    records_regex = re.compile('records:(\d)+')
    mo = records_regex.search(content)
    total_records = mo.group().split(':')[1]
    logging.log(logging.DEBUG, fund_id + ' has records: ' + total_records)

    raw_data = convert_f10content_to_rawdata(content)
    # parse rows
    rows_str = raw_data.split('</tr>')
    rows_str.remove('')

    result = []
    for row in rows_str:
        row_elements = row.split('</td>')
        row_elements.remove('')
        row_result = []
        for i in range(len(row_elements)):
            e = row_elements[i].split('>')[-1]
            row_result.append(e)
        result.append(tuple(row_result))
    return fund_id, result


def get_fundvalue_latest(fund_id):
    """
    Get latest value of the specified fund
    :param fund_id: for example, '000831'
    :return: (fund_id, value)
    """
    url_template = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&per=1'
    url = url_template.format(fund_id)
    content = urllib2.urlopen(url).read()

    raw_data = convert_f10content_to_rawdata(content)
    elements = raw_data.split('</td>')
    del elements[-1]
    # logging.log(logging.DEBUG, elements)
    result = [e.split('>')[-1] for e in elements]
    logging.log(logging.DEBUG, result)
    return fund_id, result


def get_fundvalue_bydate(fund_id, date):
    """
    Get value of the specified fund at the specified date
    :param fund_id: for example, '000831'
    :param date: the specified date
    :return: (fund_id, value)
    """
    url_template = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&sdate={1}&edate={1}'
    url = url_template.format(fund_id, date)
    content = urllib2.urlopen(url).read()

    raw_data = convert_f10content_to_rawdata(content)
    elements = raw_data.split('</td>')
    if len(elements) < 3:
        return fund_id, None
    else:
        return fund_id, [e.split('>')[-1] for e in elements]


def get_funds():
    """
    Get a list of all funds
    :return: list of alll funds
    """
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&st=asc&pi=1&pn=5000'
    content = urllib2.urlopen(url).read()

    # get number of funds
    allrecords_regex = re.compile('allRecords:(\d)+')
    mo = allrecords_regex.search(content)
    number_of_record = mo.group().split(':')[1]
    logging.log(logging.DEBUG, 'Number of all funds is ' + number_of_record)

    raw_data = convert_rankcontent_to_rawdata(content)
    return construct_rankrawdata_to_list(raw_data)


def get_top10funds_bytype(fund_type):
    """
    Get current top10 funds of the specified type of this year
    :param fund_type:
    :return:
    """
    url_template = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={0}&sc=jnzf&st=desc&pi=1&pn=10&dx=1'
    url = url_template.format(fund_type)
    content = urllib2.urlopen(url).read()

    raw_data = convert_rankcontent_to_rawdata(content)
    top10_list = construct_rankrawdata_to_top10list(raw_data)
    return fund_type, top10_list


def get_top10funds():
    """
    Get current top10 funds of this year
    :return:
    """
    return get_top10funds_bytype('all')


def get_top10funds_ofyear(year):
    """
    Get top10 funds of the specified year
    :param year:
    :return:
    """
    url_template = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&sc=qjzf&st=desc&sd={0}-12-31&ed={1}-12-31&pi=1&pn=10&dx=1'
    url = url_template.format(int(year)-1, year)
    content = urllib2.urlopen(url).read()

    raw_data = convert_rankcontent_to_rawdata(content)
    top10_list = construct_rankrawdata_to_top10yearlist(raw_data)
    return year, top10_list


# The following are helper functions
def convert_f10content_to_rawdata(content):
    begin = content.find('<tbody>') + len('<tbody>')
    end = content.find('</tbody>')
    return unicode(content[begin:end], encoding='utf-8')


def convert_rankcontent_to_rawdata(content):
    begin = content.find('[') + len('[')
    end = content.find(']')
    return unicode(content[begin:end], encoding='utf-8')


def construct_rankrawdata_to_list(raw_data):
    temp = raw_data.replace('","', '"?"').split('?')
    return [(x[0], x[1]) for x in [e[1:-1].split(',') for e in temp]]


def construct_rankrawdata_to_top10list(raw_data):
    temp = raw_data.replace('","', '"?"').split('?')
    return [(x[0], x[14], x[3], x[1]) for x in [e[1:-1].split(',') for e in temp]]


def construct_rankrawdata_to_top10yearlist(raw_data):
    temp = raw_data.replace('","', '"?"').split('?')
    return [(x[0], x[18], x[1]) for x in [e[1:-1].split(',') for e in temp]]


if __name__ == '__main__':
    # print get_fundvalue_latest('000831')
    # print get_fundvalue_latest('001076')
    #
    # print get_fundvalue_bydate('000831', '2016-12-28')
    # print get_fundvalue_bydate('000831', '2016-12-30')

    # print get_fundvalue_history('000815')

    # print get_funds()
    # my = '"a,b,c","aa,bb,cc","aaa,bbb,ccc"'
    # my = my.replace('","', '"?"')
    # print my.split('?')

    # hh_top10 = get_top10funds_bytype('hh')
    # print 'type = ' + hh_top10[0]
    # for x in hh_top10[1]:
    #     print x[0], x[1], x[2], x[3]
    #
    #
    # gp_top10 = get_top10funds_bytype('gp')
    # print 'type = ' + gp_top10[0]
    # for x in gp_top10[1]:
    #     print x[0], x[1], x[2], x[3]
    #
    # all_top10 = get_top10funds_bytype('all')
    # print 'type = ' + all_top10[0]
    # for x in all_top10[1]:
    #     print x[0], x[1], x[2], x[3]

    top10 = get_top10funds_ofyear('2015')
    print 'year = ' + top10[0]
    for x in top10[1]:
        print x[0], x[1], x[2]

    pass
