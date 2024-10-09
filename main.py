import math

# units: dB/m
def absorption_at(altitude: float) -> float:
  return 1.0

# takeOffAngle: degrees
# distToRec: km
# resolution: segments per km of altitude
def integrate(takeOffAngle: float, distToRec: float, resolution: float = 1) -> float:
  h_0: float = 50
  alpha = takeOffAngle * math.pi / 180
  h_max = distToRec / (2 * math.cos(alpha))
  delta_h = 1.0 / resolution
  segments = int((h_max - h_0) * resolution)

  L_a = 0.0
  s = 0.0
  x = h_0 / math.tan(alpha)

  print(f"take-off angle: {round(takeOffAngle,2)}°")
  print(f"h_max: {round(h_max,2)} km")
  print(f"{segments} segments")

  for i in range(segments):
    h = h_0 + i * delta_h
    delta_x = delta_h / math.tan(alpha)
    delta_s = math.sqrt(delta_x ** 2 + delta_h ** 2)
    delta_L_a = absorption_at(h) * delta_s

    x += delta_x
    s += delta_s
    L_a += delta_L_a
    # print(h)

  return L_a

result = integrate(35, 200, 1)
print("")
print(f"Total absorption: {round(result,3)} dB")