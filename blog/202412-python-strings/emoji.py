"""Download and display emoji (just to search and choose a few).

How to use:

.. code-block:: bash

    $ uv run --with=pandas,requests,jupyterlab jupyter-lab

Then in a jupyterlab cell:

.. code-block:: python

    from emoji import EmojiHandler

    eh = EmojiHandler(download=True)
    eh.show()

"""

import random
from pathlib import Path

import pandas as pd
import requests
from IPython.display import HTML, display


class EmojiHandler:

    def __init__(self, download=False, urls=None, data_dir="data"):
        self.data_dir = Path(data_dir)
        # There might be more, I don't know
        self.urls = [
            "https://unicode.org/Public/emoji/latest/emoji-zwj-sequences.txt",
            "https://unicode.org/Public/emoji/latest/emoji-sequences.txt",
            "https://unicode.org/Public/emoji/latest/emoji-test.txt",
            "https://unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt",
            "https://unicode.org/Public/16.0.0/ucd/emoji/emoji-variation-sequences.txt",
        ]

        if download:
            self.download_emoji_files()
        self._data = self.get_data()

    def download_emoji_files(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        for url in self.urls:
            response = requests.get(url)
            response.raise_for_status()
            with open(self.data_dir / url.split("/")[-1], "w") as h:
                h.write(response.text)

    @property
    def count(self):
        return len(self._data)

    @property
    def data(self):
        return pd.DataFrame(self._data)

    def get_data(self):
        def expand_ranges(data):
            """I keep the same name for all expanded codepoints."""

            def expand_range(lb_hex, ub_hex):
                lb = int(lb_hex, 16)
                ub = int(ub_hex, 16)
                return [hex(i)[2:].upper() for i in range(lb, ub + 1)]

            updated_data = []
            for d in data:
                if ".." in d["seq"]:
                    code_points = expand_range(*d["seq"].split(".."))
                    updated_data.extend(
                        [
                            {"seq": code_point, "name": d["name"]}
                            for code_point in code_points
                        ]
                    )
                else:
                    updated_data.append(d)
            return updated_data

        def parse_emoji_file_content(file_content):
            data = []
            for line in file_content.splitlines():
                if line and not line.startswith("#"):
                    line_split = line.split(";")
                    seq = line_split[0].strip()
                    # name = line_split[-1].split("#")[0].strip()
                    name = line_split[-1].strip()
                    data.append({"seq": seq, "name": name})
            return data

        data = []
        for file in Path(self.data_dir).glob("**/*"):
            with open(file, "r") as h:
                file_content = h.read()
            data.extend(parse_emoji_file_content(file_content))

        return expand_ranges(data)

    def filter_data(self, keyword):
        df = self.data
        return df[df["name"].str.contains(keyword, case=False)].to_dict("records")

    @staticmethod
    def show_str(data: str, size=100):
        display(HTML(f'<span style="font-size: {size}px;">{data}</span>'))

    @staticmethod
    def form_zwj_emoji(seq):
        return "".join([chr(int(c, 16)) for c in seq.split(" ")])

    def show(self, n=50, filter=None, index=None, size=40):
        """Show n random emoji or the emoji with the given index."""

        data = self.filter_data(filter) if filter else self._data

        table_html = '<table style="border-collapse: collapse;">'

        if len(data) == 0:
            print("No data")
            return

        if n > len(data):
            n = len(data)
            print("Limit to available data.")

        if index is not None:
            n = 1
            sample = data[index]
        else:
            sample = random.sample(data, n)

        numb_cols = min(10, n)
        numb_rows = n // numb_cols
        k = 0
        for i in range(numb_rows):
            table_html += "<tr>"
            for j in range(numb_cols):
                s = self.form_zwj_emoji(sample[k]["seq"])
                table_html += f'<td style="font-size: {size}px; padding: 7px;">{s}</td>'
                k += 1
            table_html += "</tr>"

        table_html += "</table>"
        display(HTML(table_html))

    def __repr__(self):
        return f"[EmojiHandler] {self.count}"
