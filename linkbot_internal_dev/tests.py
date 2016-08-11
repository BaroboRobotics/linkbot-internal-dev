
import concurrent
from PyQt4 import QtCore, QtGui
import time
import linkbot3 as linkbot
linkbot.config(timeout=3)
import traceback
import threading
import math

from linkbot_diagnostics.LinkbotDiagnosticGui import initialize_tables
from linkbot_diagnostics.LinkbotDiagnosticGui import LinkbotDiagnostic 
from linkbot_diagnostics.testlinkbot import TestLinkbot
import sqlite3 as sql
import appdirs
import os

db_dir = os.path.join(appdirs.user_data_dir(), "linkbot-diagnostics")
db_file = os.path.join(db_dir, "database.db")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

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
        self.state = state
        self.parent = args[0]

    def run(self):
        self.display_db_data()
        self._running = True
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        pass

    def display_db_data(self):
        try:
            global db_file
            con = sql.connect(db_file)
            cur = con.cursor()
            cur.execute('''\
    SELECT DISTINCT Id FROM linearity_tests WHERE Date >= \'{}\''''.format(
                time.strftime('%Y-%m-%d 00:00:00') ) )
            #'
            rows = cur.fetchall()
            con.close()
            self.ui.lineEdit.setText(str(len(rows)))
        except:
            print(traceback.format_exc())

    def deinit(self):
        self._lock.acquire()
        self._running = False
        self._lock.release()
        self.thread.join()

    def _run(self):
        while True:
            self._lock.acquire()
            if not self._running:
                self._lock.release()
                break
            self._lock.release()

            try:
                l = linkbot.CLinkbot('LOCL')
                l.set_buzzer_frequency(440)
                time.sleep(0.5)
                l.set_buzzer_frequency(0)
                self.state.clear()
                self.state['linkbot'] = l
                # Check the form factor: If it's a dongle, run the dongle tests.
                if l.form_factor() == linkbot.FormFactor.DONGLE:
                    print('Dongle detected.')
                    self.parent._tests = iter(self.parent.dongle_tests)
                break
            except (RuntimeError, concurrent.futures.TimeoutError) as e:
                time.sleep(0.5)
                continue
            except Exception:
                print(traceback.format_exc())
                break
        self.completed.emit()

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
        if len(set(['AEIOU0']) & set(self.ui.lineEdit.text().upper())) > 0:
            self.message_box("Error", 
                    "Illegal character in serial ID")
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
    speed_threshold = 215
    linearity_threshold = 0.95
    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = final_ui.Ui_Form()
        self.ui.setupUi(self)
        self.state = state
        self.populate()

    def run(self):
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target = self._run)
        self._thread.start()

    def _run(self):
        while True:
            self._lock.acquire()
            if not self._running:
                break
            self._lock.release()
            try:
                self.state['linkbot'].get_joint_angles()
            except RuntimeError:
                # The linkbot has been unplugged. Emit the completion signal.
                self.completed.emit()
                break

    def deinit(self):
        self._lock.acquire()
        self._running = False
        self._lock.release()
        self._thread.join()

    def populate(self):
        self._set_speed_edit(self.ui.lineEdit_m1fs, self.state['speeds'][0])
        self._set_speed_edit(self.ui.lineEdit_m1bs, self.state['speeds'][1])
        self._set_speed_edit(self.ui.lineEdit_m2fs, self.state['speeds'][2])
        self._set_speed_edit(self.ui.lineEdit_m2bs, self.state['speeds'][3])

        self._set_lin_edit(self.ui.lineEdit_m1fl, self.state['linearities'][0])
        self._set_lin_edit(self.ui.lineEdit_m1bl, self.state['linearities'][1])
        self._set_lin_edit(self.ui.lineEdit_m2fl, self.state['linearities'][2])
        self._set_lin_edit(self.ui.lineEdit_m2bl, self.state['linearities'][3])

    def _set_speed_edit(self, widget, speed):
        widget.setText('{} [>{}]'.format(str(speed)[0:6], self.speed_threshold))
        if abs(speed) > self.speed_threshold:
            widget.setStyleSheet('background:rgb(0,255,0);')
        else:
            widget.setStyleSheet('background:rgb(255,0,0);')

    def _set_lin_edit(self, widget, linearity):
        widget.setText('{} [>{}]'.format(str(linearity)[0:6],
            self.linearity_threshold))
        if linearity > self.linearity_threshold:
            widget.setStyleSheet('background:rgb(0,255,0);')
        else:
            widget.setStyleSheet('background:rgb(255,0,0);')

