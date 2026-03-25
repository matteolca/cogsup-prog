from expyriment import design, control, stimuli

exp = design.Experiment(name="Square")

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
square = stimuli.Rectangle(size=(50, 50), colour=(0, 0, 255))

control.start(subject_id=1)

square.present(clear=True, update=False)
fixation.present(clear=False, update=True)

exp.clock.wait(500)
square.present(clear=True, update=True)

exp.keyboard.wait()
control.end()