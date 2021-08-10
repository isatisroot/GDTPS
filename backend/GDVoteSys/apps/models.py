
from django.db import models

# Create your models here.


class ShareholderInfo(models.Model):
    # BE_PRESENT_CHOICE = (
    #     (0,'否'),
    #     (1,'是')
    # )

    # year = models.CharField(max_length=4, verbose_name="会议年份")
    # xh = models.SmallIntegerField()
    # cx = models.SmallIntegerField(choices=BE_PRESENT_CHOICE, verbose_name="是否出席")
    # xcorwl = models.SmallIntegerField(choices=BE_PRESENT_CHOICE,verbose_name="是否出席现场")
    gdxm = models.CharField(max_length=120) # 股东姓名
    gdtype = models.CharField(max_length=20, null=True) # 股东类型
    gddmk = models.CharField(max_length=15, unique=True)
    sfz = models.CharField(max_length=25, null=True)

    rs = models.SmallIntegerField(null=True)
    frA = models.IntegerField(null=True)
    gzA = models.IntegerField(null=True)
    gzB = models.IntegerField(null=True)
    dlr = models.CharField(max_length=10, null=True)  # 代理人
    # meno = models.CharField(max_length=20) # 备注

    # hconference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name="会议类型")

    def __str__(self):
        return self.gdxm

    class Meta:
        db_table = 'gdbook'
        verbose_name = '股东信息花名册'
        verbose_name_plural = verbose_name

class GB(models.Model):
    year = models.SmallIntegerField(verbose_name="会议年份")
    gb = models.IntegerField()
    ltag = models.IntegerField()
    ltbg = models.IntegerField()
    fltg = models.IntegerField()

    class Meta:
        db_table = 'gb'
        verbose_name = '股本信息表'
        verbose_name_plural = verbose_name

class Meeting(models.Model):
    year = models.SmallIntegerField(verbose_name="会议年份")
    current_year = models.BooleanField(default=False)
    # DateField精确到天，DateTimeField精确到秒
    date = models.DateTimeField()
    name = models.CharField(verbose_name="会议类型", max_length=20)
    motion = models.CharField(max_length=100, verbose_name="议案主题",default="")
    address = models.CharField(max_length=25, default="")
    descr = models.CharField(max_length=250, null=True)
    is_tongji = models.BooleanField(default=False, null=True)
    members = models.ManyToManyField(ShareholderInfo, through="OnSiteMeeting")
    # gb_id = models.SmallIntegerField(default=1)
    gb = models.ForeignKey(GB,  on_delete=models.SET_NULL, null=True) # 一对多，gb表是一，annual_meeting是多，当gb表记录删除时，该外键值she为null

    def __str__(self):
        return str(self.year) + self.name

    class Meta:
        db_table = 'annual_meeting'
        verbose_name = '年度会议登记本'
        verbose_name_plural = verbose_name


class OnSiteMeeting(models.Model):
    BE_PRESENT_CHOICE = (
        (0,'否'),
        (1,'是')
    )


    # gb = models.ForeignKey(GB, on_delete=models.CASCADE)
    shareholder = models.ForeignKey(ShareholderInfo, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    cx = models.BooleanField(default=False, verbose_name="是否出席")
    xcorwl = models.BooleanField(default=False,verbose_name="是否出席现场")
    rs = models.IntegerField(default=1, verbose_name="人数")
    gzA = models.IntegerField(default=0)
    gzB = models.IntegerField(default=0)
    meno = models.CharField(max_length=20, default=None, null=True) # 备注

    class Meta:
        db_table = 'on_site_meeting'
        verbose_name = '现场会议登记表'
        verbose_name_plural = verbose_name


class MotionBook(models.Model):
    name = models.CharField(verbose_name="议案主题", max_length=80)
    zanchengA = models.IntegerField(null=True)
    zanchengB = models.IntegerField(null=True)
    fanduiA = models.IntegerField(null=True)
    fanduiB = models.IntegerField(null=True)
    qiquanA = models.IntegerField(null=True)
    qiquanB = models.IntegerField(null=True)
    zxg_zanchengA = models.IntegerField(null=True)
    zxg_zanchengB = models.IntegerField(null=True)
    zxg_fanduiA = models.IntegerField(null=True)
    zxg_fanduiB = models.IntegerField(null=True)
    zxg_qiA = models.IntegerField(null=True)
    zxg_qiB = models.IntegerField(null=True)
    is_huibi = models.BooleanField(default=False, null=True)
    huibiA = models.IntegerField(null=True)
    huibiB = models.IntegerField(null=True)
    descr = models.CharField(max_length=200, null=True)
    isCumulated = models.BooleanField(null=True)
    # is_tongji = models.BooleanField(default=False, null=True)
    sharehold = models.ManyToManyField(ShareholderInfo, through="VoteRecordDetail")
    annual_meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True)
    # 自关联，例如一个累计议案叫《关于选举吴或雷为公司董事的议案》，其子议案有两个《选举吴》和《选举雷》均关联该累计议案
    pid = models.ForeignKey("MotionBook", null=True, on_delete=models.CASCADE) # 级联删除，当累计议案被删除时，子议案也被删除

    class Meta:
        db_table = 'motion_book'
        verbose_name = '议案信息表'
        verbose_name_plural = verbose_name

class AccumulateMotion(models.Model):
    """累积议案表"""
    name = models.CharField(verbose_name="议案主题", max_length=80)
    zanchengA = models.IntegerField(null=True)
    zanchengB = models.IntegerField(null=True)
    # is_tongji = models.IntegerField(default=False, null=True)
    annual_meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'accumulate_book'
        verbose_name = '议案信息表'
        verbose_name_plural = verbose_name

class NetworkVoteCount(models.Model):
    """网络投票统计记录表，由parse_excel工具类解析excel数据统计完成后存储在该表中"""
    EQUITY_TYPE_CHOICE = (
        (0,'A'),
        (1,'B')
    )
    zancheng = models.IntegerField(null=True)
    fandui = models.IntegerField(null=True)
    qiquan = models.IntegerField(null=True)
    motion_id = models.IntegerField(null=True)
    equityType = models.SmallIntegerField(choices=EQUITY_TYPE_CHOICE)
    excelName = models.CharField(max_length=120)
    class Meta:
        db_table = 'network_vote_count'
        verbose_name = '网络投票统计表'
        verbose_name_plural = verbose_name

class VoteRecordDetail(models.Model):
    """记录各股东对各议案投票记录,是会议议案表和股东信息表多对多关系的中间表"""
    VOTE_CHOICE = (
        (1, "赞成"),
        (2, "反对"),
        (3, "弃权"),
        (4, "回避")
    )
    EQUITY_TYPE_CHOICE = (
        (0,'A'),
        (1,'B')
    )
    gdId = models.ForeignKey(ShareholderInfo, on_delete=models.CASCADE)
    motionId = models.ForeignKey(MotionBook, on_delete=models.CASCADE)
    zanchengVote = models.IntegerField(null=True)
    vote = models.SmallIntegerField(choices=VOTE_CHOICE, null=True)
    equityType = models.SmallIntegerField(choices=EQUITY_TYPE_CHOICE)
    huibi_descr = models.CharField(max_length=120, default=None, null=True)

    class Meta:
        db_table = 'vote_record_detail'
        verbose_name = '投票记录统计表'
        verbose_name_plural = verbose_name