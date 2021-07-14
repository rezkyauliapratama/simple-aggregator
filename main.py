# import multiprocessing
import threading
import time

import usecases
from src.utils.log_helper import LogHelper

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    LogHelper()
    starttime = time.time()
    processes = []

    for module in usecases.usecases():
        print(f"module : {module}")
        try:
            p = threading.Thread(target=usecases.execute, args=(module,))
            processes.append(p)
            p.start()

        except Exception as exc:
            LogHelper.log_error(exc)

    for process in processes:
        process.join()

    print('Time taken = {} seconds'.format(time.time() - starttime))
