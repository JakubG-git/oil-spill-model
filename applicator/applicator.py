from model.cell import Cell
from model.particle import Particle




# #get cells that have particles in them

# def get_cells_with_particles(vis: Visualiser) -> list[Cell]:
#     cells_with_particles = []
#     for cell in vis.get_cells():
#         for particle in vis.get_particles():
#             if cell.x <= particle.x <= cell.x + cell.size and cell.y <= particle.y <= cell.y + cell.size:
#                 cells_with_particles.append(cell)
#     return cells_with_particles

def move_particles(vis):
    for particle in vis.get_particles():
        move_with_wind(particle, vis)
        # move_with_water(particle, vis)
        vis.update_particle(particle)
        vis.update()



def move_with_wind(particle: Particle, vis):
        current_cell = particle.get_current_cell(vis)
        if current_cell and current_cell.wind_vector:
            particle.x = (particle.x + int(current_cell.wind_vector[0])) % 800
            particle.y = (particle.y + int(current_cell.wind_vector[1])) % 600