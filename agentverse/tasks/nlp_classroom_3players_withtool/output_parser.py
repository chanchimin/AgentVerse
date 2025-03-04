from __future__ import annotations

import re
from typing import Union

from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish

from agentverse.parser import OutputParseError, output_parser_registry


@output_parser_registry.register("nlp_classroom_3players_withtool")
class NlpClassroom3PlayersWithtoolParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:

        cleaned_output = text.strip()
        cleaned_output = re.sub(r'\n+', '\n', cleaned_output)
        cleaned_output = cleaned_output.split('\n')
        if not (len(cleaned_output) == 3 and 
                cleaned_output[0].startswith("Thought:") and
                cleaned_output[1].startswith("Action:") and 
                cleaned_output[2].startswith("Action Input:")):
            raise OutputParseError(text)
        action = cleaned_output[1][len("Action:"):].strip()
        action_input = cleaned_output[2][len("Action Input:"):].strip()
        if action in ["Speak"]:
            return AgentFinish({"output": action_input}, text)
        elif action == "CallOn":
            return AgentFinish({"output": "[CallOn] " + action_input}, text)
        elif action == "RaiseHand":
            return AgentFinish({"output": "[RaiseHand] " + action_input}, text)
        elif action == "Listen":
            return AgentFinish({"output": ""}, text)
        else:
            return AgentAction(action.lower(), action_input, text)
