from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import auth
from .models import *
from user.models import *
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def friend_code(request): # 獲取控糖團邀請碼!
    uid = request.user.id
    try:
        user_friend = Friend.objects.get(uid=uid)
    except:
        output = {"status":"1"}
    else:
        output = {"status":"0", "invite_code":user_friend.invite_code}        
    return JsonResponse(output,safe=False)

@csrf_exempt
def friend_list(request): # 控糖團列表!
    uid = request.user.id
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, status=1):
            friends = []
            friends_list = Friend_data.objects.filter(uid=uid, status=1)
            for friend in friends_list:
                user_pro = UserProfile.objects.get(id=friend.relation_id)
                relation = UserSet.objects.get(uid=user_pro.uid)
                created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
                updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
                r = {
                        "id":user_pro.id,
                        "name":relation.name,
                        "account":relation.email,
                        "email":relation.email,
                        "phone":relation.phone,
                        "fb_id":user_pro.fb_id,
                        "status":relation.status,
                        "group":relation.group,
                        "birthday":str(relation.birthday),
                        "height":relation.height,
                        "gender":relation.gender,
                        "verified":relation.verified,
                        "privacy_policy":relation.privacy_policy,
                        "must_change_password":relation.must_change_password,
                        "badge":int(relation.badge),
                        "created_at":created_at_userfile,
                        "updated_at":updated_at_userfile,
                        "relation_type":friend.friend_type
                    }
                friends.append(r)
            output = {"status":"0", "friends":friends}
        else:
            output = {"status":"1"}
    return JsonResponse(output)

@csrf_exempt
def friend_requests(request): # 獲取控糖團邀請!
    uid = request.user.id
    try:
        requests_list = Friend_data.objects.filter(relation_id=uid, status=0)
    except:
        output = {"status":"1"}
    else:
        requests = []
        for request in requests_list:
            user_pro = UserProfile.objects.get(id=request.uid)
            user = UserSet.objects.get(uid=user_pro.uid)
            created_at_friendata = datetime.strftime(request.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(request.updated_at, '%Y-%m-%d %H:%M:%S')
            created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
            r = {
                "id":request.id,
                "user_id":request.uid,
                "relation_id":request.relation_id,
                "type":request.friend_type,
                "status":request.status,
                "created_at":created_at_friendata,
                "updated_at":updated_at_friendata,
                "user":
                        {
                            "id":user.id,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":str(user.birthday),
                            "height":float(user.height),
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":int(user.badge),
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                        
                        }
                    }
            requests.append(r)
        output = {"status":"0", "requests":requests}
    return JsonResponse(output)

@csrf_exempt
def friend_send(request): # 送出控糖團邀請!
    uid = request.user.id
    if request.method == 'POST':
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        friend_type = data['type']
        invite_code = data['invite_code']
        try:
            user_friend = Friend.objects.get(invite_code=invite_code)
            friend_uid = user_friend.uid
        except:
            output = {"status":"1"} # 1: 邀請碼無效
        else:
            try:
                Friend_data.objects.get(uid=uid, relation_id=friend_uid)
            except:
                try:
                    Friend_data.objects.create(uid=uid, relation_id=friend_uid, status=0, friend_type=friend_type, updated_at=nowtime)
                except:
                    output = {"status":"1"}
                else:
                    output = {"status":"0"}
            else:
                output = {"status":"2"} # 2: 已經成為好友
        return JsonResponse(output,safe=False)

@csrf_exempt
def friend_accept(request,friend_data_id): # 接受控糖團邀請!
    uid = request.user.id
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(1234)
    try:
        check = Friend_data.objects.get(id=friend_data_id, status=0)
        Friend_data.objects.create(uid=uid, relation_id=check.uid, status=1, read=True, imread=True, friend_type=check.friend_type, updated_at=nowtime)
        check.read = True
        check.status = 1
        check.updated_at = nowtime
        check.save()
    except:
        output = {"status":"1"}
    else:
        output = {"status":"0"}
    return JsonResponse(output,safe=False)

@csrf_exempt
def friend_refuse(request,friend_data_id): # 拒絕控糖團邀請!
    uid = request.user.id
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        check = Friend_data.objects.get(id=friend_data_id, status=0)
        check.read = True
        check.status = 2
        check.updated_at = nowtime
        check.save()
    except:
        output = {"status":"1"}
    else:
        output = {"status":"0"}
    return JsonResponse(output,safe=False)

@csrf_exempt
def friend_remove(request,friend_data_id): # 刪除控糖團邀請!
    uid = request.user.id
    if request.method == 'GET':
        try:
            Friend_data.objects.filter(id=friend_data_id, status=0).delete()
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
        return JsonResponse(output,safe=False)

@csrf_exempt
def friend_results(request): # 控糖團結果!
    uid = request.user.id
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, read=True, imread=False):
            results = []
            result = Friend_data.objects.filter(uid=uid, read=True, imread=False).latest('updated_at')
            user_pro = UserProfile.objects.get(id=result.relation_id)
            relation = UserSet.objects.get(uid=user_pro.uid)
            created_at_friendata = datetime.strftime(result.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(result.updated_at, '%Y-%m-%d %H:%M:%S')
            created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
            r = {
                "id":result.id,
                "user_id":result.uid,
                "relation_id":result.relation_id,
                "type":result.friend_type,
                "status":int(result.status),
                "read":result.read,
                "created_at":created_at_friendata,
                "updated_at":updated_at_friendata,
                "relation":
                        {
                            "id":user_pro.id,
                            "name":relation.name,
                            "account":relation.email,
                            "email":relation.email,
                            "phone":relation.phone,
                            "fb_id":user_pro.fb_id,
                            "status":relation.status,
                            "group":relation.group,
                            "birthday":str(relation.birthday),
                            "height":relation.height,
                            "gender":relation.gender,
                            "verified":relation.verified,
                            "privacy_policy":relation.privacy_policy,
                            "must_change_password":relation.must_change_password,
                            "badge":int(relation.badge),
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                        }
                    }
            result.imread = True
            result.save()
            results.append(r)
            output = {"status":"0", "results":results}
        else:
            output = {"status":"1"}
    return JsonResponse(output)

@csrf_exempt
def friend_remove_more(request): # 刪除更多好友!
    uid = request.user.id
    if request.method == 'DELETE':
        ids_list = request.GET.getlist("ids[]")
        for ids in ids_list :
            Friend_data.objects.get(uid=ids, relation_id=uid, status=1).delete()
            Friend_data.objects.get(uid=uid, relation_id=ids, status=1).delete()
        output = {"status":"0"}
    else:
        output = {"status":"1"}
    return JsonResponse(output)