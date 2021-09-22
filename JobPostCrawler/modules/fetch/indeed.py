import random
import time

import modules.adt as adt
import modules.response as response
import modules.util as util


__all__ = ["main"]

_QUIT = "Check EventLog.log"

_rnd = random.SystemRandom()


def _pause():
    """
    Pause the program between 2 minutes to 3 minutes to prevent IP ban

    :return: None
    """

    sleepTime = _rnd.randint(0, 60)
    log = f"Pause for {sleepTime} seconds"

    util.info(log)

    time.sleep(sleepTime)


def _fetch(params, limit):
    """
    fetch jobtype post in each page until it reach desire number of jobtype posts.
    Generally, each page should have 15 jobtype posts but there are exceptions.
    Sometime one page will have more than or less than 15.

    :param params: a formatted string that include the search parameter
    :return: a collection (queue) of jobtype posts (instance) for information extraction
    """

    webpage = response.IndeedWebPage(params)
    webpage.getNextWebpage()  # The first page of the search result

    # The total number of jobtype posts from the search result
    totalJobPosts = webpage.getNumJobs()
    jobPostsList = adt.IterableQueue()  # A queue for jobtype posts collection

    finished = False
    while not finished:
        # Return a list of job posts (a list of HTML elements that represent the
        # job posts in the webpage to be more specifically)

        jobPosts = webpage.getJobPosts()

        for job_post in jobPosts:
            jobPostsList.put(job_post)
            totalJobPosts -= 1

            # Stop the fetch process if find enough job posts
            if totalJobPosts <= 0 or len(jobPostsList) == limit:
                finished = True
                break

        if not finished:
            progress_status = f"Current Page: {webpage.nextPage - 1};" \
                   f"Number of jobtype posts fetched in current page : {len(jobPosts)};" \
                   f"Number of jobtype posts fetched in total : {len(jobPostsList)};" \
                   f"Number of jobtype posts remained to fetched : {totalJobPosts}"

            util.info(progress_status)

            _pause()

        # webpage.close()  # close the response for the current webpage
        webpage.getNextWebpage()  # get the response for the next webpage

    webpage.disconnect()  # close the HTML session and chromium

    log = f"Job posts fetch completed. Number of jobtype posts fetched : {len(jobPostsList)}"
    util.info(log)

    return jobPostsList


def main(params, limit):

    # Start the jobtype post gathering process
    jobPostsList = _fetch(params, 15 * limit)

    return jobPostsList
