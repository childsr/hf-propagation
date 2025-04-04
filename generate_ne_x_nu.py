import csv

def parse_input_row(row):
  height = row['height']
  electron_density = float(row['electron_density'])
  collision_frequency = float(row['collision_frequency'])
  return [height,"{:.2E}".format(electron_density*collision_frequency)]

with open('data/test2.csv', 'w', newline='') as output_file:
  with open('data/test.csv', 'r', newline='') as input_file:
    writer = csv.writer(output_file)
    reader = csv.DictReader(input_file)  # Reads rows as dictionaries
    out = map(parse_input_row,reader)
    writer.writerows(out)

