from subprocess import run
import re
import bwz_crawler
import chart


async def table():
    print("欢迎使用热搜榜分析器")
    while True:
        print("请选择要查看的热搜榜单类别，热搜榜单有以下三个类别: \n微博、百度、知乎\n请在下方输入其名称以选择:")
        while True:
            class_str = input()
            if class_str == "微博":
                class_name = 1
                break
            elif class_str == "百度":
                class_name = 2
                break
            elif class_str == "知乎":
                class_name = 3
                break
            else:
                print("输入格式有误，请重新输入")
        time = []
        print("请选择想要分析的时间，分别选择月、日、时（0-23）")

        while True:
            month = input("月:")
            month = re.sub(r'\D', '', month)
            time.append(month)
            month = int(month)
            if (month <= 12) and (month >= 1):
                break
            else:
                print("月份输入错误,请重新输入")
                time.pop()

        while True:
            day = input("日:")
            day = re.sub(r'\D', '', day)
            time.append(day)
            day = int(day)
            if month in [1, 3, 5, 7, 8, 10, 12]:
                if day <= 31 and day >= 1:
                    break
                else:
                    print("日期输入错误,请重新输入")
                    time.pop()
            elif month in [4, 6, 9, 11]:
                if day <= 30 and day >= 1:
                    break
                else:
                    print("日期输入错误,请重新输入")
                    time.pop()
            elif month == 2:
                if day <= 28 and day >= 1:
                    break
                else:
                    print("日期输入错误，请重新输入")
                    time.pop()

        while True:
            hour = input("时:")
            hour = re.sub(r'\D', '', hour)
            time.append(hour)
            hour = int(hour)
            if hour <= 23 and hour >= 0:
                break
            else:
                print("小时输入错误,请重新输入")
                time.pop()

        # 预留给API，用以生成并打开图表
        ps_command = chart.makecharts(time, class_name)
        run(["powershell.exe", ps_command], shell=True)

        print("是否选择继续查看其他时间点的其他榜单？\n是的话输入任意键，否的话输入N")
        choice = input()
        if choice == "N":
            print("table任务结束")
            break


if __name__ == '__main__':
    table()
