from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from .models import *
from django.core.mail import send_mail
import uuid , base64 , json ,string
from random import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .token import email_token
from django.core.mail import send_mail
import string
from datetime import datetime
from friend.models import *  ##
from body.models import * ##
from django.contrib.sessions.models import Session
from .form import PersonalDefaultForm

@csrf_exempt
def send(request):#傳送驗證信
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="utf-8").replace("%40","@")
        try:
            token = email_token()
            acn = str(data).split("=")[1]
            token_s = token.generate_validate_token(acn)
            title = "普元血糖帳號驗證"
            meg ="\n".join(["{0}歡迎使用普元血糖app".format(acn),
            "請點選下列連結完成註冊:\n",
            "/".join(['127.0.0.1:8000/api/check',token_s])])
            send_mail(title,meg,'ya0933632810@gmail.com',[acn])
            message = {'status':'0'}
        except:
            message = {'status':'1'}
        return JsonResponse(message)

@csrf_exempt
def check(request,token): #信箱驗證
    if request.method == "POST":
        try:
            data = request.body
            data = str(data, encoding="utf-8")
            data = json.loads(data)
            email = data['email']
            username = data['account']
            # token_use = email_token()
            # acn = token_use.confirm_validate_token(token)
            user = UserProfile.objects.get(username=username)
            user.emailck = True
            user.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
                
        return JsonResponse(message)

@csrf_exempt
def index(request): # 首頁
    return render(request, 'index.html')

@csrf_exempt
def register(request): #註冊頁面
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        # userck = UserProfile.objects.all()
        random = Random()
        # check = bool(True)
        # while check:
        #     invite_code = "".join(random.sample('0123456789',6))
        #     try:
        #         ck = UserProfile.objects.get(invite_code=invite_code)
        #     except:
        #         check = False
        # try:
        if 1:
            account = data['account']
            password = data['password']
            email = data['email']
            invite_code = "".join(random.sample('0123456789',6))
            time = datetime.now()
            timeprint = datetime.strftime(time,"%Y-%m-%d %H:%M:%s")
            uid = uuid.uuid3(uuid.NAMESPACE_DNS,account)
            user = UserProfile.objects.create_user(uid=uid,username=account,email=email,FBck=False,emailck=False,invite_code=invite_code,created_at=timeprint,updated_at=timeprint)
            user.set_password(password)
            user.save()
            abc= UserProfile.objects.get(uid=uid)
            id_number = abc.id
            UserSet.objects.create(uid=uid,name=account,privacy_policy=0,email=email,verified=0,must_change_password=True,login_times=0,created_at=timeprint,updated_at=timeprint)
            deflat.objects.create(uid=uid,created_at=timeprint,updated_at=timeprint)
            Friend.objects.create(uid=id_number,invite_code=invite_code)
            medicalinformation.objects.create(uid=uid,created_at=timeprint)
            Notification.objects.create(uid=uid)
            HbA1c.objects.create(uid=uid)
            message = {"status": "0"}
        # except:
        #     message = {"status": "1"}
        return JsonResponse(message)

@csrf_exempt
def login(request): # 登入
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        try:
            account = data['account']
            password = data['password']
            user = UserProfile.objects.get(username=account)
            auth_obj = auth.authenticate(request,username=account,password=password)
            if auth_obj:
                request.session.create()
                auth.login(request, auth_obj)
            message = {"status": "0",
            "token":request.session.session_key
            }
        except:
            message = {"status": "1"}

        return JsonResponse(message)

@csrf_exempt
def forgot(request): #找回密碼
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        
        try:
            email = data['email']
            user = UserProfile.objects.get(email=email)
            UserSet = UserSet.objects.get(uid=user.uid)
            user = str(user)
            chars=string.ascii_letters+string.digits
            user = UserProfile.objects.get(username=username)
            newpassword = ''.join([choice(chars)for i in range(4)])
            user.set_password(newpassword)
            UserSet.must_change_password = True
            user.save()
            UserSet.save()
            title = "找回密碼"
            meg ="\n".join(["歡迎".format(user.username),
            "新的密碼為:\n",newpassword])
            send_mail(title,meg,'ya0933632810@gmail.com',[email])
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)

