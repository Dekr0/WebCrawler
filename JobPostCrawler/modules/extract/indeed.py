import logging

import modules.jobtype as jobtype
import modules.util as util


__all__ = ["main"]

_QUIT = "Check EventLog.log"


def _get_company_location(job_post):
    """
    Get the company name and the location of a job post

    :param job_post: a job post represented by a HTML element
    :return: company name and location of a job post in string
    """

    try:
        company_tag = job_post.find("span.companyName", first=True)
        assert company_tag, "Failed to find company"
        location_tag = job_post.find("div.companyLocation", first=True)
        assert location_tag, "Failed to find location"

        company = company_tag.text

        location = location_tag.text

        return company, location
    except AssertionError as error:
        util.error(str(error))

        return "Unknown", "Unknown"


def _get_day_post(job_post):
    """
    Get the day that a job post is released

    :param job_post: a job post represented by a HTML element
    :return: the day that a job post is posted in string
    """

    selector = "span.date"
    try:
        tag = job_post.find(selector, first=True)
        assert tag, "Failed to find day of post"

        day_post = tag.text

        return day_post
    except AssertionError as error:
        util.error(str(error))

        return "Unknown"


def _get_id_link_title(job_post):
    """
    Get the unique job id, job title and the URL to the detailed job
    description

    :param job_post: a job post represented by a HTML element
    :return:
    """

    selector = "span[title]"
    try:
        tag = job_post.find(selector, first=True)
        assert tag, "Failed to find title or link"
    except AssertionError as error:
        util.error(str(error))

        quit(_QUIT)
    else:
        job_id = job_post.attrs["data-jk"]
        link = job_post.attrs["href"]
        title = tag.attrs["title"]

        if "\'" in title:
            title = title.replace("\'", "\'\'")

        return job_id, link, title


def _get_summary(job_post):
    """
    Get the job summary

    :param job_post: a job post represented by a HTML element
    :return:
    """

    selector = "div.job-snippet"
    try:
        summary_tag = job_post.find(selector, first=True)
        assert summary_tag, "Failed to find summary"

        # Some job summary contains list of bullet represented by a set of
        # <li> element
        li_tags = summary_tag.find("li")
        summary = ""
        for li_tag in li_tags:
            summary += li_tag.text + "\n"

        return summary
    except AssertionError as error:
        util.error(str(error))

        return "Unknown"


def _get_info(job_post):
    """
    Extract the information from a job post (HTML element)

    :param job_post: a job post represented by a HTML element
    :return: a job instance that encapsulate its information
    """

    company, location = _get_company_location(job_post)
    day_post = _get_day_post(job_post)
    job_id, link, title = _get_id_link_title(job_post)
    summary = _get_summary(job_post)

    job = jobtype.IndeedJob(company, day_post, job_id, link, location, summary,
                            title)

    return job


def main(job_posts):
    """
    Extract the information from each job post and store them into a list

    :param job_posts: a list of job posts represented by a list of HTML elements
    :return: a list of IndeedJob instances
    """

    jobs = []

    for job_post in job_posts:
        job = _get_info(job_post)
        jobs.append(job)

    log = "Extraction completed"

    util.info(log)

    return jobs