try:
    from linkbot_internal_dev.forms import final_dongle as final_dongle_ui
except:
    from forms import final_dongle as final_dongle_ui

class FinalDongle(LinkbotTest):
    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = final_dongle_ui.Ui_Form()
        self.ui.setupUi(self)
        self.state = state

    def run(self):
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target = self._run)
        self._thread.start()

    def _run(self):
        while True:
            self._lock.acquire()
            if not self._running:
                break
            self._lock.release()
            try:
                self.state['linkbot'].form_factor()
            except Exception as e:
                # The linkbot has been unplugged. Emit the completion signal.
                print('Disconnect detected:', e)
                self.completed.emit()
                break

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
            remote = linkbot.CLinkbot('TEST')
            num_tests = 50
            for i in range(num_tests):
                remote.get_joint_angles()
                self.update_progress.emit((i/num_tests) * 100)
            remote.disconnect()
            self.completed.emit()
        except Exception as e:
            print(e)
            #self.error.emit(str(e))
            self.failure.emit('Radio Test Failure: ' + str(e))

class ButtonTest(LinkbotTest):
    msg = "Label message"
    fontsize = 24
    pixmap = None
    pixmap_width = 200
    pixmap_height = 200 

    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QtGui.QVBoxLayout(self)
        if self.pixmap:
            image = QtGui.QLabel(self)
            image.setText(_fromUtf8(""))
            pixmap = QtGui.QPixmap(_fromUtf8(self.pixmap))
            pixmap_scaled = pixmap.scaled( self.pixmap_width, 
                                           self.pixmap_height, 
                                           QtCore.Qt.KeepAspectRatio)
            image.setPixmap(pixmap_scaled)
            image.setScaledContents(False)
            image.setAlignment(QtCore.Qt.AlignCenter)
            image.show()
            vbox.addWidget(image)

        label = QtGui.QLabel(self.msg, self)
        label.setWordWrap(True)
        font = label.font()
        font.setPointSize(self.fontsize)
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
    msg = "Press the POWER button."
    pixmap = ":/images/images/button_pwr.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 0 and buttonState == 0:
            self.completed.emit()

class ButtonA(ButtonTest):
    msg = "Press the 'A' button."
    pixmap = ":/images/images/button_a.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 1 and buttonState == 0:
            self.completed.emit()

class ButtonB(ButtonTest):
    msg = "Press the 'B' button."
    pixmap = ":/images/images/button_b.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, buttonNo, buttonState, timestamp):
        if buttonNo == 2 and buttonState == 0:
            self.completed.emit()

class Buzzer(ButtonTest):
    fontsize=16
    msg = "Did you hear the buzzer?\n" \
          "No : A\n" \
          "Yes : B"
    pixmap = ":/images/images/sine.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start_time = time.time()

    def run(self):
        self.l = self.state['linkbot']
        self._running = True
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        self.l.enable_button_events(self.cb)

    def cb(self, buttonNo, buttonState, timestamp):
        print('Button cb!!')
        if (time.time() - self._start_time) < 2:
            return
        if buttonState != 0:
            return
        if buttonNo == 0:
            return

        print(buttonNo, buttonState, timestamp)

        self._lock.acquire()
        print('Lock acquired.')
        self._running = False
        self._lock.release()
        self._thread.join()
        print('Thread joined.')
        #self.l.set_buzzer_frequency(0)
        if buttonNo == 1:
            # failure
            self.failure.emit("Tester indicated buzzer failure.")
        elif buttonNo == 2:
            # success
            print('success.')
            self.completed.emit()

    def _run(self):
        while (time.time()-self._start_time)<2:
            self._lock.acquire()
            if not self._running:
                self._lock.release()
                break
            self._lock.release()
            f = 50+440+ 440*math.sin(2*(time.time()-self._start_time))
            self.l.set_buzzer_frequency(int(f))
        self.l.set_buzzer_frequency(0)

