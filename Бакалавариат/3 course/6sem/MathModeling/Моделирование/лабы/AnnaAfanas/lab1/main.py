import os, sys
import prettytable 
from sympy import *

def func(x, y):
	return x*x + y*y


def pickar_method_three(start, end, step, y0, table):
	y_list = []
	x_current = start
	x = symbols('x')
	while (x_current <= end):
		y1 = y0 + integrate(func(x, y0), (x, start, x_current))
		y2 = y0 + integrate(func(x, y1), (x, start, x_current))
		y3 = y0 + integrate(func(x, y2), (x, start, x_current))
		x_current += step
		y_list.append(float(y3))
	table.add_column("Pickar_three", y_list)

def pickar_method_four(start, end, step, y0, table):
	y_list = []
	x_current = start
	x = symbols('x')
	while (x_current <= end):
		y1 = y0 + integrate(func(x, y0), (x, start, x_current))
		y2 = y0 + integrate(func(x, y1), (x, start, x_current))
		y3 = y0 + integrate(func(x, y2), (x, start, x_current))
		y4 = y0 + integrate(func(x, y3), (x, start, x_current))	
		x_current += step
		y_list.append(float(y4))
	table.add_column("Pickar_four", y_list)


def eiler_method_explicit(start, end, step, y0, table):
	y_list = []
	x_current = start
	y_current = y0
	i = 0
	while (x_current <= end):
		y_current = y_current + step*func(x_current, y_current)
		i += 1
		x_current = start + i*step
		y_list.append(y_current)
	table.add_column("Eiler explicit", y_list)

def eiler_method_nonexplicit(start, end, step, y0, table):
	y_list = []
	x_current = start
	y_current = y0
	i = 0
	while (x_current <= end):		
		y_help = y_current + step*func(x_current, y_current)
		y_current = y_current + step/2*(func(x_current, y_current) + func(x_current + step, y_help))
		i += 1
		x_current = start + i*step
		y_list.append(y_current)
	table.add_column("Eiler nonexplicit", y_list)

def runge_kutt_method_second(start, end, step, y0, table):
	y_list = []
	x_current = start
	y_current = y0
	i = 0
	while (x_current <= end):		
		y_help = y_current + step*func(x_current, y_current)
		y_current = y_current + step/2*(func(x_current, y_current) + func(x_current, y_help))
		i += 1
		x_current = start + i*step
		y_list.append(y_current)
	table.add_column("Runge-Kutt second", y_list)

def runge_kutt_method_forth(start, end, step, y0, table):
	y_list = []
	x_current = start
	y_current = y0
	i = 0
	while (x_current <= end):		
		k1 = func(x_current, y_current)
		k2 = func(x_current + step/2, y_current + step*k1/2)
		k3 = func(x_current + step/2, y_current + step*k2/2)
		k4 = func(x_current + step, y_current + step*k3)
		y_current = y_current + step/6*(k1 + 2*k2 + 2*k3 + k4)
		i += 1
		x_current = start + i*step
		y_list.append(y_current)
	table.add_column("Runge-Kutt fourth", y_list)
		


def main():
	x_list = []
	start = float(input("X start: "))
	end = float(input("X end: "))
	step = float(input("Step: "))
	y0 = float(input("Y0: "))
	x_current = start
	while (x_current <= end):
		x_list.append(x_current)
		x_current += step

	result_table = prettytable.PrettyTable()

	result_table.add_column("X", x_list)
	pickar_method_three(start, end, step, y0, result_table)
	pickar_method_four(start, end, step, y0, result_table)
	eiler_method_explicit(start, end, step, y0, result_table)
	eiler_method_nonexplicit(start, end, step, y0, result_table)
	runge_kutt_method_second(start, end, step, y0, result_table)
	runge_kutt_method_forth(start, end, step, y0, result_table)
	result_table.float_format = "5.3"
	print(result_table)

if __name__ == "__main__":
	main()