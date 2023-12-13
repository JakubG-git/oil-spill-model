from model.cell import Cell
from model.particle import Particle
import random as rand
def move_particles(vis):
    for particle in vis.get_particles():
        advection(particle, vis)
        evaporation(particle, vis)

        # do odkomentowania
        # spreading(particle, vis)
        vis.update_particle(particle)
    vis.update()


def advection(particle: Particle, vis):
        current_cell = particle.get_current_cell(vis)
        skalar = 10
        #nie wiem czy mnożenie wiatru przez skalar jest okej bo wtedy mamy zależność wiatru dużo większą od zależności wody
        if current_cell and current_cell.wind_vector and current_cell.water_vector and particle.isActive:
            particle.x = (particle.x + (skalar * 0.03 * current_cell.wind_vector[0]) + skalar * 1.1 * current_cell.water_vector[0])
            particle.y = (particle.y + (skalar * 0.03 * current_cell.wind_vector[1] + skalar * 1.1 * current_cell.water_vector[1]))

def evaporation(particle: Particle, vis):
    current_cell = particle.get_current_cell(vis)
    #evaporate based on water temp and density
    #changes drawing color in visualiser
    if current_cell and current_cell.water_temp and particle.isActive:
        if particle.density <= 0:
            particle.isActive = False
        else:
             particle.density -= 0.0001 * current_cell.water_temp

def spreading(particle: Particle, vis):
    current_cell = particle.get_current_cell(vis)
    #particles have low probability of spreading
    #create new particles by spreading giving it half of its orginal density and append to particles list in visualiser


    if current_cell and current_cell.water_temp and particle.isActive and particle.density > 0:
        if rand.random() < 0.005:
            particle.density /= 2
            vis.particles.append(Particle(particle.x + 1, particle.y + 1, particle.density))
            print(f"spread for {particle}")
        
