from datamainpulation import *
from helper import *
import re 
        
# This signupController function is use to Validate the payload name, email, password, address, phoneNumber, dob, googleId is not empty and string format.
def signupController(data):
    try:
        if  "name" in data and "email" in data  and "password" and data  and "address" in data and "phoneNumber" in data and "dob" in data and "googleId" in data:
            if data["name"] != "" and data["email"] != "" and data['address'] !="" and data['phoneNumber'] !="" and data['dob'] !="" and (data["password"] != "" or data['googleId'] !=""):
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, data["email"]):
                    return {
                        "message":"Invalid email format.",
                        "status": False,
                        "statusCode":400
                    }
                users_db = getAllUserEmail()
                user_emails = [user[0] for user in users_db]
                if data["email"] in user_emails:
                    return {
                        "message": "Email already registered.", 
                        "status": False,
                        "statusCode": 400
                    }
                else: 
                    return signup(data)
            else:
                return {
                    "message":"Invaild data !",
                    "status": False,
                    "statusCode":400
                }
        else:
            return {
                "message":"All fields (email, password, name) are required.",
                "statusCode":400,
                "status":False
            }
    except Exception as e:
        return {
                "Error":str(e),
                "status": False,
                "statusCode":400
            }
        
# This signupController function is use to Validate the payload data["name"], data["email"],data["password"], data["googleId"] is not empty and string format.
def signInController(data):
    try:
        if "email" in data and "password" in data and "googleId" in data:
            if data["email"] != "" and  (data["password"] != "" or data['googleId'] !=""):
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, data["email"]):
                    return {
                        "message":"Invalid email format.",
                        "statusCode":400,
                        "status": False,
                    }
                else:
                    return signIn(data)
            else:
                return {
                    "message":"Invaild data !",
                    "statusCode":400,
                    "status": False,
                }
        else:
            return {
                "message":"All fields (email, password) are required.",
                "statusCode":400,
                "status": False,
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":400,
                "status": False,
            }
         
# This candidateRegistrationController function is use to Validate the payload ["first_name", "middle_name", "last_name", "gender", "email", "country_code", "phone_number", "date_of_birth", "current_location", "preferred_location", "skills", "privacy_policy", "work_experience_years", "work_experience_months", "current_salary_currency", "current_salary_amount", "expected_salary_currency", "expected_salary_amount", "availability_to_join", "experience_details", "educationDetails", "resumeBase64", "resume_name", "job_id"] is not empty and string format.
def candidateRegistrationController(data):
    try:
        required_keys = [
            "first_name", "last_name", "gender", "email", "country_code", 
            "phone_number", "date_of_birth", "current_location", "preferred_location", 
            "skills", "privacy_policy", "work_experience_years", "work_experience_months", 
            "current_salary_currency", "current_salary_amount", "expected_salary_currency", 
            "expected_salary_amount", "availability_to_join", "experience_details", 
            "educationDetails", "resumeBase64", "resume_name", "job_id"
        ]
        if all(key in data and data[key] not in ["", None, []] for key in required_keys):
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, data["email"]):
                return {
                    "message":"Invalid email format.",
                    "statusCode":400,
                    "status":False
                }
            else:
                if checkApplicationExist(data['email'],data['job_id']):
                    isjobidExist = checkJobIdExist()
                    if str(data["job_id"]) in isjobidExist:
                        if data['privacy_policy'] == "true" or data['privacy_policy'] == True or data['privacy_policy'] == "True":
                            return candidateRegistration(data)
                        else:
                            return {
                                "message":"Privacy policy must be accepted.",
                                "statusCode":400,
                                "status":False
                            }
                    else :
                        return {
                            "message":"Invalid job id.",
                            "statusCode":400,
                            "status":False
                        }                
                else :
                    return {
                        "message":"Application is already Exist.",
                        "statusCode":400,
                        "status":False
                    }
        else:
            return {
                "message":"Invalid Data",
                "status":False,
                "statusCode":400
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":400,
                "status":False
            }

# This signupController function is use to Validate the payload data["userId"] is not empty and string format.
def getCandidateDetailsController(data):
    try:
        if "userId" in data :
            if data["userId"] != "":
                users_db = getAllUserId()
                user_id = [user[0] for user in users_db]
                if data["userId"] not in user_id:
                    return {
                        "message": "Invalid User ID", 
                        "status": False,
                        "statusCode": 400
                    }
                else: 
                    return getCandidateDetails(data)
            else:
                return {
                    "message":"Invaild data !",
                    "statusCode":400,
                    "status": False,
                }
        else:
            return {
                "message":"User ID are required.",
                "statusCode":400,
                "status": False,
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":400,
                "status": False,
            }

# This signupController function is use to Validate the payload data["name"], data["email"],data["contact"], data["message"],data["acceptRecurring"] is not empty and string format.
def userdetailsController(data):
    try:
        if "email" in data and "name" in data and "contact" in data and "message" in data and "acceptRecurring" in data:
            if data["email"] != "" and data["name"] != "" and data['contact'] !="" and data['message'] != "" and data['acceptRecurring'] !="":
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, data["email"]):
                    return {
                        "message":"Invalid email format.",
                        "statusCode":400,
                        "status": False,
                    }
                else:
                    return userdetails(data)
            else:
                return {
                    "message":"Invaild data !",
                    "statusCode":400,
                    "status": False,
                }
        else:
            return {
                "message":"All fields (email,name,contact,messsage,accpectRecurring) are required.",
                "statusCode":400,
                "status": False,
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":400,
                "status": False,
            }

# This getCustomerDetailsController function is use to Validate the payload data["userId"] is not empty and string format.
def getCustomerDetailsController(data):
    try:
        if "userId" in data :
            if data["userId"] != "":
                users_db = getAllUserId()
                user_id = [user[0] for user in users_db]
                if data["userId"] not in user_id:
                    return {
                        "message": "Invalid User ID", 
                        "status": False,
                        "statusCode": 400
                    }
                else: 
                    return getCustomerDetails()
            else:
                return {
                    "message":"Invaild data !",
                    "statusCode":400,
                    "status": False,
                }
        else:
            return {
                "message":"User ID are required.",
                "statusCode":400,
                "status": False,
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":400,
                "status": False,
            }
