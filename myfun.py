import requests as req
from bs4 import BeautifulSoup

# APP介紹
def app_introduction() -> str:
    return '''歡迎使用國考便利通🙌 
在這裡您將可以快速了解國考相關資訊～

📕想知道國考有那種類型? 
快前往下面選單的『國考介紹』！
📗不確定要怎麼選擇考試?
『錄取率排行』推薦給您
📙考選部最新考試資訊是什麼?
『最新消息』告訴您
📒想知道最新考選部考試公告?
前往選單的『考試公告』準沒錯

想要快速查詢也沒問題，輸入代碼就能馬上得到考科、應試資格等資訊 ！
🙋代碼在『代碼查詢』可以查詢喔～

那麽，開始蒐集資料吧！'''

# 最新消息
def moex_news() -> dict:
    url = 'https://wwwc.moex.gov.tw/main/news/wfrmNews.aspx?kind=3&menu_id=42'
    try:
        r1 = req.get(url)
    except:
        return 'Error'

    soup = BeautifulSoup(r1.text, 'html.parser')
    table = soup.find('table', attrs={'class':'list_table'})

    trs = table.find_all('tr')
    url_first = 'https://wwwc.moex.gov.tw/main/'
    carousel = {"type":"carousel","contents": []}
    for i in range(1,6):
        tds = trs[i].find_all('td')
        date = tds[1].text
        news = tds[0].find('a').text
        link = url_first + tds[0].find('a')['href'][3:]
        carousel["contents"].append(moex_news_bubble(date, news, link)) 
    return carousel

# 考試公告
def wfrm_news() -> dict:
    url = 'https://wwwc.moex.gov.tw/main/news/wfrmNews.aspx?kind=2&menu_id=41'
    try:
        r1 = req.get(url)
    except:
        return 'Error'

    soup = BeautifulSoup(r1.text, 'html.parser')
    table = soup.find('table', attrs={'class':'list_table'})
    trs = table.find_all('tr')

    url_first = 'https://wwwc.moex.gov.tw/main/'
    carousel = {"type":"carousel","contents": []}
    for i in range(1,len(trs)-2):
        tds = trs[i].find_all('td')
        date = tds[1].text
        news = tds[0].find('a').text
        link = url_first + tds[0].find('a')['href'][3:]
        carousel["contents"].append(moex_news_bubble(date, news, link)) 
    return carousel

# 最新消息與考試公告樣板
def moex_news_bubble(date:str, msg:str, link:str) -> dict:
    return {
    "type": "bubble",
    "size": "kilo",
    # "hero": {
    #     "type": "image",
    #     "url": "https://www.moex.gov.tw/images/rwd/welcome_logo.jpg",
    #     "size": "md",
    #     "aspectRatio": "20:20",
    #     "aspectMode": "cover",
    #     "action": {
    #     "type": "uri",
    #     "uri": "https://wwwc.moex.gov.tw/main/home/wfrmHome.aspx"
    #     }
    # },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": date,
            #"text": "111/12/16",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
            {
                "type": "text",
                "text": msg,
                # "text": "提升專技人員執業素養與職能研討會將於12月20日登場",
                "wrap": True,
                "flex": 5
            }
            ]
        },
        # {
        #     "type": "image",
        #     "url": "https://www.moex.gov.tw/images/rwd/welcome_logo.jpg",
        #     "size": "md",
        #     "aspectRatio": "20:20",
        #     "aspectMode": "cover",
        #     "action": {
        #     "type": "uri",
        #     "uri": "https://wwwc.moex.gov.tw/main/home/wfrmHome.aspx"
        #     }
        # }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "uri",
            "label": "官網>詳細資訊",
            "uri": link,
            # "uri": "http://linecorp.com/"
            },
            "color": "#408080"
        }
        ],
        "flex": 0
    }
    }

# 錄取率排行
def acceptance_rate(inp:str) -> dict:
    lst = []
    carousel = {"type": "carousel", "contents": []}
    if inp == '高考錄取率':
        file_name = '高考錄取率.txt'
    elif inp == '普考錄取率':
        file_name = '普考錄取率.txt'
    with open(file_name, mode='r', encoding='utf-8') as f:
        while True:
            data = f.readline().strip('\n').split()
            if not data:
                # return '\n'.join(lst)
                break
            lst.append([data[0], data[1]])
    for i in range(10):
        carousel["contents"].append(acceptance_rate_bouble(i+1, lst[i][0], lst[i][1])) 
    return carousel 

