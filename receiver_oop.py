import cv2
import numpy as np
import socket
import tkinter as tk

IP_ADDR = '192.168.1.41'
PORT = 5000
BUFFER_SIZE = 1024


class Robot():
	def __init__(self, ip, port, buffer_size):
		self.window = window
		self.window.title(window_title)
		self.ip = ip
		self.port = port
		self.buffer = buffer_size


	def connect(self):
		#insert all receiver code
		pass

	def send_cmd(self):
		#only sends one-character commands to robot
		#get_cmd
		pass

	def img_proc(self):
		#insert all image processing code
		#must work together with set_cmd
		pass

	def set_cmd(self):
		#set commands
		pass

	def get_cmd(self):
		#return self.command
		pass

	def get_pose(self):
		#return something
		pass

class GUI():
	def __init__(self, window, window_title):
		self.window = window
		self.window.title(window_title)
		Robot(IP_ADDR, PORT, BUFFER_SIZE)

		self.btn_up = tk.Button(self.window, text="UP", command = self.set_cmd)
		self.btn_up.grid(col = 2, row = 0)
		self.btn_lt = tk.Button(self.window, text="LEFT")
		self.btn_lt.grid(col = 1, row = 1)
		self.btn_dn = tk.Button(self.window, text="DOWN")
		self.btn_dn.grid(col = 2, row = 1)
		self.btn_rt = tk.Button(self.window, text="RIGHT")
		self.btn_rt.grid(col = 3, row = 1)

		self.btn_stop = tk.Button(self.window, text="STOP", width = 40)
		self.btn_stop.grid(col = 3, row = 2)

		self.window.mainloop()

	def set_cmd(self):
		print(self.btn_up.value())

	def update(self):
		pass




if __name__ == "__main__":

