import requests
import json
import csv
from collections import defaultdict

with open('credentials/keys.json') as credentialsfp:
    api_key = json.load(credentialsfp)['abuseipdb']


def check_ip(ips: list[str], output):
    res = []
    for ip in ips:
        scr, cat = check_ip_util(ip)
        res.append((ip, scr, cat))

    res.sort(key=lambda element: -1*element[1])

    with open(output, 'w') as outputfp:
        writer = csv.DictWriter(outputfp, ["ip", "score", "categories"])
        writer.writeheader()
        for ip,scr,cat in res:
            writer.writerow({'ip': ip, 'score': scr, 'categories': cat})




def check_ip_util(ipAddress: str, maxAgeInDays=7):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ipAddress,
        'maxAgeInDays': maxAgeInDays,
        'verbose': True
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key,
    }

    try:
        response = requests.request(method='GET', url=url, headers=headers, params=querystring, timeout=15)

        # Formatted output
        decodedResponse = json.loads(response.text)
        # print(json.dumps(decodedResponse, sort_keys=True, indent=4))
        return decodedResponse['data']['abuseConfidenceScore'], agg_categories(decodedResponse['data']['reports'])
    except:
        return -1,[]


def agg_categories(reports: list[dict], num_th=10, percent_th=0.15):
    categories_dict = defaultdict(int)
    n = len(reports)

    for report in reports:
        categories = report['categories']
        for category in categories:
            categories_dict[category] += 1

    res = [key for key, val in categories_dict.items() if val >= num_th or (val / n) >= percent_th]
    resolve_categories(res)
    return res


def resolve_categories(categories:list):
    attacks_dict = {
        1: 'DNS Compromise',
        2: 'DNS Poisoning',
        3: 'Fraud Orders',
        4: 'DDoS Attack',
        5: 'FTP Brute-Force',
        6: 'Ping of Death',
        7: 'Phishing',
        8: 'Fraud VoIP',
        9: 'Open Proxy',
        10: 'Web Spam',
        11: 'Email Spam',
        12: 'Blog Spam',
        13: 'VPN IP',
        14: 'Port Scan',
        15: 'Hacking',
        16: 'SQL Injection',
        17: 'Spoofing',
        18: 'Brute-Force',
        19: 'Bad Web Bot',
        20: 'Exploited Host',
        21: 'Web App Attack',
        22: 'SSH',
        23: 'IoT Targeted'
    }

    for i in range(len(categories)):
        categories[i] = attacks_dict[categories[i]]

    # return categories