# 錄取率排行模板
def acceptance_rate_bouble(rank:str, name:str, rate:str) -> dict:
    return {
            "type": "bubble",
            "size": "micro",
            "hero": {
                "type": "image",
                "url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80",
                "size": "full",
                "aspectRatio": "320:213",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": f'第{rank}名',
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True,
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": name,
                            "wrap": True,
                            "color": "#8c8c8c",
                            "size": "xs",
                            "flex": 5,
                            "align": "center"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f'錄取率 : {rate}',
                            "size": "xxs",
                            "align": "center"
                        },
                        {
                            "type": "button",
                            "style": "link",
                            "height": "sm",
                            "action": {
                            "type": "uri",
                            "label": "點我看更多",
                            "uri": "https://wwwc.moex.gov.tw/main/ExamReport/wHandStatisticsFile.ashx?file_id=2127"
                            }
                        }
                        ]
                    }
                    ]
                }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
            }
            }

# 國考介紹
def test_introduction() -> dict:
    return {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1614610741181-2bce5e06976d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "國考介紹",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "國考是成為公務員的一種方式，大致可以分為高/普/初考、特種考試和國營事業。想知道更多有關這三種考試的資訊，請點選下方按鍵👇",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0,
                "wrap": True
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "詳細資訊",
            "text": "@國考類型"
            }
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        }
        ],
        "flex": 0
    }
    }

# 高普初考詳細介紹
def test_introduction_1() -> dict:
    return {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1547424450-a69b33b2cdc2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "高/普/初考",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "　　一般公務人員考試可以依照「應試條件」，分為高考、普考、初考。其中高考又分為高考一級、二級和三級，考試資格分別是博士、碩士和學士，由於一級和二級的缺額較少，這裡以高考三級為主。想了解高考三級、普考、初考別錯過下面的選項～",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0,
                "wrap": True
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "高考三級",
            "text": "#高考詳細介紹"
            },
            "color": "#00AFAF"
        },
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "普通考試",
            "text": "#普考詳細介紹"
            },
            "color": "#00AFAF"
        },
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "初等考試",
            "text": "#初考詳細介紹"
            },
            "color": "#00AFAF"
        }
        ],
        "flex": 0
    }
    }
def test_introduction_1h() -> dict:
    return {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "基本介紹",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "🌟關於高考三級需要知道的事\n■高考三級需要「大學以上」才能報考，尤其技術類需要是「相關科系」才能報考！\n■高考進用是從薦任 6 職等開始 (最高14職等)\n■這兩年錄取率分別是10.54%、10.59%\n■填選志願後，會依照成績分發到當年的開缺單位\n■初任公務人員會經過4個月的訓練期，其中4週的基礎訓練，會到機關以外的地方受訓，是聯誼的好機會😆 其餘「實務訓練」時間則會在機關裡進行。\n■可以享有結婚補助費、生育補助費、喪葬補助費、子女教育補助費(最高35,800元) 、國旅卡等福利",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "薪資",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "💰 約46,460~49,550元，但可能依據職務專業性或扣除退撫提撥費用和公保有所調整。",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "考試報名期間",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "📝報名時間：\n112/3/14-3/23\n📅考試時間：\n112/7/9-112/7/11",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        }
    ]
    }
def test_introduction_1m() -> dict:
    return {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "基本介紹",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "🌟關於普考需要知道的事\n■普考需要「高中職以上」才能報考，尤其技術類需要是「相關科系」才能報考！\n■普考進用是從委任 3 職等開始 (最高14職等)\n■這兩年錄取率分別是7.47%、9.45%\n■填選志願後，會依照成績分發到當年的開缺單位\n■初任公務人員會經過4個月的訓練期，其中4週的基礎訓練，會到機關以外的地方受訓，是聯誼的好機會🤭其餘「實務訓練」時間則會在機關裡進行。\n■可以享有結婚補助費、生育補助費、喪葬補助費、子女教育補助費(最高35,800元) 、國旅卡等福利\n■需要通過考試或訓練才能晉升到薦任 6 職等",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "薪資",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "💰約38,890元，但可能依據職務專業性或扣除退撫提撥費用和公保有所調整。",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "考試報名期間",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "📝報名時間：\n112/3/14-3/23\n📅考試時間：\n112/7/7-112/7/8",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        }
    ]
    }
