import main

def parse_line(line: str):
  substrs = line.split(":")
  date_substrs = substrs[0].split("-")
  year = int(date_substrs[0])
  month = int(date_substrs[1])
  hour = int(date_substrs[2])
  haf = float(substrs[1])
  return ((year,month,hour), haf)

with open("data/haf.txt") as file:
  for line in file.readlines():
    date, haf = parse_line(line)
    if haf == 0: continue
    year, month, hour = date
    if month == 1: hour -= 7
    else: hour -= 6
    date_str = f"{year}-{month:02d}-{hour:02d}"
    print(date_str)
    data = main.read_iri_data_json(f"data/iri-data/{date_str}.json")
    result = main.integrate(90, haf, data, 2)
    print(result)