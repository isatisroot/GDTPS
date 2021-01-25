import json
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from .models import Meeting, ShareholderInfo,OnSiteMeeting,GB
from django.contrib.auth import login
from rest_framework_jwt.settings import api_settings
from datetime import datetime,date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.utils import timezone as datetime

class Login(View):
    def post(self, request):
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return HttpResponseNotFound(json.dumps({"errCode": "0001",
                                                    "msg": "登录失败，错误原因:用户不存在",
                                                    "success": 0}))

        # if not check_password(password,user.password):
        # if user.password != password:
        #     return JsonResponse({'msg': '密码错误'},status=400)

        # 将登录成功的信息写入到session中
        login(request,user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return JsonResponse({'username': username, 'user_id': user.id, 'token': token, 'msg': '登录成功', "success": 1})



class QueryYear(View):
    # @method_decorator(login_required)
    def get(self, request):
        try:
            m = Meeting.objects.get(current_year=1)
            # 将时间提前10分钟并转化为字符串格式
            # m.date = m.date + timedelta(minutes=-10)
            str_date = m.date.strftime('%Y-%m-%d %H:%M:%S')
            # print(str_date)
            qs = Meeting.objects.filter(year=m.year)
            meeting_list = []
            for q in qs:
                meeting_list.append(q.name)
            sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}

            return JsonResponse({"year": m.year, "name": m.name, "date": str_date, "meeting_list": meeting_list, 'sharehold': sharehold})
        except Exception as e:
            print(e)
            # 如果没有在表中查询到最近一次会议的年份则返回系统当前年份
            year = date.today().year
            return JsonResponse({"year": year})

class Current(View):
    def get(self, request):
        """
        向数据库中查询标记为最近一次会议的会议信息
        :return: 当前会议信息：年份，名称，时间, 参会股东信息; 当前年份下所有会议信息的列表; 股本数;
        """
        motion = []
        detail_list = []
        meeting_list = []
        m = Meeting.objects.get(current_year=1)
        str_date = m.date.strftime('%Y-%m-%d %H:%M:%S')
        # 会议议案
        if m.motion:
            motion = m.motion.split(";")
            motion.pop()

        current = {"year": m.year, "name": m.name, "date": str_date, "motion": motion}

        # 查询该会议现场登记表信息
        qs1 = m.onsitemeeting_set.all()
        for q in qs1:
            # 根据登记表查找到股东信息表q
            s = q.shareholder
            data = {
                'id':q.shareholder_id,
                'cx': q.cx,
                'xc': q.xcorwl,
                'gdxm': s.gdxm,
                'gdtype': s.gdtype,
                'gddmk': s.gddmk,
                'sfz': s.sfz,
                'rs': s.rs,
                'gzA': q.gzA,
                'gzB': q.gzB,
                'meno': q.meno  # 备注信息
            }
            detail_list.append(data)

        # 查询当前年份下有多少个会议
        qs2 = Meeting.objects.filter(year=m.year)
        for q in qs2:
            meeting_list.append(q.name)

        # 查询股本数
        sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}

        return JsonResponse({"current": current, "detail_list": detail_list,
                             "meeting_list": meeting_list, 'sharehold': sharehold})


class AddMeeting(View):
    def get(self, request):
        queryset = ShareholderInfo.objects.all()
        shareholders_list = []
        for q in queryset:
            shareholders_list.append({'key': q.id, 'label': q.gdxm})
        data = {'list': shareholders_list}
        return JsonResponse(data, safe=False)

    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        meeting = req_data.get('meeting')
        motion = req_data.get("motion")
        gdid_list = req_data.get('gdid')
        name = meeting.get("name")
        address = meeting.get("address")
        date1 = meeting.get("date1")
        date2 = meeting.get('date2')

        year = date1.split("-")[0]
        if not all((date1, date2, address)):
            return HttpResponseBadRequest(json.dumps({'msg': '请填写时间和日期'}))

        text = ''
        for i in motion:
            if bool(i):
                text += i.get('motion','')+ ";"

        try:
            if Meeting.objects.filter(year=year, name=name):
                return HttpResponseBadRequest( json.dumps({'msg':'会议已存在，无需添加'}))
            try:
                q = Meeting.objects.get(current_year=1)
                q.current_year = False
                q.save()
            except Exception as e:
                print(e)

            stru_date = datetime.strptime(date1 +"\xa0" + date2, "%Y-%m-%d %H:%M")
            gb =  GB.objects.last()
            m = Meeting.objects.create(
                year=year,
                date=stru_date,
                name=name,
                current_year=1,
                address=address,
                motion=text,
                gb=gb
            )
            m.members.set(gdid_list)
            for i in gdid_list:
                gd = ShareholderInfo.objects.get(id=i)
                OnSiteMeeting.objects.filter(meeting_id=m.id, shareholder_id=i).update(gzA=gd.gzA, gzB=gd.gzB)
            return JsonResponse({'code':200, 'msg': 'success'})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content_type="'application/json'")

class QueryMeeting(View):
#     """
#     通过年份查询该年份一共有多少会议，返回该年份所有的会议名称
#     """
    def get(self, request, year):
        query = Meeting.objects.filter(year=year)
        data = {}
        meeting_list = []
        for q in query:
            meeting_list.append(q.name)
# #
        data[year] = meeting_list
#         # 使用safe = False可以将字典中包含的列表直接转换成json
        response = JsonResponse(data, safe=False)
        return response
