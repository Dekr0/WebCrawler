import logging

import modules.models as models


__all__ = []

_QUIT = "Check EventLog.log"


def _get_company_location(job_post):
    try:
        company_tag = job_post.find("span.companyName", first=True)
        assert company_tag, "Failed to find company"
        location_tag = job_post.find("div.companyLocation", first=True)
        assert location_tag, "Failed to find location"

        company = company_tag.text

        location = location_tag.text

        return company, location
    except AssertionError as error:
        logging.error(error, exc_info=True)

        quit(_QUIT)


def _get_day_post(job_post):
    selector = "span.date"
    try:
        tag = job_post.find(selector, first=True)
        assert tag, "Failed to find day of post"

        day_post = tag.text

        return day_post
    except AssertionError as error:
        logging.error(error, exc_info=True)

        quit(_QUIT)


def _get_id_link_title(job_post):
    selector = "span[title]"
    try:
        tag = job_post.find(selector, first=True)
        assert tag, "Failed to find title or link"
    except AssertionError as error:
        logging.error(error, exc_info=True)

        quit(_QUIT)
    else:
        job_id = job_post.attrs["data-jk"]
        link = job_post.attrs["href"]
        title = tag.attrs["title"]

        if "\'" in title:
            title = title.replace("\'", "\'\'")

        return job_id, link, title


def _get_summary(job_post):
    selector = "div.job-snippet"
    try:
        summary_tag = job_post.find(selector, first=True)
        assert summary_tag, "Failed to find summary"

        li_tags = summary_tag.find("li")
        summary = ""
        for li_tag in li_tags:
            summary += li_tag.text + "\n"

        return summary
    except AssertionError as error:
        logging.error(error, exc_info=True)

        quit(_QUIT)


def _get_info(job_post):
    company, location = _get_company_location(job_post)
    day_post = _get_day_post(job_post)
    job_id, link, title = _get_id_link_title(job_post)
    summary = _get_summary(job_post)

    job = models.IndeedJobs(company, day_post, job_id, link, location, summary,
                            title)

    return job


def handle(job_posts):
    jobs = models.IndeedJobsSet()

    for job_post in job_posts:
        job = _get_info(job_post)
        jobs.add_job(job)

    log = "Extraction completed"

    print(log)
    logging.info(log)

    return jobs
