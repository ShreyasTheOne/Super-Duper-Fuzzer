from random import randrange
from api_interface import api_configuration
from api_interface.request_engine import RequestEngine
from api_interface.constants import DataTypeNotAccepted
from core.sample_fuzzer.data_generators import (
    BoolGenerator,
    IntGenerator,
    StrGenerator,
)


class SampleFuzzer:
    def __init__(self):
        self._API_CONFIGURATION = api_configuration.API_CONFIGURATION.structure
        self._endpoints = self._API_CONFIGURATION["endpoints"]
        self._requestEngines = {}

        # Generate request engines
        for endpointName, endpointDetails in self._endpoints.items():
            self._requestEngines[endpointName] = RequestEngine(endpointName)

        for endpointName, endpointDetails in self._endpoints.items():
            self.fuzz(self._requestEngines[endpointName], endpointName)

    def fuzz(self, requestEngine: RequestEngine, endpointName):
        """
        Fuzz request with endpoint_name
        """
        endpointDetails = self._API_CONFIGURATION["endpoints"][endpointName]
        requestMethod = endpointDetails["method"]
        payloadStructure = endpointDetails["payload"]

        payloadGenerated = self.generatePayload(payloadStructure)

        if requestMethod == "GET":
            # Query params
            requestEngine.send_request(params=payloadGenerated)
        elif requestMethod in ["PUT", "POST", "UPDATE"]:
            requestEngine.send_request(json=payloadGenerated)
        elif requestMethod in ["DELETE", "OPTIONS"]:
            requestEngine.send_request()

    def generatePayload(self, payloadStructure, upperLimitList=5):
        if payloadStructure is None:
            return None
        if payloadStructure["exact"]:
            return payloadStructure["payload"]
        if payloadStructure["data_type"] is None:
            return None
        if payloadStructure["data_type"] == bool:
            return BoolGenerator.generate()
        elif payloadStructure["data_type"] == int:
            return IntGenerator.generate()
        elif payloadStructure["data_type"] == str:
            return StrGenerator.generate()
        elif payloadStructure["data_type"] == list:
            return [
                self.generatePayload(payloadStructure["payload"])
                for _ in range(randrange(upperLimitList))
            ]
        elif payloadStructure["data_type"] == dict:
            payload = {}
            for key, value in payloadStructure["payload"].items():
                payload[key] = self.generatePayload(value)
            return payload
        raise DataTypeNotAccepted(payloadStructure["data_type"])