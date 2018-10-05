# 8bitbonanza
musical experiment

A lightweight, dirty 8bit 'VCO' for the Raspberry Pi.

weird algorithms create u8int waveforms based on a 't' counter in a loop.

TODO:
- add layering option to cli args
- midi-over-usb support
- if i get really weird, maybe ADSR... maybe a bad low-pass filter
- low notes take ages to generate because i'm literally doing it in the worst way possible
- soften loop transition clicks
- replace linearInterpolate with something that sounds less awful?