@csrf_exempt
def reset(request): #重設密碼
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        s = Session.objects.get(
            pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()
        
        user = UserProfile.objects.get(id=s['_auth_user_id'])
        userset = UserSet.objects.get(uid=user.uid)
        try:
            new_pw = data['password']
            user.set_password(new_pw)
            userset.must_change_password = False
            user.save()
            userset.save()

            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)


@csrf_exempt
def default(request): # 個人預設值
    message = {"status":"1"}
    try:
        uid = request.user.uid
        user = deflat.objects.get(uid=uid)
        if request.method == 'PATCH':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            f = PersonalDefaultForm(data)
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user, i, filtered[i])
                        print(7777777777777)
                    user.save()
                message = {"status":"0"}
    except:
        pass
    return JsonResponse(message)

@csrf_exempt
def userdata(request):
    if request.method == 'PATCH':  #個人設定上傳
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        user = UserSet.objects.get(uid=uid)
        try:
            user.after_recording = data['after_recording']
            user.no_recording_for_a_day = data['no_recording_for_a_day']
            user.over_max_or_under_min = data['over_max_or_under_min']
            user.after_mael = data['after_mael']
            user.unit_of_sugar = data['unit_of_sugar']
            user.unit_of_weight = data['unit_of_weight']
            user.unit_of_height = data['unit_of_height']
            user.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message,safe=False)
@csrf_exempt
def sett(request): 
    if request.method == 'PATCH':  #個人資訊上傳
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        user = UserSet.objects.get(uid=uid)
        try:
            user.name = data['name']
            user.birthday = data['birthday']
            user.height = data['height']
            user.gender = data['gender']
            user.address = data['address']
            user.weight = data['weight']
            user.phone = data['phone']
            user.email = data['email']
            user.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message,safe=False)

    if request.method == 'GET':   # 個人設定展示
        s = Session.objects.all()[0]
        s.expire_date
        s = Session.objects.get(
           pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()
        # s = Session.objects.get(pk=request.GET['token']).get_decoded()#postman
        UserProfiledata = UserProfile.objects.get(id=s['_auth_user_id'])
        UserSetdata = UserSet.objects.get(uid=UserProfiledata.uid)
        Userdeflat = deflat.objects.get(uid=UserProfiledata.uid)
        try:
            message = {
            "status":"0",
            "user":{
            "id":UserProfiledata.id, 
            "name":UserSetdata.name,
            "account":UserSetdata.name,
            "email":UserSetdata.email,
            "phone":UserSetdata.phone,
            "fb_id":UserProfiledata.fb_id,
            "status":UserSetdata.status,
            "group":UserSetdata.group,
            "birthday":UserSetdata.birthday,
            "height":UserSetdata.height,
            "weight":UserSetdata.weight,
            "gender":UserSetdata.gender,
            "address":UserSetdata.address,
            "unread_records":[int(UserSetdata.unread_records_one),UserSetdata.unread_records_two,int(UserSetdata.unread_records_three)],
            "verified":int(UserSetdata.verified),
            "privacy_policy":UserSetdata.privacy_policy,
            "must_change_password":1 if UserSetdata.must_change_password else 0,
            "fcm_id":UserSetdata.fcm_id,
            "badge":int(UserSetdata.badge),
            "login_time":int(UserSetdata.login_times),
            "created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")},
            "default":{
            "id": UserProfiledata.id,
            "user_id": Userdeflat.uid,
            "sugar_delta_max": int(Userdeflat.sugar_dalta_max),
            "sugar_delta_min":int(Userdeflat.sugar_delta_min),
            "sugar_morning_max": int(Userdeflat.sugar_morning_max),
            "sugar_morning_min": int(Userdeflat.sugar_morning_min),
            "sugar_evening_max": int(Userdeflat.sugar_evening_max),
            "sugar_evening_min": int(Userdeflat.sugar_evening_min),
            "sugar_before_max": int(Userdeflat.sugar_before_max),
            "sugar_before_min": int(Userdeflat.sugar_before_min),
            "sugar_after_max": int(Userdeflat.sugar_after_max),
            "sugar_after_min":int(Userdeflat.sugar_after_min),
            "systolic_max": int(Userdeflat.systolic_max),
            "systolic_min": int(Userdeflat.systolic_min),
            "diastolic_max": int(Userdeflat.diastolic_max),
            "diastolic_min":int(Userdeflat.diastolic_min),
            "pulse_max": int(Userdeflat.pulse_max),
            "pulse_min":int(Userdeflat.pulse_min),
            "weight_max": int(Userdeflat.weight_max),
            "weight_min": int(Userdeflat.weight_min),
            "bmi_max": int(Userdeflat.bmi_max),
            "bmi_min": int(Userdeflat.bmi_min),
            "body_fat_max": int(Userdeflat.body_fat_max),
            "body_fat_min": int(Userdeflat.body_fat_min),
            "created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")},
            "setting":{
            "id": UserProfiledata.id,
            "user_id":Userdeflat.uid,
            "after_recording": int(UserSetdata.after_recording),
            "no_recording_for_a_day": int(UserSetdata.no_recording_for_a_day),
            "over_max_or_under_min": int(UserSetdata.over_max_or_under_min),
            "after_meal":int(UserSetdata.after_mael),
            "unit_of_sugar": int(UserSetdata.unit_of_sugar),
            "unit_of_weight": int(UserSetdata.unit_of_weight),
            "unit_of_height": int(UserSetdata.unit_of_height),
            "created_at":datetime.strftime(UserSetdata.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strftime(UserSetdata.updated_at ,"%Y-%m-%d %H:%M:%S")
            }}
            message = message
        except:
            message = {"status":"1"}
        return JsonResponse(message,safe=False)

