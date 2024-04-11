import streamlit as st
import os
import google.generativeai as genai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re


st.title("FusionXperience")


os.environ['GOOGLE_API_KEY'] = "AIzaSyAKy0DBzkk0lyMtaZym9KilBjq4SjTOg_4"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

eventtype=st.text_input("Enter the event type")
if eventtype.lower() == 'birthday':
    age = st.text_input("Enter the age of the birthday person")

attendies=st.number_input("Enter the number of event attendies")
budget=st.number_input("Enter the budget you have")
eventlocation=st.text_input("Enter the location of event")
email=st.text_input("Enter the email you want to send the itinerary to")

if "@" not in email:
    st.write("Please enter a valid email")
    st.stop()

input_prompt=f"""


You are a event planning expert tasked with planning a trip for a traveler. The traveler has provided you with the following details:

- Event type: [type of event whether it is a birthday or marriage or any other event]
- Attendies: [Number of attendies user is expecting]
- Budget: [Budget Amount in indian rupees]
- Location: [event location]

Your task is to create a full fledged plan of event for the user, suggesting cuisine and other options like vendors, decoration type that the user can have within the given budget. Additionally, recommend some suggestions that people use for the respective event with the provided budget and attendies.

Your itinerary should include a list of suggested cuisine, decoration suggetions, vendor options(if compatible with budget), return gift according to event, as well as estimated costs for each activity. Be sure to consider the traveler's interests and preferences when planning the itinerary.

Remember that the cost on each suggestion should be a specific portion of overall budget. The suggestions should not exceed the given budget at any cost. also the overall estimated cost(with addition of a cuisine suggestion estimated cost, decoration estimated cost, vendor estimated cost etc) should also be less that the given budget. Remember this very carefully!!
Once you have created the itinerary, present it in the following format:

1. Cuisine suggestion:
-suggestion 1: with its estimated cost per dish as well as for total event(remember that the cost should be resonable with respect to the event budget)
-suggestion 2: with its estimated cost per dish as well as for total event
-suggestion 3: with its estimated cost per dish as well as for total event
remember that the total cost for cuisine should not be more that half of the total budget

2. Decoration suggestion:
-suggestion 1: with its estimated cost(remember that the cost should be resonable with respect to the event budget)
-suggestion 2: with its estimated cost
-suggestion 3: with its estimated cost
 calculate total cost that can go for the respective suggestion in that suggestion itself.


3. vendor suggestion(choose only food vendors like icecream or snack etc. only if its possible at the available budget):
-suggestion 1: with its estimated cost(remember that the cost should be resonable with respect to the event budget)
-suggestion 2: with its estimated cost
-suggestion 3: with its estimated cost
 calculate total cost that can go for the respective suggestion in that suggestion itself.


4. What can be more efficent to use the budget
[Explain your answer here. write total calculation of above suggestions. also what can be the effective way that the money can be used effectively and need less expandeture.].

5.What are cuisine and vendor options available according to the location of user.

if the event is birthday, tell what can be the return gifts that can be provided and estimated cost for it with the specification of gift and that too keeping the budget in mind.

6.extra suggestions:
write some one liner suggestions here:

"""

input=f'Eventtype: {eventtype}, Attendies: {attendies} attendies, Budget: {budget} rupees, Location{eventlocation}'

model = genai.GenerativeModel('gemini-pro')


ans=''
if st.button("Generate plan and Send Via Mail"):
    response = model.generate_content(f'Consider the following prompt: {input_prompt} and make a one like for{input}')
    st.write(response.text)
    ans=response.text
    
    i=1
    pdf_filename = f"example{i}.pdf"
    i+=1
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    content=[]
    for t in response.text.split("**"):
        content.append(Paragraph(t,))

    
    doc.build(content)

    print(f"PDF created successfully: {pdf_filename}")
    
    smtp_port = 587                 
    smtp_server = "smtp.gmail.com"  

    # Set up the email lists
    email_from = "legionofcode11@gmail.com"
    email_list = [email]

    
    pswd = "onsk hxnu qnhf jzdr" 


    # name the email subject
    subject = "EventPlan for you...By FusionExperience..."


    def send_emails(email_list):

        for person in email_list:

            
            body = f"""
            Event Plan for you....By Us...
            """

            
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = person
            msg['Subject'] = subject

            
            msg.attach(MIMEText(body, 'plain'))

            
            
            attachment= open(pdf_filename, 'rb')  

            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + pdf_filename)
            msg.attach(attachment_package)

            
            text = msg.as_string()

            print("Connecting to server...")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls()
            TIE_server.login(email_from, pswd)
            print("Succesfully connected to server")
            print()


            
            print(f"Sending email to: {person}...")
            TIE_server.sendmail(email_from, person, text)
            print(f"Email sent to: {person}")
            print()
        
        TIE_server.quit()

    send_emails(email_list)



        







