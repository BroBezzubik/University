/*****************************************************************************

		Copyright (c) My Company

 Project:  LAB_12
 FileName: LAB_12.PRO
 Purpose: No description
 Written by: Visual Prolog
 Comments:
******************************************************************************/

include "lab_12.inc"

domains
	fio, univ = string.

predicates
	studing(fio, univ)


clauses
	studing("Barsukov N.", "BMSTU").
	studing("Barsukov N.", "Green Leaf").
	studing("Ivanov I.", "BMSTU").
	studing("Sidorov I.", "MGU").
	studing("Sidorov I.", "BMSTU").
	studing("Kolesnikov G.", "MAI").
	studing("Ivanov I.", Where) :- studing("Kolesnikov G.", Where).
goal
	/*studing(_, "BMSTU").*/
	/*studing(Who, "BMSTU").*/
	/*studing("Ivanov I.", _).*/
	studing("Ivanov I.", Where).

	