@csrf_exempt
def logout(request): # 登出
    auth.logout(request)
    return HttpResponseRedirect('api/login')

@csrf_exempt
def newnews(request): #最新消息
    if request.method == 'GET':
        # s = Session.objects.get(
        #     pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()
        # user = UserProfile.objects.get(id=s['_auth_user_id'])
        user = UserProfile.objects.get(id=2)
        UserSetdata = UserSet.objects.get(uid=user.uid)
        Notificationdata = Notification.objects.get(uid=UserSetdata.uid)

        try:
            message = {
            'status':'0',
            'news':{
                # 'id':UserProfiledata.id,
                # 'member_id':Notificationdata.member_id,    
                # 'group':UserSetdata.group,        
                # 'message':Notificationdata.message,  
                # 'pushed_at':datetime.strftime(UserSetdata.pushed_at ,"%Y-%m-%d %H:%M:%S"),
                # 'created_at':datetime.strftime(UserSetdata.created_at ,"%Y-%m-%d %H:%M:%S"), 
                # 'updated_at':datetime.strftime(UserSetdata.updated_at ,"%Y-%m-%d %H:%M:%S")
                "id": 2,
                "member_id": 1,
                "group": 1,
                "message": "456",
                "pushed_at": "2017-11-16 16:33:06",
                "created_at": null,
                "updated_at": null
                }
            }
        except:
            message = {'status':'1'}
        
        return JsonResponse(message)

@csrf_exempt
def Medical_information(request):   
    if request.method == 'GET': #就醫資訊展示
        uid = request.user.uid
        medicalinformationdata = medicalinformation.objects.get(uid=uid)
        UserProfiledata = UserProfile.objects.get(uid=uid)
        try:
            message = {
            "status":"0",
            "medical_info":{
            "id":int(UserProfiledata.id),
            "user_id":int(UserProfile.id),
            "diabetes_type":int(medicalinformationdata.diabetes_type),
            "oad":int(medicalinformationdata.oad),
            "insulin":int(medicalinformationdata.insulin),
            "anti_hypertensivers":int(medicalinformationdata.anti_hypertensivers),
            "created_at":datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at":datetime.strftime(UserProfiledata.updated_at ,"%Y-%m-%d %H:%M:%S")
            }}
            message = message

        except:
            message = {'status':'1'}
        return JsonResponse(message,safe=False)

    if request.method == 'PATCH': #就醫資訊新增
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        
        user = medicalinformation.objects.get(uid=uid)
        try:
            user.user_id = data['account']
            user.diabetes_type = data['diabetes_type']
            user.oad = data['oad']
            user.insulin = data['insulin']
            user.anti_hypertensivers = data['anti_hypertensivers']
            user.save()
            # time = datetime.now()
            # timeprint = datetime.strftime(time,"%Y-%m-%d %H:%M:%s")
            # user.updated_at = updated_at
            status = {"status":"0"}
        except:
            status = {"status":"1"}
        return JsonResponse(status)

