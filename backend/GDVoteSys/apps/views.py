import json
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponseBadRequest
from .models import Meeting, ShareholderInfo,OnSiteMeeting,GB

from datetime import datetime,date,timedelta
# from django.utils import timezone as datetime

class QueryYear(View):
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
            # 通过m查找现场会议登记的中间表
            queryset = m.onsitemeeting_set.all()
            # _d = m.date + timedelta(minutes=-10)
            str_date = m.date.strftime('%Y-%m-%d %H:%M:%S')
            motion = m.motion.split(";")
            motion.pop()
            # print(motion)
            for i in queryset:
                # 根据中间表查找到股东信息表
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
                    'gzA': q.gzA,
                    'gzB': q.gzB,
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
        try:
            m = Meeting.objects.get(year=year,name=meeting_name)
            for data in tableData:
                id = data.get("id",None)
                OnSiteMeeting.objects.filter(meeting_id=m.id, shareholder=id).update(
                    cx=data.get("cx"),
                    xcorwl=data.get("xc"),
                    gzA=int(data.get("gzA")),
                    gzB=int(data.get("gzB")),
                    meno = data.get("meno")
                )
                ShareholderInfo.objects.filter(id=id).update(
                    gdxm=data.get("gdxm"),
                    gdtype = data.get("gdtype"),
                    gddmk = data.get("gddmk"),
                    sfz = data.get("sfz"),
                    rs = data.get("rs"),
                    gzA = data.get("gzA"),
                    gzB = data.get("gzB")
                )
            return JsonResponse({'code':200, 'msg':'更新成功'})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content_type="'application/json'")



class Upload(View):
    def post(self, request):
        print(request.body)
        return JsonResponse({'code': 200, 'msg': '上传成功'})