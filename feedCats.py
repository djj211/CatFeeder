from feeder import Feeder
from datetime import datetime, timedelta

datetime_object = datetime.strptime(Feeder.getDate(), '%Y-%m-%d %H:%M:%S')

if datetime_object < datetime.now()-timedelta(hours=4):
    feed = Feeder()
    feed.feed()
