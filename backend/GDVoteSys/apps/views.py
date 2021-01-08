import json
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponseBadRequest
from .models import Meeting, ShareholderInfo

from datetime import datetime,date,timedelta


class QueryYear(View):
    def get(self, request):
        try:
            m = Meeting.objects.get(current_year=1)
            # 将时间提前10分钟并转化为字符串格式
            m.date = m.date + timedelta(minutes=-10)
            str_date = m.date.strftime('%Y年%m月%d日 %H时%M分')
            print(str_date)
            qs = Meeting.objects.filter(year=m.year)
            meeting_list = []
            for q in qs:
                meeting_list.append(q.name)
            return JsonResponse({"year": m.year, "name": m.name, "date": str_date, "meeting_list": meeting_list})
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
        print(motion)
        text = ''
        for i in motion:
            text += i['motion']+ ";"
        print(text)
        try:
            try:
                q = Meeting.objects.get(current_year=1)
                q.current_year = False
                q.save()
            except Exception as e:
                print(e)

            stru_date = datetime.strptime(date1 +"\xa0" + date2, "%Y-%m-%d %H:%M")
            m = Meeting.objects.create(year=year, date=stru_date, name=name, current_year=1, address=address,motion=text)
            m.members.set(gdid_list)
            return JsonResponse({'msg': 'success'})
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
#         # response["Access-Control-Allow-Origin"] = "*"
#         # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
#         # response["Access-Control-Max-Age"] = "1000"
#         # response["Access-Control-Allow-Headers"] = "*"
        return response
#
class QueryDetail(View):
    def get(self, request, year, meeting_name):
#         # year = request.GET.get('year')
#         # meeting_name = request.GET.get('meeting_name')
#         print(year, meeting_name)
        global str_date
        detail_list = []
        motion = []
        try:
            m = Meeting.objects.get(year=year,name=meeting_name)
            queryset = m.onsitemeeting_set.all()
            _d = m.date + timedelta(minutes=-10)
            str_date = _d.strftime('%Y年%m月%d日 %H时%M分')
            motion = m.motion.split(";")
            motion.pop()
            print(motion)
            for i in queryset:
                q = i.shareholder
                print(i.cx)
                data = {
                    'cx': i.cx,
                    'xc': i.xcorwl,
                    'gdxm': q.gdxm,
                    'gdtype': q.gdtype,
                    'gddmk': q.gddmk,
                    'sfz': q.sfz,
                    'rs': q.rs,
                    'frA': q.frA,
                    'gzA': q.gzA,
                    'gzB': q.gzB,
                    'dlr': q.dlr,
                    'meno': q.meno
                }
                detail_list.append(data)
        except Exception as e:
            print(e)

        # print(detail_list)


        return JsonResponse({'date': str_date, 'motion':motion, 'list':detail_list})
