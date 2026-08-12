#!/usr/bin/env python3
"""Synthesized sound design for the blue-sphere shot.

Reads the timeline markers printed by capture.cjs and renders a 48 kHz stereo
WAV keyed to them: charge riser -> pregnant-pause near-silence -> launch boom
-> chase wind -> time-dilation pitch drop -> slo-mo rumble with spark tinkles
-> snap-back shatter impact -> decaying tail.

Usage: python3 sound.py <duration_s> <tLaunch> <tDil> <tContact> <tSnap> <out.wav>
"""
import sys
import numpy as np
import wave

DUR = float(sys.argv[1])
T_LAUNCH = float(sys.argv[2])
T_DIL = float(sys.argv[3])
T_CONTACT = float(sys.argv[4])
T_SNAP = float(sys.argv[5])
OUT = sys.argv[6]

SR = 48000
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(1337)

T_CHARGE0, T_PAUSE0 = 2.0, 5.2

def env_between(t0, t1, atk=0.05, rel=0.05):
    """Trapezoid envelope between t0 and t1."""
    e = np.clip((t - t0) / max(atk, 1e-6), 0, 1) * np.clip((t1 - t) / max(rel, 1e-6), 0, 1)
    return np.clip(e, 0, 1)

from scipy.signal import lfilter

def lowpass(x, cutoff_hz):
    """One-pole lowpass. Accepts a scalar or per-sample cutoff array."""
    if np.isscalar(cutoff_hz):
        a = np.exp(-2 * np.pi * cutoff_hz / SR)
        return lfilter([1 - a], [1, -a], x)
    # time-varying cutoff: process in blocks with the block's mean cutoff
    y = np.empty_like(x)
    zi = np.zeros(1)
    B = 4096
    for s in range(0, len(x), B):
        e = min(s + B, len(x))
        a = np.exp(-2 * np.pi * float(np.mean(cutoff_hz[s:e])) / SR)
        y[s:e], zi = lfilter([1 - a], [1, -a], x[s:e], zi=zi)
    return y

def fade_out(x, sec=0.6):
    n = int(sec * SR)
    if n < len(x):
        x[-n:] *= np.linspace(1, 0, n)
    return x

mix = np.zeros(N)

# ---------------- charge riser (2.0 -> pause) ----------------
p = np.clip((t - T_CHARGE0) / (T_PAUSE0 - T_CHARGE0), 0, 1)
riser_f = 55 * (220 / 55) ** p                       # 55 -> 220 Hz sweep
phase = np.cumsum(2 * np.pi * riser_f / SR)
vib = 0.4 * np.sin(2 * np.pi * 5.5 * t)
riser = np.sin(phase + vib) + 0.45 * np.sin(2 * phase) + 0.2 * np.sin(3 * phase)
riser *= env_between(T_CHARGE0, T_PAUSE0, atk=1.6, rel=0.25) * (0.10 + 0.34 * p ** 1.6)
mix += riser

# shimmering noise sweeping upward
nz = rng.standard_normal(N)
shimmer = nz - lowpass(nz, 320 + 2500 * p)           # highpassed noise, rising floor
shimmer = lowpass(shimmer, 6000)
mix += shimmer * env_between(T_CHARGE0 + 0.4, T_PAUSE0, atk=2.0, rel=0.3) * 0.05 * p

# accelerating heartbeat thumps
beat_f = 1.4 + 5.2 * p ** 2
beat_phase = np.cumsum(beat_f / SR)
tick = (beat_phase % 1.0) < 0.012
thump_src = np.zeros(N); thump_src[tick] = 1.0
thump = lowpass(thump_src, 70) * 260
mix += thump * env_between(T_CHARGE0 + 0.3, T_PAUSE0, atk=1.0, rel=0.2) * (0.4 + 0.6 * p)

# ---------------- pregnant pause: near-silence with a thin air tone ----------------
air = np.sin(2 * np.pi * 1150 * t) * 0.012 + np.sin(2 * np.pi * 1730 * t) * 0.006
mix += air * env_between(T_PAUSE0, T_LAUNCH, atk=0.35, rel=0.08)
# sub drop-out swell right before launch
mix += np.sin(2 * np.pi * 38 * t) * env_between(T_LAUNCH - 0.28, T_LAUNCH, atk=0.26, rel=0.02) * 0.30

# ---------------- launch: boom + whoosh ----------------
li = int(T_LAUNCH * SR)
boom_t = np.clip(t - T_LAUNCH, 0, None)
boom = np.sin(2 * np.pi * (58 * np.exp(-boom_t * 2.2) + 30) * boom_t) * np.exp(-boom_t * 5.5)
boom[t < T_LAUNCH] = 0
mix += boom * 0.9
crack_n = int(0.05 * SR)
if li + crack_n < N:
    mix[li:li + crack_n] += rng.standard_normal(crack_n) * np.linspace(0.8, 0, crack_n)

