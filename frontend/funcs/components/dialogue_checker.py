from .llm import LLM
class DialogueChecker:
    def __init__(self, dialogue_checker_name, dialogue_checker_description, dialogue_checker_prompt, query_list_generation_prompt=None, knowledge_base_id=None, model_id=None, max_tokens=8192, stop_sequences=[], temperature=0, region='us-east-1') -> None:
        self.llm = LLM(
            model_id=model_id,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            temperature=temperature,
            region=region
            )
        self.dialogue_checker_name = dialogue_checker_name
        self.dialogue_checker_description = dialogue_checker_description
        self.dialogue_checker_prompt = dialogue_checker_prompt
        self.query_list_generation_prompt = query_list_generation_prompt
        self.knowledge_base_id = knowledge_base_id
        