from logging import getLogger
from datetime import datetime

log = getLogger(__name__)
prev_ts = None

def now():
    now = datetime.now()
    youbi_list = ["月", "火", "水", "木", "金", "土", "日"]
    youbi = youbi_list[now.weekday()]
    format = f"%Y/%m/%d({youbi}) %H:%M:%S"
    msg = now.strftime(format)
    log.info(msg)
    return msg

def ts():
    global prev_ts
    now = datetime.now()
    prev = prev_ts or now
    dif = now - prev
    dif_us = dif.seconds * (10**6) + dif.microseconds
    dif_str = f"{dif_us:+,d}us"
    format = f"%Y/%m/%d %H:%M:%S,%f  {dif_str:>15s}"
    msg = now.strftime(format)
    log.info(msg)
    prev_ts = now
    return msg
