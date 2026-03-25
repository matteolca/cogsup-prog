from expyriment import design, control, stimuli

exp = design.Experiment(name="Two squares")

control.set_develop_mode()
control.initialize(exp)

offset = 200

left_square = stimuli.Rectangle(size=(50, 50), colour=(255, 0, 0), position=(-offset//2, 0))
right_square = stimuli.Rectangle(size=(50, 50), colour=(0, 255, 0), position=(offset//2, 0))

control.start(subject_id=1)

left_square.present(clear=True, update=False)
right_square.present(clear=False, update=True)
exp.keyboard.wait()

control.end()