def test_introduction_1l() -> dict:
    return {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "基本介紹",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "🌟關於初考需要知道的事\n■初考「不限學歷」，需要但「滿18歲」才能報考！\n■普考進用是從委任 1 職等開始 (最高14職等)\n■這兩年錄取率分別是2.74%、2.27%\n■填選志願後，會依照成績分發到當年的開缺單位\n■初任公務人員會經過4個月的訓練期，其中4週的基礎訓練，會到機關以外的地方受訓，是聯誼的好機會💘其餘「實務訓練」時間則會在機關裡進行\n■可以享有結婚補助費、生育補助費、喪葬補助費、子女教育補助費(最高35,800元) 、國旅卡等福利",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "薪資",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "💰 約 31,450元，但可能依據職務專業性或扣除退撫提撥費用和公保有所調整。",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        },
        {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "考試報名期間",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#003E3E"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "📝報名時間：\n111/10/25-111/11/3\n📅考試時間：\n112/1/8",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        }
    ]
    }

# 特考詳細介紹
def test_introduction_2() -> dict:
    return {
    "type": "carousel",
    "contents": [
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "司法特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "司法特考招募的是「司法」從業人員，包含公證人、行政執行官、司法事務官等。在筆試通過後，還有二、三試需要準備。依報格資格可分為三等、四等、五等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "五等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "司法特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "一般警察特考招募的是「警職人員」，依報格資格可分為二等、三等、四等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "二等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "鐵路特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "鐵路特考招募的是「鐵路相關人員」，依報格資格可分為高員級、員級、佐級考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "高員級",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "員級",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "佐級",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "移民署特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "移民署特考招募的是「移民工作人員」，依報格資格可分為二等、三等、四等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "二等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "關務特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "關務特考招募的是「海關人員」，依報格資格可分為三等、四等、五等考試。工作需要排班和配合輪調。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "五等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "外交特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "外交特考招募的是「外交人員」，依報格資格可分為三等、四等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "調查特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "調查特考招募的是「犯罪偵查與情報人員」，依報格資格可分為三等、四等、五等考試。錄取後還須至幹部訓練所歷經一年完整的養成教育。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "五等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "國安特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "國安特考招募的是「國安人員」，依報格資格可分為三等、四等、五等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "國安三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "國安四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "國安五等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        },
        {"type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "地方特考",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#336666"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "地方特考招募的是「地方政府公務人員」，考試方式是分區錄取及分發，依報格資格可分為三等、四等、五等考試。",
                "wrap": True,
                "size": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "地特三等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "地特四等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "地特五等",
                "text": "尚未開放"
                },
                "style": "primary",
                "height": "sm",
                "color": "#00AFAF"
            }
            ],
            "spacing": "sm"
        }
        }
    ]
    }

# 國營詳細介紹
def test_introduction_3() -> dict:
    return {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "國營事業",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "　　國營事業是廣義的公務員，與正式公務人員主要差別在於適用的是勞保。國營事業的範圍很廣，常見的包含台電、台糖、台水、中油、台灣菸酒、郵局、公股銀行、中鋼等。招募管道則有聯招和獨招，按下選項看更多👇🏻",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0,
                "wrap": True
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "<聯招>",
            "text": "#聯招詳細介紹"
            },
            "color": "#00AFAF"
        },
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "<獨招>",
            "text": "#獨招詳細介紹"
            },
            "color": "#00AFAF"
        },
        ],
        "flex": 0
    }
    }
def test_introduction_3_1() -> dict:
    return  {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "聯招",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#007979"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "聯招，顧名思義是多個國營事業共同招募「職員」。考生經錄取並通過內部訓練考核，才可填寫志願，並依成績高低分發到參與聯招的事業(如油水電糖四大國營事業聯招)。\n🎓須大專以上學歷才能報考",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        }
def test_introduction_3_2() -> dict:
    return  {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "獨招",
                "size": "xl",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ],
            "backgroundColor": "#007979"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "不同於聯招，獨招招募的是「僱員」(如台電新進僱用人員甄試、中油僱用人員甄試)。\n🎓須高中職以上學歷才能報考",
                "wrap": True,
                "size": "sm"
            }
            ]
        }
        }

