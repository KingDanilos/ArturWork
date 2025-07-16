import os


def list_levels():
    files = os.listdir(path='.')
    result = []
    for file in files:
        if file.lower().endswith('.txt'):
            result.append(file)
    
    return result


def load(file):
    # 1. Загрузить весь файл в строку
    f = open(file, 'r')
    s = f.read()

    # 2. Заменить все пробелы и переводы строки на "ничего"
    s = s.replace(' ', '')
    s = s.replace('\n', '')

    # 3. Из полученной строки создать массив, используя разделитель ","
    a = s.split(',')

    # a - массив чисел из а
    f.close()
    return a