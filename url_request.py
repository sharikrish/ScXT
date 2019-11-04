import urllib.request, urllib.parse

import argparse
import json
import os, ssl
import sys
import time, requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
#
# # Try to make the connection and get a response.
# def response_data(sample_url):
#     try:
#         header_dict = {'accept': 'application/json', 'Content-Type': 'application/json'}
#         url_data = urllib.parse.urlencode(header_dict).encode()
#         response = urllib.request.urlopen(sample_url, data=url_data)
#         url_response = response.read()
#         return url_response
#     except urllib.error.HTTPError as e:
#         print('Error: Server could not fullfil the request')
#         print('Error: Error code =', e.code)
#         exit()
#     except urllib.error.URLError as e:
#         print('Error: Failed to reach the server')
#         print('Error: Reason =', e.reason)
#         exit()
#
#     json_data = json.loads(url_response)

def getArguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )
    # Field in the API to use for x dimension of the heatmap
    parser.add_argument("base_url")
    #parser.add_argument("filter_query")
    #parser.add_argument("x_values")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the program in verbose mode.")
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    # Get the command line arguments.
    options = getArguments()
    sample_url = options.base_url
    PARAMS= {'cell_id' : '1003'}
    # sending get request and saving the response as response object
    r = requests.get(url=sample_url)
    var = json.loads(r.text)
    print(var)


    def find(todo):
        check = todo["cell_id"]
        max_var = todo["userId"] in users
        return check and max_var

