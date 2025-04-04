import math
import csv
import argparse
import json

E = 1.60217663e-19
"""Elementary charge (e) in coulombs"""
EPSILON_0 = 8.8541878188e-12
"""Vacuum Permittivity (ε₀) in farads per meter"""
C = 299_792_458
"""Speed of light in vacuum (c) in meters per second"""
M_E = 9.1093837e-31
"""Electron mass in kg"""
H_0 = 60e3
"""Altitude of the bottom of the D-layer in meters"""
H_MAX = 100e3
"""Altitude of the top of the D-layer in meters"""

def lerp(a,b,t):
  if a == None or b == None:
    return 0
  else:
    return (1 - t) * a + b * t
def last_element_leq(lst, x):
  """
  Returns the index of the last element in `lst` that is less than
  or equal to `x`; or, if `x` is less than every element in `lst`,
  `-1` is returned.

  `lst` is assumed to be sorted in ascending order.
  
  Parameter
  ----------
  lst : list[number]
  x : number
  """
  n = len(lst)
  if x < lst[0]:
    return -1
  if x >= lst[n-1]:
    return n - 1
  for i in range(1,n):
    if lst[i] > x:
      return i-1
  return n - 1
def get_i_and_t(height_data,h):
  i = last_element_leq(height_data,h)
  if i == -1:
    return 0, 0
  if i == len(height_data) - 1:
    return i, 0
  t = (h - height_data[i]) / (height_data[i+1] - height_data[i])
  return i, t
def get_data(data,height_data):
  def f(h):
    i, t = get_i_and_t(height_data,h)
    if i == len(data) - 1:
      return data[-1]
    else:
      return lerp(data[i],data[i+1],t)
  return f

def integrate(
    take_off_angle: float,
    frequency: float,
    data: list[tuple[float,float,float]],
    model = 1
  ):
  """Calculate total absorption (L_a) in dB

  Parameters
  ----------
  takeOffAngle 
    Take off angle in degrees
  frequency 
    signal frequency in MHz
  data
    height, electron density, and collision frequency in
    the form of a list of triples (i.e. (height,n_e,nu))

  Returns
  -------
  float
    The total absorption in dB
  """
  height_data = list(map(lambda row: row[0], data))
  electron_density_data = list(map(lambda row: row[1], data))
  collision_frequency_data = list(map(lambda row: row[2], data))

  get_electron_density = get_data(electron_density_data,height_data)
  get_collision_frequency = get_data(collision_frequency_data,height_data)
  
  coeff = -8.69 * (E**2 / (8 * math.pi**2 * EPSILON_0 * M_E * C * (frequency * 1e6)**2))
  coeff2 = -8.69 * (E**2 / (2 * EPSILON_0 * M_E * C))
  
  theta = take_off_angle * math.pi / 180
  
  resolution = 1000
  d_layer_height = H_MAX - H_0
  total_s = d_layer_height / math.sin(theta)
  delta_s = resolution / math.sin(theta)

  def integrand(s):
    h = H_0 + s * math.sin(theta)
    n_e = get_electron_density(h)
    nu = get_collision_frequency(h)
    return n_e * nu
  def integrand2(s):
    h = H_0 + s * math.sin(theta)
    n_e = get_electron_density(h)
    nu = get_collision_frequency(h)
    return n_e * nu / ((2*math.pi * frequency * 1e6)**2 + nu**2)
  
  def int_loop():
    n = math.floor(d_layer_height/resolution)
    total = 0
    c = coeff
    int = integrand
    if model == 2:
      int = integrand2
      c = coeff2
    for i in range(0,n):
      s = i * delta_s
      total = total + int(s) * delta_s
    # multiply by 2 to account for the path back down through the D-region
    return c * total * 2

  total = int_loop()
  

  return total

def test():
  data: list[tuple[float,float,float]] = []
  with open('data/hf_data.csv', newline='', encoding='utf-8') as file:
      reader = csv.DictReader(file)  # Reads rows as dictionaries
      for row in reader:
        height = 1000.0 * float(row['height']) # convert to meters
        electron_density = float(row['electron_density'])
        collision_frequency = float(row['collision_frequency'])

        data.append((height, electron_density, collision_frequency))

  f = 3
  alpha = 90
  result = integrate(alpha, f, data, 2)
  print(f"Take Off Angle: {alpha}")
  print(f"Signal Frequency: {round(f,2)} MHz")
  print(f"Total ionospheric absorption: {round(result,3)} dB")
  # print(result)

def read_std_neutral_density_json():
  data = {}
  with open("data/std_neutral_density.json", "r") as file:
    data = json.load(file)
  return data

def read_iri_data_json(file_path):
  """Read the json file and return a list of tuples (height (in km), electron density, collision frequency)"""
  data = []
  std_nn = read_std_neutral_density_json()
  with open(file_path, newline='', encoding='utf-8') as file:
    json_data = json.load(file)
    for entry in json_data:
      h_index = str(round(entry["height"]))
      nn = std_nn[h_index]
      height = 1000.0 * float(entry['height'])  # convert to meters

      ne = entry['ne']
      electron_density = 0
      if ne != None:
        electron_density = float(ne)

      Te = entry['Te']
      collision_frequency = 0
      if Te != None:
        collision_frequency = 5.4e-10 * nn * math.sqrt(float(Te))
      
      data.append((height, electron_density, collision_frequency))
  return data

def main():
  parser = argparse.ArgumentParser(description="Compute the total ionospheric absorption (L_a) in dB")

  # Required arguments
  parser.add_argument("-t", "--takeOffAngle", required=True, help="take off angle in degrees", type=float)
  parser.add_argument("-f", "--frequency", required=True, help="signal frequency in MHz", type=float)
  parser.add_argument("-d", "--data", required=True, help="path to the data file")

  args = parser.parse_args()
  data = read_iri_data_json(args.data)

  result = integrate(
    args.takeOffAngle,
    args.frequency,
    data
  )
  print(result)
if __name__ == "__main__":
  # main()
  test()

# test()
