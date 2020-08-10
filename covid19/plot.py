import matplotlib.pyplot as plt
import pandas as pd

MONTHS = 6


def plot(data):
    pv = pd.pivot_table(
        data, index=data.index.month, columns=data.index.year, aggfunc="sum",
    )[:MONTHS]
    fig, axarr = plt.subplots(29, 3, figsize=(14, 98))
    i = j = 0
    for region in data.columns:
        if j > 2:
            i += 1
            j = 0
        axarr[i][j].set_title(region)
        mean = pv[region][:][[2016, 2017, 2018, 2019]].mean(axis=1)
        mean.name = "2016-2019"
        df = pd.concat([mean, pv[region][2019], pv[region][2020]], axis=1)
        df.plot(ax=axarr[i][j], marker="o")
        j += 1
    plt.tight_layout()
    fig.savefig("output.png")


if __name__ == "__main__":
    aa = pd.read_csv("./data/deaths.csv", index_col=0)
    nn = aa.columns.astype("datetime64[ns, Europe/Moscow]")
    data = aa.set_axis(nn, axis="columns").T
    plot(data)
