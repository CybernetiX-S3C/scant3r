from typing import Any, Dict

from core.data import SSTI as SSTI_PAYLOADS
from core.requester import httpSender
from core.utils import insert_to_params_urls
from modules.python.scan import Scan


class Main(Scan):
    def __init__(self, opts: Dict[str, Any], http: httpSender):
        super().__init__(opts, http, "scanning")

    def start(self) -> Dict[str, str]:
        report = {}
        for method in self.opts["methods"]:
            for payload in SSTI_PAYLOADS:
                new_url = insert_to_params_urls(self.opts["url"], payload)
                self.log.debug("SSTI: GENERATE A NEW URL: {new_url}")
                response = self.send_request(method, new_url, self.opts["url"])
                if response.__class__.__name__ == "Response":
                    self.log.debug("SSTI: MATCHING  WITH scan10tr")
                    if "scan10tr" in response.text:
                        self.log.debug(f"SSTI: MATCHED {response.url}")
                        report = {
                            "name": "Server-Side template injection",
                            "url": response.url,
                            "payload": payload,
                            "matching": "scan10tr",
                        }
                        self.show_report(**report)
        return report
