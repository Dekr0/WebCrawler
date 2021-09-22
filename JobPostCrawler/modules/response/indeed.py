import re

import modules.util as util


_QUIT = "Check EventLog.log"


class IndeedWebPage:

    """
    A class that represents each webpage from the search result. The class
    also encapsulates the agent for requesting a response from Indeed, as
    well as the method for manipulation of the response and webpage.
    """

    def __init__(self, params):
        """
        :param params: a formatted string that include the search parameter
        """

        self.nextPage = 0  # Page index starts from 0
        self.requestAgent = util.RequestFactory.get_request("indeed")(params)
        self.response = None

    def close(self):
        """
        Close the current response of a webpage

        :return: None
        """

        if self.response:
            self.response.close()
            self.response = None

    def disconnect(self):
        """
        Close the current HTML session (Chromium tab or thread).

        :return: None
        """

        self.requestAgent.close()

    def getNextWebpage(self):
        """
        Get the response of the next webpage from the search result

        :return: None
        """

        self.requestAgent.set_search_parameter(self.nextPage)
        self.response = self.requestAgent.request()

        # render the webpage since its source code is most likely JavaScript
        self.render()

        self.nextPage += 1

    def getJobPosts(self):
        """
        Get all the job post from the current webpage

        :return: A list of job posts represented by a list of HTML elements
        """

        # Need to change if the source code is updated
        sel = "[class*=\"tapItem fs-unmask result\"]"
        try:
            jobPosts = self.response.html.find(sel)
            assert jobPosts, "Failed to find jobtype posts"
        except Exception as error:
            util.error(str(error))

            quit(_QUIT)
        else:
            return jobPosts

    def getNumJobs(self):
        """
        Get the total number of job posts from the search result

        :return:
        """

        sel = "#searchCountPages"
        try:
            tag = self.response.html.find(sel, first=True)
            assert tag, "Failed to find total number of jobs"
        except Exception as error:
            util.error(str(error))

            quit(_QUIT)
        else:
            text = tag.text

            match = re.search(r"(?P<numJobs>((?<=of )[0-9,]+(?= jobs)))", text)
            content = match.group("numJobs")

            content = content.replace(",", "")

            numJobs = int(content)

            return numJobs

    def isRender(self):
        """
        Check if the webpage is render from JavaScript into HTML.

        :return: True if the webpage is true
        """

        # If the webpage is render in HTML, it should a set of elements
        # that match the css selector.
        sel = "[class*=\"tapItem fs-unmask result\"]"
        contents = self.response.html.find(sel)

        return False if len(contents) == 0 else True

    def render(self):
        """
        Render the webpage if its source code is JavaScript. Notice the render
        process probably fail sometimes.

        :return: None
        """

        log = "Failed to render javascript : "

        flag = self.isRender()
        timeout = 10

        while not flag:

            try:
                self.response.html.render()
                flag = self.isRender()
            except Exception as error:
                util.error(log + str(error))

                timeout -= 1

            if timeout == 0:
                util.error(log + "Timeout")

                quit(_QUIT)

        if not flag:
            util.error(log + "Timeout")

            quit(_QUIT)