@csrf_exempt
def drug(request): 
    if request.method == 'GET': # 藥物資訊展示
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        druginformationdata = druginformation.objects.get(uid=uid)
        UserProfiledata = UserProfile.objects.get(uid=uid)
        UserSetdata = UserSet.objects.get(uid=uid)
        try:
            type1 = data['type']
            type1 = str(type1)
            if type1 == '0':
                message = {
                "status":"0",
                "drug_useds":{
                "id":UserProfiledata.id,
                "user_id":UserSetdata.name,
                "type":druginformationdata.drugtype,
                "name":druginformationdata.drugname,
                "recorded_at":druginformationdata.recorded_at
                }}
                message = message
        except:
            message = {'status':'1'}
        return JsonResponse(message,safe=False)

    if request.method == 'POST': #藥物資訊上傳
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        user = druginformation.objects.create(uid=uid)
        try:
            user.drugname = data['name']
            user.drugtype = data['type']
            time = datetime.now()
            timeprint = datetime.strftime(time,"%Y-%m-%d %H:%M:%s")
            timeprint = str(timeprint)
            user.updated_at = timeprint
            user.save()
            status = {"status":"0"}
        except:
            status = {"status":"1"}
        return JsonResponse(status)
            
    if request.method == 'DELETE':  #藥物資訊刪除
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        user = druginformation.objects.get(uid=uid)
        try:
            deletedwho = data['ids']
            if deletedwho == 'drugname':
                user.drugname = []
                user.save()
                message = {'status':'0'}
            elif deletedwho == 'drugtype':
                user.drugtype  = []
                user.save()
                message = {'status':'0'}
        except:
            message = {'status':'1'}
        return JsonResponse(message)

@csrf_exempt   
def showHbA1c (request): #展示醣化血色素
    if request.method == 'GET':
        uid = request.user.uid
        HbA1cdata = HbA1c.objects.get(uid=uid)
        UserProfiledata = UserProfile.objects.get(uid=uid)
        print(HbA1cdata)
        try:
            message = {
            "status":"0",
            "a1cs":{
            "id":int(UserProfiledata.id),
            "user_id":int(UserProfiledata.id),
            "a1c":int(HbA1cdata.a1c),
            "created_at":datetime.strftime(HbA1cdata.created_at ,"%Y-%m-%d %H:%M:%s"),
            "updated_at":datetime.strftime(HbA1cdata.updated_at ,"%Y-%m-%d %H:%M:%s"),
            "recorded_at":datetime.strftime(HbA1cdata.recorded_at ,"%Y-%m-%d %H:%M:%s")
            }}
            message = message
        except:
            message = {'status':'1'}
        return JsonResponse(message,safe=False)
 
    if request.method == 'POST': #醣化血色素資訊上傳
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        profiledata = UserProfile.objects.get(uid=uid)
        user = HbA1c.objects.get(uid=uid)
        try:
            user.a1c = data['a1c']
            # time = datetime.datetime.now()
            # nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
            # timeprint= str(nowtime)
            # recorded_at = timeprint
            # updated_at = timeprint
            # created_at = timeprint
            # user.recorded_at = recorded_at
            # user.updated_at = updated_at
            # user.created_at = created_at
            user.save()
            status = {"status":"0"}
        except:
            status = {"status":"1"}
        return JsonResponse(status)

    if request.method == 'DELETE':  #醣化血色素資訊刪除
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        user = HbA1c.objects.get(uid=uid)
        try:
            deletedwho = data['ids']
            if deletedwho == '1':
                user.user_id =''
                user.save()
                message = {'status':'0'}
            elif deletedwho == '2':
                user.a1c = 0
                user.save()
                message = {'status':'0'}
        except:
            message = {'status':'1'}
        return JsonResponse(message)

#------------------------------------------------------- (家偉)

