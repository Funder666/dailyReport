import requests
import datetime
from bs4 import BeautifulSoup
import base64
import json
import random
import sys

def get_cookies(studentInfo):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    loginUrl = "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MDY2NTA3MzEzODc1NDIzODYsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmIiwic3RhdGUiOiIifQ=="
    data = {"username": studentInfo[0],
            "password": studentInfo[1],
    }
    response = requests.post(loginUrl,headers=header,data=data,allow_redirects=False)
    response = requests.get("https://newsso.shu.edu.cn" + response.headers["location"], cookies=response.cookies,allow_redirects=False)
    response = requests.get(response.headers["location"],allow_redirects=False)
    return (response.cookies)



def daily_report(cookie,reportData,delayReport = False):  #最后个参数是补报用的
    # if(delayReport==False):
    #     reportUrl = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=" + reportData["Time_1or2"]
    # else:
    #     reportUrl = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day="+ reportData["date"].replace(" ","") + "t=" + reportData["Time_1or2"]
    reportUrl = "https://selfreport.shu.edu.cn/DayReport.aspx"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    response = requests.get(reportUrl, cookies=cookie)
    soup = BeautifulSoup(response.text, 'html.parser')
    view_state = soup.find('input', attrs={'name': '__VIEWSTATE'})
    data = {
        "__EVENTTARGET": "p1$ctl00$btnSubmit",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": view_state['value'],
        "__VIEWSTATEGENERATOR": "7AD7E509",
        "p1$ChengNuo": "p1_ChengNuo",
        "p1$BaoSRQ": reportData["date"],
        "p1$DangQSTZK": "良好",
        "p1$TiWen": "",
        "p1$JiuYe_ShouJHM": "",
        "p1$JiuYe_Email": "",
        "p1$JiuYe_Wechat": "",
        "p1$QiuZZT":  "",
        "p1$JiuYKN": "",
        "p1$JiuYSJ": "",
        "p1$TiWen": "",
        "p1$ZaiXiao": "不在校",
        "p1$MingTDX":"不到校",
        "p1$BanChe_1$Value": "0",
        "p1$BanChe_1": "不需要乘班车",
        "p1$BanChe_2$Value": "0",
        "p1$BanChe_2": "不需要乘班车",
        "p1$GuoNei": "国内",
        "p1$ddlGuoJia$Value": "-1",
        "p1$ddlGuoJia": "选择国家",
        "p1$ddlSheng$Value": reportData["sheng"],  #当天所在省
        "p1$ddlSheng":  reportData["sheng"],
        "p1$ddlShi$Value": reportData["shi"],#当天所在市
        "p1$ddlShi": reportData["shi"],
        "p1$ddlXian$Value": reportData["xian"],
        "p1$ddlXian": reportData["xian"],
        "p1$XiangXDZ": reportData["location"],
        # "p1$ddlXian$Value": reportData["county"],#当天所在县
        # "p1$ddlXian": reportData["county"],
       # "p1$XiangXDZ": reportData["location"],
        "p1$FengXDQDL": "否",
        "p1$TongZWDLH": "否",
        "p1$CengFWH": "否",
        "p1$CengFWH_RiQi": "",
        "p1$CengFWH_BeiZhu": "",
        "p1$JieChu": "否",
        "p1$JieChu_RiQi": "",
        "p1$JieChu_BeiZhu": "",
        "p1$TuJWH": "否",
        "p1$TuJWH_RiQi": "",
        "p1$TuJWH_BeiZhu": "",
        "p1$QueZHZJC$Value": "否",
        "p1$QueZHZJC": "否",
        "p1$DangRGL": "否",
        "p1$GeLDZ": "",
        "p1$FanXRQ": "",
        "p1$WeiFHYY": "",
        "p1$ShangHJZD": "",
        "p1$DaoXQLYGJ": "",
        "p1$DaoXQLYCS": "",
        "p1$JiaRen_BeiZhu": "",
        "p1$SuiSM": "绿色",
        "p1$LvMa14Days": "是",
        "p1$Address2": "",
        "F_TARGET": "p1_ctl00_btnSubmit",
        "p1_ContentPanel1_Collapsed": "true",
        "p1_GeLSM_Collapsed": "false",
        "p1_Collapsed": "false",
        'F_STATE': get_FState(reportData),
    }
    header = {
        'X-FineUI-Ajax': 'true',
    }
    response = requests.post(reportUrl, data=data, cookies=cookie,headers=header)
    print(response.text)
    return response.text.find("提交成功")


