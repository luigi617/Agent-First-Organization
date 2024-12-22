import requests
import logging
from dotenv import load_dotenv

import langsmith as ls

from agentorg.utils.trace import TraceRunName

load_dotenv(override=True)
logger = logging.getLogger(__name__)


class NLU:
    def __init__(self, url):
        self.url = url

    def execute(self, text:str, intents:dict, chat_history_str:str, metadata:dict) -> str:
        logger.info(f"candidates intents by using NLU API: {intents}")
        data = {
            "text": text,
            "intents": intents,
            "chat_history_str": chat_history_str
        }
        response = requests.post(self.url, json=data)
        with ls.trace(name=TraceRunName.NLU, inputs=data) as rt:
            rt.end(
                outputs=response.json(),
                metadata={"conv_id": metadata.get("conv_id"), "turn_id": metadata.get("turn_id")}
            )
        if response.status_code == 200:
            results = response.json()
            pred_intent = results['intent']
            logger.info(f"pred_intent is {pred_intent}")
        else:
            pred_intent = "others"
            logger.error('Remote Server Error when predicting NLU')

        
        return pred_intent
    

class SlotFilling:
    def __init__(self, url):
        self.url = url

    def execute(self, text:str, slots:list, chat_history_str:str, metadata: dict) -> dict:
        logger.info(f"extracted slots: {slots}")
        data = {
            "text": text,
            "slots": slots,
            "chat_history_str": chat_history_str
        }
        response = requests.post(self.url, json=data)
        with ls.trace(name=TraceRunName.SlotFilling, inputs=data) as rt:
            rt.end(
                outputs=response.json(),
                metadata={"conv_id": metadata.get("conv_id"), "turn_id": metadata.get("turn_id")}
            )
        if response.status_code == 200:
            pred_slots = response.json()
            logger.info(f"pred_slots is {pred_slots}")
        else:
            pred_slots = slots
            logger.error('Remote Server Error when predicting Slot Filling')

        
        return pred_slots
