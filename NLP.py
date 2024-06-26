from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from prompts import start_prompts, booking_prompts
from queries import queries
from api_key import api_key
import regex as re
from general_functions import general_functions as gf

safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

llm = ChatGoogleGenerativeAI(model = "gemini-pro", google_api_key=api_key, temperature= 0.00001,safety_settings=safety_settings)
funcs = gf() #creating an instance of general functions

mysql_uri = 'mysql+pymysql://root:root@127.0.0.1:3306/doctors_appointments'
db = SQLDatabase.from_uri(mysql_uri)

class start:

    history = """You are conversational Generative AI chatbot. Your function is to assist the users with booking, editing
        and deleting with doctors appointment. Also you assist the users to get information about their booked appointments.
        The chat history with the user and you so far is shown below.
        
        Note : While returning your response just return your response dont add prefixes like "AI: " or "Bot : "  or "Assistant : " """

    def __init__(self):
        pass

    def fallback(self, reason, func):
        fallback_template = str(start.history) + start_prompts["fallback_prompt"]
        fallback_prompt = PromptTemplate(input_variables=["reason"],template = fallback_template)
        fallback_chain = (
            fallback_prompt
            | llm
            | StrOutputParser()
        )

        response = fallback_chain.invoke({"reason" : reason})
        start.history = str(start.history) + "\n\n bot : " + response

        return response, func 

    def intent_classifier(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat

        intent_classification_template = start_prompts["intent_classifier_prompt"]
        intent_classification_prompt = PromptTemplate(input_variables=["user_chat"], template=intent_classification_template)
        
        response_chain = (
            intent_classification_prompt
            | llm
            | StrOutputParser()
        )

        self.intent = response_chain.invoke({"user_input" : user_chat})

        if(self.intent == "other"):
            reason = """
            The user has entered an intent that's out of the scope of the functionality of the chatbot.
            Tell the user that you can only assist with booking, cancelling, editing and getting information of 
            a booked appointment.
            """
            text, function = self.fallback(reason, self.intent_classifier)
            return text, function
        
        else:
            intent_confirmation_template = str(start.history) + start_prompts["intent_confirmation_prompt"]
            intent_confirmation_prompt = PromptTemplate(input_variables=["intent"], template=intent_confirmation_template)
            
            intent_confirmation_chain = (
                intent_confirmation_prompt
                | llm
                | StrOutputParser()
            )

            confirmation = intent_confirmation_chain.invoke({"intent" : user_chat})
            start.history = str(start.history) + "\n\n bot : " + confirmation

            self.state = "intent_confirmation_response"
            return confirmation, self.intent_confirmation_response
    
    def intent_confirmation_response(self, user_chat):
        
        start.history = str(start.history) + "\n\n user : " + user_chat

        intent_confirmation_response_template = str(start.history) + start_prompts["intent_confirmation_response_prompt"]
        intent_confirmation_response_prompt = PromptTemplate(input_variables=["response"], template=intent_confirmation_response_template)

        intent_confirmation_response_chain = (
            intent_confirmation_response_prompt
            | llm
            | StrOutputParser()
        )

        intent_confirmation_response = intent_confirmation_response_chain.invoke({"response" : user_chat})

        if (intent_confirmation_response == "yes"):
            if(self.intent == "booking"):
                booking_ = booking()
                text, function = booking_.get_date()
                return text, function
            

class booking(start):

    def __init__(self):
        super().__init__()
        self.date_string = ""
        self.response_table = ""
        self.booking_date = ""
        self.time_string = ""
        self.booking_time = ""
        self.patient_id = ""
        self.name=""
        self.pov =""
        self.appointment_id = ""

    def get_date(self):
        query = queries["date_fetch_query"]
        self.response_table = db.run(query)

        self.date_string = funcs.dates_string(self.response_table) #calling the date string formatting function from general functions

        get_date_template = str(start.history) + booking_prompts["get_date_prompt"]
        get_date_prompt = PromptTemplate(input_variables=["dates"], template = get_date_template)

        get_date_chain = (
            get_date_prompt
            | llm
            | StrOutputParser()
        )

        response = get_date_chain.invoke({"dates":self.date_string})
        self.date_response = response
        start.history = start.history + "\n\n bot : " + response

        return response, self.get_date_response
    
    def get_date_response(self, user_chat):
        start.history = start.history + "\n\n user : " + user_chat
        extracting_date_template = str(start.history) + booking_prompts["extracting_date_prompt"]
        extracting_date_prompt = PromptTemplate(input_variables=["user_chat", "dates"], template = extracting_date_template)

        extracting_date_chain = (
            extracting_date_prompt
            | llm
            | StrOutputParser()
        )

        date = extracting_date_chain.invoke({"user_chat": user_chat, "dates" : self.date_string})

        if date in self.date_string:
            date = date
        else:
            date = "fallback"

        if date != "fallback":
            self.booking_date = date
            text, function = self.get_time()
            return text, function
        else:
            reason = """The user have entered a wrong date. (user's response : {response}) 
            Either that's not in the available dates (Available dates : {dates} ) or an invalid input 
            Ask the user to enter a correct date from this list."""
            reason = reason.format(response = user_chat, dates = self.date_string)
            text, function = self.fallback(reason, self.get_date_response)
            start.history = str(start.history) + "\n\n bot : " + text
            return text, function
        
    def get_time(self):
        date = self.booking_date
        query = queries["time_fetch_query"].format(date=date)
        result = db.run(query)

        self.time_string = funcs.time_string(result)

        get_time_prompt = PromptTemplate(input_variables=["string"],template=booking_prompts["get_time_prompt"])
        get_time_chain = (
        get_time_prompt
        | llm
        | StrOutputParser()
        )   

        response = get_time_chain.invoke({"string" : self.time_string})
        start.history = str(start.history) + "\n\n bot : " + response
        return response, self.get_time_response
    
    def get_time_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        extracting_time_template = str(start.history) + booking_prompts["extracting_time_prompt"]
        extracting_time_prompt = PromptTemplate(input_variables = ["user_chat", "slots"], template = extracting_time_template)
        extracting_time_chain = (
            extracting_time_prompt
            | llm
            | StrOutputParser()
        )

        response = extracting_time_chain.invoke({"slots" : self.time_string,"user_chat" : user_chat})

        if response in self.time_string:
            self.booking_time = str(response)
            text,function  = self.date_time_confirmation()
            return text, function
        else:
            reason = """The user has entered a invalid response (The response : {response}) when asked to choose a time slot or has entered 
            a time slot that's not in the available slots : {slots}. Ask the user to reenter the correct time slot."""
            reason = reason.format(response = user_chat, slots = self.time_string )
            text, function  = self.fallback(reason, self.get_time_response)
            start.history = str(start.history) + "\n\n bot : " + text
            return text, function
        
    def date_time_confirmation(self):
        date_time_confirmation_template = str(start.history) + booking_prompts["date_time_confirmation_prompt"]
        date_time_confirmation_prompt = PromptTemplate(input_variables=["date", "time"], template=date_time_confirmation_template)
        date_time_confirmation_chain = (
            date_time_confirmation_prompt
            | llm
            | StrOutputParser()
        )

        response = date_time_confirmation_chain.invoke({"date" : self.booking_date, "time" : self.booking_time})

        start.history = str(start.history) + "\n\n bot : " + response

        return response, self.date_time_confirmation_response
    
    def date_time_confirmation_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        confirmation_response_template = str(start.history) +booking_prompts["date_time_confirmation_response_prompt"]
        confirmation_response_prompt = PromptTemplate(input_variables=["user_chat"], template=confirmation_response_template)
        confirmation_response_chain = (
            confirmation_response_prompt
            | llm
            | StrOutputParser()
        )

        response = confirmation_response_chain.invoke({"user_chat" : user_chat})

        if response == "yes":
            text, function = self.registration_confirmation()
            return text, function
        else :
            text, function = self.get_date()
            return text, function
        
    def registration_confirmation(self):
        registration_confirmation_template = booking_prompts["user_registration_check_prompt"]
        registration_confirmation_prompt = PromptTemplate(input_variables=[""], template=registration_confirmation_template)
        registration_confirmation_chain = (
            registration_confirmation_prompt
            | llm
            | StrOutputParser()
        )

        response = registration_confirmation_chain.invoke({})
        start.history = str(start.history) + "\n\n bot  : " + response
        return response, self.regconf_response
    
    def regconf_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        regconf_response_template = str(start.history) + booking_prompts["regconf_prompt"]
        regconf_response_prompt = PromptTemplate(input_variables=["user_chat"], template=regconf_response_template)
        regconf_response_chain = (
            regconf_response_prompt
            | llm
            | StrOutputParser()
        )

        response = regconf_response_chain.invoke({"user_chat" : user_chat})

        if response == "yes":
            text, function = self.get_patient_id()
            return text, function
        else:
            text, function = self.patient_registration()
            return text, function
        
    def get_patient_id(self):
        response = "Enter your patient id"
        start.history = str(start.history) +  "\n\n bot : " + response       
        return response, self.get_patient_id_response
    
    def get_patient_id_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        response = user_chat.upper()

        is_id, id = gf.is_patient_id(response)

        if is_id:
            text, function = self.check_patid(id)
            return text, function
        else:
            text = "The response that you have given is invalid. Enter a valid one."
            start.history = str(start.history) + "\n\n bot : " + text
            return text, self.get_patient_id_response
    
    def check_patid(self,id):
        query = queries["patient_id_check_query"].format(id=id)
        result = db.run(query)

        if(result == ""):
            text = "You have entered a patient id that does not exist in our database recheck your id and enter a valid one"
            start.history = str(start.history) + "\n\n bot : " + text
            return text, self.get_patient_id_response
        else:
            self.patient_id = id
            text, function = self.check_name()
            return text, function
        
    def check_name(self):
        query = queries["get_pname_query"]
        query = query.format(id=self.patient_id)
        result = db.run(query)
        name = result[3:-4]
        self.name = name
        check_name_template = str(start.history) + booking_prompts["check_pname_prompt"]
        check_name_prompt = PromptTemplate(input_variables=["name"], template=check_name_template)
        check_name_chain = (
            check_name_prompt
            | llm
            | StrOutputParser()
        )

        response = check_name_chain.invoke({"name" : name})
        start.history = str(start.history) + "\n\n bot  : " + response 
        return response, self.check_name_response
    
    def check_name_response(self, user_chat):
        check_response_template =str(start.history) + booking_prompts["regconf_prompt"]
        check_response_prompt = PromptTemplate(input_variables=["user_chat"], template = check_response_template)
        check_response_chain = (
            check_response_prompt
            | llm
            | StrOutputParser()
        )
        
        response = check_response_chain.invoke({"user_chat" : user_chat})

        if response == "yes":
            text, function = self.get_pov(user_chat)
            return text, function
        else:
            text = "Apologies for the mistake. Try re entering your patient id"
            return text, self.get_patient_id_response
    
    def patient_registration(self):
        response = "Can you enter your name to proceed with the registration?"
        start.history = str(start.history) + "\n\n bot : " + response
        return response, self.get_pat_name
    
    def get_pat_name(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        get_patname_template  = str(self.history)+ booking_prompts["get_patname_prompt"]
        get_patname_prompt = PromptTemplate(input_variables=["user_chat"], template=get_patname_template)
        get_patname_chain =(
            get_patname_prompt
            | llm
            | StrOutputParser()
        )
        response = get_patname_chain.invoke({"user_chat" : user_chat})

        if(response != "fallback"):
            self.name = response
            text, function = self.register_patient()
            return text, function
        else:
            reason = "The user has not entered a name. Please ask the user to enter his/her name to continue their registration process"
            text, function = self.fallback(reason, self.get_pat_name)
            return text, function
        
    def register_patient(self):
        query = queries["new_user_reg_query"]
        result = db.run(query)
        self.patient_id = result[3:9]
        
        say_user_id_template = str(start.history) + booking_prompts["say_user_id_prompt"]
        say_user_id_prompt = PromptTemplate(input_variables=["user_id"], template=say_user_id_template)
        say_user_id_chain = (
            say_user_id_prompt
            | llm
            | StrOutputParser()
        )

        response = say_user_id_chain.invoke({"user_id" : self.patient_id})
        start.history = str(start.history) + "\n\n bot  : " + response
        return response, self.get_pov
        
    def get_pov(self,user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        get_pov_template = str(start.history) + booking_prompts["get_pov_prompt"]
        get_pov_prompt = PromptTemplate(input_variables=["name"], template=get_pov_template)
        get_pov_chain = (
            get_pov_prompt
            | llm
            | StrOutputParser()
        )

        response = get_pov_chain.invoke({"name" : self.name})
        start.history = str(start.history) + "\n\n bot  : " + response
        return response, self.get_pov_response
    
    def get_pov_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat
        get_pov_response_template =str(start.history)+ booking_prompts["get_pov_response_prompt"]
        get_pov_response_prompt = PromptTemplate(input_variables=["user_chat"], template = get_pov_response_template)
        get_pov_response_chain = (
            get_pov_response_prompt
            | llm
            | StrOutputParser()
        )

        response = get_pov_response_chain.invoke({"user_chat": user_chat})
        self.pov = response

        text, function = self.get_patient_approval()
        return text, function
    
    def get_patient_approval(self):
        date = self.booking_date
        time = self.booking_time
        name = self.name
        pov = self.pov

        get_patient_approval_template = str(start.history) + booking_prompts["get_patient_approval_prompt"]
        get_patient_approval_prompt = PromptTemplate(input_variables=["name", "date", "time","pov"], template=get_patient_approval_template)
        get_patient_approval_chain =(
            get_patient_approval_prompt
            | llm
            | StrOutputParser()
        )

        response = get_patient_approval_chain.invoke({"name": name, "date" : date, "time": time, "pov":pov})
        start.history = str(start.history) + "\n\n bot : " + response 
        return response, self.get_patient_approval_response

    def get_patient_approval_response(self, user_chat):
        start.history = str(start.history) + "\n\n user : " + user_chat 
        template = str(start.history)+ booking_prompts["get_patient_approval_reponse_prompt"]
        prompt = PromptTemplate(input_variables=["user_chat"], template=template)
        chain = (
            prompt
            | llm
            | StrOutputParser()
        )

        response = chain.invoke({"user_chat" : user_chat})

        if response == "yes" : 
            text, function = self.book_appointment()
            return text, function
        else:
            reason = """The user changed the mind. Help them from the start once again. Here are the available dates:{dates}"""
            text, function = self.fallback(reason, self.get_date_response)
            return text, function

    def book_appointment(self):
        date = self.booking_date
        time = self.booking_time
        name = self.name
        pov = self.pov
        pat_id = self.patient_id

        appt_id_query = queries["get_new_appointmentid"]
        result = db.run(appt_id_query)
        self.appointment_id = result[3:10]
        appt_id = self.appointment_id

        sno_query = queries["get_new_sno"]
        result = db.run(sno_query)
        sno = result[2:-3]

        appointment_booking_query = queries["appointment_booking_query"].format(sno=sno, appt_id = appt_id, pat_id =pat_id , name=name, date=date, time=time, pov=pov)
        result = db.run(appointment_booking_query)

        appointment_booking_template = str(start.history) + booking_prompts["booking_confirmation_prompt"]
        appointment_booking_prompt = PromptTemplate(input_variables=["name", "date","time", "pov","appt_id"], template=appointment_booking_template)
        appointment_booking_chain = (
            appointment_booking_prompt
            | llm
            | StrOutputParser()
        )

        response = appointment_booking_chain.invoke({"name" : name, "date" : date,"time": time, "pov":pov, "appt_id":appt_id})
        start.history = str(start.history) + "\n\n bot : " + response
        
        return response, self.reset

    def reset(self, user_chat):
        text = """
        Hello I'm a doctors appointment managing chatbot. I can help you with 
        booking, editing and cancelling your appointments. Along with this I can also get information
        about already booked appointments.

        How can I help you today ?"""

        return text, self.intent_classifier

        

        
        



        