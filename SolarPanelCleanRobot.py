import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

class Robot:
    def __init__(self):
        self.motor_pins = {
            "DC Motor 1 IN1": 17,  # Sol ön tekerlek IN1
            "DC Motor 1 IN2": 27,  # Sol ön tekerlek IN2
            "DC Motor 2 IN1": 18,  # Sağ ön tekerlek IN1
            "DC Motor 2 IN2": 22,  # Sağ ön tekerlek IN2
            "DC Motor 3 IN1": 23,  # Sol arka tekerlek IN1
            "DC Motor 3 IN2": 24,  # Sol arka tekerlek IN2
            "DC Motor 4 IN1": 25,  # Sağ arka tekerlek IN1
            "DC Motor 4 IN2": 4,  # Sağ arka tekerlek IN2
            "DC Motor 5": 5  # Temizleme silindiri
        }
        self.water_pump_pin = 6  # Su pompası
        self.setup_gpio()


    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.motor_pins.values()), GPIO.OUT)
        GPIO.setup(self.water_pump_pin, GPIO.OUT)

    def move_robot(self, direction, duration=0):
        if direction == "ileri":
            print("Robot ileri hareket ediyor...")
            self.set_motor_direction("ileri")
        elif direction == "geri":
            print("Robot geri hareket ediyor...")
            self.set_motor_direction("geri")
        elif direction == "dur":
            self.stop_all_motors()
            return

        self.activate_motors(["DC Motor 1", "DC Motor 2", "DC Motor 3", "DC Motor 4"])
        if duration > 0:
            time.sleep(duration)
            self.stop_all_motors()

    
    def set_motor_direction(self, direction):
        if direction == "ileri":
            GPIO.output(self.motor_pins["DC Motor 1 IN1"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 1 IN2"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 2 IN1"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 2 IN2"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 3 IN1"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 3 IN2"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 4 IN1"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 4 IN2"], GPIO.LOW)
        elif direction == "geri":
            GPIO.output(self.motor_pins["DC Motor 1 IN1"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 1 IN2"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 2 IN1"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 2 IN2"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 3 IN1"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 3 IN2"], GPIO.HIGH)
            GPIO.output(self.motor_pins["DC Motor 4 IN1"], GPIO.LOW)
            GPIO.output(self.motor_pins["DC Motor 4 IN2"], GPIO.HIGH)

    def activate_motors(self, motors):
        for motor in motors:
            in1_pin = self.motor_pins[motor + " IN1"]
            in2_pin = self.motor_pins[motor + " IN2"]
            GPIO.output(in1_pin, GPIO.HIGH)
            GPIO.output(in2_pin, GPIO.LOW)

    def stop_all_motors(self):
        for pin in self.motor_pins.values():
            GPIO.output(pin, GPIO.LOW)

    def start_cleaning(self):
        print("Temizleme işlemi başlatılıyor...")
        GPIO.output(self.motor_pins["DC Motor 5"], GPIO.HIGH)
        GPIO.output(self.water_pump_pin, GPIO.HIGH)
        print("Su pompası çalışıyor...")

    def stop_cleaning(self):
        print("Temizleme işlemi durduruluyor...")
        GPIO.output(self.motor_pins["DC Motor 5"], GPIO.LOW)
        GPIO.output(self.water_pump_pin, GPIO.LOW)
        print("Su pompası durduruluyor...")


def scan_surface(camera, original_image):
    ret, frame = camera.read()
    if not ret:
        print("Kamera hatası!")
        return False

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    difference = cv2.absdiff(original_image, gray_frame)
    _, thresh = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        print("Kir tespit edildi!")
        return True
    else:
        return False


camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Kamera açılamadı!")
    exit()

ret, original_frame = camera.read()
if not ret:
    print("Kamera hatası!")
    exit()
original_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)

robot = Robot()

original_image = cv2.imread('clean_panel_image.png')  # Temiz panelin orijinal görüntüsü
original_gray_static = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

try:
    while True:
        if scan_surface(camera, original_gray_static):
            robot.move_robot("dur")
            robot.start_cleaning()
            time.sleep(2)
            robot.stop_cleaning()
        else:
            robot.move_robot("ileri", 1)
        time.sleep(1)
except KeyboardInterrupt:
    print("Program sonlandırıldı.")

finally:
    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
