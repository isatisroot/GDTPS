
"""
解析excel导入的数据，针对普通议题A股、普通议题B股、累计议题A股、累计议题B股提供四种方法统计
然后合并到现场投票当中
"""
import xlrd
from GDVoteSys.settings import BASE_DIR
from apps.models import Meeting, ShareholderInfo, NetworkVoteCount, OnSiteMeeting, GB, VoteRecordDetail, MotionBook


class ParseExcel():
    def __init__(self, excelName, year, meeting_name):
        """一个实例化对象只打开一个工作簿"""
        self.excelName = excelName
        self.year = year
        self.meeting_name = meeting_name

        self.meeting = Meeting.objects.get(year=year, name=meeting_name)
        self.qs_all = ShareholderInfo.objects.all()

        # 股本类型，A股还是B股
        if "A" in self.excelName:
            self.equityType = "A"
        else:
            self.equityType = "B"
        # 议案类型，normal普通议案，cumulative累计投票议案
        if "普通" in self.excelName:
            self.motionType = "normal"
        else:
            self.motionType = "cumulative"

        __path = BASE_DIR + "\\files\\" + excelName
        __book = xlrd.open_workbook(__path)
        self.sheet = __book.sheet_by_index(0)
        self.row_num = self.sheet.nrows # 获取列表有效行数
    def __get_each_motion_rows(self):
        """
        每项议案有若干个人投票，占据若干行，找出每项议案第一个投票人所在的行数
        :return: 数组的元素是每项议案第一个投票人所在行数。长度是议案数量
        """
        rows_array = []
        motion_num = [] # excel表中的提案号
        for i in range(1,self.row_num):
            v0 = self.sheet.cell_value(i - 1,5).rstrip("\x00")
            v1 = self.sheet.cell_value(i, 5).rstrip("\x00")
            if v1 != v0:
                rows_array.append(i)
                motion_num.append(v1)
        # 得到例如[1,11,21]列表，表示第一项议案投票股东所在行数在1-11行之间，第二项议案投票股东所在行数在11-21之间
        rows_array.append(self.row_num)
        # 反转为了后面更好的使用pop取数
        rows_array.reverse()
        return rows_array, motion_num
            
    def create_gd(self):
        """:param
        在excel表中逐行与数据库进行比对，发现该行的股东并不存在与数据库时，添加该股东至库中
        根据证券账户（股东代码卡）与数据库中登记表对比找出非中小股股东，即大股东或董监高
        """
        rows_array, _ = self.__get_each_motion_rows()
        # start_row excel表中第一行股东数据， end_row末行股东数据
        start_row = rows_array.pop()
        end_row = rows_array.pop()

          # 所有股东信息
        onSite_qs_all = self.meeting.onsitemeeting_set.all() # 股东出席登记表——参加此次会议的所有股东
        gb = GB.objects.last()

        account_set = set()
        for i in range(start_row, end_row):
            row_data = self.sheet.row_values(i, 0, 4)
            account = row_data[0].rstrip("\x00")
            gdxm = row_data[1].rstrip("\x00")
            sfz = row_data[2].rstrip("\x00")
            shares = int(row_data[3])
            qs = self.qs_all.filter(gddmk=account)
            onSite_qs = []
            shareholder = None
            # 如果为真说明在数据库股东信息表中存在这个股东，无需再添加该股东;
            if qs:
                shareholder = qs[0]
                # 判断该股东是否是中小股，不是则添加到集合中
                if qs[0].gdtype != "中小股":
                    account_set.add((qs[0].id, qs[0].gddmk))

                # 如果excel里的持股数和数据库中不匹配，则将excel里的更新到库中
                if self.equityType == "A" and qs[0].gzA != shares:
                    ShareholderInfo.objects.filter(gddmk=account).update(gzA=shares)
                elif self.equityType == "B" and qs[0].gzB != shares:
                    ShareholderInfo.objects.filter(gddmk=account).update(gzB=shares)

            else:
                percent = shares / gb.gb
                if self.equityType == "A" :
                    # 如果小于5%则是中小股东
                    shareholder = ShareholderInfo.objects.create(gddmk=account,gdxm=gdxm,sfz=sfz,
                                                                 gzA=shares, gzB=0, gdtype="中小股" if percent < 0.05 else None)
                elif self.equityType == "B":
                    shareholder = ShareholderInfo.objects.create(gddmk=account,gdxm=gdxm,sfz=sfz,
                                                                 gzA=0, gzB=shares, gdtype="中小股" if percent < 0.05 else None)

            onSite_qs = onSite_qs_all.filter(shareholder_id=shareholder.id)
            # 如果表中没有数据，且shareholer存在时，新增数据，如果shareholder为空，不管onSite_qs为真还是假都无法进入里面的判断
            if not onSite_qs and shareholder:
                # excel表中的股东是已投票的股东，表明他们参加了此次会议，因此补录到股东会议登记表，
                if self.equityType == "A":
                    OnSiteMeeting.objects.create(cx=True, xcorwl=False, meeting_id=self.meeting.id,
                                             shareholder_id=shareholder.id, rs=1, gzA=shares)
                if self.equityType == "B":
                    OnSiteMeeting.objects.create(cx=True, xcorwl=False, meeting_id=self.meeting.id,
                                                 shareholder_id=shareholder.id, rs=1, gzB=shares)

        return account_set
    def match_motion(self):
        """
        :param year:
        :param meeting_name:
        :return:
        excel表中的议案是1000,2000,3000……这样的顺序标识多个议案的，现在要将这些顺序与数据库中
        议案id一一对应，1000对应该会议里的第一个议案，以此类推
        :return motions_match=(('1000', 17), ('2000', 18)), 1000是excel议案号，17是数据库议案id
        """
        _, motion_num = self.__get_each_motion_rows()
        print(motion_num)
        # 从数据库中取出议案，并组装成（17,18）这样的元组
        motions = tuple(zip(*self.meeting.motionbook_set.all().values_list("id")))[0]
        motions_match = tuple(zip(motion_num, motions))  # 将两个元组里的元素一一对应组成字典

        return motions_match

    def __sum_motion(self, motions_match):
        """
        :param equityType: A股还是B股
        统计普通议案网络投票的情况，
        """

        rows_array,_ = self.__get_each_motion_rows()
        # 列表元素减1则为议案数量
        motions = len(rows_array)
        end = None
        for idx in range(1, motions):
            start = end if end != None else rows_array.pop()
            end = rows_array.pop()
            print(start, end)
            motion_id = motions_match[idx - 1][1]
            motion = MotionBook.objects.get(id=motion_id)
            sum_zancheng = sum_fandui = sum_qiquan = 0
            # 从start到end都是相同的议案，这里是对相同议案不同股东进行投票统计
            for row in range(start, end):
                row_data = self.sheet.row_values(row, 0, 8)
                account = row_data[0].rstrip("\x00")
                vote = int(row_data[4])
                votingResult = row_data[7].rstrip("\x00")

                qs = self.qs_all.filter(gddmk=account)
                if qs:
                    shareholder= qs[0]
                    exist = VoteRecordDetail.objects.filter(gdId=shareholder.id, motionId=motion_id)
                    if not exist:
                        equityType= 0 if self.equityType == "A" else 1
                        if "同意" in votingResult:
                            VoteRecordDetail.objects.create(gdId=shareholder, motionId=motion, vote=1,
                                                            equityType= equityType)
                            sum_zancheng += vote
                        elif "反对" in votingResult:
                            VoteRecordDetail.objects.create(gdId=shareholder, motionId=motion, vote=2, equityType=equityType)
                            sum_fandui += vote
                        elif "弃权" in votingResult:
                            VoteRecordDetail.objects.create(gdId=shareholder, motionId=motion, vote=3, equityType=equityType)
                            sum_qiquan += vote

            # motion_idx是1,2,3……这样的数字，代表excel表中的1000,2000,3000……
            # 将其替换为表中议案的id，如此字典里键是议案的id，值是该议案对应的值
            # defaults是需要更新的数据字典，后面参数是用来查询的是否存在的，如果存在就更新，反之insert
            NetworkVoteCount.objects.update_or_create(
                defaults={
                "zancheng": sum_zancheng,
                "fandui":  sum_fandui,
                "qiquan":  sum_qiquan,
                "motion_id": motion_id,
                "equityType": 0 if self.equityType == "A" else 1,
                "excelName": self.excelName
                },
                motion_id=motion_id
            )

    def __sum_leijimotion(self):
        pass

    def run_sum(self):
        """运行统计程序，根据excel的名称，识别是普通还是累计议案，然后调用相应的方法进行统计"""
        if self.motionType == "normal":
            self.create_gd()
            self.__sum_motion(self.match_motion())
        else:
            self.__sum_leijimotion()



# if __name__ == '__main__':
#     path = r"C:\Users\admin\WebstormProjects\GDTPS\backend\GDVoteSys\files\佛山照明(000541)-B股股东普通议题投票结果明细202012181505.xls"
#     excel = ParseExcel(path)
