import numpy as np
from scipy.integrate import ode
from tqdm import tqdm
from utils.RotationMatrix import RotationMatrix
import yaml
from os.path import join, abspath

class QuadCopter:
	def __init__(self, config_file=None):
		default_config_file = abspath(join('..', 'cfg', 'FMA.yaml'))

		if config_file is not None:
			self.config_file = config_file
		else:
			self.config_file = default_config_file

		try:
			with open(self.config_file, 'r') as file:
				config = yaml.safe_load(file)
		except FileNotFoundError:
			raise FileNotFoundError(f"Config file not found: {self.config_file}")

		for key in config.keys():
			try:
				setattr(self, key, config[key])
			except KeyError:
				raise ValueError(f"Invalid config. Missing key: {key}")

		self.config = config
		self.I = np.array([[self.Ixx, 0, 0], [0, self.Iyy, 0], [0, 0, self.Izz]])


	def ForcedSystemODE(self, t, State):
		return self.SystemODE(t, State)

	def SystemODE(self, t, State):

		# Unpack System Vars
		Pos = State[0:3]
		Vel = State[3:6]
		Orient = State[6:9]
		Omega = State[9:]
		
		# Inputs
		T = 0
		Tau = 0

	
		# Initilize State Derivative Vector
		Xdot = np.zeros(12)
	
		# Velocity
		Xdot[0:3] = Vel
	
		# Acceleration	
		R = RotationMatrix(Orient)
		Xdot[3:6] = np.array([0, 0, self.g]) + R @ np.array([0, 0, T/self.m]) 

		# Angular Velocity
		Phi = Orient[0] 
		Theta = Orient[1]
		Xdot[6:9] = np.linalg.solve(np.array([[1, 0, -np.sin(Theta)], [0, np.cos(Phi), np.cos(Theta) * np.sin(Phi)], [0, -np.sin(Phi), np.cos(Theta) * np.cos(Phi)]]), Omega)
	
		# Angular Acceleration
		Xdot[9:] = np.linalg.inv(self.I) @ (Tau - np.cross(Omega, self.I @ Omega))


		return Xdot



	def Simulate(self, x0=np.zeros(12), t=np.linspace(0, 10), solver='dopri5'):
		"""Simulates the system for given initial conditions and time points and Controller."""

		AvailableSolvers = ['dopri5', 'vode', 'zvode', 'lsoda', 'dop853']
		if solver not in AvailableSolvers:
			raise ValueError(
				f"Invalid solver. Available options are:{AvailableSolvers}")

	 	# Solver Properties Selection
		Solver = ode(self.ForcedSystemODE).set_integrator(solver)
		Solver.set_initial_value(x0, t[0])

		# Memoery Allocation and Initial Condition Set
		x = np.zeros((len(t), len(x0)))
		x[0, :] = x0

		for i, _t in tqdm(enumerate(t[1:]), total=len(t[1:]), desc="Simulating in Progress!"):
			Solver.integrate(_t)
			if Solver.successful():
				x[i+1, :] = Solver.y
			else:
				print(f"Integration failed at t={_t}")
				print("Return code:", Solver.get_return_code())
				break

		return x, t
		



if __name__ == "__main__":
	# Example usage with a custom YAML file named 'my_quadcopter_config.yaml'
	Quad = QuadCopter()
	S, t = Quad.Simulate(x0=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], t=np.linspace(0, 10, 1000))
	print(S.shape)
