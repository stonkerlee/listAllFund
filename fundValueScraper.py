#coding=utf-8

'''
Download all fund's values and save them to files
'''

import urllib2
import re
import logging
import csv
import listAllFund

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_fund(fund_id):
    URL = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&per=100000'.format(fund_id)
    res = urllib2.urlopen(URL).read()

    # get total records
    recordsRegex = re.compile('records:(\d)+')
    mo = recordsRegex.search(res)
    total_records = mo.group().split(':')[1]
    logging.log(logging.DEBUG, fund_id + ' has records: ' + total_records)

    # get values
    tbody_begin_pos = res.find('<tbody>')
    tbody_end_pos = res.find('</tbody>')
    values = res[tbody_begin_pos + len('<tbody>') : tbody_end_pos]

    # parse rows
    rows_str = values.split('</tr>')
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

    return (fund_id, result)

def save_to_csv(data):
    fund_id, values = data
    header = ['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态', '分红配送']
    save_file = open('{0}.csv'.format(fund_id), 'w')
    writer = csv.writer(save_file)
    writer.writerow(header)
    writer.writerows(values)
    save_file.close()

if __name__ == '__main__':
    # data = scrape_fund('000831')
    # save_to_csv(data)
    for fund in listAllFund.listAllFund():
        fund_id = fund[0]
        save_to_csv(scrape_fund(fund_id))
