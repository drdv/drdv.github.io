"""Visualize my walking data from my iphone's health app."""

import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class HealthData:
    def __init__(
        self,
        clean_data_file: str = "data/export_clean.csv",
        iphone_data_file: str = "data/export.xml",
        load_from_iphone=False,
    ):
        if load_from_iphone:
            self.data_file = iphone_data_file
            self._df_all = self._read_data_iphone()
        else:
            self.data_file = clean_data_file
            self._df_all = self._read_clean_data()

        self.df = self._df_all.copy()

    def show(self, unit="dist km"):
        unit_label = "_".join(unit.split(" "))

        self.filter_df("2024-05-21", "2024-08-13")
        self.plot_value(unit, f"img/entire_challenge_{unit_label}.png", True)

        self.filter_df("2024-07-13", "2024-08-12")
        self.plot_value(unit, f"img/last_month_{unit_label}.png")

        self.filter_df("2024-05-21", "2024-08-13")
        self.plot_rolling_value(unit, 31, f"img/rolling_31days_{unit_label}.png")
        self.plot_rolling_value(unit, 7, f"img/rolling_7days_{unit_label}.png")

        self.filter_df("2024-08-14", "2024-11-06")
        self.plot_value(unit, f"img/post_challange_{unit_label}.png")

    def filter_df(self, start_date=None, end_date=None):
        df = self._df_all.reset_index()
        if start_date is not None:
            df = df[df.date >= start_date]

        if end_date is not None:
            df = df[df.date <= end_date]

        self.df = df.set_index("date")

    def plot_value(self, unit="km", figfile=None, mark_shoes_dates=False):
        df = self.df[self.df.unit == unit]

        fig, ax = plt.subplots(figsize=(15, 7))
        ax.bar(df.index, df["value"])

        ax.set_xticks(df.index)
        ax.set_xticklabels(df.index, rotation=90)
        ax.set_title(
            f"[#days: {len(df)}] "
            f"mean: {df.value.mean().item(): 0.2f}, "
            f"median: {df.value.median().item(): 0.2f}, "
            f"total: {df.value.sum().item(): 0.2f}",
            fontsize=14,
        )
        ax.set_ylabel(unit, fontsize=13)
        ax.grid(True)

        if mark_shoes_dates:
            ax.axvline("2024-06-08", color="b", linestyle="--", label="Shoes bought")
            ax.axvline("2024-08-13", color="r", linestyle="--", label="Shoes discarded")
            ax.legend()

        self._save_file(fig, figfile)

    def plot_rolling_value(self, unit="km", n=31, figfile=None):
        df = self.df[self.df.unit == unit]

        df = df["value"].rolling(window=n).sum()
        z = pd.DataFrame({unit: df, f"{unit}_per_day": df / n})

        fig, ax1 = plt.subplots(figsize=(15, 5))

        ax1.plot(z[unit], marker="o", color="blue", label=unit)
        ax1.set_xlabel("date")
        ax1.set_ylabel(f"Total {unit} during the period", fontsize=13)

        ax1.set_xticks(z.index[n - 1 :])
        ax1.set_xticklabels(z.index[n - 1 :], rotation=90)
        ax1.grid(True)
        ax1.set_title(f"Period: last {n} days", fontsize=14)

        ax2 = ax1.twinx()
        ax2.plot(z[f"{unit}_per_day"], color="blue", label="km_per_day")
        ax2.set_ylabel(f"Average {unit} per day over the period", fontsize=13)

        self._save_file(fig, figfile)

    def save_clean_data(self):
        """Save processed data."""
        self.filter_df("2024-05-21", "2024-11-06")
        self.df.to_csv("data/export_clean.csv", index=True)

    def _read_clean_data(self):
        """Read already processed data."""
        return pd.read_csv(self.data_file, index_col="date")

    def _read_data_iphone(self):
        """Reads the original data."""
        root = ET.parse(self.data_file).getroot()
        records = [record.attrib for record in root.iter("Record")]
        df = pd.DataFrame(records)

        df["date"] = pd.to_datetime(df["creationDate"]).dt.strftime("%Y-%m-%d")
        df["value"] = df["value"].astype(float)

        cols = [
            "HKQuantityTypeIdentifierDistanceWalkingRunning",  # distance km
            "HKQuantityTypeIdentifierStepCount",  # step count
        ]

        df = df[df.type.isin(cols)][["date", "unit", "value"]]
        df["unit"] = df["unit"].replace("count", "step count")
        df["unit"] = df["unit"].replace("km", "dist km")
        return (
            df.groupby(["date", "unit"], as_index=False)[["value"]]
            .sum()
            .set_index("date")
        )

    @staticmethod
    def _save_file(fig, file=None):
        if file is not None:
            file = Path(file)
            file.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(file, bbox_inches="tight", dpi=75)
