# SageMaker Configuration
SAGEMAKER_CONFIG = {
    'ENDPOINT': {
        'NAME': 'gpt-sovits-sagemaker-endpoint',  # 你的实际endpoint名称
        'REGION': 'us-west-2'
    },
    'AUDIO': {
        'BUCKET': 'sagemaker-us-west-2-134927008626',
        'REFERENCE_WAV': 's3://sagemaker-us-west-2-134927008626/gpt-sovits/wav_ref/ref-4.wav',
        'SAMPLE_RATE': 32000
    },
    'TEXT': {
        'DEFAULT_LANGUAGE': 'zh',
        'CUT_PUNCTUATION': ',，.。:：!！\"\"\'\'',
    }
} 