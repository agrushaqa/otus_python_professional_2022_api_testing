#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser

from loguru import logger

from src.parse_request import ParseRequest
from src.config.config import Config


def method_handler(request, ctx, store):
    logger.info("start method_handler")
    parser = ParseRequest(request)
    return parser.get()


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    @logger.catch
    def do_POST(self):
        response, code = {}, HTTPStatus.OK
        context = {"request_id": self.get_request_id(self.headers)}
        logger.info("request id:")
        logger.info(context["request_id"])
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            logger.debug("data string:")
            logger.debug(data_string)
            request = json.loads(data_string)
        except Exception:
            code = HTTPStatus.BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logger.info(
                "%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path](
                        {"body": request, "headers": self.headers}, context,
                        self.store)
                except Exception:
                    code = HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in Config().errors:
            r = {"response": response, "code": code}
        else:
            logger.info("response:")
            logger.info(response)
            r = {"error": response or Config().errors.get(code, "Unknown "
                                                                "Error"),
                 "code": code}
        context.update(r)
        logger.info(context)
        logger.info("response:")
        logger.info(r)
        self.wfile.write(bytes(json.dumps(r), "utf8"))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logger.info("Starting server at %s" % opts.port)
    logger.add(opts.log, retention="10 days")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
