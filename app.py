from flask import Flask, render_template, request
from decimal import Decimal
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # Replace with your MySQL root password
    database="citizen_db"      
)
cursor = db.cursor(dictionary=True)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_citizen', methods=['GET', 'POST'])
def add_citizen():
    if request.method == 'POST':
        ssn = request.form['ssn']
        name = request.form['name']
        dob = request.form['dob']
        citizenship_status = request.form['citizenship_status']
     
        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        existing_citizen = cursor.fetchone()

        if existing_citizen:
            return "Error: Citizen with this SSN already exists.", 400

        cursor.execute(
            "INSERT INTO Citizen (SSN, Name, DOB, CitizenshipStatus) VALUES (%s, %s, %s, %s)",
            (ssn, name, dob, citizenship_status)
        )
        db.commit()

        return "Citizen added successfully!"

    return render_template('add_citizen.html')

@app.route('/update_employment', methods=['GET', 'POST'])
def update_employment_status():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id') 
        ssn = request.form['ssn']
        job_title = request.form['job_title']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        citizen = cursor.fetchone()
        if not citizen:
            return "Error: Citizen with this SSN does not exist.", 400

        if employee_id: 
            cursor.execute("SELECT * FROM employment WHERE EmploymentID = %s", (employee_id,))
            employment_record = cursor.fetchone()

            if employment_record:
            
                cursor.execute(
                    "UPDATE employment SET JobTitle = %s, StartDate = %s, EndDate = %s, SSN = %s WHERE EmploymentID = %s",
                    (job_title, start_date, end_date, ssn, employee_id)
                )
                db.commit()
                return "Employment record updated successfully!"
            else:
                return f"Error: Employee with ID {employee_id} does not exist.", 400
        else:
            cursor.execute(
                "INSERT INTO employment (SSN, JobTitle, StartDate, EndDate) VALUES (%s, %s, %s, %s)",
                (ssn, job_title, start_date, end_date)
            )
            db.commit()
            return "New employment record added successfully!"

    return render_template('update_employment.html')



@app.route('/add_contribution', methods=['GET', 'POST'])
def add_contribution():
    if request.method == 'POST':
        ssn = request.form['ssn']
        contribution = request.form['contribution']
        benefits = request.form['benefits']

        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        citizen = cursor.fetchone()
        if not citizen:
            return f"Error: Citizen with SSN {ssn} does not exist.", 400

        cursor.execute(
            "INSERT INTO SocialSecurityRecord (SSN, Contributions, Benefits) VALUES (%s, %s, %s)",
            (ssn, contribution, benefits)
        )
        db.commit()

        return f"Contribution of ${contribution} and Benefits of ${benefits} added successfully for SSN {ssn}!"

    return render_template('add_contribution.html')


@app.route('/calculate_benefits', methods=['GET', 'POST'])
def calculate_social_security_benefits():
    if request.method == 'POST':
        ssn = request.form['ssn']

        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        citizen = cursor.fetchone()
        if not citizen:
            return f"Error: Citizen with SSN {ssn} does not exist.", 400

        cursor.execute("SELECT Contributions FROM SocialSecurityRecord WHERE SSN = %s", (ssn,))
        records = cursor.fetchall()
        if not records:
            return f"Error: No contributions found for SSN {ssn}.", 400

        total_contributions = sum(Decimal(record["Contributions"]) for record in records)

        benefits = total_contributions * Decimal(0.75)

        return f"Estimated social security benefits for SSN {ssn}: ${benefits:.2f}"

    return render_template('calculate_benefits.html')

@app.route('/file_tax_return', methods=['GET', 'POST'])
def file_tax_return():
    if request.method == 'POST':
        ssn = request.form['ssn']
        max_income = request.form['max_income']
        tax_paid = request.form['tax_paid']
        year = request.form['year']
        authority_id = request.form['authority_id']

        
        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        if not cursor.fetchone():
            return f"Error: Citizen with SSN {ssn} does not exist.", 400

        cursor.execute("SELECT * FROM TaxAuthority WHERE AuthorityID = %s", (authority_id,))
        if not cursor.fetchone():
            return f"Error: Tax Authority with ID {authority_id} does not exist.", 400

        
        cursor.execute("SELECT * FROM TaxReturn WHERE SSN = %s AND Year = %s", (ssn, year))
        tax_return = cursor.fetchone()
        if tax_return:
            
            cursor.execute(
                "UPDATE TaxReturn SET Max_Income = %s, Tax_Paid = %s, AuthorityID = %s WHERE SSN = %s AND Year = %s",
                (max_income, tax_paid, authority_id, ssn, year)
            )
        else:
            
            cursor.execute(
                "INSERT INTO TaxReturn (SSN, Max_Income, Tax_Paid, Year, AuthorityID) VALUES (%s, %s, %s, %s, %s)",
                (ssn, max_income, tax_paid, year, authority_id)
            )
        db.commit()
        return "Tax return filed successfully!"

    
    cursor.execute("SELECT * FROM TaxAuthority")
    tax_authorities = cursor.fetchall()

    return render_template('file_tax_return.html', tax_authorities=tax_authorities)


