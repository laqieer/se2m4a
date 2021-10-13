#!/usr/bin/env python3

import sys
sys.path.append("..")
from se2m4a import *
import matplotlib.pyplot as plt

SNR_all = []
PSNR_all = []

for audio_file in sys.argv[1:]:
    SNR_audio = []
    PSNR_audio = []
    for freq in magic_rates:
        audio_name, audio_ext = os.path.splitext(audio_file)
        audio_freq = audio_name + "-" + str(freq) + audio_ext
        os.system("sox --norm " + audio_file + " -r " + str(freq) + " -b 8 -c 1 " + audio_freq)
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
        PSNR = calculate_PSNR(uncompressed_data, decompressed_data)
        PSNR_audio.append(PSNR)
    SNR_all.append(SNR_audio)
    PSNR_all.append(PSNR_audio)

figure, axis = plt.subplots(1, 2)

axis[0].set_title('SNR-Frequency')
axis[0].set_ylabel('SNR/dB')
axis[0].set_xlabel('freq/Hz')
axis[0].set_xticks(magic_rates)
axis[0].tick_params('x', labelrotation=-30)
for SNR in SNR_all:
    axis[0].plot(magic_rates, SNR)

axis[1].set_title('PSNR-Frequency')
axis[1].set_ylabel('PSNR/dB')
axis[1].set_xlabel('freq/Hz')
axis[1].set_xticks(magic_rates)
axis[1].tick_params('x', labelrotation=-30)
for PSNR in PSNR_all:
    axis[1].plot(magic_rates, PSNR)

plt.tight_layout()
plt.show()
