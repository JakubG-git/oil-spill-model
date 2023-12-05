from model.cell import Cell
from model.particle import Particle




# get cells that have particles in them

# def get_cells_with_particles(vis: Visualiser) -> list[Cell]:
#     cells_with_particles = []
#     for cell in vis.get_cells():
#         for particle in vis.get_particles():
#             if cell.x <= particle.x <= cell.x + cell.size and cell.y <= particle.y <= cell.y + cell.size:
#                 cells_with_particles.append(cell)
#     return cells_with_particles

def move_particles(vis):
    for particle in vis.get_particles():
        advection(particle, vis)
        # move_with_water(particle, vis)
        vis.update_particle(particle)
    vis.update()


def advection(particle: Particle, vis):
        current_cell = particle.get_current_cell(vis)
        if current_cell and current_cell.wind_vector and current_cell.water_vector and particle.isActive:
            particle.x = (particle.x + int((0.2 * current_cell.wind_vector[0]) + 0.55 * current_cell.water_vector[0])) 
            particle.y = (particle.y + int((0.2 * current_cell.wind_vector[1] + 0.55 * current_cell.water_vector[1]))) 

