"""
Module containing all the forces acting on a rocket

Version: WIP
last edit: 17.10.2018

--Propulse NTNU--
"""
import numpy as np
import RocketModule.Rocket as RockMod
from scipy.constants import R, g

#Constants
T0 = RockMod.find_parameter("environment.dot", "temperature") + 273  # Temperature of Air [K]
P0 = RockMod.find_parameter("environment.dot", "pressure")  # Barometric pressure at sea level [Pa]
m = 29e-3  # Molecular mass of Air [kg]
rho0 = P0/(R*T0/m)  # Air density at sea level [kg*m^-3]
h = R*T0/(m*g)  # Height constant of Air ~ 1e4 [m]


# Forces

def gravity(rocket):
	"""
	Gravitational force on the rocket
	Assumptions:- Homogenous gravity field in -z direction
				- g to be a constant (very good approx. up to 3000 m, off by 0.1%)

	:param rocket: [rocket class] The rocket object
	:return: [np.array] gravity vector in the inertial frame [N].
	"""
	return np.array([0,0,-rocket.getMass()*g])


def thrust(rocket, t):
	"""
	:param rocket: [rocket class] The rocket object
	:param t: [float] point in time [s]
	:return: [np.array] thrust force at time t in rocket frame
	"""
	Thrust = rocket.getMotor().thrust(t)

	return np.array([Thrust, 0, 0])


def SAMdrag(rocket, state):
	"""
	TODO: Add wind?
		Assumptions:- AoA ~ 0
					- Quadratic drag F ~ -kv^2
	:param rocket: [rocket class] The rocket object
	:param state: [np.array] The current state of the rocket object
	:return: [np.array] The drag force (SAM) in the world frame
	"""
	z = state[2] # Vertical position of rocket
	V = state[3:6] # Velocity of rocket
	Cd = rocket.getCd(state)
	Aref = np.pi*(rocket.body.D/2)**2
	k = 1/2*rho0*Aref*Cd*np.exp(-z/h)

	return -k*np.linalg.norm(V)*V


# Torques

def SAMmoment(rocket, state):
	"""

	:param rocket: [rocket class] The rocket object
	:param state: [np.array] The current state of the rocket object
	:return: [np.array] The moment created by Drag about CM of the rocket (SAM)
	"""
	r = rocket.getCOP() - rocket.getCOM()
	return np.cross(r,SAMdrag(rocket, state))

