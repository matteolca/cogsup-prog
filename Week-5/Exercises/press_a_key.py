#Find the circle, present a circle and a square, right key is correct, left key is incorrect, present feedback
#import the keys, K_RIGHT, K_LEFT
#build all the stimuli, circle =, square =, correct =, incorrect =
#present instructions, stimulus, key, compute present feedback

from expyriment import design, control, stimuli
from expyriment.misc.constants import K_RIGHT, K_LEFT

# ── Experiment setup ──────────────────────────────────────────────────────────
exp = design.Experiment(name="Find the circle")
exp.add_data_variable_names(["response_key", "correct", "rt"])

control.set_develop_mode()
control.initialize(exp)

# ── Build stimuli ─────────────────────────────────────────────────────────────
instructions = stimuli.TextLine("Find the circle — press RIGHT if you see it, LEFT if not")

circle   = stimuli.Circle(radius=50, colour=(255, 255, 255))
square   = stimuli.Rectangle(size=(100, 100), colour=(255, 255, 255))

correct_fb   = stimuli.TextLine("Correct!", text_colour=(0, 220, 80))
incorrect_fb = stimuli.TextLine("Incorrect!", text_colour=(220, 60, 60))

# Pre-load everything to avoid runtime delays
for s in (circle, square, correct_fb, incorrect_fb):
    s.preload()

# ── Block / trial structure ───────────────────────────────────────────────────
block = design.Block(name="main")

# Trial 1 — circle present → correct answer is RIGHT
t1 = design.Trial()
t1.set_factor("stimulus", "circle")
t1.add_stimulus(circle)
block.add_trial(t1)

# Trial 2 — square present → correct answer is LEFT
t2 = design.Trial()
t2.set_factor("stimulus", "square")
t2.add_stimulus(square)
block.add_trial(t2)

block.shuffle_trials()
exp.add_block(block)

# ── Run ───────────────────────────────────────────────────────────────────────
control.start(skip_ready_screen=False)

# Instructions
instructions.present()
exp.keyboard.wait([K_RIGHT, K_LEFT])

for trial in exp.blocks[0].trials:
    stim_name = trial.get_factor("stimulus")

    # Present stimulus
    trial.stimuli[0].present()

    # Wait for response
    key, rt = exp.keyboard.wait([K_RIGHT, K_LEFT])

    # Determine correctness
    # Circle is on the RIGHT, so RIGHT = correct when stimulus is circle
    if stim_name == "circle":
        is_correct = (key == K_RIGHT)
    else:                          # square
        is_correct = (key == K_LEFT)

    # Present feedback
    if is_correct:
        correct_fb.present()
    else:
        incorrect_fb.present()
    exp.clock.wait(1000)

    # Save data
    exp.data.add([key, int(is_correct), rt])

control.end()