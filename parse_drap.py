import os
import re

def parse_longitude_line(line: str):
  return list(map(float,line.strip().split()))
def parse_data_line(line: str):
  strs = line.split()
  longitude = float(strs[0])
  data = list(map(float, strs[2:]))
  return longitude, data
def parse_data_lines(data_lines: list[str]):
  rows = map(parse_data_line, data_lines)
  latitudes: list[float] = []
  data: list[list[float]] = []
  for lat, row in rows:
    latitudes.append(lat)
    data.append(row)
  return latitudes, data
def build_dict(latitudes: list[float], longitudes: list[float], data: list[list[float]]):
  dct = {}
  for i in range(0,len(latitudes)):
    for j in range(0,len(longitudes)):
      dct[(latitudes[i],longitudes[j])] = data[i][j]
  return dct

PATH = "data/drap-data/SWX_DRAP20_C_SWPC_20151001220000_GLOBAL.txt"
DIR = "data/drap-data"
OUTPUT_DIR = "data/haf"

def get_haf(path):
  with open(path) as file:
    # Filter out the header lines
    lines = [line for line in file.readlines() if not line.startswith("#")]
    
    longitude_line = lines[0]
    longitudes = parse_longitude_line(longitude_line)
    
    # Drop the latitude line from the list as well as the following line, which is all dashes.
    data_lines = lines[2:]
    latitudes, data = parse_data_lines(data_lines)
    drap = build_dict(latitudes,longitudes,data)
    
    return drap[(45.0,-110.0)]

lines: list[str] = []
for file_path in os.listdir(DIR):
  date_str: str = re.findall("SWPC_(\\d+)_GLOBAL",file_path)[0]
  
  year = date_str[0:4]
  month = date_str[4:6]
  hour = date_str[8:10]
  haf = get_haf(os.path.join(DIR, file_path))
  
  with open(f"{OUTPUT_DIR}/haf-{year}-{month}-{hour}.txt","w") as file:
    file.write(str(haf))