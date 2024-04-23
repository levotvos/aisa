from typing import List
import guidance
from guidance import gen, select, one_or_more

@guidance
def ner_instruction(model, text, few_shot_examples = "",):
   
    instruction_text = f"""
    Collect all named entities into a JSON list from the following text!
    {few_shot_examples}
    ---
    Input: {text}
    Output: [{one_or_more('"' + gen('entities', list_append=True, stop='"') + select(['"','", ']))}]
    """
    return model + instruction_text

@guidance(stateless=True)
def labeler(model, labels: List[str]):
    return model + select(options=labels, name="label")
 