#
class QueryDetail(View):
    def get(self, request, year, meeting_name):
#         # year = request.GET.get('year')
#         # meeting_name = request.GET.get('meeting_name')
#         print(year, meeting_name)
        global str_date, sharehold
        str_date = ""
        sharehold = {}
        detail_list = []
        motion = []
        try:
            # m是annual_meeting年度会议表的模型类对象
            m = Meeting.objects.get(year=year,name=meeting_name)
            if m.gb:
                # 通过年度会议查找股本信息
                sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}
            # 通过m查找现场会议登记的中间表queset
            queryset = m.onsitemeeting_set.all()
            # _d = m.date + timedelta(minutes=-10)
            str_date = m.date.strftime('%Y-%m-%d %H:%M:%S')
            if m.motion:
                motion = m.motion.split(";")
                motion.pop()
            # print(motion)
            for i in queryset:
                # 根据中间表查找到股东信息表q
                q = i.shareholder
                # print(i.cx)
                data = {
                    'id':i.shareholder_id,
                    'cx': i.cx,
                    'xc': i.xcorwl,
                    'gdxm': q.gdxm,
                    'gdtype': q.gdtype,
                    'gddmk': q.gddmk,
                    'sfz': q.sfz,
                    'rs': q.rs,
                    # 'frA': q.frA,
                    'gzA': i.gzA,
                    'gzB': i.gzB,
                    # 'dlr': q.dlr,
                    'meno': i.meno
                }
                detail_list.append(data)
        except Exception as e:
            print(e)

        return JsonResponse({'date': str_date, 'motion':motion, 'list':detail_list, 'sharehold': sharehold})

class UpdateMeeting(View):
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        year = req_data.get("year")
        meeting_name = req_data.get("meeting")
        tableData = req_data.get("tableData",None)
        if not tableData:
            return HttpResponseBadRequest(content=json.dumps({'msg':'更新失败'}),content_type="'application/json'")
        try:
            m = Meeting.objects.get(year=year,name=meeting_name)
            for data in tableData:
                id = data.get("id",None)
                # id是随着查询时发送到前端的，返回后如果没有id表示是前端新增的数据
                if not id:
                    gdxm=data.get('gdxm')
                    sfz = data.get("sfz", None)
                    qs = ShareholderInfo.objects.filter(gdxm=gdxm, sfz=sfz)
                    if qs:
                        return HttpResponseBadRequest(content=json.dumps({'msg': '更新失败，数据库已有该股东信息'}))

                    s = ShareholderInfo.objects.create(
                        gdxm=data.get('gdxm'),
                        gdtype=data.get('gdtype',None), # cannot be null
                        gddmk=data.get('gddmk', None),
                        sfz=data.get('sfz', None),
                        rs=data.get('rs',0),
                        frA=data.get("frA",0),
                        gzA=data.get('gzA',0),
                        gzB=data.get('gzB',0),
                        dlr=data.get('dlr',None)
                    )
                    id = s.id

                # 如果存在则对股东信息进行修改
                else:
                    s = ShareholderInfo.objects.get(id=id)
                    s.gdxm=data.get("gdxm")
                    s.gdtype = data.get("gdtype")
                    s.gddmk = data.get("gddmk", None)
                    s.sfz = data.get("sfz", None)
                    s.rs = data.get("rs", 1)
                    s.gzA = data.get("gzA", 0)
                    s.gzB = data.get("gzB", 0)

                qs = OnSiteMeeting.objects.filter(meeting_id=m.id, shareholder=id)
                # 判断登记表中是否有该条记录，有则修改，没有则添加
                if qs:
                    qs.update(
                    cx=data.get("cx") if data.get("cx") else False,
                    xcorwl=data.get("xc") if data.get("xc") else False,
                    gzA=int(data.get("gzA", 0)),
                    gzB=int(data.get("gzB", 0)),
                    meno = data.get("meno", None)
                )
                else:
                    OnSiteMeeting.objects.create(
                        meeting_id=m.id,
                        shareholder=s,
                        cx=data.get("cx") if data.get("cx") else False,
                        xcorwl=data.get("xc") if data.get("xc") else False,
                        gzA=int(data.get("gzA", 0)),
                        gzB=int(data.get("gzB", 0)),
                        meno = data.get("meno", None)
                    )

            return JsonResponse({'code':200, 'msg':'更新成功'})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content=json.dumps({'msg':'更新失败'}),content_type="'application/json'")

class Upload(View):
    def post(self, request):
        print(request.body)
        return JsonResponse({'code': 200, 'msg': '上传成功'})

class LoadAll(View):
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        idList = req_data.get("gdid",[])
        data_list = []
        qs = ShareholderInfo.objects.all()
        for q in qs:
            if q.id in idList:
                continue
            data = {
                'id':q.id,
                'value': q.gdxm,
                'gdtype': q.gdtype,
                'gddmk': q.gddmk,
                'sfz': q.sfz,
                'rs': q.rs,
                'gzA': q.gzA,
                'gzB': q.gzB,
            }
            data_list.append(data)

        return JsonResponse(data_list, safe=False)

class Delete(View):
    def delete(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        id = req_data.get("id")
        year = req_data.get("year")
        meeting = req_data.get("meeting")

        if id:
            m = Meeting.objects.get(year=year, name=meeting)
            OnSiteMeeting.objects.filter(meeting=m.id, shareholder=id).delete()

        return JsonResponse({'code':200, 'msg':'删除成功'})

