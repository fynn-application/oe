from __future__ import annotations
import pandas as pd
import os

dirname = os.path.dirname(__file__)
stats_file = os.path.join(dirname, "data/stats.csv")


class AdStats:
    columns: list[str] = [
        "ad_id",
        "ad_duration",
        "ip_addr",
        "time",
        "country",
        "region",
        "region_code",
        "city",
        "zip",
    ]

    @staticmethod
    def read():
        return pd.read_csv(stats_file, index_col=False)

    @staticmethod
    def add_row(data):
        df = pd.DataFrame(data, columns=AdStats.columns, index=[0])
        df.to_csv(stats_file, mode="a", header=False, index=False)