@csrf_exempt
def notification(request): # 親友團通知!
    uid = request.user.id
    if request.method == 'POST':
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        message = data['message']
        try:
            friend_list = Friend_data.objects.filter(uid=uid, friend_type=1, status=1)
            for friend in friend_list:
                Notification.objects.create(uid=uid, member_id=1, reply_id=friend.relation_id, message=message, updated_at=nowtime)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
        return JsonResponse(output,safe=False)

@csrf_exempt
def share(request): # 分享!
    uid = request.user.id
    if request.method == 'POST':
        data = request.POST.dict()
        share_id = data['id']
        data_type = data['type']
        relation_type = data['relation_type']
        try:
            Share.objects.create(uid=uid, fid=share_id, data_type=data_type, relation_type=relation_type)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
        return JsonResponse(output,safe=False)

@csrf_exempt
def share_check(request,relation_type): # 查看分享（含自己分享出去的）!
    uid = request.user.id
    if request.method == 'GET':
        if Share.objects.filter(relation_type=relation_type):
            share_checks = Share.objects.filter(relation_type=relation_type)
            datas = []
            for share_check in share_checks:
                if int(share_check.uid) != uid:
                    Friend_data.objects.get(uid=uid, relation_id=share_check.uid, status=1, friend_type=relation_type)
                    user_pro = UserProfile.objects.get(id=share_check.uid)
                    user = UserSet.objects.get(uid=user_pro.uid)
                else:
                    user_pro = UserProfile.objects.get(id=uid)
                    user = UserSet.objects.get(uid=user_pro.uid)
                if share_check.data_type == '0' :
                    share_data = Blood_pressure.objects.get(uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "systolic":share_data.systolic,
                        "diastolic":share_data.diastolic,
                        "pulse":share_data.pulse,
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":0,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                if share_check.data_type == '1' :
                    share_data = Weight.objects.get(uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "weight":float(share_data.weight),
                        "body_fat":float(share_data.body_fat),
                        "bmi":float(share_data.bmi),
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":1,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                if share_check.data_type == '2' :
                    share_data = Blood_sugar.objects.get(uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "sugar":float(share_data.sugar),
                        "timeperiod":int(share_data.timeperiod),
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":2,
                        "user":{
                            "id":user_pro.id,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                if share_check.data_type == '3' :
                    share_data = Diary_diet.objects.get(uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    image = str(share_data.image)
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "description":share_data.description,
                        "meal":int(share_data.meal),
                        "tag":share_data.tag,
                        "image":str(image),
                        "lat":share_data.lat,
                        "lng":share_data.lng,
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":3,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                datas.append(r)
            output = {"status":"0", "records":datas}
        else:
            output = {"status":"1"}
        return JsonResponse(output)
# @csrf_exempt
# def badge(request):
#     if request.method == 'PUT': #更新badge
#             # data = request.body
#             # data = str(data, encoding="utf-8")
#             # data = {
#             # i.split('=')[0]: i.split('=')[1]
#             # for i in data.replace("%40","@").split('&') if i.split('=')[1]
#             # }

#             s = Session.objects.get(
#             pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()

#             UserProfiledata = UserProfile.objects.get(id=s['_auth_user_id'])
#             user = UserSet.objects.get(uid=UserProfiledata.uid)
#             try:
#                 user.badge = data['badge']
#                 user.save()
#                 status = {"status":"0"}
#             except:
#                 status = {"status":"1"}

#             return JsonResponse(status)
@csrf_exempt
def badge(request):
    # 39.更新badge
    status = {"status":"1"}
    try:
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')[7:]).get_decoded()
        user = UserSet.objects.get(id=s['_auth_user_id'])
        if request.method == 'PUT':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            if 'badge' in data:
                user.badge = data['badge']
                user.save()
                status = {"status":"0"}
    except:
        pass
    return JsonResponse(status)

@csrf_exempt
def registercheck(request): #註冊確認
    if request.method == 'GET':
        user_ck = request.GET["account"]
        try:
            user = UserProfile.objects.get(username=user_ck)
            message = {'status':'1'}
        except:
            message = {'status':'0'}
        return JsonResponse(message)

# def privacy_policy(request): # 隱私權聲明 FBLogin
#     result = '1'
#     try:
#         if request.method == 'POST':
#             result = '0'
#     except:
#         pass
#     return JsonResponse({'status': result})