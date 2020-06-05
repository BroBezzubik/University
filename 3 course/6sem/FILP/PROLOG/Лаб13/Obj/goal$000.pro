/*****************************************************************************

		Copyright (c) My Company

 Project:  LAB13
 FileName: LAB13.PRO
 Purpose: No description
 Written by: Visual Prolog
 Comments:
******************************************************************************/

include "lab13.inc"

domains

	first_name, bank_name, car_make, color, phone, acc = string.
	cost, sum = real.
	address = string*.

predicates

	telephone_book(first_name, phone, address).
	cars(first_name, car_make, color, cost).
	depositors(first_name, bank_name, acc, sum).
	
	find_owner_by_telephone(phone, first_name, car_make, cost).
	
clauses

	telephone_book("Barsukov", "00001", ["City1", "Street1", "House1", "Appartaments1"]).
	
	depositors("Barsukov", "GerBank", "0001", 200).
	
	cars("Barsukov", "Porshe", "black", 20).
	cars("Barsukov", "Lada", "red", 1).
	cars("Ivanov", "Moscvich", "black", 20).
	
	find_owner_by_telephone(Phone, First_name, Car_make, Cost) :-
		telephone_book(First_name, Phone, _),cars(First_name, Car_make, _, Cost).
	


goal
	/*find_owner_by_telephone("00001", First_name, Car_make, Cost). (a)<*/
	find_owner_by_telephone("00001", _, Car_make, _).
	
