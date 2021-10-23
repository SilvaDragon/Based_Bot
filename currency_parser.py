from datetime import datetime, timedelta
import urllib.request
import shutil
import openpyxl
import csv


def menu(name, duration):  # name = 34 different 3 letter names. duration: days from now
    date1, date2 = get_dates(duration)

    save_file_name = "C:/Users/Admin/Desktop/dbs/tmp.xlsx"
    header_filename = "C:/Users/Admin/Desktop/dbs/header.csv"
    tmp_csv_filename = "C:/Users/Admin/Desktop/dbs/tmp.csv"

    qid = get_label_id(header_filename, name)
    query = query_assembly(qid, date1, date2)

    with urllib.request.urlopen(query) as response, open(save_file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    excel = openpyxl.load_workbook(save_file_name)
    sheet = excel.active
    with open(tmp_csv_filename, 'w', newline="\n") as f:
        col = csv.writer(f)
        for r in sheet.rows:
            col.writerow([cell.value for cell in r])

    result = []
    with open(tmp_csv_filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            result.append(float(row[2]))
        # print(result)

    numeration = list(range(duration))  # days to curdate
    # print(numeration)
    return result, numeration


def get_dates(duration):
    curdate_raw = datetime.date(datetime.now())
    curdate_raw_split = str(curdate_raw).split("-")
    curdate = curdate_raw_split[2] + "." + curdate_raw_split[1] + "." + curdate_raw_split[0]
    startdate_raw = datetime.date(datetime.today() - timedelta(days=duration))
    startdate_raw_split = str(startdate_raw).split("-")
    startdate = startdate_raw_split[2] + "." + startdate_raw_split[1] + "." + startdate_raw_split[0]
    return startdate, curdate


def query_assembly(qid, date1, date2):
    date1_split = date1.split(".")
    date2_split = date2.split(".")
    date1_2 = date1_split[1] + "/" + date1_split[0] + "/" + date1_split[2]
    date2_2 = date2_split[1] + "/" + date2_split[0] + "/" + date2_split[2]

    query_address = "https://www.cbr.ru/Queries/UniDbQuery/DownloadExcel/98956?Posted=True&so=1&mode=1"
    q_url = query_address + "&VAL_NM_RQ=" + qid + "&From=" + date1 + "&To=" + date2 + "&FromDate=" + date1_2 + "&ToDate=" + date2_2
    # print(q_url)
    return q_url


def get_headers(filename):
    labels = []
    ids = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            lsplit = line.split(";")
            labels.append(lsplit[1].split("\n")[0])
            ids.append(lsplit[0])
    return ids, labels


def get_label_id(filename, label):
    ids, labels = get_headers(filename)
    i = 0
    for labeli in labels:
        if labeli == label:
            return ids[i]
        i = i + 1
    return -1


# print(menu('USD', 30))
