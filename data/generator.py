import numpy as np
from model.cell import Cell

def generate_random_vectors_and_temps(cells: list[Cell]):
    for cell in cells:
        # Generate random wind vectors
        wind_speed = np.random.uniform(0, 20)
        wind_direction = np.random.uniform(0, 360)
        wind_direction_rad = np.radians(wind_direction)
        wind_vector = (wind_speed * np.cos(wind_direction_rad), wind_speed * np.sin(wind_direction_rad))

        # Generate random water vectors and temperatures
        water_speed = np.random.uniform(0, 10)
        water_direction = np.random.uniform(0, 360)
        water_direction_rad = np.radians(water_direction)
        water_vector = (water_speed * np.cos(water_direction_rad), water_speed * np.sin(water_direction_rad))
        water_temp = np.random.uniform(0, 30)

        cell.set_vectors_n_temp(wind_vector, water_vector, water_temp)
    return cells