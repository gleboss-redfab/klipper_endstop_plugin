# A Klipper plugin and macros for controling endstops on 3D printer.
The original system is not able to process endstop sensors as separate objects, like [extruder] or [fan]. But sometimes this option is necessary in complex mechanisms, for example, the toolchanger mechanism. Of course you can use [gcode_button] for some critical moments, but this klipper object don't allow use endstop state inside а custom macros. And with my extra module now you can :)


# Instalation
- *Connect via ssh*
```
cd ~
git clone https://github.com/RedFabLab/klipper_endstop_plugin
cp ./klipper_endstop_plugin/endstop_custom.py ./klipper/klippy/extras
```
Check instalation:
```
ls ./klipper/klippy/extras/endstop_custom.py
```
You shoud get answer: ```/klipper/klippy/extras/endstop_custom.py```

Restart Klipper:
```
sudo systemctl restart klipper.service
```

# Configure
```
[endstop_custom endstop_1]
pin: P1.25
```

# Usage
Run from Fluidd or Mainsail console and get answer.
```
QUERY_ENDSTOP ENDSTOP=endstop_1
```

Inside macros you can read endstop state like state of printer's object
```
# read direct from .state
    {% if printer["endstop_custom endstop_1"].state %}
```

For more details and examples check ./config/endstop_example.cfg
[here](https://github.com/RedFabLab/klipper_endstop_plugin/blob/6ce40fd9e7ad932d8cf3e6bfb37e3c95fd099d01/config/endstop_example.cfg)
