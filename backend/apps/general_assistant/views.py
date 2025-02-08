from rest_framework import viewsets
from rest_framework.views import APIView, View
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from asgiref.sync import sync_to_async
from asyncio import ensure_future
import asyncio
import boto3
from frontend.configs.sagemaker_config import SAGEMAKER_CONFIG

from .models import UserPrompt
from .serializers import UserPromptSerializer
from .bedrock_utils import streaming_chat_feishu
from .feishu_utils import AESCipher, TokenManager, LarkMsgSender

from django.http import StreamingHttpResponse, HttpResponse, JsonResponse

class UserPromptViewSet(viewsets.ModelViewSet):
    queryset = UserPrompt.objects.all()
    serializer_class = UserPromptSerializer
    

        
# Feishu setting 
app_id = "cli_a692712a82799013"
app_secret = "X8qGkLY9jV5kRVhmsOcTEbP8lc7TGbv2"
verification_token = "3X6wZbD6eYlLp0xMSC6gnd76GJqRNBfB"
encryption_key = "XwIEv6YHtsccvLjramOD4gTI3IzKxuJU"

cipher = AESCipher(encryption_key)
users_info = {}
token_manager = TokenManager(app_id=app_id, app_secret=app_secret)
sender = LarkMsgSender(token_manager)
        
class ChatFeishuView(View):
    permission_classes = []

    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        cipher = AESCipher(encryption_key)

        try:
            parsed_data = json.loads(cipher.decrypt_string(data['encrypt']))
        except:
            return HttpResponse('Parsing Error')

        if 'challenge' in parsed_data:
            return JsonResponse({'challenge': parsed_data['challenge']})

        if 'event' in parsed_data and 'message' in parsed_data['event'] and 'content' in parsed_data['event']['message']:
            content = json.loads(parsed_data['event']['message']['content'])
            
            if 'text' in content:
                user_id = parsed_data['event']['sender']['sender_id']['user_id']
                user_prompt = await sync_to_async(UserPrompt.objects.get, thread_sensitive=True)(id=1)
                prompt = content['text']
                messages = []
                messages.append({"role": "user", "content": prompt})
                model_id = await sync_to_async(lambda: user_prompt.model_id.model_id, thread_sensitive=True)()
                model_region = await sync_to_async(lambda: user_prompt.model_id.region, thread_sensitive=True)()

                loop = asyncio.get_event_loop()
                future = ensure_future(streaming_chat_feishu(
                    system_prompt=user_prompt.system_prompt,
                    messages=messages,
                    model_id=model_id,
                    model_region=model_region,
                    max_tokens=user_prompt.max_tokens,
                    stop_sequences=user_prompt.stop_sequences,
                    temperature=user_prompt.temperature,
                    sender=sender,
                    user_id=user_id,
                ))
        return JsonResponse({'message': 'ok'})

class GeneralAssistantViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def chat_with_audio(self, request):
        """处理带音频输出的对话请求"""
        try:
            # 1. 处理LLM响应
            llm_response = self.process_llm_request(request.data)
            
            # 2. 生成语音
            audio_response = self.generate_audio(llm_response)
            
            return Response({
                'text': llm_response,
                'audio': audio_response
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def generate_audio(self, text):
        """调用SageMaker端点生成音频"""
        runtime_client = boto3.client(
            'sagemaker-runtime',
            region_name=SAGEMAKER_CONFIG['ENDPOINT']['REGION']
        )
        
        request = {
            "refer_wav_path": SAGEMAKER_CONFIG['AUDIO']['REFERENCE_WAV'],
            "prompt_text": text[:50],
            "prompt_language": SAGEMAKER_CONFIG['TEXT']['DEFAULT_LANGUAGE'],
            "text": text,
            "text_language": SAGEMAKER_CONFIG['TEXT']['DEFAULT_LANGUAGE'],
            "output_s3uri": "",
            "cut_punc": SAGEMAKER_CONFIG['TEXT']['CUT_PUNCTUATION']
        }
        
        response = runtime_client.invoke_endpoint_with_response_stream(
            EndpointName=SAGEMAKER_CONFIG['ENDPOINT']['NAME'],
            ContentType='application/json',
            Body=json.dumps(request)
        )
        
        return self.process_audio_response(response)



         
                