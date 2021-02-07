import json
import config


def get_http():
    ip_address = []
    soup = config.requestUrl('https://www.kuaidaili.com/free/inha/1/')
    ips = soup.find(name='table', attrs={'class': 'table table-bordered table-striped'}).find_all('tr')
    for ip in ips:
        try:
            address = ip.find(name='td', attrs={'data-title': 'IP'}).text
            port = ip.find(name='td', attrs={'data-title': 'PORT'}).text
            d = {'http': 'http://' + address + ':' + port}
            ip_address.append(d)
        except AttributeError:
            continue

    with open('http.json', 'w') as file_obj:
        json.dump(ip_address, file_obj)
        file_obj.close()