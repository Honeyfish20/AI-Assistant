class LLM:
    def __init__(self, model_id, max_tokens=8192, stop_sequences=[], temperature=0, region='us-east-1') -> None:
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.stop_sequences = stop_sequences
        self.temperature = temperature
        self.region = region