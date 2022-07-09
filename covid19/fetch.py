import os
import re
from urllib import request
from urllib.error import HTTPError

MPAT = r"(?:edn)?(\d+)-?(?:\d+)?.xlsx"


def pull(src, dst):
    url = f"https://rosstat.gov.ru/storage/mediabank/{src}"
    output = f"data/rosstat/{dst}"
    dirname = os.path.dirname(output)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    request.urlretrieve(url, output)


def main():
    year = sorted(os.listdir("data/rosstat/deaths"))[-1]
    month = sorted(
        int(re.match(MPAT, x)[1]) for x in os.listdir(f"data/rosstat/deaths/{year}")
    )[-1]
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    pull(f"edn_{month:02}-{year}_t1_1.xlsx", f"deaths/{year}/edn{month:02}-{year}.xlsx")
    pull(f"edn_{month:02}-{year}_t5_1.xlsx", f"covid/{year}/{month}.xlsx")


while True:
    try:
        main()
    except HTTPError:
        break
