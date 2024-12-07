# US-Citizen-Management-Dashboard

Documentation: US Citizen Management System
Overview

The US Citizen Management System is a terminal-based application designed to manage citizen records, tax returns, employment details, social security contributions, and addresses. It allows users to perform CRUD operations and generate reports for individuals.

Core Features

	1.	Citizen Management: Add, update, and retrieve citizen records.
	2.	Employment Status: Manage and update employment history.
	3.	Tax Returns: File and update tax return details.
	4.	Social Security Benefits: Calculate social security benefits based on     contributions.
	5.	Address Management: Update or add citizen addresses.
	6.	Report Generation: Compile detailed citizen reports.

Function Descriptions and Use Cases
1. Add Citizen

	•	Purpose: Add a new citizen to the database.
	•	Steps:
		1.	Select Option 1 from the menu.
		2.	Enter the required details:
			•	SSN: Unique Social Security Number.
			•	Name: Full name of the citizen.
			•	DOB: Date of birth (YYYY-MM-DD).
			•	Citizenship Status: Citizenship status (e.g., US Citizen, Permanent Resident).
		3.	If the SSN already exists, the system will notify you.
	•	Use Case: Register new citizens in the system.
2. Update Employment Status

	•	Purpose: Update or add employment details for a citizen.
	•	Steps:
		1.	Select Option 2 from the menu.
		2.	Provide:
			•	SSN: Social Security Number of the citizen.
			•	Employer ID: Unique ID of the employer.
			•	Job Title: Citizen’s job title.
			•	Start Date: Job start date (YYYY-MM-DD).
			•	End Date: Job end date (optional).
		3.	The system will update the existing record or add a new one.
	•	Use Case: Maintain employment history for social security and tax purposes.
3. Calculate Social Security Benefits

	•	Purpose: Estimate benefits based on social security contributions.
	•	Steps:
		1.	Select Option 3 from the menu.
		2.	Input the citizen’s SSN.
		3.	The system calculates benefits using the formula:
			•	Benefits = Total Contributions * 0.75.
	•	Use Case: Provide an estimate of social security benefits.
4. File Tax Return

	•	Purpose: File or update tax returns for a citizen.
	•	Steps:
		1.	Select Option 4 from the menu.
		2.	Provide:
			•	SSN: Social Security Number of the citizen.
			•	Income: Total income for the year.
			•	Tax Paid: Taxes paid for the year.
			•	Year: Tax filing year.
		3.	The system updates the existing record or creates a new one.
	•	Use Case: Track annual income and taxes paid by citizens.
5. Update Address

	•	Purpose: Update or add a citizen’s address.
	•	Steps:
		1.	Select Option 5 from the menu.
		2.	Provide:
			•	SSN: Social Security Number of the citizen.
			•	City: Name of the city.
			•	State: Name of the state.
			•	Postal Code: ZIP code.
		3.	The system updates the address or adds a new record.
	•	Use Case: Maintain current and previous addresses for citizens.
6. Generate Citizen Report

	•	Purpose: Generate a detailed report of a citizen’s information.
	•	Steps:
		1.	Select Option 6 from the menu.
		2.	Input the citizen’s SSN.
		3.	The system compiles:
			•	Personal Information.
			•	Tax Returns.
			•	Employment History.
			•	Social Security Records.
		4.	The report is displayed in JSON format for easy reading.
	•	Use Case: Retrieve a comprehensive profile of a citizen.
7. Exit

	•	Purpose: Safely close the application.
	•	Steps:
		1.	Select Option 7.
		2.	The application disconnects from the database and exits.
	•	Use Case: Ensure proper closure of the application.

Steps to Run the Application

1.	Start the Application:
Run the Python script:
Python3 app.py

2.	Menu Navigation:
The application presents a menu with numbered options. Input the number corresponding to the desired operation.




![image](https://github.com/user-attachments/assets/1811ecd4-41d0-4805-8808-bb3e5d2fcfdf)
