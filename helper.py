import psycopg2 
from dotenv import load_dotenv
import base64
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
load_dotenv()

# Function to connect to the database
def dbconnection():
    try:
        # Create a connection to the database
        connection = psycopg2.connect(
            dbname=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password= os.getenv("PASSWORD"),
            host= os.getenv("HOST"),
            port= os.getenv("PORT")
        )
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database. {str(e)}")
        return None

# Function to get all the users email  details
def getAllUserEmail():
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT email FROM users""")
        email = cursor.fetchall()
        cursor.close()
        connection.close()
        return email        
    except Exception as e:
        print(f"Error in getAllUserEmail function: {str(e)}")
        return []
    
# Function to get all the users email  details
def getAllUserId():
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT id FROM users""")
        email = cursor.fetchall()
        cursor.close()
        connection.close()
        return email        
    except Exception as e:
        print(f"Error in getalluserId function: {str(e)}")
        return []
    
# Function to convert the base64 into file
def save_base64_to_file(base64_string, file_name):
    try :
        folder_path="Resume"
        os.makedirs(folder_path, exist_ok=True)
        file_data = base64.b64decode(base64_string)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as file:
            file.write(file_data)
        return file_path
    except Exception as e:
        print(f"Error in save_base64_to_file functions :{str(e)}")
        return None

# Function to check the application already exist or not
def checkApplicationExist(email,job_id):
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        query = """SELECT * FROM candidates WHERE email = %s AND job_id = %s;"""
        cursor.execute(query, (email,job_id))
        isExist = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(isExist)==0:
            return True          
        else:
            return False
    except Exception as e:
        print(f"Error in  checkApplicationExist functions:{str(e)}")
        return False
    
# Function to check the application already exist or not
def checkJobIdExist():
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM jobs")
        jobisExist = cursor.fetchall()
        cursor.close()
        connection.close()
        jobisExist = [str(i[0]) for i in jobisExist]
        return jobisExist
    except Exception as e:
        print(f"Error in the  checkJobIdExist function: {str(e)}")
        return []

# Function to convert the file to base64
def file_to_base64(file_path):
    try :
        with open(file_path, "rb") as file:
            base64_string = base64.b64encode(file.read()).decode("utf-8")
        return base64_string
    except Exception as e:
        print(f"Error in file_to_base64 function :{str(e)}")
        return None
    
# Function to get job name using job ID
def getJobName(id):
    try:
        connection=dbconnection()
        cursor = connection.cursor()
        cursor.execute(f"""SELECT roles FROM jobs WHERE id = {id}""")
        email = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(email) > 0:
            return email[0][0]
        else:
            return "Developer"     
    except Exception as e:
        print(f"Error in getalluserId function: {str(e)}")
        return "Developer"
    
# Send email to the Candidate who register for the JOB
def send_replay_mail_Job(mailId, Name, job, filepath, fileName):
    try:
        sender_mailId = os.getenv("SENDER_MAIL")
        passKey = os.getenv("APP_PASSWORD")        
        if not sender_mailId or not passKey:
            return False          
        msg = MIMEMultipart()
        msg['From'] = sender_mailId
        msg['To'] = mailId
        msg['Subject'] = f"Thanks for Applying {job}"      
        body = f'''
        <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {Name},</p>
            <p>Thank you very much for applying for the <b><strong>{job}</strong><b> position.</p>
            <p>At <b><strong>VPEARL SOLUTIONS</strong><b>, we are undergoing an unprecedented transformation, and we are delighted that you are interested in being part of this journey.</p>
            <p>Currently, our recruitment team is reviewing all applications. We will contact you via email regarding the next steps as soon as the selection results are determined.</p>
            <p>We sincerely appreciate your application. Let's make history together!</p>
            <hr>
            <p>Warm regards,</p>
            <p><strong>VPEARL SOLUTIONS - An AI Company, Chennai</strong></p>
            <p>
                🌐 <a href="https://vpearlsolutions.com/" target="_blank">Website</a> | 
                🔗 <a href="https://www.linkedin.com/company/vpealsoutions/" target="_blank">LinkedIn</a> | 
                📷 <a href="https://www.instagram.com/vpearl_solutions" target="_blank">Instagram</a> | 
                📘 <a href="https://www.facebook.com/profile.php?id=61572978223085" target="_blank">Facebook</a>
            </p>
        </body>
        </html>
        '''
        msg.attach(MIMEText(body, 'html'))        
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', filename=fileName)
                msg.attach(attachment)
        else:
            return False
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_mailId, passKey)
            server.sendmail(sender_mailId, mailId, msg.as_string())
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error in send_replay_mail_Job function: {str(e)}")
        return False
    
