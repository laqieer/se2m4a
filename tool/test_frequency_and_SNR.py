#!/usr/bin/env python3

import os
import sys
import wave
import aifc
sys.path.append("..")
from se2m4a import *
import matplotlib.pyplot as plt

SNR_all = {}

for audio_file in sys.argv[1:]:
    SNR_audio = []
    for freq in magic_rates:
        audio_name, audio_ext = os.path.splitext(audio_file)
        audio_freq = audio_name + "-" + str(freq) + audio_ext
        os.system("sox -G -v 0.92 " + audio_file + " -r " + str(freq) + " -b 8 -c 1 " + audio_freq)
        if audio_ext in ('.wav', '.WAV'):
            audio_module = wave
        else:
            audio_module = aifc
        with audio_module.open(audio_freq, 'rb') as audio:
            frames = audio.getnframes()
            raw = audio.readframes(frames)
        if audio_module == wave:
            uncompressed_data = (np.frombuffer(raw, dtype = np.ubyte) - 0x80).astype(np.byte)
        else:
            uncompressed_data = np.frombuffer(raw, dtype = np.byte)
        compressed_data, decompressed_data = compress(uncompressed_data)
        SNR = calculate_SNR(uncompressed_data, decompressed_data)
        SNR_audio.append(SNR)
    SNR_all[os.path.split(audio_file)[-1]] = SNR_audio

plt.title('SNR-Frequency')
plt.xlabel('freq/Hz')
plt.ylabel('SNR/dB')
plt.xticks(magic_rates)
plt.xticks(rotation=-30)
for audio, SNR in SNR_all.items():
    plt.plot(magic_rates, SNR, label = audio)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()
