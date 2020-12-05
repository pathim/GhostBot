# -*- coding: utf-8 -*-

import time
from threading import Thread


BUFFER = 0.1
RESOLUTION = 10 # in ms
FLOAT_RESOLUTION = float(RESOLUTION) / 1000

import pymumble_py3
from pymumble_py3.constants import *

class MumbleGhostBot:
	"""
	Forward audio from the main channel to a secondary channel but not vice versa
	"""
	def __init__(self,host,username,password,channel_src,channel_dst):
		self.src=channel_src
		self.dst=channel_dst
		self.cursor_time = 0.0	# time for which the audio is treated

		self.exit = False

		self.users = dict()  # store some local informations about the users session

		# Create the mumble instance and assign callbals
		self.mumble = pymumble_py3.Mumble(host, username, password=password, stereo=False, reconnect=True)

		self.mumble.set_loop_rate(0.005)
		self.mumble.set_application_string("GhostBot")
		self.mumble.callbacks.add_callback(PYMUMBLE_CLBK_CONNECTED,self.connection_cb)
		self.mumble.set_receive_sound(True)
		self.mumble.start()  # start the mumble thread
		self.mumble.is_ready()	# wait for the end of the connection process

		self.loop()

	def connection_cb(self,*args):
		self.mumble.channels.find_by_name(self.src).move_in()  # move to the configured channel

		target=self.mumble.channels.find_by_name(self.dst)
		self.mumble.sound_output.set_whisper(target['channel_id'],True)


	def loop(self):
		"""Master loop""" 
		import audioop

		self.cursor_time=time.time()
		while self.mumble.is_alive():
			if self.cursor_time < time.time() - BUFFER:  # it's time to check audio
				base_sound = None

				for user in self.mumble.users.values():  # check the audio queue of each users

					if user.sound.is_sound():
						# available sound is to be treated now and not later
						sound = user.sound.get_sound(FLOAT_RESOLUTION)
						
						if base_sound == None:
							base_sound = sound.pcm
						else:
							base_sound = audioop.add(base_sound, sound.pcm, 2)

				if base_sound:
					self.mumble.sound_output.add_sound(base_sound)

				self.cursor_time += FLOAT_RESOLUTION
			else:
				time.sleep(FLOAT_RESOLUTION)

if __name__ == "__main__":
	import argparse
	parser=argparse.ArgumentParser(description="Mumble bot to forward voice from one channel to another")
	parser.add_argument('--host',required=True,help="Hostname of the mumble server")
	parser.add_argument('--user',required=True,help="Username the Bot will use")
	parser.add_argument('--password',required=True,help="Password of the mumble server")
	parser.add_argument('--src',required=True,help="Source channel")
	parser.add_argument('--dst',required=True,help="Destination channel")
	args=parser.parse_args()
	host=args.host
	user=args.user
	password=args.password
	src=args.src
	dst=args.dst
	recbot = MumbleGhostBot(host=host, username=user, password=password, channel_src=src, channel_dst=dst)
