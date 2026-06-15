"""
Lightsaber Duel - CircuitPython Board Code
==========================================
Streams fused IMU direction over USB serial as JSON at ~10 Hz.
Listens for block results back from the browser to trigger feedback.
"""

import time
import math
import board
import supervisor
import json

from imu_sensor import IMUSensor
from i2c_bus import I2CBus
from neopixels import NeoPixels
from audio_out import AudioOutput
from lcd_display import LCDDisplay

# ── Hardware init ─────────────────────────────────────────────────────────────
i2c   = I2CBus()
imu   = IMUSensor(i2c.bus)
neo   = NeoPixels()
audio = AudioOutput()
lcd   = LCDDisplay()

# ── Constants ─────────────────────────────────────────────────────────────────
LOOP_HZ     = 10
LOOP_PERIOD = 1.0 / LOOP_HZ

GYRO_SWING  = 1.8
GYRO_STRONG = 3.5
ACCEL_IMPACT = 8.0
TILT_THRESH = 20
DIR_HOLD = 2

# ── State ─────────────────────────────────────────────────────────────────────
direction      = "NONE"
dir_hold_count = 0

grav_x = 0.0
grav_y = 0.0
grav_z = 9.8
GRAV_ALPHA = 0.95

# ── Colour palette ────────────────────────────────────────────────────────────
BLUE_IDLE   = (0, 60, 200)
CLASH_WHITE = (255, 255, 255)
HIT_GREEN   = (0, 220, 80)
MISS_RED    = (220, 0, 0)
NEO_OFF     = (0, 0, 0)

# ── Helpers ───────────────────────────────────────────────────────────────────
def mag(x, y, z):
    return math.sqrt(x*x + y*y + z*z)

def roll_deg(ax, ay, az):
    return math.degrees(math.atan2(ay, az))

def pitch_deg(ax, ay, az):
    return math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

def fuse_direction(ax, ay, az, gx, gy, gz, dax, day, daz):
    gx_m    = abs(gx)
    gy_m    = abs(gy)
    gz_m    = abs(gz)
    g_total = mag(gx, gy, gz)

    if g_total >= GYRO_SWING:
        if gz_m >= gx_m and gz_m >= gy_m:
            return "LEFT" if gz > 0 else "RIGHT"
        elif gx_m >= gy_m:
            return "UP" if gx > 0 else "DOWN"
        else:
            return "LEFT" if gy > 0 else "RIGHT"

    da_total = mag(dax, day, daz)
    if da_total >= ACCEL_IMPACT:
        if abs(daz) >= abs(dax) and abs(daz) >= abs(day):
            return "LEFT" if daz > 0 else "RIGHT"
        elif abs(dax) >= abs(day):
            return "UP" if dax > 0 else "DOWN"
        else:
            return "LEFT" if day > 0 else "RIGHT"

    roll  = roll_deg(ax, ay, az)
    pitch = pitch_deg(ax, ay, az)
    if abs(roll) >= abs(pitch):
        if roll > TILT_THRESH:
            return "LEFT"
        elif roll < -TILT_THRESH:
            return "RIGHT"
    else:
        if pitch > TILT_THRESH:
            return "UP"
        elif pitch < -TILT_THRESH:
            return "DOWN"

    return "NONE"

# ── Feedback handlers ─────────────────────────────────────────────────────────
def on_hit():
    neo.fill(CLASH_WHITE)
    audio.play_tone(880, volume=0.2, duration=0.05)
    neo.fill(HIT_GREEN)
    time.sleep(0.1)
    neo.fill(BLUE_IDLE)

def on_miss():
    neo.fill(MISS_RED)
    audio.play_tone(200, volume=0.2, duration=0.05)
    time.sleep(0.1)
    neo.fill(BLUE_IDLE) 

def on_win():
    neo.rainbow_cycle(wait=0.005, cycles=2)
    audio.play_tone(523, volume=0.15, duration=0.1)
    audio.play_tone(659, volume=0.15, duration=0.1)
    audio.play_tone(784, volume=0.15, duration=0.2)
    grp, _ = lcd.make_group(0x002200)
    lcd.add_label(grp, "VICTORY", 120, 52, color=0x00FF44, scale=3)
    time.sleep(2.0)
    neo.fill(BLUE_IDLE)

def on_lose():
    for _ in range(3):
        neo.fill(MISS_RED)
        time.sleep(0.15)
        neo.fill(NEO_OFF)
        time.sleep(0.1)
    grp, _ = lcd.make_group(0x330000)
    lcd.add_label(grp, "DEFEATED", 120, 56, color=0xFF0000, scale=2)
    time.sleep(2.0)
    neo.fill(BLUE_IDLE)

# ── Startup ───────────────────────────────────────────────────────────────────
lcd.backlight_on()
grp, _ = lcd.make_group(0x000022)
lcd.add_label(grp, "DUEL", 120, 50, color=0x4488FF, scale=4)
neo.fill(BLUE_IDLE)

# ── Main loop ─────────────────────────────────────────────────────────────────
print("READY")

while True:
    try:
        t0 = time.monotonic()

        ax, ay, az = imu.acceleration
        gx, gy, gz = imu.gyro

        grav_x = GRAV_ALPHA * grav_x + (1 - GRAV_ALPHA) * ax
        grav_y = GRAV_ALPHA * grav_y + (1 - GRAV_ALPHA) * ay
        grav_z = GRAV_ALPHA * grav_z + (1 - GRAV_ALPHA) * az

        dax = ax - grav_x
        day = ay - grav_y
        daz = az - grav_z

        new_dir = fuse_direction(ax, ay, az, gx, gy, gz, dax, day, daz)

        if new_dir != "NONE":
            direction      = new_dir
            dir_hold_count = DIR_HOLD
        elif dir_hold_count > 0:
            dir_hold_count -= 1
        else:
            direction = "NONE"

        g_total = mag(gx, gy, gz)

        tilt_angle = roll_deg(ax, ay, az)
        frame = {
            "d": direction,
            "g": round(g_total, 2),
            "a": round(mag(dax, day, daz), 2),
            "t": round(tilt_angle, 1)
        }
        print(json.dumps(frame))

       
        elapsed = time.monotonic() - t0
        if elapsed < LOOP_PERIOD:
            time.sleep(LOOP_PERIOD - elapsed)

    except Exception as e:
        print("ERR:" + str(e))
        time.sleep(0.5)