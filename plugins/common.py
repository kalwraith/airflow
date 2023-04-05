import re
from dateutil.relativedelta import relativedelta

def calc_relative_datetime(
        time_obj,
        rel_op,
        rel_flag,
        rel_n,
        dt_op,
        dt_flag,
        dt_n,
):
    """
    지난 주, 지난 달, 지난 달 1일, 지난 주 월요일 등
    텍스트로 작성된 상대적 날짜 표현을 datetime object 에 적용.

    """
    if rel_op is not None:
        if rel_op == "-":
            rel_n = rel_n * -1
        if rel_flag == "yyyy":
            time_obj = time_obj + relativedelta(years=rel_n)
        elif rel_flag == "MM":
            time_obj = time_obj + relativedelta(months=rel_n)
        elif rel_flag == "dd":
            time_obj = time_obj + relativedelta(days=rel_n)
        elif rel_flag == "HH":
            time_obj = time_obj + relativedelta(hours=rel_n)
        elif rel_flag == "mm":
            time_obj = time_obj + relativedelta(minutes=rel_n)
        elif rel_flag == "ss":
            time_obj = time_obj + relativedelta(seconds=rel_n)
        elif rel_flag == "ww":  # 주 단위
            time_obj = time_obj + relativedelta(weeks=rel_n)
        elif rel_flag == "QQ":  # 분기
            time_obj = time_obj + relativedelta(months=rel_n * 3)
    else:
        if rel_flag == "yyyy":
            time_obj = time_obj.replace(year=rel_n)
        elif rel_flag == "MM":
            time_obj = time_obj.replace(month=rel_n)
        elif rel_flag == "dd":
            if rel_n == 99:
                rel_n = 1
            time_obj = time_obj.replace(day=rel_n)
        elif rel_flag == "HH":
            time_obj = time_obj.replace(hour=rel_n)
        elif rel_flag == "mm":
            time_obj = time_obj.replace(minute=rel_n)
        elif rel_flag == "ss":
            time_obj = time_obj.replace(second=rel_n)
        elif rel_flag == "ww":
            time_obj = time_obj - relativedelta(days=time_obj.isoweekday() - rel_n)
        elif rel_flag == "ML":  # 월 말일.
            time_obj = time_obj.replace(day=1) + relativedelta(months=1)
            time_obj = time_obj - relativedelta(days=rel_n + 1)

    if dt_op is not None:
        if dt_op == "-":
            dt_n = dt_n * -1
        if dt_flag == "yyyy":
            time_obj = time_obj + relativedelta(years=dt_n)
        elif dt_flag == "MM":
            time_obj = time_obj + relativedelta(months=dt_n)
        elif dt_flag == "dd":
            time_obj = time_obj + relativedelta(days=dt_n)
        elif dt_flag == "HH":
            time_obj = time_obj + relativedelta(hours=dt_n)
        elif dt_flag == "mm":
            time_obj = time_obj + relativedelta(minutes=dt_n)
        elif dt_flag == "ss":
            time_obj = time_obj + relativedelta(seconds=dt_n)
        elif dt_flag == "ww":  # 주 단위
            time_obj = time_obj + relativedelta(weeks=dt_n)
        elif dt_flag == "QQ":  # 분기
            time_obj = time_obj + relativedelta(months=dt_n * 3)
    else:
        if dt_flag == "yyyy":
            time_obj = time_obj.replace(year=dt_n)
        elif dt_flag == "MM":
            time_obj = time_obj.replace(month=dt_n)
        elif dt_flag == "dd":
            if dt_n == 99:
                dt_n = 1
            time_obj = time_obj.replace(day=dt_n)
        elif dt_flag == "HH":
            time_obj = time_obj.replace(hour=dt_n)
        elif dt_flag == "mm":
            time_obj = time_obj.replace(minute=dt_n)
        elif dt_flag == "ss":
            time_obj = time_obj.replace(second=dt_n)
        elif dt_flag == "ww":
            time_obj = time_obj - relativedelta(days=time_obj.isoweekday() - dt_n)
        elif dt_flag == "ML":  # 월 말일.
            time_obj = time_obj.replace(day=1) + relativedelta(months=1)
            time_obj = time_obj - relativedelta(days=dt_n + 1)

    return time_obj


