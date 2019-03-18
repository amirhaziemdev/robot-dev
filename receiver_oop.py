import cv2
import numpy as np
import socket
import tkinter as tk

IP_ADDR = '192.168.1.41'
PORT = 8485
BUFFER_SIZE = 1024


class Robot():
	def __init__(self, ip, port, buffer_size):
		self.ip = ip
		self.port = port
		self.buffer = buffer_size
		self.command = "default"

	def connect(self):
		#insert all receiver code
		pass

	def recv_frame(self):




	def get_info(self):
		print("INFO:\n", "\nIP Address:", self.ip, "\nPort No:", self.port, "\nBuffer Size:", self.buffer)

	def send_cmd(self):
		#only sends one-character commands to robot
		#get_cmd
		pass

	def get_cmd(self):
		return self.command

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

		self.robot = Robot(IP_ADDR, PORT, BUFFER_SIZE)
		self.command = "default"

		self.btn_up = tk.Button(self.window, text="FORWARD", command = self.set_cmd_f)
		self.btn_up.grid(column = 2, row = 0)
		self.btn_lt = tk.Button(self.window, text="LEFT", command = self.set_cmd_l)
		self.btn_lt.grid(column = 1, row = 1)
		self.btn_dn = tk.Button(self.window, text="REVERSE", command = self.set_cmd_b)
		self.btn_dn.grid(column = 2, row = 1)
		self.btn_rt = tk.Button(self.window, text="RIGHT", command = self.set_cmd_r)
		self.btn_rt.grid(column = 3, row = 1)

		self.btn_stop = tk.Button(self.window, text="STOP", width = 20, command = self.set_cmd_stop)
		self.btn_stop.grid(column = 1, row = 2, columnspan=3)

		self.window.mainloop()

	def get_command(self):
		print(self.robot.command)
		return self.command

	def set_cmd_f(self):
		self.robot.command = "f"
		self.command = "f"
		self.get_command()

	def set_cmd_b(self):
		self.robot.command = "b"
		self.command = "b"
		self.get_command()

	def set_cmd_l(self):
		self.robot.command = "l"
		self.command = "l"
		self.get_command()

	def set_cmd_r(self):
		self.robot.command = "r"
		self.command = "r"
		self.get_command()

	def set_cmd_stop(self):
		self.robot.command = "s"
		self.command = "s"
		self.get_command()


	def update(self):
		pass




if __name__ == "__main__":
	GUI(tk.Tk(), "Robot Controller")

