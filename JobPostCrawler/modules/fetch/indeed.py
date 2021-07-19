import logging
import random
import time

import modules.models as models
import modules.util as util


__all__ = ["handle"]

_QUIT = "Check EventLog.log"

_JOB_LIMIT = 1000

_rnd = random.SystemRandom()


def _pause():
    sleep_time = _rnd.randint(120, 180)
    log = f"Pause for {sleep_time}"

    print(log)
    logging.info(log)

    time.sleep(sleep_time)


def _fetch(params):
    webpage = util.IndeedWebPage(params)
    webpage.get_next_webpage()

    total_job_posts = webpage.get_num_jobs()
    job_posts_list = models.IndeedJobPosts()

    finished = False
    while not finished:
        job_posts = webpage.get_job_posts()

        for job_post in job_posts:
            job_posts_list.put(job_post)
            total_job_posts -= 1

            if total_job_posts <= 0 or len(job_posts_list) == _JOB_LIMIT:
                finished = True
                break

        if not finished:
            page_log = f"Current Page: {webpage.next_page - 1};" \
                       f"Number of job posts fetched in current page : {len(job_posts)};" \
                       f"Number of job posts fetched in total : {len(job_posts_list)};" \
                       f"Number of job posts remained to fetched : {total_job_posts}"

            print(page_log)
            logging.info(page_log)

            _pause()

        webpage.close()
        webpage.get_next_webpage()

    webpage.disconnect()
    complete_log = f"Job posts fetch completed. Number of job posts fetched : {len(job_posts_list)}"

    print(complete_log)
    logging.info(complete_log)

    return job_posts_list


def handle(params):
    job_posts_list = _fetch(params)

    return job_posts_list
