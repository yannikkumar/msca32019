
import unittest
import numpy as np
import threading
import statistics

from server_solution import ThreadedTCPServer, ThreadedTCPRequestHandler
from client_solution import TCPClient, res_mean, res_stdev




class ValuesTest(unittest.TestCase):

	def test_get_mean_stdev(self):
		HOST, PORT = "localhost", 9998
		server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = True
		server_thread.start()

		thread_number = 10
		thread_list = []
				 
		for i in range(0,thread_number):
			thread_list.append(TCPClient(i, HOST, PORT))

		for i in range(0,thread_number):
			thread_list[i].start()

		for i in range(0,thread_number):
			thread_list[i].join()

		server.shutdown()
		server.socket.close()

		mean = statistics.mean([i for i in res_mean if i is not None])
		stdev = statistics.mean([i for i in res_stdev if i is not None])
		print(f"Mean of sample means is {mean}")
		print(f"Mean of sample standard deviations is {stdev}")
		self.assertAlmostEqual(mean, 0, places=1)
		self.assertAlmostEqual(stdev, 1, places=1)


if __name__ == '__main__':
	np.random.seed(1)
	unittest.main()