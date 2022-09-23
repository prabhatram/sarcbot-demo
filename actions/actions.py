# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import sqlite3


#def clean_name(name):
#    return "".join([c for c in name if c.isalpha()])

class ValidateOrderNumberForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_number_form"

    def validate_order_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        
        # If the name is super short, it might be wrong.
        order = slot_value
        print(f"Order number = {order} length = {len(order)}")
        if len(order) == 0:
            dispatcher.utter_message(text="Shouldn't your order number be made of actual order number?")
            return {"order_number": None}
        elif len(order) < 4:
            dispatcher.utter_message(text="That order number is way too short. How about you provide me a 4-character order number?")
            return {"order_number": None}
        elif len(order) > 4:
            dispatcher.utter_message(text="That order number is way too long. How about you provide me a 4-character order number?")
            return {"order_number": None}
        
        return {"order_number": order}
        #return f"Good job at providing a proper order number {(order)}."

# class QueryOrderDetails(Action):

#     def name(self) -> Text:
#         return "query_order_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         """
#         Runs a query using only the order ID column, outputs an utterance 
#         to the user w/ the relevent 
#         information for one of the returned rows.
#         """
#         conn = DbQueryingMethods.create_connection(db_file="sarcdb/SarcbotDB.db")

#         slot_value = tracker.get_slot("order_number")

#         get_query_results = DbQueryingMethods.select_by_slot(conn=conn,slot_value=slot_value)
        
#         dispatcher.utter_message(text=str(get_query_results))

#         return 


# class DbQueryingMethods:
#     def create_connection(db_file):
#         """ 
#         create a database connection to the SQLite database
#         specified by the db_file
#         :param db_file: database file
#         :return: Connection object or None
#         """
#         conn = None
#         try:
#             conn = sqlite3.connect(db_file)
#         except Error as e:
#             print(e)

#         return conn

#     def select_by_slot(conn, slot_value):
#         """
#         Query all rows in the Orders table
#         :param conn: the Connection object
#         :return:
#         """
#         cur = conn.cursor()
#         cur.execute(f'''SELECT EstimatedDeliveryDate from Orders
#                     WHERE OrderID="{slot_value}"''')

#         # return an array
#         deliveryDate = cur.fetchall()

#         if len(list(deliveryDate)) < 1:
#             return "There is no such order number."
#         else:
#             for row in deliveryDate:
#                 return f"Looks like your order will be delivered by {(row[0])}."