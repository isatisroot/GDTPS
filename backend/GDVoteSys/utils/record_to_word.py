from docx import Document
from apps.models import Meeting, ShareholderInfo, OnSiteMeeting, GB, MotionBook, AccumulateMotion
class RecordToWord():
    """
    将统计的唱票结果写入到word文档中
    """
    def __init__(self):
        self.document = Document()
    def vote_result(self,year, name):
        m = Meeting.objects.filter(year=year, name=name)[0]
        totalShare= m.gb.gb
        AShareTotal= m.gb.ltag
        BShareTotal=m.gb.ltbg
        qs = m.onsitemeeting_set.all()
        qs1 = qs.filter(cx=True)
        cx_num = len(qs1)
        cx_gb = 0
        for q in qs1:
            cx_gb += q.gzA + q.gzB
        percent1 = cx_gb / totalShare
        cx_gb = format(cx_gb, ",")  # 转千分符

        qs2 = qs.filter(cx=True, xcorwl=True)
        xcorwl_num = len(qs2)
        xcorwl_gb = 0
        for q in qs2:
            xcorwl_gb += q.gzA + q.gzB
        percent2 = xcorwl_gb / totalShare
        xcorwl_gb = format(xcorwl_gb, ",")

        qs3= qs.filter(cx=True, xcorwl=False)
        wl_num = len(qs3)
        wl_gb = 0
        for q in qs3:
            wl_gb += q.gzA + q.gzB
        percent3 = wl_gb / totalShare
        wl_gb = format(wl_gb, ",")

        self.document.add_heading("佛山电器照明股份有限公司", level=2)
        self.document.add_heading("{}议案投票表决统计结果".format(year+name), level=1)

        self.document.add_paragraph("1.出席的总体情况：")
        content1 = """股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{:.2%}。其中,现场会议股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{:.2%}。网络投标股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{:.2%}。"""\
            .format(cx_num, cx_gb, percent1, xcorwl_num, xcorwl_gb, percent2, wl_num, wl_gb, percent3)
        self.document.add_paragraph(content1)


        self.document.add_paragraph("2.A股股东出席情况：")
        qs4 = qs.filter(gzA__gt=0)
        num4 = len(qs4)
        sum4 = 0
        for q in qs4:
            sum4 += q.gzA
        percent4 = sum4 / AShareTotal
        sum4 = format(sum4, ",")

        qs5 = qs.filter(gzB__gt=0)
        num5 = len(qs5)
        sum5 = 0
        for q in qs5:
            sum5 += q.gzB
        percent5 = sum5 / BShareTotal
        sum5 = format(sum5, ",")
        content2 = """A股股东（代理人）{}人，代表股份{}股，占公司A股股东表决权股份{:.2%}。其中,现场会议股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{:.2%}。网络投标股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{:.2%}。"""\
            .format(num4, sum4, percent4, num5, sum5, percent5, wl_num, wl_gb, percent3)
        self.document.add_paragraph(content2)
        self.document.save("./"+year+name+".doc")

