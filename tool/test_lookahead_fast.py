#!/usr/bin/env python3

import sys
import time
sys.path.append("..")
from se2m4a import *
import matplotlib.pyplot as plt

lookaheads = range(1, 8)

audio_file = sys.argv[1]
os.system("soxi " + audio_file)
SNR_audio = []
PSNR_audio = []
time_audio = []
SNR_F_audio = []
PSNR_F_audio = []
time_F_audio = []
_, audio_ext = os.path.splitext(audio_file)
if audio_ext in ('.wav', '.WAV'):
    audio_module = wave
else:
    audio_module = aifc
with audio_module.open(audio_file, 'rb') as audio:
    frames = audio.getnframes()
    raw = audio.readframes(frames)
if audio_module == wave:
    uncompressed_data = (np.frombuffer(raw, dtype = np.ubyte) - 0x80).astype(np.byte)
else:
    uncompressed_data = np.frombuffer(raw, dtype = np.byte)
if frames % blk_size > 0:
    uncompressed_data = np.append(uncompressed_data, [0] * (blk_size - frames % blk_size))
for lookahead in lookaheads:
    for lookahead_fast in (False, True):
        start = time.time()
        compressed_data, decompressed_data = compress(uncompressed_data, lookahead, lookahead_fast)
        end = time.time()
        SNR = calculate_SNR(uncompressed_data, decompressed_data)
        PSNR = calculate_PSNR(uncompressed_data, decompressed_data)
        t = end - start
        if lookahead_fast:
            fast = '(fast)'
            SNR_F_audio.append(SNR)
            PSNR_F_audio.append(PSNR)
            time_F_audio.append(t)
        else:
            fast = ''
            SNR_audio.append(SNR)
            PSNR_audio.append(PSNR)
            time_audio.append(t)
        print("lookahead=%d%s: SNR: %.2fdB PSNR: %.2fdB Time:%.2fs" % (lookahead, fast, SNR, PSNR, t))

figure, axis = plt.subplots(1, 3)

axis[0].set_title('SNR-Lookahead')
axis[0].set_xlabel('lookahead')
axis[0].set_ylabel('SNR/dB')
axis[0].set_xticks(lookaheads)
axis[0].plot(lookaheads, SNR_audio, label='lookahead')
axis[0].plot(lookaheads, SNR_F_audio, label='lookahead-fast')

axis[1].set_title('PSNR-Lookahead')
axis[1].set_xlabel('lookahead')
axis[1].set_ylabel('PSNR/dB')
axis[1].set_xticks(lookaheads)
axis[1].plot(lookaheads, PSNR_audio, label='lookahead')
axis[1].plot(lookaheads, PSNR_F_audio, label='lookahead-fast')

axis[2].set_title('Time-Lookahead')
axis[2].set_xlabel('lookahead')
axis[2].set_ylabel('compression time/s')
axis[2].set_xticks(lookaheads)
axis[2].plot(lookaheads, time_audio, label='lookahead')
axis[2].plot(lookaheads, time_F_audio, label='lookahead-fast')

plt.tight_layout()
plt.show()
