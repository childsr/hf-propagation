import math
import cmd

E = 1.60217663 * 10 ** -19
"""Elementary charge (e) in coulombs"""
EPSILON_0 = 8.8541878188 * 10 ** -12
"""Vacuum Permittivity (ε₀) in farads per meter"""
C = 299_792_458
"""Speed of light in vacuum (c) in meters per second"""

def collision_frequency(altitude: float) -> float:
  """Get the collision frequency (ν) at the given altitude

  Parameter
  ---------
  altitude : float
    altitude above sea level in km

  Returns
  -------
  float
    the collision frequency (ν)
  """
  return 1.0
def electron_density(altitude: float) -> float:
  """Get the electron density (n_e) at the given altitude

  Parameter
  ---------
  altitude : float
    altitude above sea level in km

  Returns
  -------
  float
    the electron density (n_e)
  """
  return 1.0
def neutral_density(altitude: float) -> float:
  """Get the neutral density (n_n) at the given altitude

  Parameter
  ---------
  altitude : float
    altitude above sea level in km

  Returns
  -------
  float
    the neutral density (n_e)
  """
  return 1.0
def kappa1(altitude: float, frequency: float) -> float:
  """Calculate the coefficient of absorption (κ) at the given altitude
  in cases where wave frequency is much greater than collision frequency.

  Parameter
  ---------
  altitude : float
    altitude above sea level in km
  frequency : float
    signal frequency in Hz

  Returns
  -------
  float
    the coefficient of absorption (κ)
  """
  return 1.0
def kappa2(altitude: float, frequency: float) -> float:
  """Calculate the coefficient of absorption (κ) at the given altitude
  in cases where collision frequency is much greater than wave frequency.

  Parameter
  ---------
  altitude : float
    altitude above sea level in km
  frequency : float
    signal frequency in Hz

  Returns
  -------
  float
    the coefficient of absorption (κ)
  """
  return 1.0
def kappa3(altitude: float, frequency: float) -> float:
  """Calculate the coefficient of absorption (κ) at the given altitude
  in cases where wave frequency is about equal to collision frequency.

  Parameter
  ---------
  altitude : float
    altitude above sea level in km
  frequency : float
    signal frequency in Hz

  Returns
  -------
  float
    the coefficient of absorption (κ)
  """
  return 1.0
def absorption_at(altitude: float, frequency: float) -> float:
  """Calculate absorption at the given altitude

  Parameter
  ---------
  altitude : float
    altitude above sea level in km
  frequency : float
    signal frequency in Hz

  Returns
  -------
  float
    absorption in dB/m
  """
  return 1.0

def integrate(takeOffAngle: float, distToRec: float, frequency: float, resolution: float = 1) -> float:
  """Calculate total absorption (L_a) in dB

  Parameters
  ----------
  takeOffAngle : float
    Take off angle in degrees
  distToRec : float
    Distance to receiver in km
  frequency : float
    signal frequency in Hz
  resolution : float, optional
    Size in km of each segment (default: 1km)

  Returns
  -------
  float
    The total absorption in dB
  """
  h_0: float = 50
  theta = takeOffAngle * math.pi / 180
  h_max = distToRec / (2 * math.cos(theta))
  delta_h = resolution
  segments = int((h_max - h_0) / resolution)

  L_a = 0.0
  s = 0.0
  x = h_0 / math.tan(theta)

  print(f"take-off angle: {round(takeOffAngle,2)}°")
  print(f"h_max: {round(h_max,2)} km")
  print(f"{segments} segments")

  for i in range(segments):
    h = h_0 + i * delta_h
    delta_x = delta_h / math.tan(theta)
    delta_s = math.sqrt(delta_x ** 2 + delta_h ** 2)
    delta_L_a = absorption_at(h,frequency) * delta_s

    x += delta_x
    s += delta_s
    L_a += delta_L_a

  return L_a

result = integrate(35, 200, 1)
print("")
print(f"Total ionospheric absorption: {round(result,3)} dB")