class LedRed(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Is the LED <span style="color:red">RED</span>? 
    <p> No: A </p>
    <p> Yes: B </p>
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
        if buttonState != 0:
            return
        if buttonNo == 0:
            return

        if buttonNo == 1:
            # failure
            self.failure.emit("Tester indicated LED failure.")
        elif buttonNo == 2:
            # success
            self.completed.emit()

class LedGreen(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Is the LED <span style="color:green">GREEN</span>? 
    <p> No: A </p>
    <p> Yes: B </p>
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
        if buttonState != 0:
            return
        if buttonNo == 0:
            return

        if buttonNo == 1:
            # failure
            self.failure.emit("Tester indicated LED failure.")
        elif buttonNo == 2:
            # success
            self.completed.emit()

class LedBlue(ButtonTest):
    msg = """
    <html> <head/>
    <body>
    Is the LED <span style="color:blue">BLUE</span>? 
    <p> No: A </p>
    <p> Yes: B </p>
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
        if buttonState != 0:
            return
        if buttonNo == 0:
            return

        if buttonNo == 1:
            # failure
            self.failure.emit("Tester indicated LED failure.")
        elif buttonNo == 2:
            # success
            self.completed.emit()


class AccelerometerTest(ButtonTest):
    fontsize = 16
    msg = "Label message"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.l = self.state['linkbot']
        self.l.enable_accelerometer_events(self.cb)
        x,y,z = self.l.get_accelerometer_data()
        self.cb(x,y,z,0)

    def deinit(self):
        print('Accel test deinit.')
        self.l.disable_accelerometer_events()

    def cb(self, x, y, z, timestamp):
        pass

class AccelerometerZ(AccelerometerTest):
    msg = """
Place the robot on a level surface with the buttons pointing upward.  """
    pixmap = ":/images/images/accel_z.png"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        if abs(z-1) < 0.1 and \
           abs(x) < 0.1 and \
           abs(y) < 0.1:
           self.completed.emit()

class AccelerometerY(AccelerometerTest):
    msg = """
Place the robot on a level surface with face 2 pointing down.  """
    pixmap = ":/images/images/accel_y.png"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        if abs(y-1) < 0.1 and \
           abs(z) < 0.1 and \
           abs(x) < 0.1:
           self.completed.emit()

class AccelerometerX(AccelerometerTest):
    msg = """
Place the robot on a level surface with face 1 pointing down.  """
    pixmap = ":/images/images/accel_x.png"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cb(self, x, y, z, timestamp):
        print(x, y, z)
        if abs(x-1) < 0.1 and \
           abs(z) < 0.1 and \
           abs(y) < 0.1:
           self.completed.emit()

class Calibration(ButtonTest):
    pixmap=":/images/images/calibrate.png"
    fontsize=16
    msg = """\
Move motors to zero position. 
Press and hold A and B.
          """
    pixmap_width=300
    timeout = 120 # 2 minute timeout

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_cond = threading.Condition()
        self._running = False
        self._start_time = time.time()

    def run(self):
        self.l = self.state['linkbot']
        self._running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        # First, wait 10 seconds
        print('Calibration thread start.')
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
                print('Got joint angles:', angles)
            except Exception as e:
                print('Failed to get joint angles: ', e)
                num_failures += 1
                time.sleep(1)
                if num_failures > 10:
                    raise
                continue
            if all( map( lambda x: abs(x) < 2, angles) ):
                i += 1
            else:
                i = 0
                if (time.time()-self._start_time) > self.timeout:
                    self.failure.emit("Calibration step timed out.")
                    return
            if i > 5:
                print('Calibration step passed.')
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

try:
    from linkbot_internal_dev.forms import motor as motor_ui
except:
    from forms import motor as motor_ui

class MotorTest(LinkbotTest):
    def __init__(self, *args, state={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = motor_ui.Ui_Form()
        self.ui.setupUi(self)
        self.state = state
    
    def run(self):
        self.thread = threading.Thread(target=self._diagnostics)
        self.thread.start()

    def _diagnostics(self):
        try:
            l = TestLinkbot('LOCL')
            x,y,z = l.getAccelerometer()
            if abs(x) > 0.1 or \
               abs(x) > 0.1 or \
               abs(z-1) > 0.1:
                 self.diagnostics_error.emit('Warning',
                         'Accelerometer readings have anomalies!')
            global db_file
            con = sql.connect(db_file)
            initialize_tables(con.cursor())
            cur = con.cursor()
# Check to see if this l is in our database already. Add it if not
            cur.execute('SELECT * FROM robot_type WHERE Id=\'{}\''.format(l.getSerialId()))
            rows = cur.fetchall()
            formFactor = None
            if l.getFormFactor() == linkbot.FormFactor.I:
                formFactor = "linkbot.Linkbot-I"
                motor2index = 2
            elif l.getFormFactor() == linkbot.FormFactor.L:
                formFactor = "linkbot.Linkbot-L"
                motor2index = 1
            else:
                formFactor = "UNKNOWN"
            print ("Testing LinkBot {}".format(l.getSerialId()))
            d = LinkbotDiagnostic(l)
            results = d.runLinearityTest()
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            if len(rows) == 0:
                cur.execute('INSERT INTO robot_type VALUES(\'{}\', \'{}\')'.format(
                    l.getSerialId(), formFactor))
            cur.execute("INSERT INTO linearity_tests "
                "VALUES('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(
                    l.getSerialId(),
                    now,
                    results[0]['forward_slope'],
                    results[0]['forward_rvalue'],
                    results[0]['backward_slope'],
                    results[0]['backward_rvalue'],
                    results[motor2index]['forward_slope'],
                    results[motor2index]['forward_rvalue'],
                    results[motor2index]['backward_slope'],
                    results[motor2index]['backward_rvalue']))

            con.commit()
            con.close()
            speeds = [ 
                        results[0]['forward_slope'],
                        results[0]['backward_slope'],
                        results[motor2index]['forward_slope'],
                        results[motor2index]['backward_slope'],
                     ]
            linearities = [
                results[0]['forward_rvalue'],
                results[0]['backward_rvalue'],
                results[motor2index]['forward_rvalue'],
                results[motor2index]['backward_rvalue'],
                          ]
            self.state['speeds'] = speeds 
            self.state['linearities'] = linearities
            self.completed.emit()

        except Exception as e:
            self.failure.emit("Test Failed: " + str(e))

try:
    from linkbot_internal_dev.forms import images_rc
except:
    from forms import images_rc

class Failure(LinkbotTest):
    fontsize = 20
    def __init__(self, *args, state = None, msg=None, **kwargs):
        LinkbotTest.__init__(self, *args, **kwargs)
        self.state = state
        
        vbox = QtGui.QVBoxLayout(self)
        label = QtGui.QLabel(msg, self)
        label.setWordWrap(True)
        font = label.font()
        font.setPointSize(self.fontsize)
        label.setFont(font)
        vbox.addWidget(label)
        self.setStyleSheet('background:rgb(255, 0, 0);')

        self.setLayout(vbox)

    def run(self):
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target = self._run)
        self._thread.start()

    def _run(self):
        while True:
            self._lock.acquire()
            if not self._running:
                break
            self._lock.release()
            try:
                self.state['linkbot'].get_joint_angles()
            except RuntimeError:
                # The linkbot has been unplugged. Emit the completion signal.
                self.completed.emit()
                break

    def deinit(self):
        self._lock.acquire()
        self._running = False
        self._lock.release()
        self._thread.join()
    