@app.route('/update_address', methods=['GET', 'POST'])
def update_address():
    if request.method == 'POST':
        ssn = request.form['ssn']
        address_id = request.form.get('address_id')  # AddressID is optional
        city = request.form['city']
        state = request.form['state']
        postal = request.form['zip'] 

        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        citizen = cursor.fetchone()
        if not citizen:
            return f"Error: Citizen with SSN {ssn} does not exist.", 400

        if address_id:
            if not address_id.isdigit():
                return f"Error: AddressID must be a numeric value.", 400

            cursor.execute("SELECT * FROM Address WHERE AddressID = %s", (address_id,))
            existing_address = cursor.fetchone()
            if existing_address:
                cursor.execute(
                    "UPDATE Address SET City = %s, State = %s, Postal = %s WHERE AddressID = %s",
                    (city, state, postal, address_id)
                )
                db.commit()
                return f"Address with ID {address_id} updated successfully!"
            else:
                return f"Error: Address with ID {address_id} does not exist.", 400
        else:
            cursor.execute(
                "INSERT INTO Address (SSN, City, State, zip) VALUES (%s, %s, %s, %s)",
                (ssn, city, state, postal)
            )
            db.commit()
            return f"New address added successfully for SSN {ssn}!"

    return render_template('update_address.html')

@app.route('/generate_report', methods=['GET', 'POST'])
def generate_citizen_report():
    if request.method == 'POST':
        ssn = request.form['ssn']

        cursor.execute("SELECT * FROM Citizen WHERE SSN = %s", (ssn,))
        citizen = cursor.fetchone()
        if not citizen:
            return f"Error: Citizen with SSN {ssn} does not exist.", 400

        cursor.execute("""
            SELECT tr.Year, tr.Max_Income, tr.Tax_Paid, ta.AuthorityID, ta.Name AS AuthorityName, ta.Region 
            FROM TaxReturn tr
            LEFT JOIN TaxAuthority ta ON tr.AuthorityID = ta.AuthorityID
            WHERE tr.SSN = %s
        """, (ssn,))
        tax_returns = cursor.fetchall()

        cursor.execute("""
            SELECT EmploymentID, JobTitle, StartDate, EndDate
            FROM employment
            WHERE SSN = %s
        """, (ssn,))
        employment_records = cursor.fetchall()

        cursor.execute("SELECT * FROM SocialSecurityRecord WHERE SSN = %s", (ssn,))
        social_security_records = cursor.fetchall()

        report = {
            "Citizen Information": citizen,
            "Tax Returns": tax_returns,
            "Employment Records": employment_records,
            "Social Security Records": social_security_records
        }

        return render_template('citizen_report.html', report=report)

    return render_template('generate_report.html')

@app.route('/tax_authority', methods=['GET', 'POST'])
def manage_tax_authority():
    if request.method == 'POST':
        action = request.form.get('action')
        authority_id = request.form.get('authority_id')
        name = request.form.get('name')
        region = request.form.get('region')

        if action == 'add':
            cursor.execute("INSERT INTO TaxAuthority (Name, Region) VALUES (%s, %s)", (name, region))
            db.commit()
            message = "Tax Authority added successfully!"
        elif action == 'update' and authority_id:
            cursor.execute("UPDATE TaxAuthority SET Name = %s, Region = %s WHERE AuthorityID = %s",
                           (name, region, authority_id))
            db.commit()
            message = "Tax Authority updated successfully!"
        elif action == 'delete' and authority_id:
            cursor.execute("DELETE FROM TaxAuthority WHERE AuthorityID = %s", (authority_id,))
            db.commit()
            message = "Tax Authority deleted successfully!"
        else:
            message = "Invalid action or missing data!"

        return render_template('tax_authority.html', message=message, tax_authorities=get_all_tax_authorities())

    return render_template('tax_authority.html', tax_authorities=get_all_tax_authorities())

def get_all_tax_authorities():
    cursor.execute("SELECT * FROM TaxAuthority")
    return cursor.fetchall()

if __name__ == '__main__':
    app.run(debug=True)
