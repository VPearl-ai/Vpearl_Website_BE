#`Flask` is a web framework. It provides tools, libraries, and technologies that allow you to build a web application. `request` is used to get the data from the user. `jsonify` is used to return the response in JSON format.
#`Cross-Origin Resource Sharing` is a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.
#importing all the functions from the controller file.
#`__name__` is a special variable in Python that is used to determine whether a script is being run as the main program or it is being imported as a module.
#`Cross-Origin Resource Sharing` is a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.
from flask import Flask, request, jsonify 
from flask_cors import CORS 
from controller import * 
from datamainpulation import *
app = Flask(__name__)
CORS(app)

# The /admin/signup route connects to the database, inserts data into the table, and finally allows the user to sign up. Implement the three-tier architecture for this API.
@app.route('/admin/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        response = signupController(data)
        return {
            "data":response,
            "statusCode":200 
        },200
    except Exception as e:
        print(f"Error in signup Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500,
                "status":False
            }),400
             
# The /admin/signIn route connects to the database, select data from table against the user email address and password, and finally allows the user to sign in. Implement the three-tier architecture for this API
@app.route('/admin/signIn', methods=['POST'])
def signIn():
    try:
        data = request.get_json()
        response = signInController(data)
        return {
            "data":response,
            "statusCode":200
        },200
    
    except Exception as e:
        print(f"Error in signIn Route : {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500,
                "status": False,
            }),400
    
# The Route /careers/jobDetails is used to the connect the Database, and select data of the job details from the table and Implement the three-tier architecture for this API
@app.route('/careers/jobDetails', methods=['GET'])
def jobDetails():
    try:
        response = jobDetailsCareers()
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in jobDetails Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400

# The /careers/getCandidateRegistration route connects to the database, inserts data into the table, and finally allows the candidate to apply for the job. Implement the three-tier architecture for this API
@app.route('/careers/candidateRegistration', methods=['POST'])
def CandidateRegistration():
    try:
        data = request.get_json()
        response = candidateRegistrationController(data)
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in getCandidateRegistration Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400
    
# The /careers/getCandidateRegistration route connects to the database, inserts data into the table, and finally allows the candidate to apply for the job. Implement the three-tier architecture for this API
@app.route('/careers/getCandidateDetails', methods=['POST'])
def getCandidateDetails():
    try:
        data = request.get_json()
        response = getCandidateDetailsController(data)
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in getCandidateDetails Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400
    
# The /contact/userdetails route connects to the database, SELECT data from the table. Implement the three-tier architecture for this API
@app.route('/contact/userdetails', methods=['POST'])
def userdetails():
    try:
        data = request.get_json()
        response = userdetailsController(data)
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in getCandidateDetails Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400

# The /customer/getCustomerDetails route connects to the database, Select data from the table. Implement the three-tier architecture for this API.
@app.route('/customer/getCustomerDetails', methods=['POST'])
def getCustomerDetails():
    try:
        data = request.get_json()
        response = getCustomerDetailsController(data)
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in getCandidateDetails Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400

# This is the main function in which the application runs.
if __name__ == "__main__":
    app.run(debug=True , port="8080",host="0.0.0.0")