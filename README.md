# OREF_ALERTS_API
Scrape data from the official Israeli Alert System Webpage that currently has no API, using Selenium. A simple project that was written in a couple of days.

The script opens the webpage, scrolls and clicks the appropriate buttons according to their webpage design at 11.5.2023:

The date choosing process and "Show more" clicks are automated, and then the extended webpage with all the alerts provided by "Picud Ha'oref"
is scanned and data is saved as a json-like (dictionary) object to an array, while the alerts' date and time of each date/time group are being updated contantly in local variables.

oref_alerts_api.py

  get_alerts_json(date_from, date_to, locations_set=FullSet(), category_set=FullSet()):
  
  Returns an array of json-like (dictionary) objects corresponding to the alerts in the given date range and locations and categories (last two are optional).
  Dates are each a touple of integers of the form (Day,Month,Year) 

distribution_by_place.py

  A simple usage script that prints the json_array for the Missile Alerts in the date range given as a CLA in the locations provided by user input.
