import logging
import re

import modules.util as util


_QUIT = "Check EventLog.log"


class IndeedWebPage:


    def __init__(self, params):
        self.next_page = 0
        self.request_agent = util.RequestFactory.get_request("indeed")(params)
        self.response = None

    def close(self):
        if self.response:
            self.response.close()
            self.response = None

    def disconnect(self):
        self.request_agent.close()

    def get_next_webpage(self):
        self.request_agent.set_search_parameter(self.next_page)
        self.response = self.request_agent.request()

        self.render()

        self.next_page += 1

    def get_job_posts(self):
        sel = "[class*=\"tapItem fs-unmask result\"]"
        try:
            job_posts = self.response.html.find(sel)
            assert job_posts, "Failed to find job posts"
        except Exception as error:
            logging.error(error, exc_info=True)

            quit(_QUIT)
        else:
            return job_posts

    def get_num_jobs(self):
        sel = "#searchCountPages"
        try:
            tag = self.response.html.find(sel, first=True)
            assert tag, "Failed to find total number of jobs"
        except Exception as error:
            logging.error(error, exc_info=True)

            quit(_QUIT)
        else:
            text = tag.text

            match = re.search(r"(?P<num_jobs>((?<=of )[0-9,]+(?= jobs)))", text)
            content = match.group("num_jobs")

            content = content.replace(",", "")

            num_jobs = int(content)

            return num_jobs

    def is_render(self):
        sel = "[class*=\"tapItem fs-unmask result\"]"
        contents = self.response.html.find(sel)

        return False if len(contents) == 0 else True

    def render(self):
        log = "Failed to render javascript"

        flag = self.is_render()
        timeout = 10

        while not flag:

            try:
                self.response.html.render()
                flag = self.is_render()
            except Exception as error:
                logging.error(error, exc_info=True)

                timeout -= 1

            if timeout == 0:
                logging.error(log, exc_info=True)

                quit(_QUIT)

        if not flag:
            logging.error(log, exc_info=True)

            quit(_QUIT)


