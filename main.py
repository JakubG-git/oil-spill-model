from view.visualiser import Visualizer

width = 800
height = 600
map_ = "images/map.png"

visualizer = Visualizer()
visualizer.initialize(map_, width, height)
visualizer.session()
