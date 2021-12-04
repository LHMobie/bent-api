# Copyright 2021 LNH
# All rights reserved.

import json, decimal, hug, configparser, sys, time, requests, os

from pprint import pprint
from web3 import Web3
from web3.exceptions import TimeExhausted

decimal.getcontext().rounding = decimal.ROUND_DOWN

__version__ = '0.0.1'

class APIMiddlewareRouter(object):

    def process_request(self, request, response):
        pass

    def process_response(self, request, response, resource, req_succeeded):
        if request.method == 'OPTIONS':
            response.set_header('Access-Control-Max-Age', '1728000')
            response.set_header('Content-Type', 'text/plain charset=UTF-8')
            response.set_header('Content-Length', '0')
        response.set_header('Access-Control-Allow-Origin', '*')
        response.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.set_header('Access-Control-Allow-Headers',
                            'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,'
                            'Content-Type,X-Device-UUID,Authorization,X-API-VERSION')


@hug.object
class API:
    hug_api = None

    def __init__(self):

        hug_api = hug.api.from_object(self)
        hug_api.http.add_middleware(APIMiddlewareRouter())

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        """
        Environment hard coded to MAINNET, but it can be set as an environment variable.  Must have matching structure in config.ini
        """
        # self.env = os.getenv('BLOCKCHAIN')
        self.env = 'MAINNET'

        # Node Services Provider
        self.eth_w3_http = Web3(Web3.HTTPProvider(self.config['ETH-{}'.format(self.env)]['HTTPProvider']))

        # Load Bent token contract abi
        with open('bent_abi.json', 'r') as myfile:
            data=myfile.read()
            self.token_abi = json.loads(data)

        # Configure Bent contract interface
        self.token_contract = self.eth_w3_http.eth.contract(
            address=Web3.toChecksumAddress(self.config['ETH-{}'.format(self.env)]['token_contract']), 
            abi=self.token_abi)

    """
    SYSTEM ENDPOINTS
    """
    @hug.object.get('/sys/version', versions=1)
    def get_version(self, request=None):
        return __version__

    @hug.object.get('/sys/health_check', versions=1)
    def get_health_check(self, request=None):
        return True

    @hug.object.get('/sys/is_address/{eth_address}', versions=1)
    def ksh_is_admin(self, eth_address: hug.types.text = None, request=None):

        if not (isinstance(eth_address, str) and len(eth_address) <= 64):
            return self.format_dict_or_list({'success': False, 'msg': 'wrong arguments (type)'})

        return Web3.isAddress(eth_address)

    """
    BENT CONTRACT ENDPOINTS
    """
    @hug.object.get('/bent/contract', versions=1)
    def bent_contract(self, request=None):

        return self.config['ETH-{}'.format(self.env)]['token_contract']

    @hug.object.get('/bent/max_supply', versions=1)
    def bent_max_supply(self, request=None):

        return float(Web3.fromWei(self.token_contract.functions.maxSupply().call(), 'ether'))

    @hug.object.get('/bent/current_supply', versions=1)
    def bent_current_supply(self, request=None):

        return float(Web3.fromWei(self.token_contract.functions.totalSupply().call(), 'ether'))

    @hug.object.get('/bent/circulating_supply', versions=1)
    def bent_circulating_supply(self, request=None):

        supply = float(Web3.fromWei(self.token_contract.functions.totalSupply().call(), 'ether'))

        locked_addresses = json.loads(self.config['ETH-{}'.format(self.env)]["lock_addresses"])

        for locked_address in locked_addresses:
            supply = supply - float(Web3.fromWei(self.token_contract.functions.balanceOf(Web3.toChecksumAddress(locked_address)).call(), 'ether'))

        return supply
