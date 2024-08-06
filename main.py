import codecs
import json
import time
from datetime import datetime, timedelta


def array_to_file(data_array, endfile_name, category):
    """Forming a JSON structure and writing it in certain file

    :param data_array: source array
    :param endfile_name: name of category file
    :param category: -- category's name

    """
    data_array = sorted(data_array, key=lambda x: (x['Время'], x['Нагрудный номер']))
    prize_name = ''.join(['prizes_list_', category, '.txt'])
    prize_file = codecs.open(prize_name, 'r', 'utf_8_sig')
    endfile = open(endfile_name, 'w', encoding='utf-8')

    for i in range(len(data_array)):
        data_array[i]['Место'] = i + 1
        if i < 49:
            # Removing "Х место" from prize description
            data_array[i]['Приз'] = ' '.join(prize_file.readline().split()[2:])

        data_array[i]['Время'] = str(data_array[i]['Время'])

    prize_file.close()
    endfile.write(json.dumps(data_array, indent=4, ensure_ascii=False))
    endfile.close()


def main():
    m15_array, m16_array, m18_array, w15_array, w16_array, w18_array = ([] for _ in range(6))
    arrays_dict = {"M15": m15_array, "M16": m16_array, "M18": m18_array,
                   "W15": w15_array, "W16": w16_array, "W18": w18_array}

    data_file = codecs.open('race_data.json', 'r', 'utf_8_sig')
    data = json.load(data_file)
    data_file.close()

    for elem in data:
        number = elem['Нагрудный номер']
        fio = ' '.join([elem['Имя'], elem['Фамилия']])
        runtime = (datetime.strptime(elem['Время финиша'], "%H:%M:%S") -
                   datetime.strptime(elem['Время старта'], "%H:%M:%S"))
        if runtime.days < 0:
            runtime = timedelta(seconds=runtime.total_seconds() + 3600 * 24)
        # Adding an element to certain array based on its category
        arrays_dict[elem['Категория']].append({'Нагрудный номер': number, 'Имя и Фамилия': fio, 'Время': runtime})

    array_to_file(m15_array, 'm15.json', 'm15')
    array_to_file(m16_array, 'm16.json', 'm16')
    array_to_file(m18_array, 'm18.json', 'm18')
    array_to_file(w15_array, 'w15.json', 'w15')
    array_to_file(w16_array, 'w16.json', 'w16')
    array_to_file(w18_array, 'w18.json', 'w18')


if __name__ == '__main__':
    main()
