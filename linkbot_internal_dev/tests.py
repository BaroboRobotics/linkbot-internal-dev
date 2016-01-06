
from PyQt4 import QtCore, QtGui
import time
import linkbot
import traceback
import threading

class LinkbotTest(QtGui.QWidget):
    completed = QtCore.pyqtSignal()
    failure = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def __init__(self, *args, state=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.linkbot = linkbot
        self.error.connect(self.error_message)

    def run(self):
        pass

    def deinit(self):
        pass

    def message_box(self, title, message):
        QtGui.QMessageBox.information(self, title, message)

    def error_message(self, msg):
        self.message_box('Error', msg)

try:
    from linkbot_internal_dev.forms import start as start_ui
except:
    from forms import start as start_ui

class Start(LinkbotTest):
    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = start_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_start.clicked.connect(self.clicked)
        self.state = state

    def _run(self):
        self.state.clear()
        self.state['linkbot'] = linkbot.Linkbot()
        self.completed.emit()

    def clicked(self):
        self.ui.pushButton_start.setEnabled(False)
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

try:
    from linkbot_internal_dev.forms import serial_id as serial_id_ui
except:
    from forms import serial_id as serial_id_ui

class SerialId(LinkbotTest):
    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self.ui = serial_id_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.pushButton_set_id.clicked.connect(self.set_id)
        self.ui.lineEdit.returnPressed.connect(self.async_set_id)

    def run(self):
        self.ui.lineEdit.setFocus()

    def async_set_id(self):
        self.thread = threading.Thread(target=self.set_id)
        self.thread.start()

    def set_id(self):
        if len(self.ui.lineEdit.text()) != 4:
            self.message_box("Error", 
                    "Serial ID must be 4 characters in length.")
            return
        try:
            l = self.state['linkbot']
            l._setSerialId(self.ui.lineEdit.text().upper())
            l.set_buzzer_frequency(440)
            time.sleep(0.4)
            l.set_buzzer_frequency(0)
        except:
            self.error.emit(traceback.format_exc())
        else:
            self.completed.emit()

try:
    from linkbot_internal_dev.forms import final as final_ui
except:
    from forms import final as final_ui

class Final(LinkbotTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = final_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.clicked)

    def clicked(self):
        # TODO: Save data to database here
        self.completed.emit()

try:
    from linkbot_internal_dev.forms import radio as radio_ui
except:
    from forms import radio as radio_ui

class Radio(LinkbotTest):
    update_progress = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = radio_ui.Ui_Form()
        self.ui.setupUi(self)

        self.update_progress.connect(self.ui.progressBar.setValue)
        self.error.connect(self.error_message)

    def run(self):
        self.thread = threading.Thread(target=self.runtest)
        self.thread.start()

    def runtest(self):
        try:
            remote = linkbot.Linkbot('TEST')
            num_tests = 50
            for i in range(num_tests):
                remote.get_joint_angles()
                self.update_progress.emit((i/num_tests) * 100)
            self.completed.emit()
        except Exception as e:
            print(e)
            #self.error.emit(str(e))
            self.failure.emit('Radio Test Failure: ' + str(e))

class ButtonTest(LinkbotTest):
    msg = "Label message"

    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QtGui.QVBoxLayout(self)
        label = QtGui.QLabel(self.msg, self)
        label.setWordWrap(True)
        font = label.font()
        font.setPointSize(24)
        label.setFont(font)
        vbox.addWidget(label)
        self.setLayout(vbox)
        self.state = state

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_button_events(self.cb)

    def deinit(self):
        self.l.disable_button_events()

class ButtonPwr(ButtonTest):
    msg = "Press the POWER button to continue."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 0:
            self.completed.emit()

class ButtonA(ButtonTest):
    msg = "Press the 'A' button to continue."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 1:
            self.completed.emit()

class ButtonB(ButtonTest):
    msg = "Press the 'B' button to continue."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 2 and buttonState == 0:
            self.completed.emit()

class Buzzer(ButtonTest):
    msg = "Check that the buzzer is buzzing and press any button on the\
    Linkbot to continue."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_button_events(self.cb)
        self.l.set_buzzer_frequency(440)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonState == 0:
            self.l.set_buzzer_frequency(0)
            self.completed.emit()

class LedRed(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Make sure the LED is <p style="color:red">RED</p> and press any button on the
    Linkbot to continue.
    </body>
    </html>
          """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_button_events(self.cb)
        self.l.set_led_color(255, 0, 0)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonState == 0:
            self.completed.emit()

class LedGreen(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Make sure the LED is <p style="color:green">GREEN</p> and press any button on the
    Linkbot to continue.
    </body>
    </html>
          """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_button_events(self.cb)
        self.l.set_led_color(0, 255, 0)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonState == 0:
            self.completed.emit()

class LedBlue(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Make sure the LED is <p style="color:blue">BLUE</p> and press any button on the
    Linkbot to continue.
    </body>
    </html>
          """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_button_events(self.cb)
        self.l.set_led_color(0, 0, 255)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonState == 0:
            self.completed.emit()

class AccelerometerTest(ButtonTest):
    msg = "Label message"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_accelerometer_events(self.cb)
        x,y,z = self.l.get_accelerometer_data()
        self.cb(x,y,z,0)

    def deinit(self):
        self.l.disable_accelerometer_events()

    def cb(self, x, y, z, timestamp):
        pass

class AccelerometerZ(AccelerometerTest):
    msg = """
        Place the robot on a level surface with the buttons pointing upward.
        """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        if abs(z-1) < 0.1 and \
           abs(x) < 0.1 and \
           abs(y) < 0.1:
           self.completed.emit()

class AccelerometerY(AccelerometerTest):
    msg = """
        Place the robot on a level surface with face 2 pointing down.
        """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        if abs(y-1) < 0.1 and \
           abs(z) < 0.1 and \
           abs(x) < 0.1:
           self.completed.emit()

class AccelerometerX(AccelerometerTest):
    msg = """
        Place the robot on a level surface with face 1 pointing down.
        """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        if abs(x-1) < 0.1 and \
           abs(z) < 0.1 and \
           abs(y) < 0.1:
           self.completed.emit()

class Calibration(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    <ol>
    <li> Move both motors to their zero positions.
    <li> Press and hold the A and B buttons until the motors start spinning.
    <li> Set the robot down for the remainder of the test.
    </body>
    </html>
          """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_cond = threading.Condition()
        self._running = False

    def run(self):
        self.l = self.state['linkbot']
        self._running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        # First, wait 10 seconds
        self.thread_cond.acquire()
        self.thread_cond.wait(10)
        if not self._running:
            self.thread_cond.release()
            return
        self.thread_cond.release()
        # Now, wait until the motors have been settled at 0 position for 3
        # seconds
        i = 0
        num_failures = 0
        while True:
            try:
                angles = self.l.get_joint_angles()
                print(angles)
            except:
                num_failures += 1
                if num_failures > 10:
                    raise
            if all( map( lambda x: abs(x) < 2, angles) ):
                i += 1
            else:
                i = 0
            if i > 5:
                break
            self.thread_cond.acquire()
            self.thread_cond.wait(0.5)
            if not self._running:
                self.thread_cond.release()
                return
            self.thread_cond.release()

        self.completed.emit()
            
    def deinit(self):
        self.thread_cond.acquire()
        self._running = False
        self.thread_cond.notify()
        self.thread_cond.release()
        self.thread.join()