def get_FState(reportData):
    F_STATE_Former = "eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjEtMDEtMjMifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+Wlve+8iOS9k+a4qeS4jemrmOS6jjM3LjPvvIkiLDFdLFsi5LiN6YCCIiwi5LiN6YCCIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLoia/lpb0ifSwicDFfWmhlbmdaaHVhbmciOnsiSGlkZGVuIjp0cnVlLCJGX0l0ZW1zIjpbWyLmhJ/lhpIiLCLmhJ/lhpIiLDFdLFsi5ZKz5Ze9Iiwi5ZKz5Ze9IiwxXSxbIuWPkeeDrSIsIuWPkeeDrSIsMV1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfUWl1WlpUIjp7IkZfSXRlbXMiOltdLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfSml1WUtOIjp7IkZfSXRlbXMiOltdLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfSml1WVlYIjp7IlJlcXVpcmVkIjpmYWxzZSwiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9KaXVZWkQiOnsiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9KaXVZWkwiOnsiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9aYWlYaWFvIjp7IkZfSXRlbXMiOltbIuS4jeWcqOagoSIsIuS4jeWcqOagoSIsMV0sWyLlrp3lsbEiLCLlrp3lsbHmoKHljLoiLDFdLFsi5bu26ZW/Iiwi5bu26ZW/5qCh5Yy6IiwxXSxbIuWYieWumiIsIuWYieWumuagoeWMuiIsMV0sWyLmlrDpl7jot68iLCLmlrDpl7jot6/moKHljLoiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuS4jeWcqOagoSJ9LCJwMV9NaW5nVERYIjp7IlNlbGVjdGVkVmFsdWUiOiLkuI3liLDmoKEiLCJGX0l0ZW1zIjpbWyLkuI3liLDmoKEiLCLkuI3liLDmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9NaW5nVEpDIjp7IlJlcXVpcmVkIjpmYWxzZSwiSGlkZGVuIjp0cnVlLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV0sIlNlbGVjdGVkVmFsdWUiOm51bGx9LCJwMV9CYW5DaGVfMSI6eyJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIjAiLCLkuI3pnIDopoHkuZjnj63ovaYiLDEsIiIsIiJdLFsiMSIsIjHlj7fnur/vvJrlmInlrprmoKHljLrljZfpl6g9PuWuneWxseagoeWMuiIsMSwiIiwiIl0sWyIyIiwiMuWPt+e6v++8muWuneWxseagoeWMuj0+5ZiJ5a6a5qCh5Yy65Y2X6ZeoIiwxLCIiLCIiXSxbIjMiLCIz5Y+357q/77ya5bu26ZW/5qCh5Yy65YyX6ZeoPT7lrp3lsbHmoKHljLoiLDEsIiIsIiJdLFsiNCIsIjTlj7fnur/vvJrlrp3lsbHmoKHljLo9PuW7tumVv+agoeWMuuWMl+mXqCIsMSwiIiwiIl0sWyI1IiwiNeWPt+e6v++8muWYieWumuagoeWMuuWNl+mXqD0+5bu26ZW/5qCh5Yy65YyX6ZeoIiwxLCIiLCIiXSxbIjYiLCI25Y+357q/77ya5bu26ZW/5qCh5Yy65YyX6ZeoPT7lmInlrprmoKHljLrljZfpl6giLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIjAiXX0sInAxX0JhbkNoZV8yIjp7IkhpZGRlbiI6dHJ1ZSwiRl9JdGVtcyI6W1siMCIsIuS4jemcgOimgeS5mOePrei9piIsMSwiIiwiIl0sWyIxIiwiMeWPt+e6v++8muWYieWumuagoeWMuuWNl+mXqD0+5a6d5bGx5qCh5Yy6IiwxLCIiLCIiXSxbIjIiLCIy5Y+357q/77ya5a6d5bGx5qCh5Yy6PT7lmInlrprmoKHljLrljZfpl6giLDEsIiIsIiJdLFsiMyIsIjPlj7fnur/vvJrlu7bplb/moKHljLrljJfpl6g9PuWuneWxseagoeWMuiIsMSwiIiwiIl0sWyI0IiwiNOWPt+e6v++8muWuneWxseagoeWMuj0+5bu26ZW/5qCh5Yy65YyX6ZeoIiwxLCIiLCIiXSxbIjUiLCI15Y+357q/77ya5ZiJ5a6a5qCh5Yy65Y2X6ZeoPT7lu7bplb/moKHljLrljJfpl6giLDEsIiIsIiJdLFsiNiIsIjblj7fnur/vvJrlu7bplb/moKHljLrljJfpl6g9PuWYieWumuagoeWMuuWNl+mXqCIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsiMCJdfSwicDFfR3VvTmVpIjp7IkZfSXRlbXMiOltbIuWbveWGhSIsIuWbveWGhSIsMV0sWyLlm73lpJYiLCLlm73lpJYiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuWbveWGhSJ9LCJwMV9kZGxHdW9KaWEiOnsiRGF0YVRleHRGaWVsZCI6Ilpob25nV2VuIiwiRGF0YVZhbHVlRmllbGQiOiJaaG9uZ1dlbiIsIkhpZGRlbiI6dHJ1ZSwiRl9JdGVtcyI6W1siLTEiLCLpgInmi6nlm73lrrYiLDEsIiIsIiJdLFsi6Zi/5bCU5be05bC85LqaIiwi6Zi/5bCU5be05bC85LqaIiwxLCIiLCIiXSxbIumYv+WwlOWPiuWIqeS6miIsIumYv+WwlOWPiuWIqeS6miIsMSwiIiwiIl0sWyLpmL/lr4zmsZciLCLpmL/lr4zmsZciLDEsIiIsIiJdLFsi6Zi/5qC55bu3Iiwi6Zi/5qC55bu3IiwxLCIiLCIiXSxbIumYv+aLieS8r+iBlOWQiOmFi+mVv+WbvSIsIumYv+aLieS8r+iBlOWQiOmFi+mVv+WbvSIsMSwiIiwiIl0sWyLpmL/psoHlt7QiLCLpmL/psoHlt7QiLDEsIiIsIiJdLFsi6Zi/5pu8Iiwi6Zi/5pu8IiwxLCIiLCIiXSxbIumYv+WhnuaLnOeWhiIsIumYv+WhnuaLnOeWhiIsMSwiIiwiIl0sWyLln4Plj4oiLCLln4Plj4oiLDEsIiIsIiJdLFsi5Z+D5aGe5L+E5q+U5LqaIiwi5Z+D5aGe5L+E5q+U5LqaIiwxLCIiLCIiXSxbIueIseWwlOWFsCIsIueIseWwlOWFsCIsMSwiIiwiIl0sWyLniLHmspnlsLzkupoiLCLniLHmspnlsLzkupoiLDEsIiIsIiJdLFsi5a6J6YGT5bCUIiwi5a6J6YGT5bCUIiwxLCIiLCIiXSxbIuWuieWTpeaLiSIsIuWuieWTpeaLiSIsMSwiIiwiIl0sWyLlronlnK3mi4kiLCLlronlnK3mi4kiLDEsIiIsIiJdLFsi5a6J5o+Q55Oc5ZKM5be05biD6L6+Iiwi5a6J5o+Q55Oc5ZKM5be05biD6L6+IiwxLCIiLCIiXSxbIuWlpeWcsOWIqSIsIuWlpeWcsOWIqSIsMSwiIiwiIl0sWyLlpaXlhbDnvqTlspsiLCLlpaXlhbDnvqTlspsiLDEsIiIsIiJdLFsi5r6z5aSn5Yip5LqaIiwi5r6z5aSn5Yip5LqaIiwxLCIiLCIiXSxbIuW3tOW3tOWkmuaWryIsIuW3tOW3tOWkmuaWryIsMSwiIiwiIl0sWyLlt7TluIPkuprmlrDlh6DlhoXkupoiLCLlt7TluIPkuprmlrDlh6DlhoXkupoiLDEsIiIsIiJdLFsi5be05ZOI6amsIiwi5be05ZOI6amsIiwxLCIiLCIiXSxbIuW3tOWfuuaWr+WdpiIsIuW3tOWfuuaWr+WdpiIsMSwiIiwiIl0sWyLlt7Tli5Lmlq/lnaYiLCLlt7Tli5Lmlq/lnaYiLDEsIiIsIiJdLFsi5be05p6XIiwi5be05p6XIiwxLCIiLCIiXSxbIuW3tOaLv+mprCIsIuW3tOaLv+mprCIsMSwiIiwiIl0sWyLlt7Topb8iLCLlt7Topb8iLDEsIiIsIiJdLFsi55m95L+E572X5pavIiwi55m95L+E572X5pavIiwxLCIiLCIiXSxbIueZvuaFleWkpyIsIueZvuaFleWkpyIsMSwiIiwiIl0sWyLkv53liqDliKnkupoiLCLkv53liqDliKnkupoiLDEsIiIsIiJdLFsi6LSd5a6BIiwi6LSd5a6BIiwxLCIiLCIiXSxbIuavlOWIqeaXtiIsIuavlOWIqeaXtiIsMSwiIiwiIl0sWyLlhrDlspsiLCLlhrDlspsiLDEsIiIsIiJdLFsi5rOi5aSa6buO5ZCEIiwi5rOi5aSa6buO5ZCEIiwxLCIiLCIiXSxbIuazouWFsCIsIuazouWFsCIsMSwiIiwiIl0sWyLms6Lmlq/lsLzkuprlkozpu5HloZ7lk6Xnu7TpgqMiLCLms6Lmlq/lsLzkuprlkozpu5HloZ7lk6Xnu7TpgqMiLDEsIiIsIiJdLFsi54675Yip57u05LqaIiwi54675Yip57u05LqaIiwxLCIiLCIiXSxbIuS8r+WIqeWFuSIsIuS8r+WIqeWFuSIsMSwiIiwiIl0sWyLljZrojKjnk6bnurMiLCLljZrojKjnk6bnurMiLDEsIiIsIiJdLFsi5LiN5Li5Iiwi5LiN5Li5IiwxLCIiLCIiXSxbIuW4g+Wfuue6s+azlee0oiIsIuW4g+Wfuue6s+azlee0oiIsMSwiIiwiIl0sWyLluIPpmobov6oiLCLluIPpmobov6oiLDEsIiIsIiJdLFsi5biD57u05bKbIiwi5biD57u05bKbIiwxLCIiLCIiXSxbIuacnemynCIsIuacnemynCIsMSwiIiwiIl0sWyLotaTpgZPlh6DlhoXkupoiLCLotaTpgZPlh6DlhoXkupoiLDEsIiIsIiJdLFsi5Li56bqmIiwi5Li56bqmIiwxLCIiLCIiXSxbIuW+t+WbvSIsIuW+t+WbvSIsMSwiIiwiIl0sWyLkuJzluJ3msbYiLCLkuJzluJ3msbYiLDEsIiIsIiJdLFsi5Lic5bid5rG2Iiwi5Lic5bid5rG2IiwxLCIiLCIiXSxbIuWkmuWTpSIsIuWkmuWTpSIsMSwiIiwiIl0sWyLlpJrnsbPlsLzliqAiLCLlpJrnsbPlsLzliqAiLDEsIiIsIiJdLFsi5L+E572X5pav6IGU6YKmIiwi5L+E572X5pav6IGU6YKmIiwxLCIiLCIiXSxbIuWOhOeTnOWkmuWwlCIsIuWOhOeTnOWkmuWwlCIsMSwiIiwiIl0sWyLljoTnq4vnibnph4zkupoiLCLljoTnq4vnibnph4zkupoiLDEsIiIsIiJdLFsi5rOV5Zu9Iiwi5rOV5Zu9IiwxLCIiLCIiXSxbIuazleWbveWkp+mDveS8miIsIuazleWbveWkp+mDveS8miIsMSwiIiwiIl0sWyLms5XnvZfnvqTlspsiLCLms5XnvZfnvqTlspsiLDEsIiIsIiJdLFsi5rOV5bGe5rOi5Yip5bC86KW/5LqaIiwi5rOV5bGe5rOi5Yip5bC86KW/5LqaIiwxLCIiLCIiXSxbIuazleWxnuWcreS6mumCoyIsIuazleWxnuWcreS6mumCoyIsMSwiIiwiIl0sWyLmorXokoLlhogiLCLmorXokoLlhogiLDEsIiIsIiJdLFsi6I+y5b6L5a6+Iiwi6I+y5b6L5a6+IiwxLCIiLCIiXSxbIuaWkOa1jiIsIuaWkOa1jiIsMSwiIiwiIl0sWyLoiqzlhbAiLCLoiqzlhbAiLDEsIiIsIiJdLFsi5L2b5b6X6KeSIiwi5L2b5b6X6KeSIiwxLCIiLCIiXSxbIuWGiOavlOS6miIsIuWGiOavlOS6miIsMSwiIiwiIl0sWyLliJrmnpwiLCLliJrmnpwiLDEsIiIsIiJdLFsi5Yia5p6c77yI6YeR77yJIiwi5Yia5p6c77yI6YeR77yJIiwxLCIiLCIiXSxbIuWTpeS8puavlOS6miIsIuWTpeS8puavlOS6miIsMSwiIiwiIl0sWyLlk6Xmlq/ovr7pu47liqAiLCLlk6Xmlq/ovr7pu47liqAiLDEsIiIsIiJdLFsi5qC85p6X57qz6L6+Iiwi5qC85p6X57qz6L6+IiwxLCIiLCIiXSxbIuagvOmygeWQieS6miIsIuagvOmygeWQieS6miIsMSwiIiwiIl0sWyLmoLnopb/lspsiLCLmoLnopb/lspsiLDEsIiIsIiJdLFsi5Y+k5be0Iiwi5Y+k5be0IiwxLCIiLCIiXSxbIueTnOW+t+e9l+aZruWymyIsIueTnOW+t+e9l+aZruWymyIsMSwiIiwiIl0sWyLlhbPlspsiLCLlhbPlspsiLDEsIiIsIiJdLFsi5Zyt5Lqa6YKjIiwi5Zyt5Lqa6YKjIiwxLCIiLCIiXSxbIuWTiOiQqOWFi+aWr+WdpiIsIuWTiOiQqOWFi+aWr+WdpiIsMSwiIiwiIl0sWyLmtbflnLAiLCLmtbflnLAiLDEsIiIsIiJdLFsi6Z+p5Zu9Iiwi6Z+p5Zu9IiwxLCIiLCIiXSxbIuiNt+WFsCIsIuiNt+WFsCIsMSwiIiwiIl0sWyLpu5HlsbEiLCLpu5HlsbEiLDEsIiIsIiJdLFsi5rSq6YO95ouJ5pavIiwi5rSq6YO95ouJ5pavIiwxLCIiLCIiXSxbIuWfuumHjOW3tOaWryIsIuWfuumHjOW3tOaWryIsMSwiIiwiIl0sWyLlkInluIPmj5AiLCLlkInluIPmj5AiLDEsIiIsIiJdLFsi5ZCJ5bCU5ZCJ5pav5pav5Z2mIiwi5ZCJ5bCU5ZCJ5pav5pav5Z2mIiwxLCIiLCIiXSxbIuWHoOWGheS6miIsIuWHoOWGheS6miIsMSwiIiwiIl0sWyLlh6DlhoXkuprmr5Tnu40iLCLlh6DlhoXkuprmr5Tnu40iLDEsIiIsIiJdLFsi5Yqg5ou/5aSnIiwi5Yqg5ou/5aSnIiwxLCIiLCIiXSxbIuWKoOe6syIsIuWKoOe6syIsMSwiIiwiIl0sWyLliqDok6wiLCLliqDok6wiLDEsIiIsIiJdLFsi5p+s5Z+U5a+oIiwi5p+s5Z+U5a+oIiwxLCIiLCIiXSxbIuaNt+WFiyIsIuaNt+WFiyIsMSwiIiwiIl0sWyLmtKXlt7TluIPpn6YiLCLmtKXlt7TluIPpn6YiLDEsIiIsIiJdLFsi5ZaA6bqm6ZqGIiwi5ZaA6bqm6ZqGIiwxLCIiLCIiXSxbIuWNoeWhlOWwlCIsIuWNoeWhlOWwlCIsMSwiIiwiIl0sWyLnp5Hnp5Hmlq/vvIjln7rmnpfvvInnvqTlspsiLCLnp5Hnp5Hmlq/vvIjln7rmnpfvvInnvqTlspsiLDEsIiIsIiJdLFsi56eR5pGp572XIiwi56eR5pGp572XIiwxLCIiLCIiXSxbIuenkeeJuei/queTpiIsIuenkeeJuei/queTpiIsMSwiIiwiIl0sWyLnp5HlqIHnibkiLCLnp5HlqIHnibkiLDEsIiIsIiJdLFsi5YWL572X5Zyw5LqaIiwi5YWL572X5Zyw5LqaIiwxLCIiLCIiXSxbIuiCr+WwvOS6miIsIuiCr+WwvOS6miIsMSwiIiwiIl0sWyLlupPlhYvnvqTlspsiLCLlupPlhYvnvqTlspsiLDEsIiIsIiJdLFsi5ouJ6ISx57u05LqaIiwi5ouJ6ISx57u05LqaIiwxLCIiLCIiXSxbIuiOsee0ouaJmCIsIuiOsee0ouaJmCIsMSwiIiwiIl0sWyLogIHmjJ0iLCLogIHmjJ0iLDEsIiIsIiJdLFsi6buO5be05aupIiwi6buO5be05aupIiwxLCIiLCIiXSxbIueri+mZtuWumyIsIueri+mZtuWumyIsMSwiIiwiIl0sWyLliKnmr5Tph4zkupoiLCLliKnmr5Tph4zkupoiLDEsIiIsIiJdLFsi5Yip5q+U5LqaIiwi5Yip5q+U5LqaIiwxLCIiLCIiXSxbIuWIl+aUr+aVpuWjq+eZuyIsIuWIl+aUr+aVpuWjq+eZuyIsMSwiIiwiIl0sWyLnlZnlsLzmsarlspsiLCLnlZnlsLzmsarlspsiLDEsIiIsIiJdLFsi5Y2i5qOu5aChIiwi5Y2i5qOu5aChIiwxLCIiLCIiXSxbIuWNouaXuui+viIsIuWNouaXuui+viIsMSwiIiwiIl0sWyLnvZfpqazlsLzkupoiLCLnvZfpqazlsLzkupoiLDEsIiIsIiJdLFsi6ams6L6+5Yqg5pav5YqgIiwi6ams6L6+5Yqg5pav5YqgIiwxLCIiLCIiXSxbIumprOaBqeWymyIsIumprOaBqeWymyIsMSwiIiwiIl0sWyLpqazlsJTku6PlpKsiLCLpqazlsJTku6PlpKsiLDEsIiIsIiJdLFsi6ams6ICz5LuWIiwi6ams6ICz5LuWIiwxLCIiLCIiXSxbIumprOaLiee7tCIsIumprOaLiee7tCIsMSwiIiwiIl0sWyLpqazmnaXopb/kupoiLCLpqazmnaXopb/kupoiLDEsIiIsIiJdLFsi6ams6YeMIiwi6ams6YeMIiwxLCIiLCIiXSxbIumprOWFtumhvyIsIumprOWFtumhvyIsMSwiIiwiIl0sWyLpqaznu43lsJTnvqTlspsiLCLpqaznu43lsJTnvqTlspsiLDEsIiIsIiJdLFsi6ams5o+Q5bC85YWL5bKbIiwi6ams5o+Q5bC85YWL5bKbIiwxLCIiLCIiXSxbIumprOe6pueJuSIsIumprOe6pueJuSIsMSwiIiwiIl0sWyLmr5vph4zmsYLmlq8iLCLmr5vph4zmsYLmlq8iLDEsIiIsIiJdLFsi5q+b6YeM5aGU5bC85LqaIiwi5q+b6YeM5aGU5bC85LqaIiwxLCIiLCIiXSxbIue+juWbvSIsIue+juWbvSIsMSwiIiwiIl0sWyLnvo7lsZ7okKjmkankupoiLCLnvo7lsZ7okKjmkankupoiLDEsIiIsIiJdLFsi6JKZ5Y+kIiwi6JKZ5Y+kIiwxLCIiLCIiXSxbIuiSmeeJueWhnuaLieeJuSIsIuiSmeeJueWhnuaLieeJuSIsMSwiIiwiIl0sWyLlrZ/liqDmi4kiLCLlrZ/liqDmi4kiLDEsIiIsIiJdLFsi56eY6bKBIiwi56eY6bKBIiwxLCIiLCIiXSxbIuWvhuWFi+e9l+WwvOilv+S6miIsIuWvhuWFi+e9l+WwvOilv+S6miIsMSwiIiwiIl0sWyLnvIXnlLgiLCLnvIXnlLgiLDEsIiIsIiJdLFsi5pGp5bCU5aSa55OmIiwi5pGp5bCU5aSa55OmIiwxLCIiLCIiXSxbIuaRqea0m+WTpSIsIuaRqea0m+WTpSIsMSwiIiwiIl0sWyLmkannurPlk6UiLCLmkannurPlk6UiLDEsIiIsIiJdLFsi6I6r5qGR5q+U5YWLIiwi6I6r5qGR5q+U5YWLIiwxLCIiLCIiXSxbIuWiqOilv+WTpSIsIuWiqOilv+WTpSIsMSwiIiwiIl0sWyLnurPnsbPmr5TkupoiLCLnurPnsbPmr5TkupoiLDEsIiIsIiJdLFsi5Y2X6Z2eIiwi5Y2X6Z2eIiwxLCIiLCIiXSxbIuWNl+aWr+aLieWkqyIsIuWNl+aWr+aLieWkqyIsMSwiIiwiIl0sWyLnkZnpsoEiLCLnkZnpsoEiLDEsIiIsIiJdLFsi5bC85rOK5bCUIiwi5bC85rOK5bCUIiwxLCIiLCIiXSxbIuWwvOWKoOaLieeTnCIsIuWwvOWKoOaLieeTnCIsMSwiIiwiIl0sWyLlsLzml6XlsJQiLCLlsLzml6XlsJQiLDEsIiIsIiJdLFsi5bC85pel5Yip5LqaIiwi5bC85pel5Yip5LqaIiwxLCIiLCIiXSxbIue6veWfgyIsIue6veWfgyIsMSwiIiwiIl0sWyLmjKrlqIEiLCLmjKrlqIEiLDEsIiIsIiJdLFsi6K+656aP5YWL5bKbIiwi6K+656aP5YWL5bKbIiwxLCIiLCIiXSxbIuW4leWKsyIsIuW4leWKsyIsMSwiIiwiIl0sWyLnmq7nibnlh6/mgannvqTlspsiLCLnmq7nibnlh6/mgannvqTlspsiLDEsIiIsIiJdLFsi6JGh6JCE54mZIiwi6JGh6JCE54mZIiwxLCIiLCIiXSxbIuaXpeacrCIsIuaXpeacrCIsMSwiIiwiIl0sWyLnkZ7lhbgiLCLnkZ7lhbgiLDEsIiIsIiJdLFsi55Ge5aOrIiwi55Ge5aOrIiwxLCIiLCIiXSxbIuiQqOWwlOeTpuWkmiIsIuiQqOWwlOeTpuWkmiIsMSwiIiwiIl0sWyLokKjmkankupoiLCLokKjmkankupoiLDEsIiIsIiJdLFsi5aGe5bCU57u05LqaIiwi5aGe5bCU57u05LqaIiwxLCIiLCIiXSxbIuWhnuaLieWIqeaYgiIsIuWhnuaLieWIqeaYgiIsMSwiIiwiIl0sWyLloZ7lhoXliqDlsJQiLCLloZ7lhoXliqDlsJQiLDEsIiIsIiJdLFsi5aGe5rWm6Lev5pavIiwi5aGe5rWm6Lev5pavIiwxLCIiLCIiXSxbIuWhnuiIjOWwlCIsIuWhnuiIjOWwlCIsMSwiIiwiIl0sWyLmspnnibnpmL/mi4nkvK8iLCLmspnnibnpmL/mi4nkvK8iLDEsIiIsIiJdLFsi5Zyj6K+e5bKbIiwi5Zyj6K+e5bKbIiwxLCIiLCIiXSxbIuWco+Wkmue+juWSjOaZruael+ilv+avlCIsIuWco+Wkmue+juWSjOaZruael+ilv+avlCIsMSwiIiwiIl0sWyLlnKPotavli5Lmi78iLCLlnKPotavli5Lmi78iLDEsIiIsIiJdLFsi5Zyj5Z+66Iyo5ZKM5bC857u05pavIiwi5Zyj5Z+66Iyo5ZKM5bC857u05pavIiwxLCIiLCIiXSxbIuWco+WNouilv+S6miIsIuWco+WNouilv+S6miIsMSwiIiwiIl0sWyLlnKPpqazlipvor7oiLCLlnKPpqazlipvor7oiLDEsIiIsIiJdLFsi5Zyj5paH5qOu54m55ZKM5qC85p6X57qz5LiB5pavIiwi5Zyj5paH5qOu54m55ZKM5qC85p6X57qz5LiB5pavIiwxLCIiLCIiXSxbIuaWr+mHjOWFsOWNoSIsIuaWr+mHjOWFsOWNoSIsMSwiIiwiIl0sWyLmlq/mtJvkvJDlhYsiLCLmlq/mtJvkvJDlhYsiLDEsIiIsIiJdLFsi5pav5rSb5paH5bC85LqaIiwi5pav5rSb5paH5bC85LqaIiwxLCIiLCIiXSxbIuaWr+WogeWjq+WFsCIsIuaWr+WogeWjq+WFsCIsMSwiIiwiIl0sWyLoi4/kuLkiLCLoi4/kuLkiLDEsIiIsIiJdLFsi6IuP6YeM5Y2XIiwi6IuP6YeM5Y2XIiwxLCIiLCIiXSxbIuaJgOe9l+mXqOe+pOWymyIsIuaJgOe9l+mXqOe+pOWymyIsMSwiIiwiIl0sWyLntKLpqazph4wiLCLntKLpqazph4wiLDEsIiIsIiJdLFsi5aGU5ZCJ5YWL5pav5Z2mIiwi5aGU5ZCJ5YWL5pav5Z2mIiwxLCIiLCIiXSxbIuazsOWbvSIsIuazsOWbvSIsMSwiIiwiIl0sWyLlnabmoZHlsLzkupoiLCLlnabmoZHlsLzkupoiLDEsIiIsIiJdLFsi5rGk5YqgIiwi5rGk5YqgIiwxLCIiLCIiXSxbIueJueeri+WwvOi+vuWSjOWkmuW3tOWTpSIsIueJueeri+WwvOi+vuWSjOWkmuW3tOWTpSIsMSwiIiwiIl0sWyLnqoHlsLzmlq8iLCLnqoHlsLzmlq8iLDEsIiIsIiJdLFsi5Zu+55Om5Y2iIiwi5Zu+55Om5Y2iIiwxLCIiLCIiXSxbIuWcn+iAs+WFtiIsIuWcn+iAs+WFtiIsMSwiIiwiIl0sWyLlnJ/lupPmm7zmlq/lnaYiLCLlnJ/lupPmm7zmlq/lnaYiLDEsIiIsIiJdLFsi5omY5YWL5YqzIiwi5omY5YWL5YqzIiwxLCIiLCIiXSxbIueTpuWIqeaWr+e+pOWym+WSjOWvjOWbvue6s+e+pOWymyIsIueTpuWIqeaWr+e+pOWym+WSjOWvjOWbvue6s+e+pOWymyIsMSwiIiwiIl0sWyLnk6bliqrpmL/lm74iLCLnk6bliqrpmL/lm74iLDEsIiIsIiJdLFsi5Y2x5Zyw6ams5ouJIiwi5Y2x5Zyw6ams5ouJIiwxLCIiLCIiXSxbIuWnlOWGheeRnuaLiSIsIuWnlOWGheeRnuaLiSIsMSwiIiwiIl0sWyLmlofojrEiLCLmlofojrEiLDEsIiIsIiJdLFsi5LmM5bmy6L6+Iiwi5LmM5bmy6L6+IiwxLCIiLCIiXSxbIuS5jOWFi+WFsCIsIuS5jOWFi+WFsCIsMSwiIiwiIl0sWyLkuYzmi4nlnK0iLCLkuYzmi4nlnK0iLDEsIiIsIiJdLFsi5LmM5YW55Yir5YWL5pav5Z2mIiwi5LmM5YW55Yir5YWL5pav5Z2mIiwxLCIiLCIiXSxbIuilv+ePreeJmSIsIuilv+ePreeJmSIsMSwiIiwiIl0sWyLopb/mkpLlk4jmi4kiLCLopb/mkpLlk4jmi4kiLDEsIiIsIiJdLFsi5biM6IWKIiwi5biM6IWKIiwxLCIiLCIiXSxbIuaWsOWKoOWdoSIsIuaWsOWKoOWdoSIsMSwiIiwiIl0sWyLmlrDlloDph4zlpJrlsLzkupoiLCLmlrDlloDph4zlpJrlsLzkupoiLDEsIiIsIiJdLFsi5paw6KW/5YWwIiwi5paw6KW/5YWwIiwxLCIiLCIiXSxbIuWMiOeJmeWIqSIsIuWMiOeJmeWIqSIsMSwiIiwiIl0sWyLlj5nliKnkupoiLCLlj5nliKnkupoiLDEsIiIsIiJdLFsi54mZ5Lmw5YqgIiwi54mZ5Lmw5YqgIiwxLCIiLCIiXSxbIuS6mue+juWwvOS6miIsIuS6mue+juWwvOS6miIsMSwiIiwiIl0sWyLkuZ/pl6giLCLkuZ/pl6giLDEsIiIsIiJdLFsi5LyK5ouJ5YWLIiwi5LyK5ouJ5YWLIiwxLCIiLCIiXSxbIuS8iuaclyIsIuS8iuaclyIsMSwiIiwiIl0sWyLku6XoibLliJciLCLku6XoibLliJciLDEsIiIsIiJdLFsi5oSP5aSn5YipIiwi5oSP5aSn5YipIiwxLCIiLCIiXSxbIuWNsOW6piIsIuWNsOW6piIsMSwiIiwiIl0sWyLljbDluqblsLzopb/kupoiLCLljbDluqblsLzopb/kupoiLDEsIiIsIiJdLFsi6Iux5Zu9Iiwi6Iux5Zu9IiwxLCIiLCIiXSxbIue6puaXpiIsIue6puaXpiIsMSwiIiwiIl0sWyLotorljZciLCLotorljZciLDEsIiIsIiJdLFsi6LWe5q+U5LqaIiwi6LWe5q+U5LqaIiwxLCIiLCIiXSxbIuazveilv+WymyIsIuazveilv+WymyIsMSwiIiwiIl0sWyLkuY3lvpciLCLkuY3lvpciLDEsIiIsIiJdLFsi55u05biD572X6ZmAIiwi55u05biD572X6ZmAIiwxLCIiLCIiXSxbIuaZuuWIqSIsIuaZuuWIqSIsMSwiIiwiIl0sWyLkuK3pnZ4iLCLkuK3pnZ4iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIi0xIl19LCJwMV9kZGxTaGVuZyI6eyJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeecgeS7vSIsMSwiIiwiIl0sWyLljJfkuqwiLCLljJfkuqwiLDEsIiIsIiJdLFsi5aSp5rSlIiwi5aSp5rSlIiwxLCIiLCIiXSxbIuS4iua1tyIsIuS4iua1tyIsMSwiIiwiIl0sWyLph43luoYiLCLph43luoYiLDEsIiIsIiJdLFsi5rKz5YyXIiwi5rKz5YyXIiwxLCIiLCIiXSxbIuWxseilvyIsIuWxseilvyIsMSwiIiwiIl0sWyLovr3lroEiLCLovr3lroEiLDEsIiIsIiJdLFsi5ZCJ5p6XIiwi5ZCJ5p6XIiwxLCIiLCIiXSxbIum7kem+meaxnyIsIum7kem+meaxnyIsMSwiIiwiIl0sWyLmsZ/oi48iLCLmsZ/oi48iLDEsIiIsIiJdLFsi5rWZ5rGfIiwi5rWZ5rGfIiwxLCIiLCIiXSxbIuWuieW+vSIsIuWuieW+vSIsMSwiIiwiIl0sWyLnpo/lu7oiLCLnpo/lu7oiLDEsIiIsIiJdLFsi5rGf6KW/Iiwi5rGf6KW/IiwxLCIiLCIiXSxbIuWxseS4nCIsIuWxseS4nCIsMSwiIiwiIl0sWyLmsrPljZciLCLmsrPljZciLDEsIiIsIiJdLFsi5rmW5YyXIiwi5rmW5YyXIiwxLCIiLCIiXSxbIua5luWNlyIsIua5luWNlyIsMSwiIiwiIl0sWyLlub/kuJwiLCLlub/kuJwiLDEsIiIsIiJdLFsi5rW35Y2XIiwi5rW35Y2XIiwxLCIiLCIiXSxbIuWbm+W3nSIsIuWbm+W3nSIsMSwiIiwiIl0sWyLotLXlt54iLCLotLXlt54iLDEsIiIsIiJdLFsi5LqR5Y2XIiwi5LqR5Y2XIiwxLCIiLCIiXSxbIumZleilvyIsIumZleilvyIsMSwiIiwiIl0sWyLnlJjogoMiLCLnlJjogoMiLDEsIiIsIiJdLFsi6Z2S5rW3Iiwi6Z2S5rW3IiwxLCIiLCIiXSxbIuWGheiSmeWPpCIsIuWGheiSmeWPpCIsMSwiIiwiIl0sWyLlub/opb8iLCLlub/opb8iLDEsIiIsIiJdLFsi6KW/6JePIiwi6KW/6JePIiwxLCIiLCIiXSxbIuWugeWkjyIsIuWugeWkjyIsMSwiIiwiIl0sWyLmlrDnloYiLCLmlrDnloYiLDEsIiIsIiJdLFsi6aaZ5rivIiwi6aaZ5rivIiwxLCIiLCIiXSxbIua+s+mXqCIsIua+s+mXqCIsMSwiIiwiIl0sWyLlj7Dmub4iLCLlj7Dmub4iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuS4iua1tyJdfSwicDFfZGRsU2hpIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5biCIiwxLCIiLCIiXSxbIuS4iua1t+W4giIsIuS4iua1t+W4giIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5LiK5rW35biCIl19LCJwMV9kZGxYaWFuIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5Y6/5Yy6IiwxLCIiLCIiXSxbIum7hOa1puWMuiIsIum7hOa1puWMuiIsMSwiIiwiIl0sWyLljaLmub7ljLoiLCLljaLmub7ljLoiLDEsIiIsIiJdLFsi5b6Q5rGH5Yy6Iiwi5b6Q5rGH5Yy6IiwxLCIiLCIiXSxbIumVv+WugeWMuiIsIumVv+WugeWMuiIsMSwiIiwiIl0sWyLpnZnlronljLoiLCLpnZnlronljLoiLDEsIiIsIiJdLFsi5pmu6ZmA5Yy6Iiwi5pmu6ZmA5Yy6IiwxLCIiLCIiXSxbIuiZueWPo+WMuiIsIuiZueWPo+WMuiIsMSwiIiwiIl0sWyLmnajmtabljLoiLCLmnajmtabljLoiLDEsIiIsIiJdLFsi5a6d5bGx5Yy6Iiwi5a6d5bGx5Yy6IiwxLCIiLCIiXSxbIumXteihjOWMuiIsIumXteihjOWMuiIsMSwiIiwiIl0sWyLlmInlrprljLoiLCLlmInlrprljLoiLDEsIiIsIiJdLFsi5p2+5rGf5Yy6Iiwi5p2+5rGf5Yy6IiwxLCIiLCIiXSxbIumHkeWxseWMuiIsIumHkeWxseWMuiIsMSwiIiwiIl0sWyLpnZLmtabljLoiLCLpnZLmtabljLoiLDEsIiIsIiJdLFsi5aWJ6LSk5Yy6Iiwi5aWJ6LSk5Yy6IiwxLCIiLCIiXSxbIua1puS4nOaWsOWMuiIsIua1puS4nOaWsOWMuiIsMSwiIiwiIl0sWyLltIfmmI7ljLoiLCLltIfmmI7ljLoiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWuneWxseWMuiJdfSwicDFfWGlhbmdYRFoiOnsiTGFiZWwiOiLlm73lhoXor6bnu4blnLDlnYAiLCJUZXh0Ijoi5paw5qCh5Yy65Y2XMTQifSwicDFfQ29udGVudFBhbmVsMV9aaG9uZ0dGWERRIjp7IlRleHQiOiI8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+6auY6aOO6Zmp5Zyw5Yy677yaPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6JeB5Z+O5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5paw5LmQ5biCPGJyLz5cclxu5rKz5YyX55yB6YKi5Y+w5biC5Y2X5a6r5biCPGJyLz5cclxu6buR6b6Z5rGf55yB57ul5YyW5biC5pyb5aWO5Y6/PGJyLz5cclxu5ZCJ5p6X55yB6YCa5YyW5biC5Lic5piM5Yy6PGJyLz5cclxu5YyX5Lqs5biC5aSn5YW05Yy65aSp5a6r6Zmi6KGX6YGT6J6N5rGH56S+5Yy6PGJyLz5cclxuPGJyLz5cclxu5Lit6aOO6Zmp5Zyw5Yy677yaPGJyLz5cclxu5YyX5Lqs5biC6aG65LmJ5Yy65YyX55+z5qe96ZWH6KW/6LW15ZCE5bqE5p2RPGJyLz5cclxu5YyX5Lqs5biC6aG65LmJ5Yy65YyX55+z5qe96ZWH5YyX55+z5qe95p2RPGJyLz5cclxu5YyX5Lqs5biC6aG65LmJ5Yy66LW15YWo6JCl6ZWH6IGU5bqE5p2RPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6auY5paw5Yy66LW15p2R5paw5Yy65bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6auY5paw5Yy65Li76K+t5Z+O5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5peg5p6B5Y6/5Lic5YyX6L+c5p2RPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5peg5p6B5Y6/6KW/6YOd5bqE5p2RPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5q2j5a6a5Y6/56m65riv6Iqx5Zut5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5q2j5a6a5Y6/5a2U5p2RPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5paw5Y2O5Yy66YO95biC6Ziz5YWJ5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5paw5Y2O5Yy65Li96YO95rKz55WU5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5qGl6KW/5Yy65bmz5a6J5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KGM5ZSQ5Y6/5ruo5rKz5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65aSp5rW36KqJ5aSp5LiL5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65pm25b2p6IuR5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65LyX576O5buK5qGl5Zub5a2jQeWMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuS4nOaWueaYjuePoOWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guahpeilv+WMuueZvemHkeWFrOWvkzxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guahpeilv+WMuuWNjua2puS4h+ixoeWfjjxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gum5v+azieWMuuinguWzsOWYiemCuOWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guato+WumuWOv+WGr+WutuW6hOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guato+WumuWOv+S4nOW5s+S5kOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumVv+WuieWMuuWNmumbheebm+S4luWwj+WMukXljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrlm73otavnuqLnj4rmub7lsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILpq5jmlrDljLrlpKrooYzlmInoi5HlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrljZPkuJzlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrmlrDljY7oi5HlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILpub/ms4nljLrpk7blsbHoirHlm63mlrDljLrlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILmlrDljY7ljLrlsJrph5Hoi5HlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrliY3ov5vmnZE8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrmma7lkozlsI/ljLrljZfpmaI8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrlu7rmmI7lsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrnroDnrZHlrrblm63lsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrkv53liKnoirHlm61C5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65L+d5Yip6Iqx5ZutROWMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumVv+WuieWMuuiDuOenkeWMu+mZouWFrOWvk+WMl+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumrmOaWsOWMuuWQjOelpeWfjuWwj+WMukPljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILpq5jmlrDljLrlkozlkIjnvo7lrrblsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrmtbflpKnpmLPlhYnlm63lsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrljYHkuozljJblu7rlsI/ljLoxNuWPt+alvDxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuWNgeS6jOWMluW7uuWwj+WMujE35Y+35qW8PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65rKz5YyX5Z+O5bu65a2m5qCh5a625bGe6ZmiPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5qC+5Z+O5Yy65Y2T6L6+5aSq6Ziz5Z+O5biM5pyb5LmL5rSy5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5bmz5bGx5Y6/6Ziy55ar56uZ5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB5buK5Z2K5biC5Zu65a6J5Y6/6Iux5Zu95a6rNeacnzxici8+XHJcbuays+WMl+ecgemCouWPsOW4gumahuWwp+WOv+eDn+iNieWutuWbre+8iOeDn+iNieWFrOWPuOWutuWxnumZou+8iTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gui1teWOv+S7u+W6hOadkTxici8+XHJcbui+veWugeecgeWkp+i/nuW4gumHkeaZruaWsOWMuuWFieS4reihl+mBk+iDnOWIqeilv+ekvuWMujxici8+XHJcbui+veWugeecgeWkp+i/nuW4gumHkeaZruaWsOWMuuaLpeaUv+ihl+mBk+WPpOWfjueUsuWMujxici8+XHJcbum7kem+meaxn+ecgeWkp+W6huW4gum+meWHpOWMuuS4lue6quWUkOS6uuS4reW/g+Wwj+WMujLmoIsx5Y2V5YWDPGJyLz5cclxu6buR6b6Z5rGf55yB6b2Q6b2Q5ZOI5bCU5biC5piC5piC5rqq5Yy65aSn5LqU56aP546b5p2RPGJyLz5cclxu6buR6b6Z5rGf55yB5ZOI5bCU5ruo5biC6aaZ5Z2K5Yy66aaZ5Z2K5aSn6KGX6KGX6YGT5Yqe5LqL5aSE6aaZ5Lit56S+5Yy65Y+k6aaZ6KGXMTLlj7c8YnIvPlxyXG7pu5HpvpnmsZ/nnIHlk4jlsJTmu6jluILpppnlnYrljLrlpKfluobot6/ooZfpgZPlip7kuovlpITnlLXloZTlsI/ljLoxMDHmoIs35Y2V5YWDPGJyLz5cclxu6buR6b6Z5rGf55yB5ZOI5bCU5ruo5biC6aaZ5Z2K5Yy65ZKM5bmz6Lev6KGX6YGT5Yqe5LqL5aSE6aOO5Y2O56S+5Yy655+z5YyW5bCP5Yy6OeagizbljZXlhYM8YnIvPlxyXG7pu5HpvpnmsZ/nnIHlk4jlsJTmu6jluILlkozlubPot6/ooZfpgZPlip7kuovlpITkuIrkuJznpL7ljLrkuIfosaHkuIrkuJzlsI/ljLpF5qCLMuWNleWFgzxici8+XHJcbuWQieael+ecgemVv+aYpeW4guWFrOS4u+WyreW4guiMg+WutuWxr+mVhzxici8+XHJcbuWQieael+ecgemVv+aYpeW4gue7v+WbreWMuuiTieahpeWjueWPt0PljLo8YnIvPlxyXG7lkInmnpfnnIHplb/mmKXluILnu7/lm63ljLrlpKfnprnljY7pgqZC5Yy6PGJyLz5cclxu5ZCJ5p6X55yB6ZW/5pil5biC5LqM6YGT5Yy66bKB6L6J5Zu96ZmF5Z+O6I235YWw5bCP6ZWH5bCP5Yy6PGJyLz5cclxu5ZCJ5p6X55yB6YCa5YyW5biC5Yy76I2v6auY5paw5Yy65aWV6L6+5bCP5Yy6PGJyLz5cclxu5ZCJ5p6X55yB5p2+5Y6f5biC57uP5rWO5oqA5pyv5byA5Y+R5Yy65paw5Yac5bCP5Yy6N+WPt+alvDxici8+XHJcbuS4iua1t+W4gum7hOa1puWMuuaYremAmui3r+WxheawkeWMuu+8iOemj+W3nui3r+S7peWNl+WMuuWfn++8iTwvc3Bhbj4ifSwicDFfQ29udGVudFBhbmVsMSI6eyJJRnJhbWVBdHRyaWJ1dGVzIjp7fX0sInAxX0ZlbmdYRFFETCI6eyJMYWJlbCI6IjAx5pyIMDnml6Xoh7MwMeaciDIz5pel5piv5ZCm5ZyoPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7pgJfnlZkiLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfVG9uZ1pXRExIIjp7IlJlcXVpcmVkIjp0cnVlLCJMYWJlbCI6IuS4iua1t+WQjOS9j+S6uuWRmOaYr+WQpuaciTAx5pyIMDnml6Xoh7MwMeaciDIz5pel5p2l6IeqPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7nmoTkuroiLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfQ2VuZ0ZXSCI6eyJMYWJlbCI6IjAx5pyIMDnml6Xoh7MwMeaciDIz5pel5piv5ZCm5ZyoPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7pgJfnlZnov4ciLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLlkKYifSwicDFfQ2VuZ0ZXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0NlbmdGV0hfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodSI6eyJMYWJlbCI6IjAx5pyIMDnml6Xoh7MwMeaciDIz5pel5piv5ZCm5LiO5p2l6IeqPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7lj5Hng63kurrlkZjlr4bliIfmjqXop6YiLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfSmllQ2h1X1JpUWkiOnsiSGlkZGVuIjp0cnVlfSwicDFfSmllQ2h1X0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9UdUpXSCI6eyJMYWJlbCI6IjAx5pyIMDnml6Xoh7MwMeaciDIz5pel5piv5ZCm5LmY5Z2Q5YWs5YWx5Lqk6YCa6YCU5b6EPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfVHVKV0hfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9UdUpXSF9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfUXVlWkhaSkMiOnsiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxLCIiLCIiXSxbIuWQpiIsIuWQpiIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5ZCmIl19LCJwMV9EYW5nUkdMIjp7IlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9HZUxTTSI6eyJIaWRkZW4iOnRydWUsIklGcmFtZUF0dHJpYnV0ZXMiOnt9fSwicDFfR2VMRlMiOnsiUmVxdWlyZWQiOmZhbHNlLCJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuWxheWutumalOemuyIsIuWxheWutumalOemuyIsMV0sWyLpm4bkuK3pmpTnprsiLCLpm4bkuK3pmpTnprsiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6bnVsbH0sInAxX0dlTERaIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ZhblhSUSI6eyJIaWRkZW4iOnRydWV9LCJwMV9XZWlGSFlZIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1NoYW5nSEpaRCI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIwMeaciDA55pel6IezMDHmnIgyM+aXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtiJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1N1aVNNIjp7IlJlcXVpcmVkIjp0cnVlLCJTZWxlY3RlZFZhbHVlIjoi57u/6ImyIiwiRl9JdGVtcyI6W1si57qi6ImyIiwi57qi6ImyIiwxXSxbIum7hOiJsiIsIum7hOiJsiIsMV0sWyLnu7/oibIiLCLnu7/oibIiLDFdXX0sInAxX0x2TWExNERheXMiOnsiUmVxdWlyZWQiOnRydWUsIlNlbGVjdGVkVmFsdWUiOiLmmK8iLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9jdGwwMF9idG5SZXR1cm4iOnsiT25DbGllbnRDbGljayI6ImRvY3VtZW50LmxvY2F0aW9uLmhyZWY9Jy9EZWZhdWx0LmFzcHgnO3JldHVybjsifSwicDEiOnsiSUZyYW1lQXR0cmlidXRlcyI6e319fQ=="
    # if reportData["Time_1or2"] == "1" : p1 = "每日两报（上午）"
    # if reportData["Time_1or2"] == "2" : p1 = "每日两报（下午）"
    p1_BaoSRQ = reportData["date"].replace(" ","")   #这报送网站的变量名属实有点秀
   # p1_TiWen = reportData["temperature"]
    p1_ZaiXiao = reportData["campusLocation"]
    p1_ddlXian = reportData["xian"]
    p1_XiangXDZ = reportData["location"]
    F_State_Former_str = str(base64.b64decode(F_STATE_Former), encoding='utf-8')
    F_STATE_Former_dict = json.loads(F_State_Former_str)
   # F_STATE_Former_dict["p1"].update({'Title': p1})
    F_STATE_Former_dict['p1_BaoSRQ'].update({'Text': p1_BaoSRQ})
   # F_STATE_Former_dict['p1_TiWen'].update({'Text': p1_TiWen})
    F_STATE_Former_dict['p1_ZaiXiao'].update({'SelectedValue': p1_ZaiXiao})
    F_STATE_Former_dict['p1_ddlXian'].update({'SelectedValueArray': [p1_ddlXian]})
   #  F_STATE_Former_dict['p1_XiangXDZ'].update({'Text': p1_XiangXDZ})
    print(F_State_Former_str)
    F_State_New_str = json.dumps(F_STATE_Former_dict, ensure_ascii=False, separators=(',', ':'))
    F_State_New=base64.b64encode(F_State_New_str.encode("utf-8")).decode()
    return  F_STATE_Former


