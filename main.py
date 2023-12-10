from view.visualiser import Visualizer

width = 840
height = 720
map_ = "images/mapa840x720.png"

visualizer = Visualizer()
visualizer.initialize(map_, width, height)
visualizer.session()
