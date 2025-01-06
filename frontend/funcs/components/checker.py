from .llm import LLM
class Checker:
    def __init__(self, checker_name, checker_description, checker_prompt, checker_time_limit, model_id, max_tokens=8192, stop_sequences=[], temperature=0, region='us-east-1') -> None:
        self.llm = LLM(
            model_id=model_id,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            temperature=temperature,
            region=region
            )
        self.checker_name = checker_name
        self.checker_prompt = checker_prompt
        self.checker_description = checker_description
        self.checker_time_limit = checker_time_limit