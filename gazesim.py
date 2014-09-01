import itertools

import numpy as np
import matplotlib.pyplot as plt


class ObjectPositionSimulator(object):
	def __init__(self, width=20.0, height=20.0, rate=1.0/0.250):
		self.width = width
		self.height = height
		self.pos = [0.0, 0.0]
		self.rate = rate
		
	
	def __call__(self, dt):
		# In a homogenous Poisson process the probability
		# that there's exactly zero events during dt reduces
		# to exp(-rate * dt). So we can check if we
		# have an event as follows:
		if np.random.rand() < np.exp(-self.rate*dt):
			# No event at this time
			return self.pos, False

		x = (np.random.rand()-0.5)*self.width
		y = (np.random.rand()-0.5)*self.height
		self.pos = [x, y]

		return self.pos, True

def gaussian_noiser(sx=1.0, sy=1.0):
	def noiser(dt, xy):
		x = xy[0]+np.random.randn()*sx
		y = xy[1]+np.random.randn()*sy
		return [x,y]
	return noiser

def infrange(i=0):
	while True:
		yield i
		i += 1

def generate_sequence(simulator, noiser, sampling_rate=100.0):
	dt = 1.0/sampling_rate
	t = 0.0
	while True:
		pos, had_saccade = simulator(dt)
		gaze = noiser(dt, pos)
		yield t, pos, gaze, had_saccade
		
		t += dt
		

if __name__ == '__main__':
	sampling_rate = 100.0
	duration = 60.0
	simulator = ObjectPositionSimulator()
	noiser = gaussian_noiser()
	generator = generate_sequence(simulator, noiser)
	t, pos, gaze, saccades = zip(*itertools.islice(generator, int(duration*sampling_rate)))
	plt.plot(t, zip(*pos)[0])
	plt.plot(t, zip(*gaze)[0], '.')
	plt.show()

"""
	import time
	sim = ObjectPositionSimulator()
	noiser = gaussian_noiser()
	
	#x, y = zip(*xy)
	#plt.plot(x)
	plt.xlim(-0.5*sim.width, 0.5*sim.width)
	plt.ylim(-0.5*sim.width, 0.5*sim.width)
	plt.ion()
	
	npoints = 10
	pointstack = []
	prev_gaze = None
	prev_t = time.time()
	gazes = []
	thruths = []
	times = []
	for i in range(1000):
		#t = time.time()
		t = i/60.0
		times.append(t)
		dt = t - prev_t
		prev_t = t
		pos = sim(dt)
		gaze = noiser(dt, pos)
		gazes.append(gaze)
		thruths.append(pos)
		
		#continue
		for gp in pointstack:
			gp.set_alpha(gp.get_alpha()*0.8)
		if prev_gaze is not None:
			gp, = plt.plot([gaze[0], prev_gaze[0]], [gaze[1], prev_gaze[1]], '-', color='red', alpha=1.0, markersize=6, linewidth=4)
			pointstack.append(gp)
		prev_gaze = gaze
		if len(pointstack) > npoints:
			gp = pointstack.pop(0)
			gp.remove()
		

		plt.pause(0.0001)
	
	plt.clf()
	plt.ioff()
	plt.plot(times, zip(*thruths)[0], color='green')
	plt.plot(times, zip(*gazes)[0], color='red')

	plt.show()
"""
