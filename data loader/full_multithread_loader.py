import requests
import json
import threading
import time
import pathlib
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

headers = {"Authorization": "Bearer token"}
get_full_vacancy_by_id_url = "https://api.hh.ru/vacancies/"
add_vacancies_url = "http://localhost:8080/saveVacancies"

it_vacancies_folder = '55.25M_55.5M'
all_vacancies_folder = '36M_37.5M_full'

first_id = 55230000
last_id =  55500000
starts = []
ends = []
chunk_size = 1000

total = last_id - first_id
N = int(total / chunk_size) + 1

for i in range(0, N):
    s = first_id + i * chunk_size
    e = s + chunk_size
    starts.append(s)
    ends.append(e)

finished = 0
it_vacs = 0
all_vacs = 0

def load_by_id(S, E):
    it_entries = []
    all_entries = []
    global it_vacs
    global all_vacs

    print(str(threading.current_thread().ident) + " [" + str(S) + ", " + str(E) + "]")

    N = E - S
    for i in range(S, E):
        if i % 100 == 0:
            print(str(threading.current_thread().ident) + " " + str(i-S) + "/" + str(N))
        query = get_full_vacancy_by_id_url + str(i)
        response = None
        while response == None:
            try:
                response = requests.get(query, headers=headers)
            except:
                print("Connection refused by the server..")
                print("Zzzzzz...")
                time.sleep(5)
                print("Trying to continue...")
                continue

        vacancy = json.loads(response.text)
        #all_entries.append(vacancy)

        if 'specializations' in vacancy:
            all_vacs += 1
            specializations = vacancy['specializations']
            for s in specializations:
                if s['id'] == '1.221':
                    it_entries.append(vacancy)
                    it_vacs += 1
                    break

    if len(it_entries) > 0:
        filename = it_vacancies_folder + '/' + str(S) + '_' + str(E) + '.json'
        with open(filename, 'w') as outfile:
            json.dump(it_entries, outfile)
            it_entries.clear()

    # if len(all_entries) > 0:
    #     filename = all_vacancies_folder + '/' + str(S) + '_' + str(E) + '.json'
    #     with open(filename, 'w') as outfile:
    #         json.dump(all_entries, outfile)
    #         all_entries.clear()

    global finished

    finished = finished + E - S
    print("progress: " + str(finished) + "/" + str(total))
    print("it_vacs: " + str(it_vacs))
    print("all_vacs: " + str(all_vacs))


if __name__ == '__main__':

    pathlib.Path(it_vacancies_folder).mkdir(parents=True, exist_ok=True)
    pathlib.Path(all_vacancies_folder).mkdir(parents=True, exist_ok=True)

    with PoolExecutor(max_workers=50) as executor:
        for _ in executor.map(load_by_id, starts, ends):
            pass
