import json
import xlrd
import redis
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, \
    HttpResponse

from GDVoteSys.settings import BASE_DIR
from .models import Meeting, ShareholderInfo, OnSiteMeeting, GB, MotionBook, AccumulateMotion, VoteRecordDetail
from django.contrib.auth import login
from rest_framework_jwt.settings import api_settings
from datetime import datetime,date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django_redis import get_redis_connection
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.record_to_word import RecordToWord
from utils.parse_excel import ParseExcel
# from django.utils import timezone as datetime
from django import forms
from openpyxl import load_workbook

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
        :return: 当前会议信息：年份，名称，时间, 参会股东信息; 当前年份下所有会议信息的列表; 股本数; 备选股东信息
        """
        motion = []
        detail_list = []
        meeting_list = []
        s_list = []
        extr_sh_list = []
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
            s_list.append(s.id)
            detail_list.append(data)

        # 找出在登记表中没有关联的股东信息
        extr_shareholds = ShareholderInfo.objects.exclude(id__in = s_list)
        for s in extr_shareholds:
            data = {
                'id':s.id,
                'value': s.gdxm,
                'gdtype': s.gdtype,
                'gddmk': s.gddmk,
                'sfz': s.sfz,
                'rs': s.rs,
                'gzA': s.gzA,
                'gzB': s.gzB,
            }
            extr_sh_list.append(data)
        
        # 查询当前年份下有多少个会议
        qs2 = Meeting.objects.filter(year=m.year)
        for q in qs2:
            meeting_list.append(q.name)

        # 查询股本数
        sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}

        return JsonResponse({"current": current, "detail_list": detail_list,
                             "meeting_list": meeting_list, 'sharehold': sharehold, "extr_shareholds": extr_sh_list})


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
        leijimotion = req_data.get("leijimotion",[])
        gdid_list = req_data.get('gdid')
        name = meeting.get("name")
        address = meeting.get("address")
        date1 = meeting.get("date1")
        date2 = meeting.get('date2')
        descr = meeting.get("descr")

        year = date1.split("-")[0]
        if not all((date1, date2, address)):
            return HttpResponseBadRequest(json.dumps({'msg': '请填写时间和日期'}))

        for i in leijimotion:
            motion.remove(i)
        # text = ''
        # for i in motion:
        #     if bool(i):
        #         text += i.get('motion','')+ ";"

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
            # 写入年度会议表
            m = Meeting.objects.create(
                year=year,
                date=stru_date,
                name=name,
                current_year=1,
                address=address,
                descr=descr,
                gb=gb
            )
            #判断有无议案，有则写入议案表
            for i in motion:
                if i.get("motion"):
                    MotionBook.objects.create(name=i['motion'], annual_meeting=m)

            for i in leijimotion:
                if i.get("motion"):
                    AccumulateMotion.objects.create(name=i["motion"], annual_meeting=m)

            # 写入中间表——登记表，并关联年度会议和股东id，记录当年股东的股份数
            m.members.set(gdid_list)
            for i in gdid_list:
                gd = ShareholderInfo.objects.get(id=i)
                OnSiteMeeting.objects.filter(meeting_id=m.id, shareholder_id=i).update(gzA=gd.gzA, gzB=gd.gzB, cx=True, xcorwl=False)
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

        global str_date, sharehold, extr_sh_list, meeting_list, current
        motion = []
        str_date = ""
        sharehold = {}
        current = {}
        s_list = []
        detail_list = []
        meeting_list = []
        extr_sh_list = []

        try:
            # m是annual_meeting年度会议表的模型类对象
            m = Meeting.objects.get(year=year,name=meeting_name)
            if m.gb:
                # 通过年度会议查找股本信息
                sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}
            # 通过m查找现场会议登记的中间表queset
            zxg_gd = ShareholderInfo.objects.filter(gdtype="中小股").values_list("id")
            queryset = m.onsitemeeting_set.all()
            # 因为OnSiteMeeting表没有gdtype属性，只有shareholder_id属性，因此需要先找出属于中小股股东的id，然后根据id排除掉他们
            queryset = queryset.exclude(shareholder_id__in=zxg_gd)  # 排除掉中小股股东的查询集

            str_date = m.date.strftime('%Y-%m-%d %H:%M:%S')
            # if m.motion:
            #     motion = m.motion.split(";")
            #     motion.pop()
            motion_qs =  m.motionbook_set.all()
            for i in motion_qs:
                motion.append(i.name)

            leijimotion = []
            leijimotion_qs = m.accumulatemotion_set.all()
            for i in leijimotion_qs:
                leijimotion.append(i.name)

            address = m.address
            current = {"year": m.year, "name": m.name, "date": str_date, "motion": motion, "leijimotion": leijimotion, "address": address}

            for q in queryset:
                # 根据中间表查找到股东信息表q
                s = q.shareholder
                # print(i.cx)
                data = {
                    'id':q.shareholder_id,
                    'cx': q.cx,
                    'xc': q.xcorwl,
                    'gdxm': s.gdxm,
                    'gdtype': s.gdtype,
                    'gddmk': s.gddmk,
                    'sfz': s.sfz,
                    'rs': q.rs,
                    'gzA': q.gzA,
                    'gzB': q.gzB,
                    'meno': q.meno
                }
                s_list.append(s.id)
                detail_list.append(data)

            # 找出在登记表中没有关联的股东信息
            extr_shareholds = ShareholderInfo.objects.exclude(id__in = s_list)
            for s in extr_shareholds:
                data = {
                    'id':s.id,
                    'gdxm': s.gdxm,
                    'gdtype': s.gdtype,
                    'gddmk': s.gddmk,
                    'sfz': s.sfz,
                    'rs': s.rs,
                    'gzA': s.gzA,
                    'gzB': s.gzB,
                }
                extr_sh_list.append(data)

            qs2 = Meeting.objects.filter(year=m.year)
            for q in qs2:
                meeting_list.append(q.name)
        except Exception as e:
            print(e)

        # return JsonResponse({'date': str_date, 'motion':motion, 'list':detail_list, 'sharehold': sharehold})
        return JsonResponse({"current": current, "detail_list": detail_list, "meeting_list": meeting_list, 'sharehold': sharehold, "extr_shareholds": extr_sh_list})
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
                    # if qs:
                    #     return HttpResponseBadRequest(content=json.dumps({'msg': '更新失败，数据库已有该股东信息'}))

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
                    rs = data.get("rs")
                    s = ShareholderInfo.objects.get(id=id)
                    s.gdxm=data.get("gdxm")
                    s.gdtype = data.get("gdtype")
                    s.gddmk = data.get("gddmk", None)
                    s.sfz = data.get("sfz", None)
                    s.rs = int(data.get("rs", 1))
                    s.gzA = data.get("gzA", 0)
                    s.gzB = data.get("gzB", 0)
                    s.save()

                qs = OnSiteMeeting.objects.filter(meeting_id=m.id, shareholder=id)
                # 判断登记表中是否有该条记录，有则修改，没有则添加
                if qs:
                    qs.update(
                    cx=data.get("cx") if data.get("cx") else False,
                    xcorwl=data.get("xc") if data.get("xc") else False,
                    gzA=int(data.get("gzA", 0)),
                    gzB=int(data.get("gzB", 0)),
                    meno = data.get("meno", None),
                    rs=int(data.get("rs",1))
                )
                else:
                    OnSiteMeeting.objects.create(
                        meeting_id=m.id,
                        shareholder=s,
                        cx=data.get("cx") if data.get("cx") else False,
                        xcorwl=data.get("xc") if data.get("xc") else False,
                        gzA=int(data.get("gzA", 0)),
                        gzB=int(data.get("gzB", 0)),
                        meno = data.get("meno", None),
                        rs=int(data.get("rs",1))
                    )

            return JsonResponse({'code':200, 'msg':'更新成功'})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content=json.dumps({'msg':'更新失败'}),content_type="'application/json'")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class Upload(View):
    def post(self, request):
        # print(request.body)
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     wb = load_workbook(filename=request.FILES['file'].file)
        #     print(wb)
        file = request.FILES.get("file")
        year = request.POST["year"]
        meeting_name = request.POST["name"]
        filename = file.name
        print(filename)
        if not filename.endswith("xls"):
            return HttpResponseBadRequest(content=json.dumps({'msg':'excel格式不正确，请上传xls文件'}),content_type="'application/json'")

        if "普通" not in filename and "累计" not in filename:
            return HttpResponseBadRequest(content=json.dumps({'msg':'文件名不正确'}),content_type="'application/json'")
        if "A股" not in filename and "B股" not in filename:
            return HttpResponseBadRequest(content=json.dumps({'msg':'文件名不正确'}),content_type="'application/json'")

        try:
            for chunk in file.chunks():
                with open(BASE_DIR + "/files/" + filename, 'wb+') as f:
                    f.write(chunk)

            book = ParseExcel(filename, year, meeting_name)
            # book.create_gd()
            book.run_sum()
        except xlrd.biffh.XLRDError as e:
            return HttpResponseBadRequest(content=json.dumps({'msg':'格式不正确，请另存为xls文件后重新上传'}),content_type="'application/json'")
        except FileNotFoundError as e:
            print(e)

        return JsonResponse({'code': 200, 'msg': '上传成功'})

class LoadAll(View):
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        idList = req_data.get("gdid",[])
        data_list = []
        gddmk_data_list = []
        qs = ShareholderInfo.objects.all()
        for q in qs:
            if q.id in idList:
                continue
            data = {
                'id':q.id,
                'value': q.gdxm,
                'gdxm': q.gdxm,
                'gdtype': q.gdtype,
                'gddmk': q.gddmk,
                'sfz': q.sfz,
                'rs': q.rs,
                'gzA': q.gzA,
                'gzB': q.gzB,
            }
            data2 = {
                'id':q.id,
                'value': q.gddmk,
                'gdxm': q.gdxm,
                'gdtype': q.gdtype,
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

class Result(View):
    """查询结果"""
    def get(self, request, year, meeting_name):
        """
        motion是普通议案，要对其投赞成，反对，弃权和回避票进行统计，leijimotion是累计投票的议案，只统计赞成票（A股和B股）
        redis缓存了某个议案投反对和弃权票的股东ID，先向redis查看有无投反对票或弃权票的股东，有无导入excel的动作，
        有则拿出来合并统计，未做记录的参会股东默认赞成票
        把redis的投票信息合并进来统计，然后清除缓存，写入到mysql数据库，发到前端；
        没有则判断是否有统计过，统计过则直接从数据库中拿数据，未统计则返回空值
        :return:
        """
        motion_list = []
        leijimotion = []
        con = get_redis_connection("default")
        m = Meeting.objects.get(year=year,name=meeting_name)
        motion_qs =  m.motionbook_set.all()
        onSite_qs =  m.onsitemeeting_set.all()
        if con.get("vote"):
            for motion in motion_qs:
            # 获取出席该会议股东id列,持A股数，持B股数的数据,返回<QuerySet [(1,), (2,), (3,)……]>
                sum_zan_A = sum_zan_B = sum_fan_A = sum_fan_B = sum_qi_A = sum_qi_B \
                    =zxg_sum_zan_A = zxg_sum_zan_B = zxg_sum_fan_A = zxg_sum_fan_B \
                    = zxg_sum_qi_A = zxg_sum_qi_B = sum_huibiA = sum_huibiB = 0

                motion_id = str(motion.id)
                name_fandui = motion_id +"fandui"
                name_qiquan = motion_id + "qiquan"
                name_huibi = motion_id + "huibi"
                fandui_gd = con.smembers(name_fandui)
                qiquan_gd = con.smembers(name_qiquan)
                huibi_gd = con.hkeys(name_huibi)  # 取出所有的键，即所有回避的股东id
                huibi_descr = con.hvals(name_huibi)
                descr_text = ""
                for descr in huibi_descr: descr_text += descr
                # 如果redis中有个别股东投反对票，那么要进行重新计算统计，否则直接从数据库中获取统计结果

                for id in fandui_gd:
                    qs = onSite_qs.filter(shareholder_id=id)
                    if qs:
                        q = qs[0]
                        equityType = 0 if q.gzA > 0 else 1
                        VoteRecordDetail.objects.update_or_create(defaults={
                            "gdId": qs[0].shareholder,
                            "motionId": motion,
                            "equityType": equityType,
                            "vote": 2
                        }, gdId=q.shareholder, motionId=motion,  equityType=equityType)

                for id in qiquan_gd:
                    qs = onSite_qs.filter(shareholder_id=id)
                    if qs:
                        equityType = 0 if qs[0].gzA > 0 else 1
                        VoteRecordDetail.objects.update_or_create(defaults={
                            "gdId": qs[0].shareholder,
                            "motionId": motion,
                            "equityType": equityType,
                            "vote": 3
                        }, gdId=qs[0].shareholder, motionId=motion, equityType=equityType)
                for id in huibi_gd:
                    qs = onSite_qs.filter(shareholder_id=id)
                    if qs:
                        equityType = 0 if qs[0].gzA > 0 else 1
                        VoteRecordDetail.objects.update_or_create(defaults={
                            "gdId": qs[0].shareholder,
                            "motionId": motion,
                            "equityType": equityType,
                            "vote": 4
                        }, gdId=qs[0].shareholder, motionId=motion,  equityType=equityType)
                # 剩下的就是投赞成票的股东
                exclude = list(qiquan_gd & fandui_gd) + huibi_gd
                zancheng_gd = onSite_qs.exclude(shareholder_id__in=exclude)
                for gd in zancheng_gd:
                    equityType = 0 if gd.gzA > 0 else 1
                    VoteRecordDetail.objects.update_or_create(defaults={
                        "gdId": gd.shareholder,
                        "motionId": motion,
                        "equityType": equityType,
                        "vote": 1
                    }, gdId=gd.shareholder, motionId=motion,  equityType=equityType)

                    # 合并网络投票
                #     sum_zan_A += excel_A.get_zancheng("A")[i.id]
                #     sum_fan_A += excel_A.get_fandui("A")[i.id]
                #     sum_qi_A += excel_A.get_qiquan("A")[i.id]

                # 将统计完的数据更新到数据库中
                #     MotionBook.objects.update_or_create(
                #         defaults={
                #         "zanchengA": sum_zan_A,
                #         "zanchengB": sum_zan_B,
                #         "fanduiA": sum_fan_A,
                #         "fanduiB": sum_fan_B,
                #         "qiquanA": sum_qi_A,
                #         "qiquanB": sum_qi_B,
                #         "zxg_zanchengA": zxg_sum_zan_A,
                #         "zxg_zanchengB": zxg_sum_zan_B,
                #         "zxg_fanduiA": zxg_sum_fan_A,
                #         "zxg_fanduiB": zxg_sum_fan_B,
                #         "zxg_qiA": zxg_sum_qi_A,
                #         "zxg_qiB": zxg_sum_qi_B,
                #         "is_huibi": True if sum_huibiA >0 or sum_huibiB > 0 else False,
                #         "huibiA": sum_huibiA,
                #         "huibiB": sum_huibiB,
                #         "descr": descr_text
                #         },
                #         id=motion.id)

        motion_qs =  m.motionbook_set.all()
        for i in motion_qs:
            data = {
                "id": i.id,
                "name": i.name,
                "zanchengA": i.zanchengA,
                "zanchengB": i.zanchengB,
                "fanduiA": i.fanduiA,
                "fanduiB": i.fanduiB,
                "qiquanA": i.qiquanA,
                "qiquanB": i.qiquanB,
                "is_huibi": i.is_huibi,
                "huibiA": i.huibiA,
                "huibiB": i.huibiB,
                "huibi_descr": i.descr
            }
            motion_list.append(data)

        # 对每一个累计议案进行统计，写入数据库然后发送到前端
        leijimotion_qs = m.accumulatemotion_set.all()
        for i in leijimotion_qs:
            data = {
                "id": i.id,
                "name": i.name,
                "zanchengA": i.zanchengA,
                "zanchengB": i.zanchengB
            }
            leijimotion.append(data)

        queryset = m.onsitemeeting_set.filter(cx=True)
        sharehold_cx_A = 0
        sharehold_cx_B = 0
        cx_gd = []
        cx_gb = []
        for i in queryset:

            sharehold_cx_A += i.gzA
            sharehold_cx_B += i.gzB
            cx_gd.append(i.shareholder.gdxm)
            cx_gb.append(i.gzB + i.gzA)

        ncx_gb = m.gb.gb - sharehold_cx_A -sharehold_cx_B

        # 生成word文档
        content = {}
        # try:
        #     doc = RecordToWord()
        #     content = doc.vote_result(year, meeting_name)
        # except Exception as e:
        #     print(e)

        return  JsonResponse({"motion": motion,
                              "leijimotion": leijimotion,
                              "sharehold_cx_A": sharehold_cx_A,
                              "sharehold_cx_B": sharehold_cx_B,
                              "cx_gd": cx_gd,
                              "cx_gb": cx_gb,
                              "ncx_gb": ncx_gb,
                              "content": content})

class Motion(View):
    def get(self, request, year, meeting_name):

        try:
            m = Meeting.objects.get(year=year,name=meeting_name)
            sharehold = {"totalShare": m.gb.gb, "AShareTotal": m.gb.ltag, "BShareTotal": m.gb.ltbg}
            # 获取该年度所有议案
            motion = []
            motion_qs =  m.motionbook_set.all()
            for i in motion_qs:
                data = {
                    "id": i.id,
                    "name": i.name,
                    # "checked": 1  # 默认是赞成票，1代表赞成，2反对，3弃权
                }

                motion.append(data)

            leijimotion = []
            leijimotion_qs = m.accumulatemotion_set.all()
            for i in leijimotion_qs:
                data = {
                    "id": i.id,
                    "name": i.name,
                    "agree": None
                }
                leijimotion.append(data)
            queryset = m.onsitemeeting_set.filter(cx=True)
            data_list = []
            for q in queryset:
                # 根据中间表查找到股东信息表q
                s = q.shareholder
                # print(i.cx)
                data = {
                    'id':q.shareholder_id,
                    # 'cx': q.cx,
                    # 'xc': q.xcorwl,
                    'gdxm': s.gdxm,
                    'gdtype': s.gdtype,
                    'gddmk': s.gddmk,
                    'sfz': s.sfz,
                    # 'rs': s.rs,
                    'gzA': q.gzA,
                    'gzB': q.gzB,
                    'motion': motion,
                    'leijimotion': leijimotion
                    # 'meno': q.meno
                }
                data_list.append(data)
            return JsonResponse({"motion": motion, "leijimotion": leijimotion, "gdmsg": data_list, "isRecord": m.is_tongji})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content=json.dumps({'msg':'查询失败'}),content_type="'application/json'")

class Record(View):
    """唱票功能，将普通议案的赞成，反对和弃权票汇总后写入数据库，将累计议案的赞成票汇总后写入数据库"""
    def get(self, request):
        year = request.GET.get("year")
        name = request.GET.get("name")
        print(year, name)
        items = request.session.get(1)
        # keys = request.session.keys()
        # print(keys)
        print(items)
        # redis = get_redis_connection('verify')
        # text = redis.get(1)
        # print(text)
        return JsonResponse({"msg": "统计成功"})
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        vote = req_data.get("vote")
        year = req_data.get("year")
        name = req_data.get("name")
        # m = Meeting.objects.get(year=year,name=name)
        # motion_qs =  m.motionbook_set.all()

        data = {}
        data2 = {}
        for i in vote:
            gd_id = i.get("id")
            gzA = i.get("gzA")
            gzB = i.get("gzB")
            motion = i.get("motion")  # [{'id': 1, 'name': '关于与广东省广晟财务有限公司签署《金融服务协议》的议案', 'checked': 1}, {'id': 2, 'name': '关于修订《公司章程》的议案', 'checked': 1}]
            leijimotion = i.get("leijimotion") #[{'id': 1, 'name': '累计投票议案１', 'agree': '122694246'}, {'id': 2, 'name': '累计投票议案２', 'agree': '122694246'}]
            for j in motion:
                motion_id = j.get("id")
                _array = data.get(motion_id, [])
                checked = j.get("checked")
                is_huibi = j.get("ishuibi", None)
                descr = j.get("descr")
                _array.append({"gdid": gd_id, "checked": checked, "is_huibi": is_huibi, "descr": descr})
                # data的键是议案的id，值是一个列表，列表里面的元素是字典，每个字典包含投了该议案的股东及投了赞成还是反对票的信息
                data[motion_id]= _array

            for q in leijimotion:
                leijimotion_id = q.get("id")
                _array = data2.get(leijimotion_id, [])
                agree = q.get("agree",0)

                _array.append({"gdid": gd_id, "agree": agree})
                data2[leijimotion_id]= _array

        # print(data)
        # print(data2)
        # k是议案id，统计每个id有多少个股东投了赞成，反对或弃权票，如果有回避则记录回避表述descr_text
        for k,v in data.items():
            descr_text = ""
            m = MotionBook.objects.filter(id=k)
            is_huibi = None
            sum_zan_A = sum_zan_B = sum_fan_A = sum_fan_B = sum_qi_A = sum_qi_B\
                =zxg_sum_zan_A = zxg_sum_zan_B = zxg_sum_fan_A = zxg_sum_fan_B \
                = zxg_sum_qi_A = zxg_sum_qi_B = huibiA = huibiB = 0
            for i in v:
                gd_id = i.get("gdid")
                j = i.get("checked")
                is_huibi = i.get("is_huibi")
                descr = i.get("descr", "")
                s = ShareholderInfo.objects.get(id=gd_id)
                if j == 1:
                    # 单独对中小股动投票情况进行统计
                    if s.gdtype == "中小股":
                        zxg_sum_zan_A += s.gzA
                        zxg_sum_zan_B += s.gzB
                    sum_zan_A += s.gzA
                    sum_zan_B += s.gzB
                elif j == 2:
                    if s.gdtype == "中小股":
                        zxg_sum_fan_A += s.gzA
                        zxg_sum_fan_B += s.gzB
                    sum_fan_A += s.gzA
                    sum_fan_B += s.gzB
                elif j == 3:
                    if s.gdtype == "中小股":
                        zxg_sum_qi_A += s.gzA
                        zxg_sum_qi_B += s.gzB
                    sum_qi_A += s.gzA
                    sum_qi_B += s.gzB

                if is_huibi:
                    huibiA += s.gzA
                    huibiB += s.gzB
                    # 当有多个股东回避表述时，用分号间隔开
                    if descr:
                        descr_text += descr + " "

            m.update(
                zanchengA = sum_zan_A,
                zanchengB = sum_zan_B,
                fanduiA = sum_fan_A,
                fanduiB = sum_fan_B,
                qiquanA = sum_qi_A,
                qiquanB = sum_qi_B,
                zxg_zanchengA = zxg_sum_zan_A,
                zxg_zanchengB = zxg_sum_zan_B,
                zxg_fanduiA = zxg_sum_fan_A,
                zxg_fanduiB = zxg_sum_fan_B,
                zxg_qiA = zxg_sum_qi_A,
                zxg_qiB = zxg_sum_qi_B,
                is_huibi = True if huibiA >0 or huibiB > 0 else False,
                huibiA = huibiA,
                huibiB = huibiB,
                descr = descr_text
            )

        for k,v in data2.items():
            m = AccumulateMotion.objects.filter(id=k)
            zanchengA = 0
            zanchengB = 0
            for i in v:
                agree = i.get("agree", "0")
                gdid = i.get("gdid")
                gd = ShareholderInfo.objects.get(id=gdid)
                if gd.gzA > 0:
                    zanchengA += int(agree)
                else:
                    zanchengB += int(agree)

            m.update(zanchengA = zanchengA, zanchengB=zanchengB)

        return JsonResponse({"success": 1, "msg": "唱票成功"})

class Refresh(View):
    def get(self, request):
        year = request.GET.get('year')
        name = request.GET.get('name')
        print(year, name)
        Meeting.objects.filter(year=year, name=name).update(is_tongji = False)
        return JsonResponse({"success": 1, "msg": "更新成功"})

class Download(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        response = {}
        file_name = data.get("file_name")
        if not file_name:
            response["meta"] = {"code": 400}
            response["error"] = {"error_msg": "parameter error, no file_path"}
            HttpResponse(json.dumps(response))

        year = data.get("year")
        name = data.get("name")


        # file_path = BASE_DIR + "/files/" + year + name +".doc"

        file = open(BASE_DIR + "/files/" + file_name+".doc", "rb")
        response = HttpResponse(file)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = "attachment:filename={}".format(file_name+".docx")
        file.close()
        return response


class UpdateAnnualMeeting(View):
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        year = req_data.get("year")
        name = req_data.get("name")
        form = req_data.get("form", {})
        motion = req_data.get("motion")
        leijimotion = req_data.get("leijimotion")
        addmotion = req_data.get("addmotion", [])
        addleijimotion = req_data.get("addleijimotion", [])
        for i in addleijimotion:
            addmotion.remove(i)
        address = form.get("address")
        date1 = form.get("date1")
        date2 = form.get('date2')
        descr = form.get("descr")
        if " " in date1:

            stru_date = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
        else:
            stru_date = datetime.strptime(date1 +"\xa0" + date2, "%Y-%m-%d %H:%M")

        m = Meeting.objects.filter(year=year, name=name)
        m.update(date=stru_date, address=address, descr=descr)
        MotionBook.objects.exclude(name__in=motion).filter(annual_meeting=m[0]).delete()
        AccumulateMotion.objects.exclude(name__in=leijimotion).filter(annual_meeting=m[0]).delete()

        for i in addmotion:
            if i.get("motion"):
                MotionBook.objects.create(name=i.get("motion"), annual_meeting=m[0])

        for i in addleijimotion:
            if i.get("motion"):
                AccumulateMotion.objects.create(name=i.get("motion"), annual_meeting=m[0])

        return JsonResponse({"success": 1, "msg": "更新成功"})

class Teller(View):
    def post(self, request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        row = req_data.get("row")
        print(row)
        con = get_redis_connection("default")
        con.set("vote", 1, ex=3600, nx=True)  # 一个小时后清除,nx=True只有vote不存在时添加
        motions = row["motion"]
        for m in motions:
            id = str(m.get("id"))
            checked = m.get("checked")
            if checked == 2:
                name = id + "fandui"
                # 集合类型，根据name可设置并获取一个集合
                con.sadd(name, row["id"])
            elif checked == 3:
                name = id + "qiquan"
                con.sadd(name, row["id"])

            ishuibi = m.get("ishuibi")
            if ishuibi:
                descr = m.get("descr")
                name = id + "huibi"
                # 哈希类型， name是议案id+“huibi”组成的字符串，key是投回避票股东的id，value是他的回避描述，{name:{k1:v1,k2:v2}}
                con.hset(name, row["id"], descr)
        return JsonResponse({"success": 1, "msg": "唱票成功"})

class Tongji(View):
    def get(self, request):
        res = request.session.keys()
        print(res)
        return HttpResponse(json.dumps(res))
        # return JsonResponse({"success": 1, "msg": "唱票成功"})
