#!/usr/bin/env python3

from PyQt4 import QtCore

class BaseState(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)
    
    def __init__(self, *args, linkbot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.linkbot = linkbot

    def enter(self):
        pass

    def exit(self):
        pass

    def success(self):
        self.finished.emit()

class TestLedRed(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_led_color(255, 0, 0)

class TestLedGreen(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_led_color(0, 255, 0)

class TestLedBlue(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_led_color(0, 0, 255)

class TestButtonPower(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.enable_button_events(self.callback)

    def exit(self):
        self.linkbot.disable_button_events()

    def callback(self, buttonNo, event, timestamp):
        if buttonNo == 0:
            self.success()

class TestButtonA(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.enable_button_events(self.callback)

    def exit(self):
        self.linkbot.disable_button_events()

    def callback(self, buttonNo, event, timestamp):
        if buttonNo == 1:
            self.success()

class TestButtonB(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.enable_button_events(self.callback)

    def exit(self):
        self.linkbot.disable_button_events()

    def callback(self, buttonNo, event, timestamp):
        if buttonNo == 2:
            self.success()

class TestAccel(BaseState):
    x_changed = QtCore.pyqtSignal(int)
    y_changed = QtCore.pyqtSignal(int)
    z_changed = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.enable_accelerometer_events(self.callback)

    def exit(self):
        self.linkbot.disable_accelerometer_events()

    def callback(self, x, y, z, timestamp):
        self.x_changed.emit(x*20)
        self.y_changed.emit(y*20)
        self.z_changed.emit(z*20)

class TestMotorCcw(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_motor_powers(128, 128, 128)

    def exit(self):
        self.linkbot.stop()

class TestMotorCw(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_motor_powers(-128, -128, -128)

    def exit(self):
        self.linkbot.stop()

class TestBeep(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter(self):
        self.linkbot.set_buzzer_frequency(440)
        QtCore.QTimer.singleShot(500, self.timeout)

    def timeout(self):
        self.linkbot.set_buzzer_frequency(0)

class PreassemblyTest():
    def __init__(self, linkbot):
        self.linkbot = linkbot

    def next(self):
        pass

    def reset(self):
        pass

    def test_led_red(self):
        self.linkbot.set_led_color(255, 0, 0)

    def test_led_red_end(self):
        pass

    def test_led_green(self):
        self.linkbot.set_led_color(0, 255, 0)

    def test_led_green_end(self):
        pass

    def test_led_blue(self):
        self.linkbot.set_led_color(0, 0, 255)

    def test_led_blue_end(self):
        pass

    

