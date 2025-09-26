import math

# Default center: Wilmington, DE (ZIP 19804 approximate)
CENTER_LAT = 39.715
CENTER_LON = -75.588

# Radius (meters) for study area
RADIUS_M = 40000  # 40km ~ 25 miles

# H3 resolution (7 ~ neighborhood / small-area scale)
H3_RESOLUTION = 7

# Scoring weights
WEIGHT_DEMAND = 1.0
WEIGHT_COMPETITION = 1.0

# Distance decay for competition (meters)
COMPETITION_DECAY_M = 3000.0

# Random seed for any synthetic demand fallback
SEED = 42
