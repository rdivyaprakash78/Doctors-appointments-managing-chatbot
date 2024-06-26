start_prompts = {

    "fallback_prompt"
    :
    """
    The bot has encountered a invalid or a wrong response from the reason.

    Here's the reason why : {reason}

    Ask the user to give a correct input based on the previous context of the conversation.
    """,

    "intent_classifier_prompt" 
    : 
    """
    You are an intent classifier LLM. Your job is to classify the question from the user into the following intent categories:
    1. Booking an appointment
    2. Getting information on booked appointment
    3. Cancelling an appointment
    4. Changing or editing a booked appointment.

    Here are the definition of each intents. You should classify the user's question as the following intents based on the definitions

    Booking an appointment : If the user (here patient) wishes to book a doctors appointment.

    Getting information on booked appointment : If the user wants to know more details about their booked appointment such as the timings, place and name of the doctor etc. 
    Make sure that they have already booked the appointment.

    Cancelling an appointment : If the user wish to cancel their booked appointment. To cancel an appointment, the user must have booked one before.

    Changing or editing a booked appointment : If the user wish to change their appointment date or time. The user must have made an appointment before to change ro edit it.
    Make sure that they have booked one before.

    other: Choose this if the user input doesn’t fall into any of the other intents.

    Your answer should be one of these exact words: "booking" or "getinfo" or "cancelling" or "editing" or "other"

    User input : {user_input}
    intent:
    """,

    "intent_confirmation_prompt" 
    :
    """
    The intention of the user has been computed as the intent: {intent}. Replying as the AI bot reconfirm 
    with the user that whether the computed intent is right or wrong.
    """,

    "intent_confirmation_response_prompt"
    :
    """
    Here's the users response : {response}. The user would have now confirmed their intent. From their response
    give me a yes or no answer. Just give me "yes" or "no" only.
    """
}

booking_prompts = {

    "get_date_prompt"
    :
    """
    The user wishes to book a doctors appointment.
    
    Here's the dates : {dates}
    
    Formulate your answer and reply as the bot replying to the user with the available dates. 
    Ask the user to choose a date from this according to their availability. 
     
    List the dates (date-month-year format) in the form of a natural language.
    """,

    "extracting_date_prompt"
    :
    """
    \n Here's the user chat: {user_chat}.

    Identify the date the user have picked from this list of dates : {dates}

    The user might have given the date directly or in a natural language. 
    Try to identify the date from the user response and convert it into YYYY-MM_DD format and return the date.
    If you find the response of the user to be inappropriate then return the phrase "fallback".

    For example the date : 2024-07-01 can be written in the following ways.

    1. 1.7
    2. 1st of july
    3. 1/7/24
    4. 2024-7-01
    5. July 1st
    6. 7.1.24
    7. 7/1/2024 etc.
    
    Note : Your output can be either a date in YYYY-MM-DD format or the phrase "fallback".
    
    """,

    "get_time_prompt"
    :
    """
    The user has now chosen the date and wish to book his appointment.
    
    You should now show the available appointments slots in the given date. The available slots for the chosen date
    is given in the form of this table : {string}.
    
    Convert the available slots result in the form of a natural language and reply to the user. Also ask the user to select the time slot
    and confirm the timeslot
    """,

    "extracting_time_prompt"
    :
    """Covert the user input: {user_chat} to 24 hours time format HH:MM:ss

    The time slot should one of the available time slots : {slots}

    Note : Here's an example of how the user can enter the time response
    
    For time slot 17:30:00 the user response can be in the following ways:

    1. 17.30
    2. 5.30
    3. 5:00 pm
    4. 5:30:00
    5. 17:30:00
    6. 17:30
    7. 17:30 pm
    8. 30 past 5
    9. 30 minutes past 17 hours etc.

    Understand the user response and convert the time in HH:MM:SS format and return the time value. 
    If you find the response from the user as inappropriate then return the phrase "fallback". 

    Note : your response should be either a time stamp in HH:MM:SS (24 hours format) or the phrase "fallback".""",

    "date_time_confirmation_prompt" 
    :
    """For the appointment booking the user has now entered his preferrable date and time slot.
    Reconfirm with the user that is it okay for them to book the appointment on date: {date} and time: {time}.
    
    Ask the user to confirm this date and time""",

    "date_time_confirmation_response_prompt"
    :
    """
    The user have given a confirmation for the chosen date and time. Here's the confirmation
    from the user : {user_chat}.
    
    Try to understand this response from the user. If the user has agreed to teh chosen date and time return "yes".
    Else return "no".
    
    Note : your output should be either "yes" or "no". 
    """,

    "user_registration_check_prompt" 
    :
    """Ask the user if they have registered with the clinic already or not.""",

    "regconf_prompt" 
    :
    """
    Here's the user's response {user_chat}
    
    Based on the user's input return a "yes" or "no" answer.
    
    If the user has already registered with the clinic return "yes". Else return "no". 
    """,

    "patient_registration_prompt"
    :
    """
    The user wishes to get registered with the clinic. Ask for the name of the user.

    """,

    "get_patname_prompt"
    :
    """
    the user have given his name in this phrase : {user_chat}.

    identify the name of the user from the phrase and return the name.

    Note : Your response should just be the name. If you cannot find any name return the text "fallback"
    """,

    "say_user_id_prompt"
    :
    """
    The user has now registered with the clinic. Here's the user id : {user_id}. Tell the user that their registration with the clinic is succesful
    and ask the user to take note of this id for future references.
    Also ask the user to enter any response to continue.
    """,

    "check_pname_prompt"
    :
    """
    When we checked the user id of the user in the database. The name of the user is found to be :{name}.
    Check with the user that whether it is right or wrong.
    """,

    "get_pov_prompt"
    :
    """
    From now on you should adress the user as {name}. Ask the user about their purpose of visit to the clinic.
    """,

    "get_pov_response_prompt"
    :
    """
        The user must have entered their purpose of visit to the doctor to book their appointment.
        Get the synopsis of the purpose and return a 3-4 letter phrase.

        Here's the user chat : {user_chat}
        
        Here are some example purpose of visits.
        
        'Allergy'
        'Back pain'
        'Check-up'
        'Cold'
        'Dry cough'
        'Fever'
        'Flu'
        'Headache'
        'Injury'
        'Sore throat'
        'Stomach bug'

        Return the purpose of visit.

        Purpose of visit:
    """,

    "get_patient_approval_prompt"
    :
    """
    Address the user as {name}.

    They want to book an appointment on {date} at {time} for the purpose of {pov}.
    Can you ask the user to confirm if we can proceed with booking the appointment?
    """,

    "get_patient_approval_reponse_prompt"
    :
    """
    The user has given his approval to book the appointment. Here's his response: {user_chat}

    From the response identify whether he has approved to book the appointment or not

    If he has approved to book return "yes" else return "no".

    Note: your response should be either the word "yes" or "no".
    """,

    "booking_confirmation_prompt"
    :
    """
    Address the user as {name}.

    Tell the user that the appointment has been booked on {date} at {time} and the purpose of visit is {pov}.

    Here's the appointment_id {appt_id}. Ask the user to make note of the appointment id for future references.

    Also ask the user if they want any other help enter any response to continue.
    """
}