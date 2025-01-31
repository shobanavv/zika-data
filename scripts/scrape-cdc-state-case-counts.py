#!/usr/bin/env python
import requests
import lxml.html
import pandas as pd
import sys

URL = "http://www.cdc.gov/zika/geo/united-states.html"

INT_COLS = [ "travel_associated_cases", "locally_acquired_cases" ]
COLS = [ "state_or_territory" ] + INT_COLS

def scrape():
    html = requests.get(URL).content
    dom = lxml.html.fromstring(html)

    table = dom.cssselect("table")[0]
    rows = table.cssselect("tr")

    cells = [ [ td.text_content().strip() 
        for td in tr.cssselect("td") ] 
             for tr in rows ]

    data = [ c for c in cells 
        if sum(len(x) != 0 for x in c) == 3 ]

    df = pd.DataFrame(data, columns=COLS)
    df[INT_COLS] = df[INT_COLS].astype(int)

    return df

if __name__ == "__main__":
    df = scrape()
    df.to_csv(sys.stdout, index=False, encoding="utf-8")
