#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports' function so that it returns a list of airport
codes, excluding any combinations like "All".
"""

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        airport_element = soup.find(id = "AirportList")
        for airport in airport_element.findChildren():
            airport_code = airport['value']
            if not ('All' in airport_code):
                data.append(airport_code)

    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()