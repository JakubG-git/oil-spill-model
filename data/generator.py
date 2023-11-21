import numpy as np
from model.cell import Cell

def generate_random_vectors_and_temps(cells: list[Cell]):
    for cell in cells:
        # Generate random wind vectors
        wind_speed = np.random.uniform(1, 20)
        wind_direction = np.random.uniform(0, 360)
        wind_direction_rad = np.radians(wind_direction)
        wind_vector = (wind_speed * np.cos(wind_direction_rad), wind_speed * np.sin(wind_direction_rad))

        # Generate random water vectors and temperatures
        water_speed = np.random.uniform(1, 10)
        water_direction = np.random.uniform(0, 360)
        water_direction_rad = np.radians(water_direction)
        water_vector = (water_speed * np.cos(water_direction_rad), water_speed * np.sin(water_direction_rad))
        water_temp = np.random.uniform(0, 30)

        cell.set_vectors_n_temp(wind_vector, water_vector, water_temp)
    return cells


# cells is a list of Cell objects, i have a map consisting of 16x12 cells
# i want this function to generate wind vectors for each cell
# but in a pattern that makes sense, meaning that the wind vectors should be
# similar to each other in a certain area
def generate_wind_vectors(wind_speed: float, wind_direction: float) -> list[tuple[float, float]]:
    rows = 16
    columns = 12
    wind_speeds = []
    wind_directions = []

    for i in range(rows):
        row_speed = []
        row_direction = []
        for j in range(columns):
            if i == 0 and j == 0:
                row_speed.append(wind_speed)
                row_direction.append(wind_direction)
            else:
                if i > 0 and j > 0:
                    avg_speed = (wind_speeds[i][j - 1] + wind_speeds[i - 1][j]) / 2
                    avg_direction = (wind_directions[i][j - 1] + wind_directions[i - 1][j]) / 2
                elif i > 0:
                    avg_speed = wind_speeds[i - 1][j]
                    avg_direction = wind_directions[i - 1][j]
                elif j > 0:
                    avg_speed = wind_speeds[i][j - 1]
                    avg_direction = wind_directions[i][j - 1]

                wind_speed = avg_speed + np.random.uniform(-2, 2)
                wind_direction = avg_direction + np.random.uniform(-15, 15)
                row_speed.append(wind_speed)
                row_direction.append(wind_direction)

            wind_speeds.append(row_speed)
            wind_directions.append(row_direction)

    wind_vectors = []
    for i in range(rows):
        for j in range(columns):
            wind_speed_x = wind_speeds[i][j] * np.cos(np.radians(wind_directions[i][j]))
            wind_speed_y = wind_speeds[i][j] * np.sin(np.radians(wind_directions[i][j]))
            wind_vectors.append((wind_speed_x, wind_speed_y))

    return wind_vectors


# def generate_water_vectors():
#     return [(0, 0) for _ in range(192)]

def generate_water_vectors(water_speed: float, water_direction: float) -> list[tuple[float, float]]:
    rows = 16
    columns = 12
    water_speeds = []
    water_directions = []

    for i in range(rows):
        row_speed = []
        row_direction = []
        for j in range(columns):
            if i == 0 and j == 0:
                row_speed.append(water_speed)
                row_direction.append(water_direction)
            else:
                if i > 0 and j > 0:
                    avg_speed = (water_speeds[i][j - 1] + water_speeds[i - 1][j]) / 2
                    avg_direction = (water_directions[i][j - 1] + water_directions[i - 1][j]) / 2
                elif i > 0:
                    avg_speed = water_speeds[i - 1][j]
                    avg_direction = water_directions[i - 1][j]
                elif j > 0:
                    avg_speed = water_speeds[i][j - 1]
                    avg_direction = water_directions[i][j - 1]

                water_speed = avg_speed + np.random.uniform(-2, 2)
                water_direction = avg_direction + np.random.uniform(-15, 15)
                row_speed.append(water_speed)
                row_direction.append(water_direction)

            water_speeds.append(row_speed)
            water_directions.append(row_direction)

    water_vectors = []
    for i in range(rows):
        for j in range(columns):
            water_speed_x = water_speeds[i][j] * np.cos(np.radians(water_directions[i][j]))
            water_speed_y = water_speeds[i][j] * np.sin(np.radians(water_directions[i][j]))
            water_vectors.append((water_speed_x, water_speed_y))

    return water_vectors

def generate_temps():
    return [np.random.uniform(0, 30) for _ in range(192)]

def set_vectors_and_temps(cells: list[Cell]):
    wind_vectors = generate_wind_vectors(10, np.random.uniform(0, 360))
    water_vectors = generate_water_vectors(10, np.random.uniform(0, 360))
    temps = generate_temps()

    for i in range(len(cells)):
        cells[i].set_vectors_n_temp(wind_vectors[i], water_vectors[i], temps[i])

    return cells
