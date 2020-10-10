/*****************************************************************************

		Copyright (c) My Company

 Project:  LAB_11
 FileName: LAB_11.PRO
 Purpose: No description
 Written by: Visual Prolog
 Comments:
******************************************************************************/
domains
	fio, telephone = String.

predicates
	find_record(fio, telephone).
	
clauses
	find_record("Barsukov N", "0000").
	find_record("Stroganov Y", "0001").
	find_record("Ivanov I", "0002" ).
	find_record("Ivanov I", "0003" ).
	find_record("Ivanov I", "0004" ).
	find_record("Ivanov I", "0005" ). /* Ivanov very likes phones*/

goal
	/*find_record("Ivanov I", Telephone).* <-- to find telephone/
	find_record(Fio, "0005"). /*<-- to find host of telephone*/
