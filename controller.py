import requests
import psutil
import random
import time


class ClashProxyController:
    def __init__(self, config, logger, timeout=5):
        """
        Initialize the Clash Proxy Controller.

        Args:
            config (Config): Configuration parameters.
            logger (Logger): Logger for logging messages.
            timeout (int, optional): Timeout for making requests. Defaults to 5 seconds.

        Raises:
            Exception: If initialization fails.
        """
        start = False
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(attrs=['pid', 'name'])
            if "clash" in pinfo['name']:
                print("CLash process detected, pid : " + str(pinfo['pid']))
                print("Clash host : " + config.local_host + ", controller_port : " + config.cp)
                start = True
                break
        if start:
            self.control_url = f"http://{config.local_host}:{config.cp}/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9"
            self.logger = logger
            self.params = config
            try:
                res = requests.get(self.control_url, timeout=timeout)
                res.raise_for_status()  # check
            except requests.exceptions.RequestException as e:
                raise Exception(f"Initialization failed. Error: {str(e)}")

            self.proxy_list = []

            for p in list(res.json()['all']):
                self.proxy_list.append(p)

            requests.put(self.control_url, json={'name': self.proxy_list[0]})

            self.current_proxy = 0
        else:
            print("Clash not found. Exit.")
            exit(-1)

    def change_proxy(self, ran=True):
        """
        Change the current proxy.

        Args:
            ran (bool, optional): If True, select a random proxy. Defaults to True.
        """
        dead_proxy, proxy = 0, 0
        while dead_proxy < 12:
            if ran:
                self.current_proxy = random.randint(0, len(self.proxy_list) - 1)
            else:
                self.current_proxy += 1
            proxy = self.current_proxy % len(self.proxy_list)
            if self.check(self.proxy_list[proxy]):
                break
            else:
                dead_proxy += 1
        if dead_proxy >= 12:
            self.logger.info('============================(=^-ω-^=)TOO HOT!============================')
            time.sleep(300)
            self.logger.info('CLASH SLEEP 5 min...')
        requests.put(self.control_url, json={'name': self.proxy_list[proxy]})
        self.logger.info(f"The node has been replaced with [[ {self.proxy_list[proxy][3:]} ]]")

    def check(self, proxyName: str) -> bool:
        """
        Check the availability of a proxy.

        Args:
            proxyName (str): Name of the proxy to check.

        Returns:
            bool: True if the proxy is available, False otherwise.
        """
        payload = {
            "timeout": 2000,  # ms
            "url": "http://vimeo.com"
        }
        check_url = self.control_url.split('proxies/')[0] + 'proxies/' + proxyName + '/delay'
        r = requests.get(check_url, params=payload)
        if list(r.json()).count("delay"):
            self.logger.info("proxy " + proxyName[3:] + " available, delay:" + str(r.json()["delay"]))
            return True
        else:
            self.logger.info("proxy " + proxyName[3:] + " unavailable. Error message: " + r.json()["message"])
            return False

# if __name__ == '__main__':
#     c = ClashProxyController(timeout=5)
#     c.change_proxy()
