import math
import scipy
import csv
import argparse
import scipy.integrate

E = 1.60217663e-19
"""Elementary charge (e) in coulombs"""
EPSILON_0 = 8.8541878188e-12
"""Vacuum Permittivity (ε₀) in farads per meter"""
C = 299_792_458
"""Speed of light in vacuum (c) in meters per second"""
M_E = 9.1093837e-31
"""Electron mass in kg"""
H_0 = 50e3
"""Altitude of the bottom of the D-layer in meters"""
H_MAX = 100e3
"""Altitude of the top of the D-layer in meters"""

height_data: list[float] = []
electron_density_data: list[float] = []
collision_frequency_data: list[float] = []

with open('data/hf_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # Reads rows as dictionaries
    for row in reader:
      height = 1000.0 * float(row['height']) # convert to meters
      electron_density = float(row['electron_density'])
      collision_frequency = float(row['collision_frequency'])

      height_data.append(height)
      electron_density_data.append(electron_density)
      collision_frequency_data.append(collision_frequency)

def lerp(a,b,t):
  return (1 - t) * a + b * t
def last_element_leq(lst, x):
  """
  Returns the index of the last element in `lst` that is less than
  or equal to `x`; or, if `x` is less than every element in `lst`,
  `-1` is returned.

  `lst' is assumed to be sorted in ascending order.
  
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
  t = (h - height_data[i]) / (height_data[i-1] - height_data[i])
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
    height_data: list[float],
    electron_density_data: list[float],
    collision_frequency_data: list[float]
  ):
  """Calculate total absorption (L_a) in dB

  * L_a = -8.69 ∫κds
  * L_a ~ -8.69 ∫ (e^2 / (2 ε₀ m_e c)) (n_e nu / (4 π^2 f^2)) ds
  * L_a ~ -8.69 (e^2 / (2 ε₀ m_e c 4 π^2 f^2)) ∫ n_e nu ds
  * L_a ~ -8.69 (e^2 / (8 π^2 ε₀ m_e c f^2)) ∫ n_e nu ds
  * C = -8.69 (e^2 / (8 π^2 ε₀ m_e c f^2))
  * L_a ~ C * ∫ n_e nu ds

  Parameters
  ----------
  takeOffAngle 
    Take off angle in degrees
  frequency 
    signal frequency in Hz

  Returns
  -------
  float
    The total absorption in dB
  """



  get_electron_density = get_data(electron_density_data,height_data)
  get_collision_frequency = get_data(collision_frequency_data,height_data)
  
  coeff = -8.69 * (E**2 / (8 * math.pi**2 * EPSILON_0 * M_E * C * frequency**2))
  
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

  total, error = scipy.integrate.quad(integrand, 0, total_s)
  
  # n = math.floor(d_layer_height/resolution)
  # print(n)
  # total = 0
  # for i in range(0,n):
  #   s = i * delta_s
  #   total = total + absorption(s) * delta_s

  return coeff * total

def test():
  f = 14e6
  alpha = 35
  result = integrate(alpha, f)
  print(f"Take Off Angle: {alpha}")
  print(f"Signal Frequency: {round(f/1e6,2)} MHz")
  print(f"Total ionospheric absorption: {round(result,3)} dB")
  # print(result)

def main():
  parser = argparse.ArgumentParser(description="A simple CLI program example.")

  # Required argument
  parser.add_argument("--name", required=True, help="Your name")

  # Optional argument
  parser.add_argument("--age", type=int, help="Your age")

  args = parser.parse_args()

  print(args)
  # print(f"Hello, {args.name}!")
  # if args.age:
  #     print(f"You are {args.age} years old.")
  # else:
  #     print("You didn't provide your age.")

# if __name__ == "__main__":
#     main()

test()
