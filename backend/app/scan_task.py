import json
import logging
import os
import platform
import signal
import time
from pathlib import Path
from subprocess import PIPE, Popen

from app.core import constants, http_util

logger = logging.getLogger("trapper_server")
logger.setLevel(logging.INFO)
IS_WIN = platform.system() == "Windows"


def print_command(request_package, request_id):
    try:
        xsstrike_process = XSStrikeProcess(request_package, request_id)
        _status, command = xsstrike_process.get_command()
        logger.info("!!!!!Command is: {}".format(command))
    except KeyboardInterrupt as e:
        logger.exception("Print error")
    finally:
        logger.info("Trapper printing has completed")


def scan(request_package, request_id):
    logger.info(
        "Trapper scanning has started with request id: {}".format(request_id))
    try:
        xsstrike_process = XSStrikeProcess(request_package, request_id)
        xsstrike_process.engine_start()
        while not xsstrike_process.engine_has_terminated() and xsstrike_process.process is not None:
            logger.info("XSStrike program is running")
            time.sleep(5)
        xsstrike_process.engine_kill()
        logger.warn("XSStrike program has completed")
    except KeyboardInterrupt as e:
        logger.exception("Scan error")
    finally:
        logger.info("Trapper scanning has completed")


class XSStrikeProcess:
    def __init__(self, request_package, request_id):
        self.process = None
        self.request_package = request_package
        self.request_id = request_id

    def parse_header_string(self, header_data):
        if header_data is None:
            return None
        # Create a list to store the key-value pairs
        key_value_pairs = []
        # Iterate over the dictionary items and format them as key-value pairs
        for key, value in header_data.items():
            replaced_value = value.replace('\"', '\'')
            key_value_pairs.append(f"{key}: {replaced_value}")
        # Concatenate the key-value pairs with line breaks
        result = "\n".join(key_value_pairs)
        return result

    def parse_request_package(self):
        url = self.request_package['url'] if "url" in self.request_package else None
        http_method = str(
            self.request_package["method"]) if "method" in self.request_package else None
        header = http_util.header_to_lowercase(json.loads(
            self.request_package["headers"])) if "headers" in self.request_package else None
        data = self.parse_data(self.request_package, header)
        header_string = self.parse_header_string(header)

        return url, http_method, data, header, header_string

    def parse_data(self, request_package, header):
        if "data" not in request_package or request_package["data"] == "":
            return None

        if header and "content-type" in header:
            is_form_data = constants.FORM_DATA_CONTENT_TYPE in header["content-type"]
            is_default_data = constants.DEFAULT_CONTENT_TYPE in header["content-type"]
            is_json_data = constants.JSON_TEXT_CONTENT_TYPE in header["content-type"]

            if is_form_data or is_default_data:
                return http_util.json_to_urlencoded(json.loads(request_package['data']))
            elif is_json_data:
                return request_package["data"].replace('\"', '\'')

        return http_util.json_to_urlencoded(json.loads(request_package['data']))

    def get_command(self):
        """
        Get command based on data, with 3 attempts at timeout reconnection
        :return: 
        """
        command = self.init_command_by_path()
        url, http_method, data, header, header_string = self.parse_request_package()

        if not url or url == "":
            return False, command
        command += ["--url", "{}".format(url)]
        if data and data != "":
            command += ["--data", "\"{}\"".format(data)]
        if header_string and isinstance(header_string, str):
            command += ["--headers", "\"{}\"".format(header_string)]
        command += ["--trapper-celery", "{}".format(self.request_id)]
        return True, command

    def init_command_by_path(self):
        """
        Initialize command by path
        :return: 
        """
        current_root_path = os.path.normpath(
            "{}/../".format(os.path.dirname(os.path.abspath(__file__))))
        xsstrike_script_path = "{}/app/xsstrike-trapper/trapperXsstrike.py".format(
            current_root_path)
        # xsstrike_script_path = Path(__file__).resolve().parent / \
        #     "xsstrike-trapper/xsstrike.py"
        # xsstrike_script_path = "xsstrike-trapper/xsstrike.py"
        command = ["python", xsstrike_script_path]
        return command

    def engine_start(self):
        """Start the command"""
        status, command = self.get_command()
        logger.info("!!!!!Command is: {}".format(command))
        if status:
            self.process = Popen(command, shell=False,
                                 close_fds=not IS_WIN, stdout=PIPE, stderr=PIPE)
            stdout, stderr = self.process.communicate()
            # print the output
            logger.info(f'Subprocess output: {stdout.decode()}')
            # print the error
            logger.info(f'Subprocess error: {stderr.decode()}')

    def engine_stop(self):
        """
        Stop the engine
        :return: 
        """
        if self.process:
            self.process.terminate()
            return self.process.wait()
        else:
            return None

    def engine_process(self):
        return self.process

    def engine_kill(self):
        """
        Forcefully kill and delete XSStrike scan cache records
        :return: 
        """
        if self.process:
            try:
                self.process.kill()
                os.killpg(self._process.pid, signal.SIGTERM)
                return self.process.wait()
            except:
                pass
        return None

    def engine_get_id(self):
        """
        Get the process ID
        :return: 
        """
        if self.process:
            return self.process.pid
        else:
            return None

    def engine_get_returncode(self):
        """
        If None, the command is still running. If 0, it has finished executing and exited.
        :return: 
        """
        if self.process:
            self.process.poll()
            return self.process.returncode
        else:
            return None

    def engine_has_terminated(self):
        return isinstance(self.engine_get_returncode(), int)
