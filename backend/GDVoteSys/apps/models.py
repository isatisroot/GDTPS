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
    gdxm = models.CharField(max_length=20) # 股东姓名
    gdtype = models.CharField(max_length=20) # 股东类型
    gddmk = models.CharField(max_length=15)
    sfz = models.CharField(max_length=25)

    rs = models.SmallIntegerField()
    frA = models.IntegerField()
    gzA = models.IntegerField()
    gzB = models.IntegerField()
    dlr = models.CharField(max_length=10)  # 代理人
    meno = models.CharField(max_length=20) # 备注

    # hconference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name="会议类型")

    def __str__(self):
        return self.gdxm

    class Meta:
        db_table = 'gdbook'
        verbose_name = '股东信息花名册'
        verbose_name_plural = verbose_name

class Meeting(models.Model):
    year = models.SmallIntegerField(verbose_name="会议年份")
    current_year = models.BooleanField(default=False)
    # DateField精确到天，DateTimeField精确到秒
    date = models.DateTimeField()
    name = models.CharField(verbose_name="会议类型", max_length=20)
    motion = models.CharField(max_length=100, verbose_name="议案主题",default="")
    address = models.CharField(max_length=25, default="")
    members = models.ManyToManyField(ShareholderInfo, through="OnSiteMeeting")

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

    shareholder = models.ForeignKey(ShareholderInfo, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    cx = models.BooleanField(default=False, verbose_name="是否出席")
    xcorwl = models.BooleanField(default=False,verbose_name="是否出席现场")

    class Meta:
        db_table = 'on_site_meeting'
        verbose_name = '现场会议登记表'
        verbose_name_plural = verbose_name


