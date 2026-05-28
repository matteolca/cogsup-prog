from expyriment import design, control, stimuli, misc
import expyriment
import random

exp = design.Experiment(name="Deterministic vs Stochastic")
control.set_develop_mode()
control.initialize(exp)



STIMSIZE = 100
GREY = misc.constants.C_GREY
OFFSET = 300
N_TRIALS = 10
VALID_KEYS = [expyriment.misc.constants.K_RIGHT, expyriment.misc.constants.K_LEFT]

def make_stimuli(circle_side):
    if circle_side == "right":
        circle = stimuli.Circle(radius=STIMSIZE//2, colour=GREY, position=(OFFSET, 0))
        square = stimuli.Rectangle(size=(STIMSIZE, STIMSIZE), colour=GREY, position=(-OFFSET, 0))
    else:
        circle = stimuli.Circle(radius=STIMSIZE//2, colour=GREY, position=(-OFFSET, 0))
        square = stimuli.Rectangle(size=(STIMSIZE, STIMSIZE), colour=GREY, position=(OFFSET, 0))
    return circle, square

def pseudorandomize(n, max_run=3):
    sequence = ["left"] * (n // 2) + ["right"] * (n // 2)
    while True:
        random.shuffle(sequence)
        runs = [sum(1 for _ in g) for _, g in __import__("itertools").groupby(sequence)]
        if max(runs) <= max_run:
            return sequence

deterministic_sequence = ["right"] * N_TRIALS
stochastic_sequence = pseudorandomize(N_TRIALS)

for condition, sequence in [("deterministic", deterministic_sequence), ("stochastic", stochastic_sequence)]:
    block = design.Block(name=condition)
    for side in sequence:
        circle, square = make_stimuli(side)
        circle.preload()
        square.preload()
        trial = design.Trial()
        trial.set_factor("condition", condition)
        trial.set_factor("circle_side", side)
        trial.add_stimulus(circle)
        trial.add_stimulus(square)
        block.add_trial(trial)
    exp.add_block(block)

exp.data_variable_names = ["condition", "circle_side", "key", "rt"]

control.start(subject_id=1)

instruction = stimuli.TextScreen("Instructions",
    "A circle and a square will appear on screen.\n"
    "Press the arrow key on the side where the circle appears.\n\n"
    "Press any key to begin.")
instruction.present()
exp.keyboard.wait()

for block in exp.blocks:
    for trial in block.trials:
        trial.stimuli[0].present(clear=True, update=False)
        trial.stimuli[1].present(clear=False, update=True)
        key, rt = exp.keyboard.wait(VALID_KEYS)
        exp.data.add([trial.get_factor("condition"), trial.get_factor("circle_side"), key, rt])

control.end()