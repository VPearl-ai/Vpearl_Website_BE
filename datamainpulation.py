import json
from dotenv import load_dotenv
load_dotenv()
from helper import *
        
# Connect with the database and store the admin details.
def signup(data):
    try:
        connection = dbconnection()
        cursor = connection.cursor()        
        query = """INSERT INTO users (name, email, passKey, address, dob, phone_number, google_id) 
           VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"""
        cursor.execute(query, (
            data["name"], 
            data["email"], 
            data["password"], 
            data["address"], 
            data["dob"], 
            data["phoneNumber"], 
            data["googleId"]
        ))
        user_id = cursor.fetchone()[0]       
        connection.commit()
        cursor.close()
        connection.close() 
        if user_id:
            data['userId']=user_id
            return {
                "message": "User created successfully",
                "statusCode":200,
                "status":True,
                "data":data
            }
        else :
            return {
                "message":"Failed to Insert the data in Database",
                "statusCode":400,
                "status":False,
                "data":[]
            }
    except Exception as e:
        print(f"Error in the signup function :{str(e)}")
        return {    
            "Error": str(e),
            "status": False,
            "statusCode": 400,
        }

# Connect with the database and get the response for the signIn.
def signIn(data):
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        if data['password'] != "":
            query = """SELECT * FROM users WHERE email = %s AND passkey = %s AND is_active = True"""
            cursor.execute(query, (data["email"], data["password"]))
        elif data['googleId'] != "":
            query = """SELECT * FROM users WHERE email = %s AND g oogle_id = %s AND is_active = True"""
            cursor.execute(query, (data["email"], data["googleId"]))
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(users) == 0:
            return {
                "Error": "Invalid email or password",
                "status":False,
                "statusCode": 400
            }
        else:
            if users[0][2] == 'businessdevelopment@vpearlsolutions.com':
                role ='hr'
            elif users[0][2] == 'bhuvaneswari.rm@vpearlsolutions.com':
                role='admin'
            return {
                "message":"User logged in successfully",
                "status":True,
                "statusCode": 200,
                "userDetails":{
                    "role":role,
                    "id":users[0][0],
                    "name":users[0][1],
                    "email":users[0][2],
                    "address":users[0][4],
                    "dob":users[0][5],
                    "phone_number":users[0][6],
                    "created_at":users[0][8],
                }
            }
    except Exception as e:        
        print(f"Error in sign function : {str(e)}")
        return {
                "Error":str(e),
                "status":False,
                "statusCode":400
            }
    
# Connect with the database and get current opening job Details.
def jobDetailsCareers():
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        query = """SELECT * FROM jobs WHERE isactive = True"""
        cursor.execute(query)
        jobDetails = cursor.fetchall()
        cursor.close()
        connection.close()
        if jobDetails is None:
            return {
                "message":"Job Not Found",
                "status":True,
                "statusCode":200
            }
        else:
            keys = [
                "id", "department", "title", "location", "experience", "job_type",
                "description", "qualifications", "skills", "responsibilities",
                "created_at", "is_active"
            ]
            converted_data = [dict(zip(keys, item)) for item in jobDetails]
            return {
                "message":"Job Details Retrieved Successfully",
                "status":True,
                "statusCode":200,
                "jobDetails": converted_data
            }
    except Exception as e:
        print(f"Error in the jobDetailsCareers function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "status":False
            }
    
# Connect with the database and store the candidate details who registration for the job.
def candidateRegistration(data):
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        file_path =save_base64_to_file(data['resumeBase64'],data['resume_name'])
        if file_path is None:
            return {
                "message":"Failed Save the resume",
                "status":False,
                "statusCode":400
                }
        query = """INSERT INTO candidates (
                first_name, middle_name, last_name, gender, email, country_code, phone_number, 
                date_of_birth, current_location, preferred_location, skills, privacy_policy, 
                work_experience_years, work_experience_months, current_salary_currency, 
                current_salary_amount, expected_salary_currency, expected_salary_amount, 
                availability_to_join, experience_details, educationDetails, resumefile_path, job_id
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id"""
        cursor.execute(query, (
            data["first_name"], 
            data["middle_name"], 
            data["last_name"], 
            data["gender"], 
            data["email"], 
            data["country_code"], 
            data["phone_number"], 
            data["date_of_birth"], 
            data["current_location"], 
            json.dumps(data["preferred_location"]), 
            json.dumps(data["skills"]), 
            data["privacy_policy"], 
            data["work_experience_years"], 
            data["work_experience_months"], 
            data["current_salary_currency"], 
            data["current_salary_amount"], 
            data["expected_salary_currency"], 
            data["expected_salary_amount"], 
            data["availability_to_join"], 
            json.dumps(data["experience_details"]), 
            json.dumps(data["educationDetails"]), 
            file_path,
            data["job_id"]
        ))
        candidate_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        if candidate_id:
            job=getJobName(data['job_id'])
            send_replay_mail_Job(data['email'], data['first_name'], job, file_path, data['resume_name'])
            return {
                "message":"Successfullly Insert the data in Database",
                "statusCode":200,
                "status":True,
                "candidate_id":candidate_id
            }
            
        else :
            return {
                "message":"Failed to Insert the data in Database",
                "statusCode":400,
                "status":False
            }
    except Exception as e:
        print(f"Error in candidateRegistration functions : {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "status":False
            }