# Send email to the user who register for the contact
def send_replay_contact(mailId, Name):
    try:
        sender_mailId = os.getenv("SENDER_MAIL")
        passKey = os.getenv("APP_PASSWORD")        
        if not sender_mailId or not passKey:
            return False           
        msg = MIMEMultipart()
        msg['From'] = sender_mailId
        msg['To'] = mailId
        msg['Subject'] = "Thanks for reaching VPEARL SOLUTIONS"      
        
        body = f'''
        <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {Name},</p>
            <p>Thank you for your interest in VPEARL SOLUTIONS. Our team will reach out to you as soon as possible regarding your query. In the meantime, please explore our services designed to help you streamline and automate your business operations.</p>

            <h3>About VPEARL SOLUTIONS:</h3>
            <p>VPEARL SOLUTIONS is a leading provider of IT consulting and software development services. Initially established as an AI product company, we have helped numerous businesses—both IT and non-IT—enhance their performance, optimize workflows, and attract new customers through cutting-edge technology solutions. Additionally, I have attached our company details for your reference.</p>
            
            <h3>Our Offerings:</h3>
            <ul>
                <li>Custom Software Development</li>
                <li>AI-Based Web Applications for Automation</li>
                <li>Machine Learning & Artificial Intelligence Solutions</li>
                <li>Android Applications to Digitalize Business Processes</li>
                <li>Database Management & Optimization</li>
            </ul>
            
            <h3>Products We Have Developed:</h3>
            <ul>
                <li>Face Recognition AI</li>
                <li>Image Recognition AI</li>
                <li>AI-Powered Job Description Preparation</li>
                <li>Candidate Filtering Based on JD (Job Description) AI</li>
                <li>AI-Based Language Translation</li>
                <li>Chatbots for Business Automation</li>
                <li>AI-Powered Video Generation</li>
                <li>24/7 AI Voice Chatbot for Customer Support</li>
                <li>Event Management Booking App</li>
                <li>AI-Based Live Monitoring Solutions</li>
            </ul>
            
            <p>We would love to understand your specific business requirements and explore how we can assist in building a tailored solution for you. Please feel free to share your needs, and we can discuss the best possible approach to drive efficiency and growth for your business.</p>
            
            <p>Looking forward to your response!</p>
            <hr>
            <p>Warm regards,</p>
            <p><strong>VPEARL SOLUTIONS - An AI Company, Chennai</strong></p>
            <p>
                🌐 <a href="https://vpearlsolutions.com/" target="_blank">Website</a> | 
                🔗 <a href="https://www.linkedin.com/company/vpealsoutions/" target="_blank">LinkedIn</a> | 
                📷 <a href="https://www.instagram.com/vpearl_solutions" target="_blank">Instagram</a> | 
                📘 <a href="https://www.facebook.com/profile.php?id=61572978223085" target="_blank">Facebook</a>
            </p>
        </body>
        </html>
        '''        
        msg.attach(MIMEText(body, 'html'))
        filepath=r'Assest/proposal.pdf'
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', filename="Vpearl.pdf")
                msg.attach(attachment)
        else:
            return False        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_mailId, passKey)
            server.sendmail(sender_mailId, mailId, msg.as_string())
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error in send_replay_mail_Job function: {str(e)}")
        return False

# Send alter mail to Bhavana when user contant in website
def send_alter_mail(Name,mailId,phone,message):
    try:
        sender_mailId = os.getenv("SENDER_MAIL")
        passKey = os.getenv("APP_PASSWORD")        
        if not sender_mailId or not passKey:
            return False           
        msg = MIMEMultipart()
        msg['From'] = sender_mailId
        msg['To'] = "thirumurugan.vpearl@gmail.com"
        msg['Subject'] = "New Website Inquiry Alert - Immediate Attention Required"      
        body = f'''
            <html>
            <body style="font-family: Arial, sans-serif;">
                <p>Dear Bhuvana Krithika,</p>
                <p>We have received a new inquiry through our company website. Please find the details below:</p>
                
                <h3>Contact Information:</h3>
                <ul>
                    <li><strong>Name:</strong> {Name}</li>
                    <li><strong>Email:</strong> {mailId}</li>
                    <li><strong>Phone:</strong> {phone}</li>
                    <li><strong>Query:</strong> {message}</li>
                </ul>
                
                <p>We kindly request you to review the inquiry and respond at the earliest convenience to ensure a prompt and professional engagement with the prospect.</p>

                <p>Should you require any additional information or assistance, please do not hesitate to reach out.</p>
                
                <hr>
                
                <p>Best Regards,</p>
                <p><strong>VPEARL SOLUTIONS Digital Marketing Team</strong></p>
                
                <p>
                    🌐 <a href="https://vpearlsolutions.com/" target="_blank">Website</a> | 
                    🔗 <a href="https://www.linkedin.com/company/vpealsoutions/" target="_blank">LinkedIn</a> | 
                    📷 <a href="https://www.instagram.com/vpearl_solutions" target="_blank">Instagram</a> | 
                    📘 <a href="https://www.facebook.com/profile.php?id=61572978223085" target="_blank">Facebook</a>
                </p>
            </body>
            </html>
        ''' 

        msg.attach(MIMEText(body, 'html'))    
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_mailId, passKey)
            server.sendmail(sender_mailId, "bhuvaneswari.rm@vpearlsolutions.com", msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error in send_replay_mail_Job function: {str(   e)}")
        return False