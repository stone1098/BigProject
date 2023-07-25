from django.shortcuts import render
from .forms import CarTextInputForm, CarTextOutputForm
from .models import CarTextInput, CarTextOutput
from accounts.models import User
from transformers import BertForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer
import numpy as np
from django.utils import timezone
import pandas as pd
import torch
import mlflow
# Create your views here.

def index(request):
    """Process test uploaded by users"""

    if request.method == 'POST' and request.user.is_authenticated:
        form = CarTextInputForm(request.POST)
        if form.is_valid():
            carTextInput = form.save(commit=False)
            carTextInput.user = request.user
            carTextInput.save()

            input_text = form.cleaned_data.get('accident_report')  # input_text 변수 추출
            predictions = predict_fault(input_text)

            carTextOutput = CarTextOutput(
                car_text_id = carTextInput,
                result = predictions
            )
            carTextOutput.save()

            output = {'ratio': predictions, 'complement': 100 - predictions}

            # 원하는 동작을 수행 (예: 결과를 데이터베이스에 저장, 다른 페이지로 리디렉션 등)

            return render(request, 'fault_ratio/merge.html', {'forms': form, 'result': output})
        
    form = CarTextInputForm()
    output = {'ratio': '"Fault Ratio"'}
    return render(request, 'fault_ratio/merge.html', {'forms': form, 'result': output})

# def predict_fault(data):
#     import os

#     os.environ["AWS_ACCESS_KEY_ID"] = "AKIA3COSUQZN5I5P2QOW"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
#     os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://s3.ap-northeast-2.amazonaws.com"
#     mlflow.set_tracking_uri("http://3.35.215.88:5000/")

#     model_uri = "models:/fault/production"

# # Load model as a PyFuncModel.
#     model = mlflow.pyfunc.load_model(model_uri)  
    
#     predictions=model.predict(data)
#     predict=round(predictions,2)*100
#     return int(predict)

def predict_fault(data):
    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

    model_path = 'fault_ratio/static/model/aivle_model_shuffle'
    model= BertForSequenceClassification.from_pretrained(model_path)
    input_text = data

    encoded_inputs = tokenizer.encode_plus(input_text, padding='max_length', max_length=500, truncation=True, return_tensors='pt')
    input_ids = encoded_inputs['input_ids']
    attention_mask = encoded_inputs['attention_mask']
    
    outputs = model(input_ids, attention_mask=attention_mask)

    predictions = outputs.logits.item()
    predict=round(predictions,2)*100
    return int(predict)
