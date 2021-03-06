import datetime
import re
import selenium
import random
from time import sleep
from driver import driver
from vk_handler import vk_task_manager
from fb_handler import fb_task_manager
from twit_handler import twit_task_manager
from insta_handler import insta_task_manager
from Log_in import general_login
from my_logging import *
from zenja_down import debug_screenshot
from datetime import datetime


def check_profit():
    i = 1
    driver.get("https://vktarget.ru/list/")
    while True:
        try:
            xpath = str("/html/body/div[22]/div/div[3]/div[7]/div[" + str(i) + "]/div[6]")
            button = driver.find_element_by_xpath(xpath)
            sleep(random.uniform(2, 10))  # pause for stop yorzat'
            button.click()
            i += 1
        except selenium.common.exceptions.NoSuchElementException:
            break


def find_tasks(task_list):  # parse task_list for separated social network tasks
    vk_tasks, gplus_tasks, insta_tasks, fb_tasks, twit_tasks = [], [], [], [], []
    for task in task_list:
        if task.find("https://vk.com") != -1:
            vk_tasks.append(task)
        elif task.find("https://www.instagram.com") != -1:
            insta_tasks.append(task)
        elif task.find("https://plus.google.com") != -1:
            gplus_tasks.append(task)
        elif task.find("https://www.facebook.com") != -1:
            fb_tasks.append(task)
        elif task.find("https://twitter.com/") != -1:
            twit_tasks.append(task)

    if vk_tasks:
        vk_task_manager(vk_tasks)
    if fb_tasks:
        fb_task_manager(fb_tasks)
    # if gplus_tasks:
    #     gplus_handler(gplus_tasks)
    if insta_tasks:
        insta_task_manager(insta_tasks)
    if twit_tasks:
        twit_task_manager(twit_tasks)


def get_task_list():  # parse target for all tasks
    driver.get("https://vktarget.ru/list/")
    sleep(5)  # ВАЖНО
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    task_list = re.findall(r'<a rel="nofollow noopener" data-bind="url" target="_blank" href=".{1,128}</a>', html)
    if not task_list:
        sleep(10)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        task_list = re.findall(r'<a rel="nofollow noopener" data-bind="url" target="_blank" href=".{1,128}</a>', html)
    # TODO:
    print(task_list)
    return task_list


# TODO
# а если разлогинится в процессе?
general_login()

while True:
    try:
        find_tasks(get_task_list())
        sleep(5)
        check_profit()
        logging.info('выход на охоту: ' + str(datetime.now().strftime('%Y_%m_%d_%H:%M:%S')))
    except Exception:
        error = str('!!!выход провален: ' + str(datetime.now().strftime('%Y_%m_%d_%H:%M:%S')) + '\n' + str(Exception))
        logging.error(error)
    # TODO
    # в этом месте будут плодиться огненные лисы
    driver.switch_to.window(driver.window_handles[0])
    pause = 60 * random.uniform(15, 60)
    logging.info("следующий выход через (мин): " + str(pause / 60))
    sleep(pause)  # чтоб типа как человек