# Connect with the database and get the Candidate Details who applied for the job.
def getCandidateDetails(data):
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        query = """SELECT 
            candidates.id AS candidate_id,
            candidates.first_name,
            candidates.middle_name,
            candidates.last_name,
            candidates.gender,
            candidates.email,
            candidates.country_code,
            candidates.phone_number,
            candidates.date_of_birth,
            candidates.current_location,
            candidates.preferred_location,
            candidates.skills AS candidate_skills,
            candidates.privacy_policy,
            candidates.work_experience_years,
            candidates.work_experience_months,
            candidates.current_salary_currency,
            candidates.current_salary_amount,
            candidates.expected_salary_currency,
            candidates.expected_salary_amount,
            candidates.availability_to_join,
            candidates.experience_details,
            candidates.educationDetails,
            candidates.resumefile_path,
            jobs.department,
            jobs.roles,
            jobs.locations,
            jobs.experience AS job_experience,
            jobs.jobtype,
            jobs.description AS job_description,
            jobs.qualifications,
            jobs.skills AS job_skills,
            jobs.responsibilities
        FROM 
            candidates
        JOIN 
            jobs ON candidates.job_id = jobs.id;
        """
        cursor.execute(query)
        candidates = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(candidates)==0:
            return {
                "status": True,
                "statusCode": 200,
                "message": "No candidates found",
                "data": []
            }
        else:
            data =[]
            for item in candidates:
                candidate={
                    "candidate_id":item[0],
                    "first_name":item[1],
                    "middle_name":item[2],
                    "last_name":item[3],
                    "gender":item[4],
                    "email":item[5],
                    "country_code":item[6],
                    "phone_number":item[7],
                    "date_of_birth":item[8],
                    "current_location":item[9],
                    "preferred_location":json.loads(item[10]),
                    "candidate_skills":json.loads(item[11]),
                    "privacy_policy":item[12],
                    "work_experience_years":item[13],
                    "work_experience_months":item[14],
                    "current_salary_currency":item[15],
                    "current_salary_amount":item[16],
                    "expected_salary_currency":item[17],
                    "expected_salary_amount":item[18],
                    "availability_to_join":item[19],
                    "experience_details":json.loads(item[20]),
                    "educationDetails":json.loads(item[21]),
                    "resumebase64":file_to_base64(item[22]),
                    "department":item[23],
                    "roles":item[24],
                    "locations":item[25],
                    "job_experience":item[26],
                    "jobtype":item[27],
                    "job_description":item[28],
                    "qualifications":item[29],
                    "job_skills":item[30],
                    "responsibilities":item[31]
                }
                data.append(candidate)
            return {
                "status": True,
                "statusCode": 200,
                "data": data
            }
    except Exception as e:
        print(f"Error in getCandidateDetails function :{str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "status":True
            }

def userdetails(data):
    try:
        connection = dbconnection()
        cursor = connection.cursor()        
        query = """INSERT INTO contactInfo (name, email, contact, message, accept_recurring) 
           VALUES (%s, %s, %s, %s, %s) RETURNING id"""
        cursor.execute(query, (
            data["name"], 
            data["email"], 
            data["contact"], 
            data["message"], 
            data["acceptRecurring"]
        ))
        connection.commit()
        user_id = cursor.fetchone()[0]      
        connection.commit()
        cursor.close()
        connection.close() 
        if user_id:
            send_replay_contact(data['email'],data['name']) 
            send_alter_mail(data['name'],data['email'],data['contact'],data['message'])
            data['userId']=user_id
            return {
                "message": "User created successfully",
                "statusCode":200,
                "status":True,
                "data":data
            }
        else :
            return {
                "message":"Failed to Insert the data in Database",
                "statusCode":400,
                "status":False,
                "data":[]
            }
    except Exception as e:
        print(f"Error in the signup function :{str(e)}")
        return {    
            "Error": str(e),
            "status": False,
            "statusCode": 400,
        }
    
# Connect with the database and SELECT the candidate details who registration for the job.
def getCustomerDetails():
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        query = """SELECT * FROM contactInfo"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(rows)!=0:
            data=[]
            for row in rows:
                data.append({
                    "id":row[0],
                    "name":row[1],
                    "email":row[2],
                    "contact":row[3],
                    "message":row[4],
                })
            return {
                "message":"Successfullly fetch Details",
                "statusCode":200,
                "status":True,
                "customerDetails":data
            }            
        else :
            return {
                "message":"No data found",
                "statusCode":200,
                "status":True
            }
    except Exception as e:
        print(f"Error in candidateRegistration functions : {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "status":False
            }