def substitute_parameters_with_context(data_interval_end, dag_id, text):
    """
    context 필요한 string 치환 처리.

    주요 치환 대상은 날짜 표현식.
    yyyy-MM-dd|dd-1 => 실행 기준일시 하루 전 (ex. 2022-01-01)
    yyyyMMdd|MM-1 => 실행 기준일시 한 달 전 (ex. 20211202)
    yyyyMMdd|MM-1&dd15 => 실행 기준일시 한 달 전 15일 특정 (ex. 20211215)
    yyyy-MM-dd|MM-1&ML0 => 실행 기준일시 한 달 전 말일 (ex. 2021-12-31)
    yyyy-MM-dd|MM-1&ML1 => 실행 기준일시 한 달 전 말일 - 1일 (ex. 2021-12-30)
    yyyyMMddHH => 실행 기준일시, 시간까지 표시 (ex. 2022010208)
    yyyyMMddHHmmss => 시분초까지
    yyyy-MM-ddTHH:mm:ss => iso standard
    MM => 월 만 표현
    ...
    """

    if not text:
        self.log.info(f"no input")
        return text

    text = text.replace("##dag_id##",dag_id)

    fmt_map = {
        "yyyy": "%Y", "MM": "%m", "dd": "%d", "HH": "%H", "mm": "%M", "ss": "%S",
        "-": "-", "T": "T", ":": ":",
    }
    p = re.compile(
        "##(yyyy)?(-)?(MM|QQ)?(-)?(dd)?(T)?(HH)?(:)?(mm)?(:)?(ss)?(\|(yyyy|MM|QQ|dd|HH|mm|ss|ww)(-|\+)(\d+)(&(yyyy|MM|dd|HH|mm|ss|ww|ML)(-|\+)?(\d+))?)?##")
    m = p.search(text, 0)
    while m:
        # 상대날짜 표현식(dd-1&ML0 등) 추출
        rel_flag = m.group(13)  # MM,dd 등
        rel_op = m.group(14)  # -, +
        rel_n = int(m.group(15) or 0)  # number
        dt_flag = m.group(17)  # MM, ML, dd 등
        dt_op = m.group(18)  # -, +
        dt_n = int(m.group(19) or 0)  # number
        # self.log.info(f"===> rel_flag:{rel_flag} rel_op:{rel_op} rel_n:{rel_n} dt_flag:{dt_flag} dt_op:{dt_op} dt_n:{dt_n}")
        # 추출한 상대날짜 표현식(dd-1&ML0 등)으로 날짜 계산 (next_execution_date(to) 기준)
        d = calc_relative_datetime(data_interval_end, rel_op, rel_flag, rel_n, dt_op, dt_flag, dt_n)

        # 포매팅 심볼 처리(yyyy-MM-dd 등)
        fmt_string = ""
        for i in range(11):
            fmt = m.group(i + 1)
            if fmt == "QQ":
                ## 분기 Symbol 처리.
                q = int(d.strftime("%m"))
                q = int((q - 1) / 3) + 1
                fmt_string += f"{q:02d}"
            else:
                fmt_string += fmt_map.get(fmt, "")
        if fmt_string:
            repl = d.strftime(fmt_string)
            if dt_n == 99:
                repl = repl[:-2] + "99"
            text = text.replace(m.group(0), repl)
            m = p.search(text, m.end() - (len(m.group(0)) - len(repl)))
        else:
            m = p.search(text, m.end())

    return text



def get_base_id(task_meta):
    process_type = task_meta.get('PROCESS_TYPE')
    src_tgt_system = task_meta.get('SRC_TGT_SYSETM')
    process_detail = task_meta.get('PROCESS_DETAIL')
    tgt_layer = task_meta.get('TGT_LAYER')
    table_name = task_meta.get('TABLE_NAME')
    num = task_meta.get('NUM')

    return f'{process_type}{src_tgt_system}_{process_detail}{tgt_layer}_{table_name}_{num}'


def get_task_group_id(task_meta):
    return f'tg_{get_base_id(task_meta)}'


def get_task_id(task_meta, op_nm):
    return f't_{get_base_id(task_meta)}_{op_nm}'