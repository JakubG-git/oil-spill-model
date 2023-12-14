import numpy as np
from model.cell import Cell
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import pandas as pd
import os


# cells is a list of Cell objects, i have a map consisting of 16x12 cells
# i want this function to generate wind vectors for each cell
# but in a pattern that makes sense, meaning that the wind vectors should be
# similar to each other in a certain area
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


def get_water_vectors() -> list[tuple[float, float]]:
    water_vectors = []
    path = os.path.join('data', 'hycom_with_NaN_values.csv')
    df = pd.read_csv(path)
    df_size = len(df)

    for i in range(df_size):
        if df['water_u'][i] != '--':
            water_vectors.append((float(df['water_u'][i]), float(df['water_v'][i])))
        else:
            water_vectors.append((0.0, 0.0))

    water_vectors_rows = []
    for i in range(360):
        water_vectors_rows.append(water_vectors[i * 420:(i + 1) * 420])
    water_vectors_rows.reverse()
    water_vectors2 = []
    for row in water_vectors_rows:
        water_vectors2 += row

    return water_vectors2


def get_temps():
    water_vectors = []
    path = os.path.join('data', 'hycom_with_NaN_values.csv')
    df = pd.read_csv(path)
    df_size = len(df)

    for i in range(df_size):
        if df['water_u'][i] != '--':
            water_vectors.append(float(df['water_temp'][i]))
        else:
            water_vectors.append(0.0)
    return water_vectors


def set_vectors_and_temps(cells: list[Cell]):
    cells = set_wind_vectors(cells)
    cells = set_water_vectors(cells)
    cells = set_temps(cells)
    return cells


def set_water_vectors(cells: list[Cell]):
    water_vectors = get_water_vectors()
    for i in range(len(cells)):
        cells[i].set_water_wector(water_vectors[i])
    return cells


def set_wind_vectors(cells: list[Cell]):
    wind_vectors = generate_wind_vectors(2, np.random.uniform(0, 360))
    for i in range(len(cells)):
        cells[i].set_wind_wector(wind_vectors[i])
    return cells


def set_temps(cells: list[Cell]):
    temps = get_temps()
    for i in range(len(cells)):
        cells[i].set_water_temp(temps[i])
    return cells


def generate_arrows(wind_vectors, water_vectors):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')

    # Plot grid with arrows
    rows = 18
    columns = 21
    cell_size = 1.0

    for i in range(rows):
        for j in range(columns):
            x = j * cell_size
            y = rows - i - 1 * cell_size  # Invert the y-axis to match the grid
            # wind_vector = wind_vectors[i * columns + j]
            water_vector = water_vectors[i * columns + j]
            arrow_scale = 1.0
            # Plot arrow
            # arrow1 = patches.FancyArrowPatch(
            #     (x + 0.5 * cell_size, y + 0.5 * cell_size),
            #     (x + 0.5 * cell_size + arrow_scale * wind_vector[0], y + 0.5 * cell_size + arrow_scale * wind_vector[1]),
            #     color='black',
            #     mutation_scale=10,
            #     linewidth=0.6,
            #     arrowstyle='->'
            # )
            arrow2 = patches.FancyArrowPatch(
                (x + 0.5 * cell_size, y + 0.5 * cell_size),
                (x + 0.5 * cell_size + arrow_scale * water_vector[0],
                 y + 0.5 * cell_size + arrow_scale * water_vector[1]),
                color='blue',
                mutation_scale=10,
                linewidth=0.6,
                arrowstyle='->'
            )
            # ax.add_patch(arrow1)
            ax.add_patch(arrow2)
            print(x, y)

    # Set axis limits
    ax.set_xlim(0, columns)
    ax.set_ylim(0, rows)

    # Set labels
    ax.set_xticks(np.arange(0, columns + 1, 1))
    ax.set_yticks(np.arange(0, rows + 1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    path = os.path.join("images", "water_vectors_plot.png")
    plt.savefig(path)

    # Rotate the saved image
    img = Image.open(path)
    rotated_img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)  # Change the rotation angle as needed
    path = os.path.join("images", "rotated_water_vectors_plot.png")
    rotated_img.save(path)

    # Show the rotated image
    rotated_img.show()
