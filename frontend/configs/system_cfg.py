cfg_LLM_kwargs = {
    "anthropic.claude-3-sonnet-20240229-v1:0": {
                            "temperature": 0,
                            "top_p": 1,
                            "top_k": 250,
                            "max_tokens": 8191,
                            "stop_sequences": ["Human:", "</result>"],
                            "anthropic_version": "" 
                            },
    "anthropic.claude-3-haiku-20240307-v1:0": {
                            "temperature": 0,
                            "top_p": 1,
                            "top_k": 250,
                            "max_tokens": 8191,
                            "stop_sequences": ["Human:", "</result>"],
                            "anthropic_version": "" 
                            },
    "anthropic.claude-v2": {
                            "temperature": 0,
                            "top_p": 1,
                            "top_k": 250,
                            "max_tokens_to_sample": 8191,
                            "stop_sequences": ["Human:", "</result>"]
                            },
    "anthropic.claude-v2:1": {
                            "temperature": 0,
                            "top_p": 1,
                            "top_k": 250,
                            "max_tokens_to_sample": 8191,
                            "stop_sequences": ["Human:", "</result>"]
                            },
    "anthropic.claude-instant-v1": {
                            "temperature": 0,
                            "top_p": 1,
                            "top_k": 250,
                            "max_tokens_to_sample": 8191,
                            "stop_sequences": ["Human:", "</result>"]
                            }
    }

cfg_modes = {
    "Readme": "",
    "Role Assistant": "",
    "Dialogue Check Assistant": "",
}