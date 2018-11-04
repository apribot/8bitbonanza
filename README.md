# 8bitbonanza
musical experiment

A lightweight, dirty 8bit 'VCO'. Intended to work with SamplerBox on the Raspberry Pi.

weird algorithms create gross waveforms based on a counter in a loop.

plëäsë may i hävë thë sämplë lööps?

# pre-post-mortem
a harrowing example of what a lack of planning does to a project
originally allocated a minumum of effort, which obviously ended up being a effort exponent
roadmap:
 - python version, gave up due to wackiness with audio/midi support
 - lua version, gave up because midi support was even worse
 - cpp, but breifly. gave up because i forgot that c++ is substantially easier than C
 - back to lua? for no reason?
 - gave up on making a stand-alone, changed goal to creating a wave generator for SamplerBox because SB already has great midi/audio support on the raspi
 - back to python, got 99% of the way done but ran into weird issue with pydub mangling waveforms at low frequency conversions. thought about patching pydub, decided not to because other people's code is suffering.
 - back to c++, got really far with this, wonderful stuff. realized i'd need to create an expression evaluator from nealy scratch to get the functionality i wanted, gave up.
 - back to python, basically ported what i did in C++ to python and did the entire WAV/RIFF creation from scratch
 - [future state?]