import numpy as np
from model.cell import Cell
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

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
    rows = 12
    columns = 16
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


def generate_water_vectors(water_speed: float, water_direction: float) -> list[tuple[float, float]]:
    rows = 12
    columns = 16
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
    generate_arrows(wind_vectors, water_vectors)

    for i in range(len(cells)):
        cells[i].set_vectors_n_temp(wind_vectors[i], water_vectors[i], temps[i])

    return cells

# def generate_arrows(wind_vectors: list[tuple[float, float]], water_vectors: list[tuple[float, float]]):
#     fig, ax = plt.subplots(figsize=(12, 16))

#     for wind_vector, water_vector in zip(wind_vectors, water_vectors):
#         ax.arrow(0, 0, wind_vector[0], wind_vector[1], head_width=0.5, head_length=0.7, fc='blue', ec='blue', alpha=0.7)
#         ax.arrow(0, 0, water_vector[0], water_vector[1], head_width=0.5, head_length=0.7, fc='green', ec='green', alpha=0.7)

#     ax.set_xlim(-20, 20)
#     ax.set_ylim(-20, 20)
#     ax.set_aspect('equal', adjustable='box')
#     #invert x axis
#     ax.invert_xaxis()
#     ax.set_xlabel('x')
#     #invert y axis
#     ax.invert_yaxis()
#     ax.set_ylabel('y')
#     ax.set_title('Wind and Water Vectors')
#     plt.grid(True)
#     plt.savefig('arrows.png', dpi=100)

def generate_arrows(wind_vectors, water_vectors):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')

    # Plot grid with arrows
    rows = 12
    columns = 16
    cell_size = 1.0

    for i in range(rows):
        for j in range(columns):
            x = j * cell_size
            y = rows - i - 1 * cell_size  # Invert the y-axis to match the grid
            wind_vector = wind_vectors[i * columns + j]
            water_vector = water_vectors[i * columns + j]
            arrow_scale = 0.1
            # Plot arrow
            arrow1 = patches.FancyArrowPatch(
                (x + 0.5 * cell_size, y + 0.5 * cell_size),
                (x + 0.5 * cell_size + arrow_scale * wind_vector[0], y + 0.5 * cell_size + arrow_scale * wind_vector[1]),
                color='black',
                mutation_scale=10,
                linewidth=0.6,
                arrowstyle='->'
            )
            arrow2 = patches.FancyArrowPatch(
                (x + 0.5 * cell_size, y + 0.5 * cell_size),
                (x + 0.5 * cell_size + arrow_scale * water_vector[0], y + 0.5 * cell_size + arrow_scale * water_vector[1]),
                color='blue',
                mutation_scale=10,
                linewidth=0.6,
                arrowstyle='->'
            )
            ax.add_patch(arrow1)
            ax.add_patch(arrow2)

    # Set axis limits
    ax.set_xlim(0, columns)
    ax.set_ylim(0, rows)

    # Set labels
    ax.set_xticks(np.arange(0, columns + 1, 1))
    ax.set_yticks(np.arange(0, rows + 1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.savefig('wind_vectors_plot.png')

    # Rotate the saved image
    img = Image.open('wind_vectors_plot.png')
    rotated_img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)  # Change the rotation angle as needed
    rotated_img.save('rotated_wind_vectors_plot.png')

    # Show the rotated image
    rotated_img.show()