# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pickle
import csv

class SelectSymptoms(Action):
    # Capture symptom entered by user and add to list of symptoms
    def name(self) -> Text:
        return "action_select_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the selected option from the user's message
        symptom = tracker.get_slot('symptom')
        SlotSet("symptom", symptom)

        symptoms = tracker.get_slot("symptoms") or []

        dispatcher.utter_message(f"You selected {symptom}.")

        try:
            # Add the user symptom to symptoms_list
            symptoms.append(symptom)             
            
            num_symptoms = len(symptoms)

            # Repeat current symptoms to user
            if num_symptoms == 1:
                response = symptoms[0]
            else:
                response = ', '.join(symptoms[:-1]) + ' and ' + symptoms[-1]
            
            dispatcher.utter_message(f"You entered {num_symptoms} symptoms: {response}")

            if num_symptoms >= 5:
                dispatcher.utter_message(text="Are you experiencing anymore symptoms?")
            else:
                dispatcher.utter_message(text="Please insert {} more symptoms.".format((5-len(symptoms))))

            # Set the symptoms slot 
            return [SlotSet("symptoms", symptoms)]   
        except KeyError:
            dispatcher.utter_message(text="Please insert a valid symptom. Type \"show symptoms\" to see a list of symptoms. ")
    
class ActionPredictDisease(Action):
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get the symptoms entered by the user
        symptoms = tracker.get_slot("symptoms")

        # Check if the user has entered at least 5 symptoms
        if len(symptoms) < 5:
            dispatcher.utter_message(text="You have entered {} symptoms so far. To continue using the Symptom Checker, please enter at least 5 symptoms.".format((5-len(symptoms))))
            return[]
        else:
            # perform the disease prediction and return info about the disease
            # load pickled data
            with open("model.pkl", "rb") as f:
                model = pickle.load(f)

            #predict disease based off of pickled model
            predicted_disease = model.predict(symptoms)

            with open("symptom_description.csv", "r") as f:
                csvRead = csv.DictReader(f)
                for row in csvRead:
                    if row["Disease"] == predicted_disease:
                        disInfo = row["Description"]
                        dispatcher.utter_message(text=f"{predicted_disease} is a disease that {disInfo}")
                        break

            #Give the user a list of precautions to be aware of with their possible condition. 
            with open("symptom_precaution.csv", "r") as f:
                csvPrec = csv.DictReader(f)
                for row in csvPrec:
                    if  row["Disease"] == predicted_disease:
                        prec1 = row["Precaution_1"]
                        prec2 = row["Precaution_2"]
                        prec3 = row["Precaution_3"]
                        prec4 = row["Precaution_4"]
                        dispatcher.utter_message(f"When suffering from {predicted_disease} you must take care to: {prec1}, {prec2}, {prec3}, and {prec4}. /n The advice given by this chatbot is not intended as a replacement for professional medical advice. As with any medical issue, be sure to consult with your physician.")

            dispatcher.utter_message(text=f"What would you like to do now? You can enter new symptoms or learn about another disease.")

            # Set the prediction_made slot and reset the symptoms slot
            return [SlotSet("symptoms", [])]

class ActionClearSymptomsSlot(Action):
    def name(self) -> Text:
        return "action_clear_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Reset symptoms slot
        return [SlotSet("symptoms", []), SlotSet("symptom", None)] 

class SelectDiseases(Action):
    # Return information about a disease to user
    def name(self) -> Text:
        return "action_select_diseases"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Get the selected option from the user's message
            # Set the slot value to the selected option
            disease = tracker.get_slot('disease')
            SlotSet("disease", disease)


            dispatcher.utter_message(f"You selected {disease}.")
            with open("symptom_description.csv", "r") as f:
                csvRead = csv.DictReader(f)
                for row in csvRead:
                    if row["Disease"] == disease:
                        disInfo = row["Description"]
                        dispatcher.utter_message(f"Here is some more information about {disease}: /n {disInfo}")

            #Give the user a list of precautions to be aware of with their selected disease. 
            with open("symptom_precaution.csv", "r") as f:
                csvPrec = csv.DictReader(f)
                for row in csvPrec:
                    if  row["Disease"] == disease:
                        prec1 = row["Precaution_1"]
                        prec2 = row["Precaution_2"]
                        prec3 = row["Precaution_3"]
                        prec4 = row["Precaution_4"]
                        dispatcher.utter_message(f"When suffering from {disease} you must take care to: {prec1}, {prec2}, {prec3}, and {prec4}. /n The advice given by this chatbot is not intended as a replacement for professional medical advice. As with any medical issue, be sure to consult with your physician.")
            
            dispatcher.utter_message(f"What would you like to do next? You can insert a new disease or try the Symptom Checker.")
        except KeyError:
            dispatcher.utter_message(text=f"Please insert a valid disease. \nType \"show diseases\" to see a list of diseases.")
            return []
        