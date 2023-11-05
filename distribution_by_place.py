import sys
from oref_alerts_api import get_alerts_json, parse_date

def main():
    if len(sys.argv)!=3:
        print("Usage: python3 DD-MM-YYYY DD-MM-YYYY")
        sys.exit(1)

    loc_count = int(input("Enter the number of locations to filter on: "))
    given_locations = set()
    for i in range(loc_count):
        given_locations.add(input("Enter location " + str(i+1) + ": "))

    json_array = get_alerts_json(parse_date(sys.argv[1], "-"), parse_date(sys.argv[2], "-"),
           locations_set=given_locations, category_set="Missiles")
    print(json_array)
    print("Total number of alerts: " + str(len(json_array)))

if __name__=="__main__":
    main()