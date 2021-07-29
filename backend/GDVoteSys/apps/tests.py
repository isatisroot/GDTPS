from django.test import TestCase

# Create your tests here.
from utils.parse_excel import ParseExcel
from GDVoteSys.settings import BASE_DIR

class MyTestCase(TestCase):
    def test_something(self):
        path = BASE_DIR + r"\files\佛山照明(000541)-B股股东普通议题投票结果明细202012181505.xls"
        excel = ParseExcel(path)
        # rows_array = excel.get_each_motion_rows()
        # print(rows_array)
        excel.sum()
        print(excel.get_zancheng())


if __name__ == '__main__':
    MT = MyTestCase()
    MT.test_something()