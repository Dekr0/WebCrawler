#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging

import config
import modules.extract as extract
import modules.fetch as fetch
import modules.util as util
import modules.write as write

logging.basicConfig(filename="EventLog.log",
                    format="%(asctime)s - %(levelname)s - %(module)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %p",
                    level=logging.INFO)


def main():
    setting = json.load(open(config.settingPath, "rb"))

    websiteName = setting["website"]

    # formatted search parameters
    parameters = util.URLEncoder(setting["parameters"])

    limit = setting["limit"]

    # main function that start the fetch process
    fetchFunc = fetch.get(websiteName)
    # a list of job posts represented by HTML elements
    fetchResult = fetchFunc(parameters, limit)

    # main function that start the extract process
    extractFunc = extract.get(websiteName)
    # extract the information from the job post using integrated selector
    extractResult = extractFunc(fetchResult)

    writer = write.get(websiteName)
    writer(extractResult)

if __name__ == "__main__":
    main()
