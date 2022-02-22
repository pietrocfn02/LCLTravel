from multiprocessing import Process, Pool
import subprocess
import sys
from time import sleep

import src.graphics as graphics

LOADING_STRING = ['Collecting required modules - \\', 'Collecting required modules - |',
                  'Collecting required modules - /', 'Collecting required modules - ~']


def loading():
    i = 0
    while True:
        print(LOADING_STRING[i % len(LOADING_STRING)], end='\r')
        sleep(0.2)
        i += 1


def install_modules():
    # Starting to install/update required modules
    otp = subprocess.check_call([sys.executable, '-m', 'pip',
                                 'install', '-r', 'requirements.txt'])
    if otp == 0:
        print('Modules succesfully updated', end='\r')
    else:
        print('An error has occurred', end='\r')
        exit(otp)


def main():
    # Getting a pool of processes
    pool = Pool(2)
    # Creating the process that handle the little animated cli text for the loading
    loading_process = Process(target=loading)
    # Creating the process that hanle the installation/update of required modules
    install_modules_process = Process(target=install_modules)
    # Running those processes asynchronusly
    pool.apply_async(loading_process)
    await_result = pool.apply_async(install_modules_process)
    await_result.wait()
    # Terminating the loading text animation, so, terminate its processes and the pool's one itself
    pool.terminate()
    pool.close()
    pool.join()
    # Starting the gui
    graphics.main()


if __name__ == '__main__':
    main()
