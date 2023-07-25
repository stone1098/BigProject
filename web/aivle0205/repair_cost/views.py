from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import CarImageInputForm, CarImageOutputForm
from .models import CarImageInput, CarImageOutput
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from io import BytesIO

import numpy as np
import pandas as pd
import joblib
import os
import mlflow
import cv2
from PIL import Image

from sklearn.preprocessing import OneHotEncoder
# Create your views here.

def index(request):

    if request.method == 'POST' and request.FILES and request.user.is_authenticated:

        form = CarImageInputForm(request.POST, request.FILES)

        if form.is_valid():
            carImageInput = form.save(commit=False)
            carImageInput.user = request.user
            carImageInput.img = request.FILES['img']
            carImageInput.save()
            
            path = carImageInput.img.path
            
            result = predict_part(path)
            scratch_arr = result[0]
            parts_arr = np.array(result[1][1])
            layered = result[2]
                        
            scratch_list = compare_image(scratch_arr, parts_arr)
            
            data = pd.DataFrame(columns=['name','product_date','part',])
            car_company = request.POST['car_company']
            car_type = request.POST['car_type']
            product_date = int(request.POST['car_year'])
            
            cost_data = pd.DataFrame({
                'name', 'product_date', 'part'
            })
            
            for part in scratch_list:
                temp = pd.DataFrame({
                    'name': car_type,
                    'product_date': product_date,
                    'part': part
                }, index=[0])
                data = pd.concat([data, temp], ignore_index=True)
            
            cost_data = predict_cost(data)
            cost_dict = cost_data.to_dict()
            
            carImageOutput = CarImageOutput(
                car_image_id = carImageInput,
                car_company = car_company,
                car_type = car_type,
                car_year = product_date,
                result_part = cost_dict['part'],
                result_cost = cost_dict['cost'],
            )
            temp_image = BytesIO()
            layered.save(temp_image, format='JPEG')
            temp_image.seek(0)
            carImageOutput.result_img.save(f'{carImageInput.img.name}.jpg', ContentFile(temp_image.read()))
            carImageOutput.save()
            
            parts = ' '.join(list(carImageOutput.result_part.values()))
            cost = round(sum(list(carImageOutput.result_cost.values())))
            cost = format(cost, ',d')
            
            return render(request, 'repair_cost/merge.html', {'forms': form, 'carImageOutput': carImageOutput, 'parts': parts, 'cost' : cost})
    
    else:
        form = CarImageInputForm()
        default_output = {'cost': '"Repair Cost"'}

    return render(request,'repair_cost/merge.html', {'forms': form, 'result': default_output})

def predict_cost(data):
    # 파트를 인식하여 수리비용 예측
    encoder = joblib.load('repair_cost/static/model/encoder.pkl')
    model = joblib.load('repair_cost/static/model/LGBM.pkl')
    
    cost = data.copy()
    cost = encoder.transform(cost)
    
    pred = model.predict(cost)
    data['cost'] = pred
    
    return data

def predict_part(path):
    os.environ["SM_FRAMEWORK"] = "tf.keras"
    
    os.environ["AWS_ACCESS_KEY_ID"] = "AKIA3COSUQZN5I5P2QOW"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://s3.ap-northeast-2.amazonaws.com"
    
    mlflow_uri = "http://3.35.215.88:5000/"
    mlflow.set_tracking_uri(mlflow_uri)

    scratch_url = 'runs:/b8027d5a28ae41ac83530cf2ae5b8786/model_scratch_layered'
    scratch_model = mlflow.pyfunc.load_model(scratch_url)
    
    parts_url = 'runs:/9f7034f3df59452392995a9bdf367a1c/model_parts_resize'
    parts_model = mlflow.pyfunc.load_model(parts_url)
    
    scratch, layered = scratch_model.predict(path)
    parts = parts_model.predict(path)
    
    return scratch, parts, layered

def compare_image(scratch_arr, parts_arr):
    scratch_list = []

    parts_cc_dict = {
        '뒷범퍼': [255 , 0 , 0],
        '뒷도어': [32, 178, 170],
        '뒷도어': [0, 255, 255],
        '앞범퍼': [0, 255 , 0],
        '앞도어': [85, 107, 47],
        '앞도어': [0, 191, 255],
        '트렁크': [255, 255, 0],
    }
    
    for parts, colors in parts_cc_dict.items():
        part_copy = parts_arr.copy()
        mask = np.all(part_copy == colors, axis=2)

        part_copy[~mask] = [0, 0, 0]

        img1_gray = cv2.cvtColor(part_copy, cv2.COLOR_BGR2GRAY)
        # img2_gray = cv2.cvtColor(scratch_arr, cv2.COLOR_BGR2GRAY)
        if np.logical_and(img1_gray, scratch_arr).sum() > 2500:
            scratch_list.append(parts)
            
    return scratch_list