import pandas as pd
from pandas.compat import sys
from termcolor import colored


class NessusParser:
    def __init__(self, option: str):
        self.opt = option

    def read_csv(self, file: str):
        df = None
        try:
            if self.opt == "p":
                df = pd.read_csv(file)
                df = df[
                    [
                        "Plugin ID",
                        "Host",
                        "CVE",
                        "Risk",
                        "Name",
                        "Port",
                        "Protocol",
                        "Synopsis",
                        "Solution",
                    ]
                ]
                df = df[df["Risk"].notna()]
            return df
        except Exception as _:
            print(colored(f"Something went wrong reading .csv {file}", "red"))
            return df

    def parse(self, df):
        # First aggroupation
        grouped_df = (
            df.groupby(["Name", "Host"])
            .agg(
                {
                    "Port": lambda x: ", ".join(map(str, x.unique())),
                    "CVE": "first",
                    "Risk": "first",
                    "Synopsis": "first",
                    "Solution": "first",
                }
            )
            .reset_index()
        )
        # Second aggroupation
        result = (
            grouped_df.groupby(["Name", "Port"])
            .agg(
                {
                    "Host": lambda x: ", ".join(map(str, x.unique())),
                    "CVE": "first",
                    "Risk": "first",
                    "Synopsis": "first",
                    "Solution": "first",
                }
            )
            .reset_index()
        )
        filtered = result[result["Risk"] != "None"]
        return filtered

    # def hosts_per_vuln(self):
    #     grouped_df = (
    #         self.df.groupby("Name")
    #         .agg(
    #             {
    #                 "Host": lambda x: "\n".join(map(str, x.unique())),
    #                 "Risk": "first",
    #             }
    #         )
    #         .reset_index()
    #     )
    #     filtered = grouped_df[grouped_df["Risk"] != "None"]
    #     return filtered
