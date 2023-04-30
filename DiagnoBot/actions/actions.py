# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet, FollowupAction, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pickle
import csv


class ValidateSymptomCheckerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_symptom_checker_form"

    def validate_multiOption_slot(
        self,
        slot_name: str,
        valid_values: List[str],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate slots that can have multiple values"""
        if tracker.get_intent_of_latest_message() == "deny":
            return {slot_name: "complete"}

        gathered_symptoms = tracker.get_slot("symptoms") or []
        entities = tracker.latest_message.get("entities")
        selected_symptoms = list(set([entity['value'].lower() for entity in entities if entity['entity'] == 'symptom']))

        valid_symptoms = []
        invalid_symptoms = []

        for symptom in selected_symptoms:
            if symptom in valid_values:
                if symptom not in gathered_symptoms:
                    gathered_symptoms.append(symptom)
                    valid_symptoms.append(symptom)
                else:
                    dispatcher.utter_message(text="You have already entered " + symptom + ".")
            else:
                invalid_symptoms.append(symptom)

        if invalid_symptoms:
            dispatcher.utter_message(text="I'm sorry. " + ", ".join(invalid_symptoms).capitalize() + " " + ("are not listed options." if len(invalid_symptoms) > 1 else "is not a listed option."))
            dispatcher.utter_message(text="Please choose a valid option or type \"None\".")
            return {slot_name: None}

        if valid_symptoms:
            dispatcher.utter_message(text="Saving symptom" + ("" if len(valid_symptoms) == 1 else "s") + ": " + ", ".join(valid_symptoms) + "...")
            return {"symptoms": gathered_symptoms, slot_name: "complete"}
        else:
            print("unkown user message in validation form")
            dispatcher.utter_message(text="No new symptoms detected. Please choose a valid option or type \"None\".")
            return {slot_name: None}
        
    def validate_boolOptions_slot(
        self,
        slot_name: str,
        symptom: str,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate boolean slots."""
        if tracker.get_intent_of_latest_message() == "deny":
            return {slot_name: "complete"}

        if tracker.get_intent_of_latest_message() == "affirm":
            symptoms = tracker.get_slot("symptoms") or []
            if symptom not in symptoms:
                symptoms.append(symptom)
            else:
                dispatcher.utter_message(text="You have already answered this question.")
            return {"symptoms": symptoms, slot_name: "complete"}
        dispatcher.utter_message(text="I'm sorry. I didn't get that. Please enter \"Yes\" or \"No\".")
        return {slot_name: None}

    def validate_flu_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `flu_symptoms` value."""
        FLU_SYMPTOMS = ["dehydration", "fatigue", "high fever", "loss of smell", "mild fever", "shivering", "sweating", "weight loss",
                "chills", "malaise"]
        return self.validate_multiOption_slot("flu_symptoms", FLU_SYMPTOMS, dispatcher, tracker, domain)

    def validate_respiratory_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `respiratory_symptoms` value."""
        RESPIRATORY_SYMPTOMS = ["cough", "rusty sputum", "breathlessness"]
        return self.validate_multiOption_slot("respiratory_symptoms", RESPIRATORY_SYMPTOMS, dispatcher, tracker, domain)
        
    def validate_gastro_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `gastro_symptoms` value."""
        GASTRO_SYMPTOMS = ["constipation", "diarrhea", "nausea", "vomiting", "swelling of stomach", "loss of appetite", "acidity"]
        return self.validate_multiOption_slot("gastro_symptoms", GASTRO_SYMPTOMS, dispatcher, tracker, domain)
        
    def validate_neuro_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `neuro_symptoms` value."""
        NEURO_SYMPTOMS = ["coma", "headache", "irritability", "lack of concentration", "loss of balance", "muscle weakness", 
                          "painful walking", "slurred speech", "stiff neck", "unsteadiness", "altered sensorium"]
        return self.validate_multiOption_slot("neuro_symptoms", NEURO_SYMPTOMS, dispatcher, tracker, domain)
        
    def validate_body_pain_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `body_pain_symptoms` value."""
        BODY_PAIN_SYMPTOMS = ["joints pain", "knee pain", "muscle pain", "neck pain", "pain in anal region", "abdominal pain", "stomach pain", "chest pain"]
        return self.validate_multiOption_slot("body_pain_symptoms", BODY_PAIN_SYMPTOMS, dispatcher, tracker, domain)
        
    def validate_skin_nails_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `skin_nails_symptoms` value."""
        SKIN_NAILS_SYMPTOMS = ["bruising", "itching", "nodal skin eruptions", "pus filled pimples", "red spots over body", "skin rash",
                               "small dents in nails", "yellow crust ooze", "yellowish skin", "brittle nails"]
        return self.validate_multiOption_slot("skin_nails_symptoms", SKIN_NAILS_SYMPTOMS, dispatcher, tracker, domain)
        
    def validate_internal_itching_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `internal_itching_symptoms` value."""
        return self.validate_boolOptions_slot("internal_itching_symptoms", "internal itching", dispatcher, tracker, domain)
        
    def validate_appearance_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `appearance_symptoms` value."""
        APPEARANCE_SYMPTOMS = ["yellowing of eyes", "patches in throat"]
        return self.validate_multiOption_slot("appearance_symptoms", APPEARANCE_SYMPTOMS, dispatcher, tracker, domain)
    
    def validate_reproductive_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `reproductive_symptoms` value."""
        return self.validate_boolOptions_slot("reproductive_symptoms", "abnormal menstruation", dispatcher, tracker, domain)
        
    def validate_urinary_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `urinary_symptoms` value."""
        URINARY_SYMPTOMS = ["dark urine", "spotting urination", "bladder discomfort", "polyuria"]
        return self.validate_multiOption_slot("urinary_symptoms", URINARY_SYMPTOMS, dispatcher, tracker, domain)

    def validate_unsterile_injections_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `unsterile_injections_symptoms` value."""
        return self.validate_boolOptions_slot("unsterile_injections_symptoms", "receiving unsterile injections", dispatcher, tracker, domain)
        
    def validate_family_history(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `family_history` value."""
        return self.validate_boolOptions_slot("family_history", "family history", dispatcher, tracker, domain)
    
class ConfirmSymptoms(Action):
    def name(self) -> Text:
        return "action_confirm_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Return all symptoms collected from user."""

        symptoms = tracker.slots.get("symptoms")

        if not symptoms:
            dispatcher.utter_message(text="You did not enter any symptoms.")
        else:
            symptom_list = "\n".join([f"- {symptom}" for symptom in symptoms])
            message = f"Your symptoms are:\n{symptom_list}\n\nDo you want to submit your symptoms to receive a predicted disease or start over?"
            buttons = [{"title": "Start Over", "payload": "/start_over"}, {"title": "Submit", "payload": "/affirm"}]
            dispatcher.utter_message(text=message, buttons=buttons)
        return []
    
class ResetSymptoms(Action):
    def name(self) -> Text:
        return "action_reset_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Reset the symptoms slot to None."""

        return [AllSlotsReset(), FollowupAction("symptom_checker_form")]
    
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
            # slot_sets.append(FollowupAction("symptom_checker_form"))
            return [AllSlotsReset(), SlotSet("symptoms", symptoms), FollowupAction("symptom_checker_form")]
        else:
            # perform the disease prediction and return info about the disease
            # load pickled data
            #with open("model.pkl", "rb") as f:
                #model = pickle.load(f)

            #predict disease based off of pickled model
            predicted_disease = "Acne"

            with open("symptom_description.csv", "r") as f:
                csvRead = csv.DictReader(f)
                for row in csvRead:
                    if row["Disease"].lower() == predicted_disease.lower():
                        disInfo = row["Description"]
                        predicted_disease = predicted_disease.title()
                        dispatcher.utter_message(f"Here is some more information about {predicted_disease}: \n {disInfo}")
                        break

            #Give the user a list of precautions to be aware of with their possible condition. 
            with open("symptom_precaution.csv", "r") as f:
                csvPrec = csv.DictReader(f)
                for row in csvPrec:
                    if  row["Disease"].lower() == predicted_disease.lower():
                        prec1 = row["Precaution_1"]
                        prec2 = row["Precaution_2"]
                        prec3 = row["Precaution_3"]
                        prec4 = row["Precaution_4"]
                        dispatcher.utter_message(f"When suffering from {predicted_disease} you must take care to: {prec1}, {prec2}, {prec3}, and {prec4}.")
                        dispatcher.utter_message(text="The advice given by this chatbot is not intended as a replacement for professional medical advice. As with any medical issue, be sure to consult with your physician.")

        message = f"What would you like to do now?"
        buttons = [{"title": "Try the Symptom Checker again", "payload": "/start_over"}, {"title": "Learn about another disease", "payload": "/select_diseases"}]
        dispatcher.utter_message(text=message, buttons=buttons)
        return []
        
class SelectDiseases(Action):
    # Return information about a disease to user
    def name(self) -> Text:
        return "action_select_diseases"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        diseases = {
            "infectious diseases": ["chicken pox", "common cold", "dengue", "hepatitis a", "hepatitis b", "hepatitis c", "hepatitis d", 
                               "hepatitis e", "malaria", "tuberculosis", "typhoid", "urinary tract infection"],
            "cardiovascular diseases": ["heart attack", "hypertension"],
            "endocrine diseases": ["diabetes", "hypoglycemia", "hypothyroidism"],
            "gastrointestinal diseases": ["alcoholic hepatitis", "chronic cholestasis",  "gerd", "peptic ulcer diseae"],
            "hematological diseases": ["dimorphic hemmorhoids piles"],
            "musculoskeletal diseases": ["arthritis", "cervical spondylosis", "osteoarthristis"],
            "neurological diseases": ["migraine", "paralysis brain hemorrhage", "vertigo paroymsal positional vertigo"],
            "respiratory diseases": ["bronchial asthma", "pneumonia"],
            "skin diseases": ["acne", "allergy", "drug reaction", "fungal infection", "gastroenteritis", "hyperthyroidism", 
                         "impetigo", "jaundice", "psoriasis", "varicose veins"]
        }

        entities = tracker.latest_message.get("entities")
        value = list({entity['value'].lower() for entity in entities if entity['entity'] == 'disease'})

        for disease in value:
            for category in diseases:
                if disease.lower() == category.lower():
                    buttons = []
                    for x in diseases[category]:
                        disease_payload = '{{"disease": "{}"}}'.format(x)
                        payload = "/select_diseases{}".format(disease_payload)
                        button = {"title": x.title(), "payload": payload}
                        buttons.append(button)


                    message = f"Please select a disease from the list below:"
                    dispatcher.utter_message(text=message, buttons=buttons)
                    return []
                if disease.lower() in diseases[category]:
                    dispatcher.utter_message(f"You selected {disease}.")
                    with open("symptom_description.csv", "r") as f:
                        csvRead = csv.DictReader(f)
                        for row in csvRead:
                            if row["Disease"].lower() == disease.lower():
                                disInfo = row["Description"]
                                disease = disease.title()
                                dispatcher.utter_message(f"Here is some more information about {disease}: \n {disInfo}")

                    #Give the user a list of precautions to be aware of with their selected disease. 
                    with open("symptom_precaution.csv", "r") as f:
                        csvPrec = csv.DictReader(f)
                        for row in csvPrec:
                            if  row["Disease"].lower() == disease.lower():
                                prec1 = row["Precaution_1"]
                                prec2 = row["Precaution_2"]
                                prec3 = row["Precaution_3"]
                                prec4 = row["Precaution_4"]
                                dispatcher.utter_message(f"When suffering from {disease} you must take care to: {prec1}, {prec2}, {prec3}, and {prec4}.")
                                dispatcher.utter_message(text="The advice given by this chatbot is not intended as a replacement for professional medical advice. As with any medical issue, be sure to consult with your physician.")

                    return [FollowupAction("utter_default_menu")]

        buttons = []
        for category in diseases.keys():
            disease_payload = '{{"disease": "{}"}}'.format(category)
            payload = "/select_diseases{}".format(disease_payload)
            button = {"title": category.capitalize(), "payload": payload}
            buttons.append(button)


        message = f"Please select a category from the list below:"
        dispatcher.utter_message(text=message, buttons=buttons)

        return []

        