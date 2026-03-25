from expyriment import design, control, stimuli
from expyriment.design.randomize import rand_int
from math import cos, sin, radians

def draw(launcher, target):
    """Draws two shapes on the back buffer then flips it"""
    launcher.present(clear=True, update=False)
    target.present(clear=False, update=True)

def overlap(launcher, target):
    """Returns True iff the two stimuli overlap."""
    is_overlap, _ = launcher.overlapping_with_stimulus(target, mode='visible')
    return is_overlap

# Experiment setup
exp = design.Experiment(name="Launching varying axis of motion")

control.set_develop_mode()
control.initialize(exp)

def run_trial(square_length = 50, r = 300, step = 10, angle = None):
    """Display a launching event at speed `step` for squares of 
    length `square_length` (pixels), with the target initially at distance
    `r` along `angle` (deg). If angle is None, it is randomly selected from [0, 359]"""
    # Geometric coordinates
    theta = radians(rand_int(0, 359)) if angle is None else radians(angle)
    dx, dy = cos(theta), sin(theta)
    size = (square_length, square_length)

    # Create stimuli
    launcher = stimuli.Rectangle(size=size, colour=(0, 255, 0))
    target = stimuli.Rectangle(size=size, colour=(255, 0, 0))

    # Position target on a circle of radius r
    target.reposition((r * cos(theta), r * sin(theta)))

    # Display shapes for 0.5 seconds
    draw(launcher, target)
    exp.clock.wait(500)

    # Keep track of the distance traveled by the launcher
    num_steps = 0
    max_iters = 10000

    for frame in range(1, max_iters):
        launcher.move((dx, dy))
        collided = overlap(launcher, target)

        # Draw every step frames OR if pre-overlap moment was not already drawn
        must_draw = (frame % step == 0) or (collided and frame % step != 1)

        if collided:
            launcher.move((-dx, -dy))  # Backtrack to avoid shape overlap

        if must_draw:
            draw(launcher, target)
            num_steps += 1

        if collided:
            break
    
    for _ in range(num_steps):
        target.move((step * dx, step * dy))
        draw(launcher, target)

# Run experiment
control.start(subject_id=1)

for _ in range(3):
    run_trial()

control.end()