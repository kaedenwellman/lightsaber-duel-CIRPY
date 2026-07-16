Lightsaber Duel

A physical lightsaber dueling game that bridges a CircuitPython microcontroller with a browser. The board tracks your real-world motion and drives gameplay on screen in real time.

![Gameplay](gameplay.gif) 

<!-- Drop a screenshot or short GIF at docs/gameplay.gif. A phone clip of a duel in progress works fine. -->
How it works

The project has two halves:


The board. A Microchip Curiosity board (SAME51J20) running CircuitPython 10.1 reads motion from an onboard IMU and streams a directional frame as JSON over USB serial at 10 Hz. Each frame carries the fused swing direction (LEFT / RIGHT / UP / DOWN / NONE), gyro magnitude, accelerometer magnitude, and tilt angle.
The browser. An HTML/JavaScript front end reads that serial stream directly using the Web Serial API and turns your swings and hits into gameplay. The browser also sends HIT / MISS / WIN / LOSE back to the board so the NeoPixels and audio can react.


Swing the board and your saber swings on screen. Hard motion registers as an impact. Touch the cap-touch pad (A5) to ignite the blade with sound and light.

What's in here


code.py — firmware that runs on the board. Reads the IMU and cap touch, drives the NeoPixels and audio, and streams motion data over serial.
Lightsaber_Classic.html — side-by-side dueling view.
Lightsaber_FPV.html — first-person view, with the enemy saber approaching from the vanishing point.
Lightsaber_Combined.html — mode select combining both views.


Requirements


A Microchip Curiosity board with the Ruler baseboard (for the IMU, NeoPixels, LCD, and audio out).
CircuitPython 10.1 flashed to the board.
The Curiosity standard module library on the CIRCUITPY drive: imu_sensor.py, i2c_bus.py, neopixels.py, audio_out.py, lcd_display.py, cap_touch.py. These ship with the board's kit and must sit at the root of CIRCUITPY alongside code.py.
Chrome (or another Chromium-based browser). Web Serial is required, so Safari and Firefox will not work.


Running it
Lightsaber Duel

A physical lightsaber dueling game that bridges a CircuitPython microcontroller with a browser. The board tracks your real-world motion and drives gameplay on screen in real time.

Show Image

<!-- Drop a screenshot or short GIF at docs/gameplay.gif. A phone clip of a duel in progress works fine. -->
How it works

The project has two halves:


The board. A Microchip Curiosity board (SAME51J20) running CircuitPython 10.1 reads motion from an onboard IMU (ICM-20948) and streams a directional frame as JSON over USB serial at 10 Hz. Each frame carries the fused swing direction (LEFT / RIGHT / UP / DOWN / NONE), gyro magnitude, accelerometer magnitude, and tilt angle.
The browser. An HTML/JavaScript front end reads that serial stream directly using the Web Serial API and turns your swings and hits into gameplay. The browser also sends HIT / MISS / WIN / LOSE back to the board so the NeoPixels and audio can react.


Swing the board and your saber swings on screen. Hard motion registers as an impact. Touch the cap-touch pad (A5) to ignite the blade with sound and light.

What's in here


code.py — firmware that runs on the board. Reads the IMU and cap touch, drives the NeoPixels and audio, and streams motion data over serial.
Lightsaber_Classic.html — side-by-side dueling view.
Lightsaber_FPV.html — first-person view, with the enemy saber approaching from the vanishing point.
Lightsaber_Combined.html — mode select combining both views.


Requirements


A Microchip Curiosity board with the Ruler baseboard (for the IMU, NeoPixels, LCD, and audio out).
CircuitPython 10.1 flashed to the board.
The Curiosity standard module library on the CIRCUITPY drive: imu_sensor.py, i2c_bus.py, neopixels.py, audio_out.py, lcd_display.py, cap_touch.py. These ship with the board's kit and must sit at the root of CIRCUITPY alongside code.py.
Chrome (or another Chromium-based browser). Web Serial is required, so Safari and Firefox will not work.


Running it


Copy code.py onto the board's CIRCUITPY drive at the root. It runs on boot. Confirm by opening the serial console — you should see JSON frames scrolling.
Serve the HTML from a local web server. Web Serial refuses to run from file://, so double-clicking the HTML will silently fail. The easiest option is VS Code's Live Server extension; alternatively, from the repo folder run python3 -m http.server and visit http://localhost:8000.
Open one of the HTML files in Chrome.
Click Connect board and select the board's serial port (/dev/tty.usbmodem* on Mac, COMx on Windows).
If you opened Lightsaber_Combined.html, pick a view mode. Otherwise click BEGIN.
Touch the cap-touch pad to ignite the blade, then duel.


Notes

Built at a Microchip DevDay hackathon. The trickiest part was resource management on the board — serial, NeoPixels, and the display all competing, and the board crashing when resources were not released between runs. Motion tuning settled at a gyro swing threshold of 3.0 and an impact threshold of 12.0 (the accelerometer reports in meters per second squared, not g, so gravity alone is ~9.8 and impact needs to clear that with headroom). The enemy AI escalates in speed across the round.

Copy code.py onto the board's CIRCUITPY drive at the root. It runs on boot. Confirm by opening the serial console — you should see JSON frames scrolling.
Serve the HTML from a local web server. Web Serial refuses to run from file://, so double-clicking the HTML will silently fail. The easiest option is VS Code's Live Server extension; alternatively, from the repo folder run python3 -m http.server and visit http://localhost:8000.
Open one of the HTML files in Chrome.
Click Connect board and select the board's serial port (/dev/tty.usbmodem* on Mac, COMx on Windows).
If you opened Lightsaber_Combined.html, pick a view mode. Otherwise click BEGIN.
Touch the cap-touch pad to ignite the blade, then duel.


Notes

Built at a Microchip DevDay hackathon. The trickiest part was resource management on the board — serial, NeoPixels, and the display all competing, and the board crashing when resources were not released between runs. Motion tuning settled at a gyro swing threshold of 3.0 and an impact threshold of 12.0 (the accelerometer reports in meters per second squared, not g, so gravity alone is ~9.8 and impact needs to clear that with headroom). The enemy AI escalates in speed across the round.
