import random
import time

import modules.adt as adt
import modules.response as response
import modules.util as util


__all__ = ["main"]

_QUIT = "Check EventLog.log"

_JOB_LIMIT = 100  # number of jobtype posts

_rnd = random.SystemRandom()


def _pause():
    """
    Pause the program between 2 minutes to 3 minutes to prevent IP ban

    :return: None
    """

    sleep_time = _rnd.randint(120, 180)
    log = f"Pause for {sleep_time}"

    util.info(log)

    time.sleep(sleep_time)


def _fetch(params):
    """
    fetch jobtype post in each page until it reach desire number of jobtype posts.
    Generally, each page should have 15 jobtype posts but there are exceptions.
    Sometime one page will have more than or less than 15.

    :param params: a formatted string that include the search parameter
    :return: a collection (queue) of jobtype posts (instance) for information extraction
    """

    webpage = response.IndeedWebPage(params)
    webpage.get_next_webpage()  # The first page of the search result

    # The total number of jobtype posts from the search result
    total_job_posts = webpage.get_num_jobs()
    job_posts_list = adt.IterableQueue()  # A queue for jobtype posts collection

    finished = False
    while not finished:
        # Return a list of job posts (a list of HTML elements that represent the
        # job posts in the webpage to be more specifically)

        job_posts = webpage.get_job_posts()

        for job_post in job_posts:
            job_posts_list.put(job_post)
            total_job_posts -= 1

            # Stop the fetch process if find enough job posts
            if total_job_posts <= 0 or len(job_posts_list) == _JOB_LIMIT:
                finished = True
                break

        if not finished:
            progress_status = f"Current Page: {webpage.next_page - 1};" \
                       f"Number of jobtype posts fetched in current page : {len(job_posts)};" \
                       f"Number of jobtype posts fetched in total : {len(job_posts_list)};" \
                       f"Number of jobtype posts remained to fetched : {total_job_posts}"

            util.info(progress_status)

            _pause()

        webpage.close()  # close the response for the current webpage
        webpage.get_next_webpage()  # get the response for the next webpage

    webpage.disconnect()  # close the HTML session and chromium

    log = f"Job posts fetch completed. Number of jobtype posts fetched : {len(job_posts_list)}"
    util.info(log)

    return job_posts_list


def main(params):

    # Start the jobtype post gathering process
    job_posts_list = _fetch(params)

    return job_posts_list
