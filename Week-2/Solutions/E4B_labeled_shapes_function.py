from expyriment import design, control, stimuli
from expyriment.misc import geometry

""" CONSTANTS """
ARROW_LENGTH = 50
LABEL_OFFSET = ARROW_LENGTH + 20
ARROW_WIDTH = 3
LABEL_GAP = 20
ANTI_ALIASING = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPES = {3: 'triangle', 4: 'square', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon', 10: 'decagon', 12: 'dodecagon'}

def create_labeled_polygon(n, length, position, colour):
    """ Build a regular n-gon, a text label centered at `position`, and a vertical line linking them.
    Returns a tuple: (arrow, polygon, label)."""
    vertices = geometry.vertices_regular_polygon(n, length)
    
    polygon = stimuli.Shape(vertex_list = vertices, position = position, colour = colour, anti_aliasing = ANTI_ALIASING)
    label = SHAPES.get(n, "polygon")

    x, y = polygon.position
    
    text = stimuli.TextLine(label, (x, y + LABEL_OFFSET), text_colour = WHITE, background_colour = BLACK)
    arrow = stimuli.Line(start_point = polygon.position, end_point = text.position, line_width = ARROW_WIDTH, colour = WHITE)

    return (arrow, polygon, text)

def draw(labeled_polygon):
    for stim in labeled_polygon:
        stim.present(clear=False, update=False)

exp = design.Experiment(name="Labeled shapes (function)")

control.set_develop_mode()
control.initialize(exp)

labeled_triangle = create_labeled_polygon(n = 3, length = 50, position = (-100, 0), colour = (128, 0, 128))
labeled_hexagon = create_labeled_polygon(n = 6, length = 25, position = (100, 0), colour = (255, 255, 0))

control.start(subject_id=1)

exp.screen.clear()
for bundle in (labeled_triangle, labeled_hexagon):
    draw(bundle)
exp.screen.update()

exp.keyboard.wait()

control.end()