# chase wind: filtered noise, doppler-ish falling tone, ends at contact
wind_env = env_between(T_LAUNCH + 0.05, T_CONTACT, atk=0.4, rel=max(0.35, T_CONTACT - T_DIL))
wind = lowpass(rng.standard_normal(N), 900) * wind_env * 0.34
wind += lowpass(rng.standard_normal(N), 240) * wind_env * 0.30
mix += wind
whoosh_f = 480 * np.exp(-np.clip(t - T_LAUNCH, 0, None) * 1.1) + 60
whoosh = np.sin(np.cumsum(2 * np.pi * whoosh_f / SR)) * env_between(T_LAUNCH, T_LAUNCH + 1.2, atk=0.05, rel=0.8) * 0.16
mix += whoosh

# ---------------- time dilation: everything pitches down into rumble ----------------
dil_p = np.clip((t - T_DIL) / 0.5, 0, 1)
drop_f = 400 * (1 - dil_p) ** 2 + 34
drop = np.sin(np.cumsum(2 * np.pi * drop_f / SR)) * env_between(T_DIL, T_DIL + 0.9, atk=0.06, rel=0.5) * 0.30
mix += drop

# slo-mo bed: deep rumble + slow heartbeat + spark tinkles
rumble = lowpass(rng.standard_normal(N), 46) * env_between(T_DIL + 0.3, T_SNAP + 0.1, atk=0.7, rel=0.15) * 1.15
mix += rumble
slow_beat = (np.cumsum(np.full(N, 0.62) / SR) % 1.0) < 0.014
sb = np.zeros(N); sb[slow_beat] = 1.0
sb = lowpass(sb, 52) * 300
mix += sb * env_between(T_DIL + 0.5, T_SNAP, atk=0.5, rel=0.3) * 0.5
# glassy contact chime at first touch
chime_t = np.clip(t - T_CONTACT, 0, None)
for f0, amp in [(2100, 0.10), (3170, 0.07), (4400, 0.05)]:
    mix += np.sin(2 * np.pi * f0 * chime_t) * np.exp(-chime_t * 2.6) * amp * (t >= T_CONTACT)
# sparse spark tinkles hanging in slo-mo
tink_times = T_CONTACT + rng.random(26) * max(T_SNAP - T_CONTACT, 0.5)
for tt_ in tink_times:
    f0 = 1500 + rng.random() * 4800
    dt_ = np.clip(t - tt_, 0, None)
    mix += np.sin(2 * np.pi * f0 * dt_) * np.exp(-dt_ * 9) * 0.02 * (t >= tt_)

# ---------------- snap-back shatter ----------------
si = int(T_SNAP * SR)
sn_t = np.clip(t - T_SNAP, 0, None)
sub = np.sin(2 * np.pi * (46 * np.exp(-sn_t * 1.6) + 24) * sn_t) * np.exp(-sn_t * 2.6)
sub[t < T_SNAP] = 0
mix += sub * 1.5
crash_n = int(1.1 * SR)
if si < N:
    seg = min(crash_n, N - si)
    crash = rng.standard_normal(seg) * np.exp(-np.linspace(0, 6.5, seg))
    mix[si:si + seg] += lowpass(crash, 3400) * 1.0
# glass shatter: dozens of short decaying pings
ping_times = T_SNAP + rng.random(42) * 0.55
for tt_ in ping_times:
    f0 = 1400 + rng.random() * 5200
    dt_ = np.clip(t - tt_, 0, None)
    mix += np.sin(2 * np.pi * f0 * dt_) * np.exp(-dt_ * (14 + rng.random() * 18)) * 0.05 * (t >= tt_)
# debris tail rumble
mix += lowpass(rng.standard_normal(N), 90) * env_between(T_SNAP + 0.2, DUR - 0.5, atk=0.3, rel=1.2) * 0.22

# ---------------- master ----------------
mix = np.tanh(mix * 1.1) * 0.9
mix = fade_out(mix, 0.9)
# gentle stereo: slight haas offset + width from a filtered copy
off = int(0.00045 * SR)
left = mix
right = np.roll(mix, off)
right[:off] = 0
stereo = np.stack([left, right], axis=1)
peak = np.max(np.abs(stereo)) or 1
stereo = stereo / peak * 0.89

data = (stereo * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print('wrote', OUT, f'{DUR:.2f}s')
