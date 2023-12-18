import numpy as np
from model.cell import Cell
import pandas as pd
import os

def generate_wind_vectors(wind_speed: float, wind_direction: float) -> list[tuple[float, float]]:
    rows = 360
    columns = 420
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


def get_water_info() -> tuple[list[tuple[float, float]], list[float]]:
    water_vectors = []
    water_temps = []
    path = os.path.join('data', 'preprocessing', 'hycom_with_NaN_values.csv')
    df = pd.read_csv(path)
    df_size = len(df)

    for i in range(df_size):
        if df['water_u'][i] != '--':
            water_vectors.append((float(df['water_u'][i]), float(df['water_v'][i])))
            water_temps.append(float(df['water_temp'][i]))
        else:
            water_vectors.append((0.0, 0.0))
            water_temps.append(0.0)

    water_vectors_rows = []
    water_temps_rows = []
    for i in range(360):
        water_vectors_rows.append(water_vectors[i * 420:(i + 1) * 420])
        water_temps_rows.append(water_temps[i * 420:(i + 1) * 420])
    water_vectors_rows.reverse()
    water_temps_rows.reverse()
    water_vectors2 = []
    water_temps2 = []
    for row in water_vectors_rows:
        water_vectors2 += row

    for row in water_temps_rows:
        water_temps2 += row
    return water_vectors2, water_temps2


def set_vectors_and_temps(cells: list[Cell]) -> list[Cell]:
    cells = set_wind_vectors(cells)
    cells = set_water_info(cells)
    return cells

def set_water_info(cells: list[Cell]) -> list[Cell]:
    water_vectors, water_temps = get_water_info()
    for i in range(len(cells)):
        cells[i].set_water_wector(water_vectors[i])
        cells[i].set_water_temp(water_temps[i])
    return cells

def set_wind_vectors(cells: list[Cell]) -> list[Cell]:
    wind_vectors = generate_wind_vectors(2, np.random.uniform(0, 360))
    for i in range(len(cells)):
        cells[i].set_wind_wector(wind_vectors[i])
    return cells