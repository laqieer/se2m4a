# se2m4a
convert sound effect to assembly source file (.s) for GBA m4a engine

Usage:
`./se2m4a.py input_file(audio) [output_file(.s)] [-c/--compress] [-s/--snr=?]`
-c/--compress enables compression (only supported by Pokemon or [gba-hq-mixer](https://github.com/ipatix/gba-hq-mixer/))
-s/--snr is the min SNR for compression (unit: dB), just keep uncompressed if actual SNR is less than it (only works with -c/--compress)
