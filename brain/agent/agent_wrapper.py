import logging 


class AgentWrapper():

     def __init__(self):
         pass 
    
     def _get_intent(self, user_input):
         return "intent"
         

     def run(self, user_input):
         intent =  self._get_intent(user_input=user_input)

         return f"results for command: {intent}"
         