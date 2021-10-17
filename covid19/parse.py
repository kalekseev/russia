import pathlib
import re
from functools import partial

import pandas as pd

DATA_DIR = pathlib.Path(__file__).parent.absolute() / "data"


def cleanup_region(r: str) -> str:
    r = r.strip()
    if r.startswith("H"):
        # Нижегородская область и Ненецкий авт. округ
        # используют английскую заглавную h вместо русской н
        r = r.replace("H", "Н")
    elif "Севастополь" in r:
        return "г.Севастополь"
    elif r == "А":
        return ""
    elif "федер" in r.lower():
        return ""
    r = re.sub(r"\s*-\s*", "-", r)
    r = re.sub(r"\d+.*$", "", r)
    r = re.sub(r"\(.*\)", "", r)
    r = re.sub(r"без авт. округ(а|ов)", "без автономии", r)
    return r.strip()


def read_month_deaths(year: int, month: int) -> dict:
    data = None
    for ext in ["xlsx", "xls"]:
        kwargs = {
            "io": DATA_DIR / f"rosstat/deaths/{year}/edn{month:02}-{year}.{ext}",
            "sheet_name": "t1_1",
            "usecols": "A,F",
            "skiprows": 6,
            "index_col": 0,
            "header": None,
            "squeeze": True,
        }
        try:
            data = pd.read_excel(**kwargs)
        except IOError:
            pass
        except ValueError:
            kwargs["sheet_name"] = "Лист1"
            data = pd.read_excel(**kwargs)

    if data is None:
        return None
    while data.isnull().any():
        data = data[:-1]
    data = {
        region: int(v)
        for k, v in data.to_dict().items()
        if (region := cleanup_region(k)) and not region.endswith("без автономии")
    }
    assert len(data) == 85
    return data


def _cols_predicate(year, month):
    return year == 2021 and 4 < month and month != 7


def with_covid_read_month_deaths(year: int, month: int) -> dict:
    try:
        data = pd.read_excel(
            DATA_DIR / f"rosstat/covid/{year}/{month}.xlsx",
            usecols="A,B,K" if _cols_predicate(year, month) else "A,B,E",
            skiprows=9,
            index_col=0,
            header=None,
            squeeze=True,
        )
    except IOError:
        return None
    while data[1].isnull().any():
        data = data[:-1]
    data = data.to_dict()
    from_covid = data[1]
    with_covid = data[10 if _cols_predicate(year, month) else 4]
    data = {
        region: (
            0 if pd.isna(v) else int(v),
            0 if pd.isna(wv := with_covid[k]) else int(wv),
        )
        for k, v in from_covid.items()
        if (region := cleanup_region(k)) and not region.endswith("без автономии")
    }
    return data


def get_parse_stopcoronavirus():
    REPLACE = {
        "Москва": "г.Москва",
        "Санкт-Петербург": "г.Санкт-Петербург",
        "Севастополь": "г.Севастополь",
    }
    data = pd.read_csv(
        "data/stopcoronavirus.csv",
        names=["date", "region", "deaths"],
        index_col="date",
    )
    data = data.pivot_table(
        values="deaths", index=data.index, columns="region", aggfunc="sum"
    )
    data.columns = [REPLACE.get(c, c) for c in data.columns]
    data.index = [d.rsplit("-", 1)[0] for d in data.index]
    data.index.name = "month"
    data = data.fillna(0).astype("int64")
    data = data.groupby("month").agg(sum)
    data = data.T.to_dict()

    def f(year, month):
        return data.get(f"{year}-{month:02}")

    return f


def read_year_deaths(parse_fn) -> dict:
    return {month: parse_fn(month) for month in range(1, 13)}


def read_deaths(parse_fn) -> dict:
    return {
        year: data
        for year in range(2016, 2022)
        if (data := read_year_deaths(partial(parse_fn, year)))
    }


if __name__ == "__main__":
    sc = read_deaths(get_parse_stopcoronavirus())
    with_covid = read_deaths(with_covid_read_month_deaths)
    data = read_deaths(read_month_deaths)
    csv_data = sorted(
        [
            region,
            year,
            month,
            value,
            *(with_covid[year][month] or {}).get(region, (0, 0)),
            (sc[year][month] or {}).get(region, 0),
        ]
        for year, vyear in data.items()
        for month, mvalue in vyear.items()
        for region, value in (mvalue or {}).items()
    )
    deaths2 = pd.DataFrame.from_records(
        csv_data,
        columns=[
            "region",
            "year",
            "month",
            "deaths",
            "from_covid",
            "with_covid",
            "stopcoronavirus",
        ],
    )
    deaths2.to_csv(DATA_DIR / "deaths2.csv", index=False)
