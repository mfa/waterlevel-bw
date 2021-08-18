## Scrape water level data for Baden-Württemberg rivers and seas

[![Scrape latest data](https://github.com/mfa/waterlevel-bw/actions/workflows/scrape.yml/badge.svg)](https://github.com/mfa/waterlevel-bw/actions/workflows/scrape.yml)

This code downloads the water level data using [playwright](https://playwright.dev/python/) (because the [source website](https://www.hvz.baden-wuerttemberg.de) is using Javascript to generate the table).  
To schedule the downloads Github Actions are used.

Future plans are to deploy a Datasette instance with the data backed-in as an API for historical data on river water levels in Baden Württemberg.
