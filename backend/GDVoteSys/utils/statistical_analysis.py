# _*_ coding:utf-8 _*_
# Version 1.0
# Date: 2021-8-2

""" 用于统计表决情况，查询当前会议下每一项普通议案的A股、B股各自的总赞成、反对、弃权、回避票数,以及占出席会议等。
    同时统计每项普通议案中小股东总赞成、反对、弃权、回避票数等。
    统计每项累计议案总赞成票数，中小股东总赞成票数"""
from django_redis import get_redis_connection

from apps.models import Meeting, OnSiteMeeting, MotionBook
from django.core.exceptions import ObjectDoesNotExist
class Statistical():
    def per_motion(self,meeting, motion):
        """统计单个议案的投票情况
        :param
        meeting: Meeting模型类对象
        motion: MotionBook模型类对象"""
        ASumZan = BSumzan = ASumFan = BSumFan = ASumQiquan = BSumQiquan = ASumHuibi =BSumHuibi = 0
        ASumZanZXG = BSumzanZXG = ASumFanZXG = BSumFanZXG = ASumQiquanZXG = BSumQiquanZXG = 0
        HuibiDescr = ""

        # 查询该议案所有投票的股东id以及投票类型（赞成还是反对）
        voteQueryset = motion.voterecorddetail_set.all()
        for vq in voteQueryset:
            # vq.gdId是外键关联到的股东信息表gdbook的信息（元组形式），vq.gdId_id是vote_record_detail表gdId_id属性列上的值
            onSiteQueryset = OnSiteMeeting.objects.filter(shareholder_id = vq.gdId_id, meeting_id=meeting.id)
            if onSiteQueryset:
                # 如果vote是0，表示投的赞成票, equityType是0，表示A股
                if vq.equityType == 0:
                    if vq.vote == 1:
                        ASumZan += onSiteQueryset[0].gzA
                        if vq.gdId.gdtype == "中小股":
                            ASumZanZXG += onSiteQueryset[0].gzA
                    elif vq.vote == 2:
                        ASumFan += onSiteQueryset[0].gzA
                        if vq.gdId.gdtype == "中小股":
                            ASumFanZXG += onSiteQueryset[0].gzA
                    elif vq.vote == 3:
                        ASumQiquan += onSiteQueryset[0].gzA
                        if vq.gdId.gdtype == "中小股":
                            ASumQiquanZXG += onSiteQueryset[0].gzA
                    elif vq.vote == 4:
                        ASumHuibi += onSiteQueryset[0].gzA
                        if vq.huibi_descr:
                            HuibiDescr = vq.huibi_descr + ";"

                elif vq.equityType == 1:
                    if vq.vote == 1:
                        BSumzan += onSiteQueryset[0].gzB
                        if vq.gdId.gdtype == "中小股":
                            BSumzanZXG += onSiteQueryset[0].gzB
                    elif vq.vote == 2:
                        BSumFan += onSiteQueryset[0].gzB
                        if vq.gdId.gdtype == "中小股":
                            BSumFanZXG += onSiteQueryset[0].gzB
                    elif vq.vote == 3:
                        BSumQiquan += onSiteQueryset[0].gzB
                        if vq.gdId.gdtype == "中小股":
                            BSumQiquanZXG += onSiteQueryset[0].gzB
                    elif vq.vote == 4:
                        BSumHuibi += onSiteQueryset[0].gzB
                        if vq.huibi_descr:
                            HuibiDescr += vq.huibi_descr

        print(ASumZan, BSumzan)
        # 将统计完的数据更新到数据库中
        MotionBook.objects.update_or_create(
            defaults={
            "zanchengA": ASumZan,
            "zanchengB": BSumzan,
            "fanduiA": ASumFan,
            "fanduiB": BSumFan,
            "qiquanA": ASumQiquan,
            "qiquanB": BSumQiquan,
            "is_huibi": True if ASumHuibi >0 or BSumHuibi > 0 else False,
            "huibiA": ASumHuibi,
            "huibiB": BSumHuibi,
            "descr": HuibiDescr,
            "zxg_zanchengA": ASumZanZXG,
            "zxg_zanchengB": BSumzanZXG,
            "zxg_fanduiA": ASumFanZXG,
            "zxg_fanduiB": BSumFanZXG,
            "zxg_qiA": ASumQiquanZXG,
            "zxg_qiB": BSumQiquanZXG,
            },
            id=motion.id)
    def per_leijimotion(self, motion):
        """统计累计议案的赞成票，将redis中获取的赞成票与网络累计投票合并写入到MotionBook中"""
        con = get_redis_connection("default")
        Avalue = con.hget(motion.id, "A")
        Bvalue = con.hget(motion.id, "B")

        ASumZan = Avalue if Avalue else 0
        BSumzan = Bvalue if Bvalue else 0

        MotionBook.objects.update_or_create(
            defaults={
                "zanchengA": ASumZan,
                "zanchengB": BSumzan},
            id=motion.id)
        con.delete(motion.id)
    def all_motion(self, year, meeting_name):
        """自动统计该年度会议下所有普通议案的投票情况"""
        try:
            self.meeting = Meeting.objects.get(year=year, name=meeting_name)
            self.motionsQueryset = self.meeting.motionbook_set.all()

        except ObjectDoesNotExist as e:
            raise {"msg": "查无此会议"}
        for motion in self.motionsQueryset:
            self.per_motion(self.meeting, motion)