def main():
    studentId = sys.argv[1]
    password = sys.argv[2]
    Sheng = "上海",
    Shi = "上海市",
    Xian = "宝山区",
    detailedLocation = "11",
    studentInfo = [studentId, password]
    timeUTC = datetime.datetime.utcnow()
    timeLocal = timeUTC + datetime.timedelta(hours=8)
    date = timeLocal.strftime('%Y - %m - %d')
    # if(timeLocal.hour>=19):
    #     Time_1or2 = "2"
    # else:
    #     Time_1or2 = "1"
    reportData = {"date": date,
                  "campusLocation": "宝山", "location": detailedLocation, "sheng": Sheng, "shi": Shi,
                  "xian": Xian, }  # county：所在区   cmapusLocation:所在校区
    try:
        cookie = get_cookies(studentInfo)
    except:
        print("无法获取学号  " + studentInfo[0] + "  的cookie,可能是账号密码错误")
    else:
        reportUrl = "https://selfreport.shu.edu.cn/DayReport.aspx"
        response = requests.get(reportUrl, cookies=cookie)
        print (response.text)
        # reportSuccess = daily_report(cookie, reportData)
        # if (reportSuccess) == -1:
        #     print(str(studentInfo[0] + "   报送失败"))
        # else:
        #     print(str(studentInfo[0] + "   提交成功"))

if __name__ == "__main__":
    main()



