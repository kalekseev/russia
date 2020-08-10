import pathlib
import re

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
        try:
            data = pd.read_excel(
                DATA_DIR / f"rosstat/deaths/{year}/edn{month:02}-{year}.{ext}",
                sheet_name="t1_1",
                usecols="A,F",
                skiprows=6,
                index_col=0,
                header=None,
                squeeze=True,
            )
        except IOError:
            pass

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


def read_year_deaths(year: int) -> dict:
    return {month: read_month_deaths(year, month) for month in range(1, 13)}


def read_deaths() -> dict:
    return {
        year: data for year in range(2016, 2021) if (data := read_year_deaths(year))
    }


if __name__ == "__main__":
    data = read_deaths()
    deaths = pd.DataFrame.from_dict(
        {
            f"{year}-{month:02}-01": value
            for year in data.keys()
            for month, value in data[year].items()
        }
    )
    csv_data = sorted(
        [region, year, month, value]
        for year, vyear in data.items()
        for month, mvalue in vyear.items()
        for region, value in (mvalue or {}).items()
    )
    deaths2 = pd.DataFrame.from_records(
        csv_data, columns=["region", "year", "month", "deaths"]
    )
    deaths.to_csv(DATA_DIR / "deaths.csv")
    deaths2.to_csv(DATA_DIR / "deaths2.csv", index=False)
