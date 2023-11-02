import os
import pandas as pd
from itrans import Translator


def translate_text(translator, text):
    tt = translator.translate(text)
    return tt


def process_item(fr, to, item: pd.DataFrame, row_name, logger) -> pd.DataFrame:
    need = item[row_name].iloc[0]
    translator = Translator(source=fr, target=to, logger=logger)
    trans = translate_text(translator, need)
    item[row_name].iloc[0] = trans
    return item


def check_translation_status(futures):
    return all(future.done() for future in futures)


def create_temp(file_name, column):
    id_file = open(os.path.join('temp', file_name + '.id'), 'a+')
    tmp = os.path.join('temp', file_name + '.csv')
    df = pd.DataFrame(columns=column)
    df.to_csv(tmp, index=False)
    return id_file, tmp


def get_pre_list_index(path):
    with open(path, 'r', encoding='utf-8') as f:
        indexes = f.read().strip().split(' ')
    indexes = set(indexes)
    return indexes
