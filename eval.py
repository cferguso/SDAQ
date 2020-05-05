#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Charles.Ferguson
#
# Created:     05/05/2020
# Copyright:   (c) Charles.Ferguson 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys, os, requests
from requests import HTTPError


url = 'https://raw.githubusercontent.com/cferguso/SDAQ/master/tax_order_stt_abbr.txt'

resp = requests.get(url)
raw = (resp.text)
raw = raw.replace("param1", "NE")




