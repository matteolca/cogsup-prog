from expyriment import design, control, stimuli
from time import perf_counter

# Experiment setup
exp = design.Experiment(name="Launching function")

control.set_develop_mode()
control.initialize(exp)

def draw(launcher, target):
    """Present two shapes on the back buffer then flips it.
    The shapes stay on-screen for time t (ms)."""
    launcher.present(clear=True, update=False)
    target.present(clear=False, update=True)

def run_trial(square_length=50, offset=400, delay=0, gap=0, launcher_step=10, target_step_ratio=1):
    """Present a simple launching event with two colored squares.
    Optional arguments can add temporal or spatial gaps, or transform 
    the event into a triggering sequence."""

    size = (square_length, square_length)
    
    launcher = stimuli.Rectangle(size=size, colour=(255, 0, 0))
    launcher.reposition((-offset, 0))
    
    target = stimuli.Rectangle(size=size, colour=(0, 255, 0))
    target_step = int(launcher_step * target_step_ratio)

    draw(launcher, target)
    exp.clock.wait(1000)

    distance_traveled = 0

    # Move left square until collision or spatial gap
    while launcher.distance(target) > square_length + gap:
        launcher.move((launcher_step, 0))
        distance_traveled += launcher_step
        draw(launcher, target)

    exp.clock.wait(delay)

    # Move right square the same distance
    while target.position[0] < distance_traveled:
        target.move((target_step, 0))
        draw(launcher, target)

# Run experiment
control.start(subject_id=1)

# Define 4 trials and inter-trial interval length
trials = [{}, {"delay": 500}, {'gap': 50}, {'target_step_ratio': 2}]
ITI = 500

for trial_params in trials:
    run_trial(**trial_params)
    exp.clock.wait(ITI)

control.end()