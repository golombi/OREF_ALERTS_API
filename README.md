# OREF_ALERTS_API
Scrape data from the official Israeli Alert System Webpage that currently has no API, using Selenium. A simple project that was written in a couple of days.

oref_alerts_api.py

  get_alerts_json(date_from, date_to, locations_set=FullSet(), category_set=FullSet()):
  
  Returns an array of json-like objects corresponding to the alerts in the given date range and locations and categories (last two are optional).
  Dates are each a touple of integers of the form (Day,Month,Year) 

distribution_by_place.py

  A simple usage script that prints the json_array for the Missile Alerts in the date range given as a CLA in the locations provided by user input.
