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
    setting = json.load(open(config.setting_path, "rb"))

    website_name = setting["website"]

    # formatted search parameters
    parameters = util.url_encoder(setting["parameters"])

    # main function that start the fetch process
    fetch_func = fetch.get(website_name)
    # a list of job posts represented by HTML elements
    fetch_result = fetch_func(parameters)

    # main function that start the extract process
    extract_func = extract.get(website_name)
    # extract the information from the job post using integrated selector
    extract_result = extract_func(fetch_result)

    writer = write.get(website_name)
    writer(extract_result)

if __name__ == "__main__":
    main()