# 代碼查詢
def subject_id(inp:str) -> dict:
    lst = []
    if inp == '高考':
        file_name = '高考代碼查詢.txt'
    elif inp == '普考':
        file_name = '普考代碼查詢.txt'
    with open(file_name, mode='r', encoding='utf-8') as f:
        while True:
            data = f.readline().strip('\n').split()
            if not data:
                # return '\n'.join(lst)
                break
            lst.append(f'{data[0]}-{data[1]}')
    carousel = {"type":"carousel","contents": []}
    subject_n = len(lst)
    idx_s, idx_e = 0, 0 
    limit = 15
    for i in range(subject_n//limit+1):
        idx_s = i * limit
        idx_e = (i + 1) * limit
        subject_data = lst[idx_s:idx_e]
        subject_text = '\n'.join(subject_data)
        carousel["contents"].append(subject_id_bubble(subject_text))
    return carousel
# 代碼查詢模板
def subject_id_bubble(text:str) -> dict:
    return {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "代碼查詢",
            "weight": "bold",
            "color": "#FFFFFF"
        }
        ],
        "backgroundColor": "#003E3E"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": text,
            "wrap": True
        }
        ]
    }
    }

# 考科介紹
def test_subject_introduction(species:str, id:str) -> dict:
    if species == '高考':
        file_name = '高考考科介紹.txt'
    elif species == '普考':
        file_name = '普考考科介紹.txt'
    with open(file_name, mode='r', encoding='utf-8') as f:
        while True:
            data = f.readline().strip('\n').split()
            if data[0]==id:
                break
    name = data[1]
    work_job = data[2]
    work_location = data[3]
    salary = data[4]
    eligibility = data[5]
    subjects1 = data[6]
    subjects2 = data[7]
    rate = data[8]
    return test_carousel(name, work_job, work_location, salary, eligibility, subjects1, subjects2, rate)
def test_carousel(name:str, work_job:str, work_location:str, salary:str, eligibility:str, subjects1:str, subjects2:str, rate:str) -> dict:
    return {
    "type": "carousel",
    "contents": [
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "工作內容",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": work_job,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "center"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "分發地點",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": work_location,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "center"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "薪水",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": salary,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "center"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "報考資格",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": eligibility,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "start"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "共同科目",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": subjects1,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "start"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "專業科目",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": subjects2,
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "start"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "錄取率",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": f'{rate}%',
                        "wrap": True,
                        "size": "xs",
                        "flex": 5,
                        "align": "center"
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": name,
                "align": "center",
                "weight": "bold",
                "color": "#FFFFFF"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "考古題",
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center",
                "contents": []
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "請點擊",
                "text": f'@exam_{name}'
                }
            }
            ]
        },
        "styles": {
            "header": {
            "backgroundColor": "#3D7878"
            }
        }
        }
    ]
    }

# 考古題連結
def exam(subject:str) -> dict:
    carousel = {"type":"carousel","contents": []}
    with open(f'.\考古題連結\{subject}.txt', mode='r', encoding='utf-8') as f:
        row_id = 1
        while True:
            inp = f.readline().strip('\n').split(',')
            # print(inp)
            if not inp[0]:
                break
            year = inp[0][0:4]
            carousel["contents"].append(exam_bubble(subject, year, row_id))
            row_id += 1
    return carousel

# 考古題連結模板
def exam_bubble(subject:str, year: str, row_id:int) -> dict:
    return  {
    "type": "bubble",
    "size": "kilo",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": subject,
            "align": "center",
            "weight": "bold",
            "color": "#FFFFFF"
        }
        ]
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": f'{year} 考古題',
            "weight": "bold",
            "size": "xl",
            "wrap": True,
            "align": "center",
            "contents": []
        }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "請點擊",
            "text": f'#exam_{subject}_{row_id:02d}'
            },
            "style": "primary",
            "color": "#00AFAF"
        }
        ]
    },
    "styles": {
        "header": {
        "backgroundColor": "#3D7878"
        }
    }
    }
# 考古題連結文字檔
def exam_link(subject:str) -> str:
    subject_new = subject[:-3]
    # print(f'subject_new={subject_new}')
    row_id = subject[-2:]
    # print(f'row_id={row_id}')
    with open(f'.\考古題連結\{subject_new}.txt', mode='r', encoding='utf-8') as f:
        idx = 1
        while True:
            inp = f.readline().strip('\n').split(',')
            # print(inp)
            if f'{idx:02d}' == row_id:
                return '\n'.join(inp)
            if not inp[0]:
                break
            idx += 1
