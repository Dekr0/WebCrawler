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

    site = setting["site"]
    params = util.url_encoder(setting["parameters"])

    fetch_func = fetch.get(site)
    fetch_result = fetch_func(params)

    extract_func = extract.get(site)
    extract_result = extract_func(fetch_result)

    writer = write.get(site)
    writer(extract_result)

if __name__ == "__main__":
    main()
