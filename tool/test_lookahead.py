#!/usr/bin/env python3

import sys
import time
sys.path.append("..")
from se2m4a import *
import matplotlib.pyplot as plt

lookaheads = range(0, 5)
SNR_all = []
PSNR_all = []
time_all = []

for audio_file in sys.argv[1:]:
    print(audio_file)
    SNR_audio = []
    PSNR_audio = []
    time_audio = []
    audio_name, audio_ext = os.path.splitext(audio_file)
    audio_freq = audio_name + "-10512" + audio_ext
    os.system("sox --norm " + audio_file + " -r 10512 -b 8 -c 1 " + audio_freq)
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
    if frames % blk_size > 0:
        uncompressed_data = np.append(uncompressed_data, [0] * (blk_size - frames % blk_size))
    for lookahead in lookaheads:
        start = time.time()
        compressed_data, decompressed_data = compress(uncompressed_data, lookahead)
        end = time.time()
        SNR = calculate_SNR(uncompressed_data, decompressed_data)
        SNR_audio.append(SNR)
        PSNR = calculate_PSNR(uncompressed_data, decompressed_data)
        PSNR_audio.append(PSNR)
        t = end - start
        time_audio.append(t)
        print("lookahead=%d: SNR: %.2fdB PSNR: %.2fdB Time:%.2fs" % (lookahead, SNR, PSNR, t))
    SNR_all.append(SNR_audio)
    PSNR_all.append(PSNR_audio)
    time_all.append(time_audio)

figure, axis = plt.subplots(1, 3)

axis[0].set_title('SNR-Lookahead')
axis[0].set_xlabel('lookahead')
axis[0].set_ylabel('SNR/dB')
axis[0].set_xticks(lookaheads)
for SNR in SNR_all:
    axis[0].plot(lookaheads, SNR)

axis[1].set_title('PSNR-Lookahead')
axis[1].set_xlabel('lookahead')
axis[1].set_ylabel('PSNR/dB')
axis[1].set_xticks(lookaheads)
for PSNR in PSNR_all:
    axis[1].plot(lookaheads, PSNR)

axis[2].set_title('Time-Lookahead')
axis[2].set_xlabel('lookahead')
axis[2].set_ylabel('compression time/s')
axis[2].set_xticks(lookaheads)
for time in time_all:
    axis[2].plot(lookaheads, time)

plt.tight_layout()
plt.show()
