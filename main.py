import argparse
import mimetypes
from termcolor import colored
from controllers.NessusParser import NessusParser
import pandas as pd


def parse_file(file):
    mime_type, _ = mimetypes.guess_type(file)
    if mime_type == "text/csv":
        p = NessusParser(option="p")
        df = p.read_csv(file)
        return df
    else:
        print(colored(f"[I] Omitting file {file}... MIME type is not text/csv", "yellow"))
    return None


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        description="Automatizing Nessus reports parsing"
    )
    args_parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="List of input files in format .CSV",
        required=True,
    )
    args_parser.add_argument(
        "-o", "--option", choices=["p"], help="p Parse current file", required=True
    )
    args_parser.add_argument("-n","--name", help="File name", required=True)
    args = args_parser.parse_args()
    files = args.files
    name = args.name
    option = args.option
    data = list()
    if option == "p":
        for index, file in enumerate(files, 1):
            df = parse_file(file)
            if df is not None:
                data.append(df)
        if len(data) > 0:
            combined_df = pd.concat(data, ignore_index=True)
            parse = NessusParser(option="p").parse(combined_df)
            parse.to_excel(f"{name}.xlsx")
