from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import auth
from .models import *
from friend.models import *
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def blood_pressure(request): # 上傳血壓測量結果!
    uid = request.user.id
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        systolic = data['systolic']
        diastolic = data['diastolic']
        pulse = data['pulse']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        try:
            Blood_pressure.objects.create(uid=uid, systolic=systolic, diastolic=diastolic, pulse=pulse, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}    
    return JsonResponse(output)

@csrf_exempt
def body_weight(request): # 上傳體重測量結果!
    uid = request.user.id
    print(uid)
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        weight = data['weight']
        body_fat = data['body_fat']
        bmi = data['bmi']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        try:
            Weight.objects.create(uid=uid, weight=weight, body_fat=body_fat, bmi=bmi, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}        
    return JsonResponse(output) 

@csrf_exempt
def blood_sugar(request): # 上傳血糖測量結果!
    uid = request.user.id
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        # timeperiod_list = ['晨起', '早餐前', '早餐後', '午餐前', '午餐後', '晚餐前', '晚餐後', '睡前']
        timeperiod = data['timeperiod']
        sugar = data['sugar']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        try:
            Blood_sugar.objects.create(uid=uid, sugar=sugar, timeperiod=timeperiod, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}        
    return JsonResponse(output)

@csrf_exempt
def diary_diet(request): # 飲食日記!
    uid = request.user.id
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        tag = request.POST.getlist("tag[][]")
        description = data['description']
        image = request.POST.get("image")
        lat = data['lat']
        lng = data['lng']
        # meal_list = ['早餐', '午餐', '晚餐']
        meal = data['meal']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        try:
            Diary_diet.objects.create(uid=uid, description=description, meal=meal, tag=tag, image_count=image, lat=lat, lng=lng, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0", "image_url":"http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"}     
    return JsonResponse(output,safe=False)

@csrf_exempt
def last_upload(request): # 最後上傳時間!
    uid = request.user.id
    upload = []
    if request.method == 'GET':
        if Blood_pressure.objects.filter(uid=uid):
            pre = Blood_pressure.objects.filter(uid=uid).latest('recorded_at')
            pre = str(pre.recorded_at)
            upload.append({"blood_pressure":pre})
        if Weight.objects.filter(uid=uid):
            wei = Weight.objects.filter(uid=uid).latest('recorded_at')
            wei = str(wei.recorded_at)
            upload.append({"weight":wei})
        if Blood_sugar.objects.filter(uid=uid):
            sug = Blood_sugar.objects.filter(uid=uid).latest('recorded_at')
            sug = str(sug.recorded_at)
            upload.append({"blood_sugar":sug})
        if Diary_diet.objects.filter(uid=uid):
            die = Diary_diet.objects.filter(uid=uid).latest('recorded_at')
            die = str(die.recorded_at)
            upload.append({"diet":die})
        output = {
            "status":"0", 
            "last_upload":upload
        }
    else:
        output = {"status":"1"}
    return JsonResponse(output)

@csrf_exempt
def records(request): # 上一筆紀錄資訊!+刪除日記記錄!
    uid = request.user.id
    output = {"status":"1"}
    if request.method == 'POST':
        if Blood_pressure.objects.filter(uid=uid):
            pre = Blood_pressure.objects.filter(uid=uid).latest('recorded_at')
            output["blood_pressures"] = {
                    "id":pre.id,
                    "user_id":pre.uid, 
                    "systolic":pre.systolic, 
                    "diastolic":pre.diastolic, 
                    "pulse":pre.pulse, 
                    "recorded_at":str(pre.recorded_at)
                }
        if Weight.objects.filter(uid=uid):
            wei = Weight.objects.filter(uid=uid).latest('recorded_at')
            output["weights"] = {
                    "id":wei.id,
                    "user_id":wei.uid,
                    "weight":wei.weight, 
                    "body_fat":wei.body_fat, 
                    "bmi":wei.bmi, 
                    "recorded_at":str(wei.recorded_at)
                }
        if Blood_sugar.objects.filter(uid=uid):
            sug = Blood_sugar.objects.filter(uid=uid).latest('recorded_at')
            output["blood_sugars"] = {
                    "id":sug.id,
                    "user_id":sug.uid,
                    "sugar":int(sug.sugar), 
                    "timeperiod":int(sug.timeperiod), 
                    "recorded_at":str(sug.recorded_at)
                }
        timeperiod_list = ['晨起', '早餐前', '早餐後', '午餐前', '午餐後', '晚餐前', '晚餐後', '睡前']
        diets = timeperiod_list[(int(request.POST.get('diets'))-1)%8]
        output = {"status":"0"}
    if request.method == 'DELETE':
        if request.GET.getlist("blood_pressures[]"):
            data_list = request.GET.getlist("blood_pressures[]")
            for data in data_list:
                Blood_pressure.objects.get(id=data).delete()
        if request.GET.getlist("weights[]"):
            data_list = request.GET.getlist("weights[]")
            for data in data_list:
                Weight.objects.get(id=data).delete()
        if request.GET.getlist("blood_sugars[]"):
            data_list = request.GET.getlist("blood_sugars[]")
            for data in data_list:
                Blood_sugar.objects.get(id=data).delete()
        if request.GET.getlist("diets[]"):
            data_list = request.GET.getlist("diets[]")
            for data in data_list:
                Diary_diet.objects.get(id=data).delete()
        output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def diary_list(request): # 日記列表資料!
    uid = request.user.id
    date = request.GET.get("date")
    diary = []
    if date:
        if Blood_pressure.objects.filter(uid=uid, date=date):
            blood_pressures = Blood_pressure.objects.filter(uid=uid, date=date)
            for blood_pressure in blood_pressures:
                r = {
                        "id":blood_pressure.id,
                        "user_id":blood_pressure.uid, 
                        "systolic":blood_pressure.systolic,
                        "diastolic":blood_pressure.diastolic,
                        "pulse":blood_pressure.pulse,
                        "recorded_at":str(blood_pressure.recorded_at),
                        "type":"blood_pressure"
                    }
                diary.append(r)
        if Weight.objects.filter(uid=uid, date=date):
            weights = Weight.objects.filter(uid=uid, date=date)
            for weight in weights:
                r = {
                        "id":weight.id,
                        "user_id":weight.uid,
                        "weight":weight.weight,
                        "body_fat":weight.body_fat,
                        "bmi":weight.bmi,
                        "recorded_at":str(weight.recorded_at),
                        "type":"weight"
                    }
                diary.append(r)
        if Blood_sugar.objects.filter(uid=uid, date=date):
            blood_sugars = Blood_sugar.objects.filter(uid=uid, date=date)
            for blood_sugar in blood_sugars:
                r = {
                        "id":blood_sugar.id,
                        "user_id":blood_sugar.uid, 
                        "sugar":int(blood_sugar.sugar), 
                        "timeperiod":int(blood_sugar.timeperiod), 
                        "recorded_at":str(blood_sugar.recorded_at),
                        "type":"blood_sugar"
                    }
                diary.append(r)
        if Diary_diet.objects.filter(uid=uid, date=date):
            diary_diets = Diary_diet.objects.filter(uid=uid, date=date)
            for diary_diet in diary_diets:
                if UserCare.objects.filter(uid=uid, date=date):
                    reply = UserCare.objects.filter(member_id=0, date=date).latest('updated_at')
                    r = {
                            "id":diary_diet.id,
                            "user_id":diary_diet.uid, 
                            "description":diary_diet.description, 
                            "meal":int(diary_diet.meal), 
                            "tag":diary_diet.tag, 
                            "image":diary_diet.image_count,
                            "type":"diet",
                            "location":
                                {
                                    "lat":diary_diet.lat,
                                    "lng":diary_diet.lng
                                },
                            "recorded_at":str(diary_diet.recorded_at),
                            "reply":reply.message
                        }
                else:
                    r = {
                            "id":diary_diet.id,
                            "user_id":diary_diet.uid, 
                            "description":diary_diet.description, 
                            "meal":int(diary_diet.meal), 
                            "tag":diary_diet.tag, 
                            "image":diary_diet.image_count,
                            "type":"diet",
                            "location":
                                {
                                    "lat":diary_diet.lat,
                                    "lng":diary_diet.lng
                                },
                            "recorded_at":str(diary_diet.recorded_at),
                        }
                diary.append(r)
        output = {"status":"0", "diary":diary}      
    else:
        output = {"status":"1"}
    # print(json.dumps(output))
    return JsonResponse(output)

@csrf_exempt
def care(request): # 送出關懷諮詢!+獲取關懷諮詢!
    uid = request.user.id
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = {"status":"1"}
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        message = data['message']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        friend_list = Friend_data.objects.filter(uid=uid, status=1)
        for friend_data in friend_list:
            UserCare.objects.create(uid=uid, member_id=friend_data.friend_type, reply_id=friend_data.relation_id, message=message, updated_at=recorded_at)
        output = {"status":"0"}
    if request.method == 'GET':
        usercares = UserCare.objects.filter(reply_id=uid)
        cares = []
        for usercare in usercares:
            r = {
                    "id":usercare.id,
                    "user_id":usercare.uid,
                    "member_id":usercare.member_id,
                    "reply_id":usercare.reply_id,
                    "message":usercare.message,
                    "created_at":str(usercare.created_at),
                    "updated_at":str(usercare.updated_at)
                }
            cares.append(r)
        output = {"status":"0", "cares":cares}
    return JsonResponse(output)
