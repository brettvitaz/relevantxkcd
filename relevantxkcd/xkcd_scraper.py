import json
import requests
import time

URL = 'http://xkcd.com/{:d}/info.0.json'


def get_all_the_things():

    idx = 0
    while idx < 1:
        idx += 1
        if idx in [404]:
            idx += 1
        f = requests.get(URL.format(idx))
        if f.status_code == 404:
            print('finished')
            break
        while f.status_code == 503:
            time.sleep(1.0)
            f = requests.get(URL.format(idx), timeout=1.0)
        print(f.json())


if __name__ == '__main__':
    get_all_the_things()
