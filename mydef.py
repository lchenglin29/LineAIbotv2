import json,datetime,pytz

def load_json():
  with open('data/data.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
  #print(jdata)
  jFile.close()
  return jdata

def write_js(data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open('data/data.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()

def now_time():
    current_time = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Taipei')
    localized_time = current_time.astimezone(timezone)
    return localized_time.strftime("%Y-%m-%d %H:%M")

def now_data():
  taipei_timezone = pytz.timezone('Asia/Taipei')
  current_date = datetime.datetime.now(taipei_timezone).date()
  print("臺灣的當前日期:", current_date)
  return str(current_date)

def textmsg(user):
  return f'回覆:{user} | 時間:{now_time()}'