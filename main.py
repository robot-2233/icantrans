# -*- coding: UTF-8 -*-
import concurrent.futures
from config import *
from transformers import logging
from controller import ClashProxyController
from state import *
from tqdm import tqdm
import shutil

def set_global_proxy(w):
    os.environ['https_proxy'] = f'http://{w.local_host}:{w.pp}'
    os.environ['http_proxy'] = f'http://{w.local_host}:{w.pp}'


if __name__ == '__main__':

    logging.set_verbosity_error()

    if os.path.exists('temp'):
        print('cleaning temp')
        shutil.rmtree('temp')

    args, logger = get_config()
    assert os.path.exists(args.input_path), f"{args.input_path} does not exist, please check the path."

    set_global_proxy(args)

    logger.info('> Translate arguments:')
    for _ in vars(args):
        logger.info(f">>> {_}: {getattr(args, _)}")
    c = ClashProxyController(args, logger)

    for file_name in os.listdir(args.input_path):
        data = pd.read_csv(os.path.join(args.input_path, file_name)).reset_index()  ###
        all_index = set(data['index'])
        for target_lan in args.to:

            after_name = file_name.replace('.csv', f'_{target_lan}')
            save_path = os.path.join(args.output_path, after_name + '.csv')
            id_file, temp_path = create_temp(after_name, data.columns.tolist())
            id_file.seek(0)
            pre_indexes = set(id_file.read().split(' ')) if len(id_file.read()) > 3 else set()

            while len(all_index) * args.save_scale > len(pre_indexes):
                undone = list(all_index - pre_indexes)
                result_data = []
                with tqdm(total=len(undone), desc=f"Processing_{file_name}_{target_lan}") as pbar:

                    with concurrent.futures.ThreadPoolExecutor(max_workers=args.queue_num) as executor:
                        for i in range(0, len(undone), args.batch_size):
                            undone_index = undone[i:min(i + args.batch_size, len(undone))]
                            undone_data = [data.iloc[i:i + 1] for i in undone_index]

                            futures = []
                            running_num = 0

                            for item in undone_data:
                                future = executor.submit(process_item, args.fr, target_lan, item, args.row_name, logger)
                                futures.append(future)
                                running_num += 1

                            for future in concurrent.futures.as_completed(futures):
                                result = future.result()
                                pbar.update(1)
                                trans_t = result[args.row_name].iloc[0]
                                if trans_t:
                                    result_data.append(result)
                                    done_id = str(result['index'].iloc[0]) + ' '
                                    id_file.write(done_id)
                            if len(result_data) > 12:
                                id_file.flush()
                                merged_data = pd.concat(result_data, ignore_index=True)
                                result_data = []
                                merged_data.to_csv(temp_path, mode='a', header=False, index=False)

                                c.change_proxy()

                id_file.seek(0)
                pre_indexes = set(id_file.read().split(' '))

            # write into
            trans_csv = pd.read_csv(temp_path)
            id_file.close()
            os.remove(temp_path)
            trans_csv = trans_csv.sort_values(by='index')
            trans_csv = trans_csv.drop(columns=['index'])
            trans_csv.to_csv(save_path, index=False)
            logger.info(f"Save in {save_path}")

    logger.info('''============================(=^ω^=) YOUR CLASH DID IT!============================''')

    shutil.rmtree('temp')
    logger.info('Meow~')

