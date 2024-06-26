from datetime import datetime
import regex as re

class general_functions:

    def dates_string(self, result):

        result = result.replace(" ", "")
        result = result[1:]
        split = result.split("),")
        
        cleaned = []
        for i in range(len(split)):
            if(i%2==0):
                cleaned.append(split[i][15:])

        dates = []
        for i in cleaned: 
            date = datetime.strptime(i, '%Y,%m,%d')
            date = date.strftime('%Y-%m-%d')
            dates.append(date)

        dates
        dates_str = []

        for i in dates:
            dates_str.append(str(i))

        return dates_str

    def time_string(self, result):

        result = result.replace(" ", "")
        result = result.replace("(", "")
        result = result.replace(")", "")
        result = result.replace("'","")
        result = result[1:]


        split = result.split(",")

        cleaned = []
        for i in range(len(split)):
            if(i%2==0):
                cleaned.append(split[i])

        return cleaned

    def is_patient_id(id):
        pattern = r"PAT\d{3}"
        match = re.match(pattern,id)

        if match:
            is_id = True
            matches = re.findall(pattern,id)
            return_value = matches[0]
        else:
            is_id= False
            return_value = "The value you have entered is invalid. Try entering a valid patient id"

        return is_id, return_value