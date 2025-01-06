from .llm import LLM
class Skill:
    def __init__(self, skill_name, skill_description, skill_examples, skill_checker, model_id, max_tokens=8192, stop_sequences=[], temperature=0, region='us-east-1') -> None:
        self.llm = LLM(
            model_id=model_id,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            temperature=temperature,
            region=region
            )
        self.skill_name = skill_name
        self.skill_description = skill_description
        self.skill_examples = skill_examples
        self.skill_checker = skill_checker
        