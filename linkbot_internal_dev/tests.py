
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
        vbox = QtGui.QVBoxLayout()
        label = QtGui.QLabel(self.msg)
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


