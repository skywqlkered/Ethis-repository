import datetime

def write_csv_entry(entry:str):
    with open("./activity.csv", "a") as f:
        f.write(entry)

def convert_time(date_obj:datetime.datetime) -> tuple[str, str]:
    date = date_obj.strftime("%d/%m/%Y") 
    time = date_obj.strftime("%H:%M:%S")
    return (date, time)


def create_data_entry(username, action: int | None, date: datetime.datetime):
    print(f"action = {action}")
    entry = ""
    username = ""
    date_entry = convert_time(date)

    if action == 1:  # action = join
        pass

    elif action == 0:  # action = leave
        entry = ",".join([])

    else:
        print("action wasnt clear")
        
        
date = datetime.datetime.now()
create_data_entry("sky", action=1, date=date)