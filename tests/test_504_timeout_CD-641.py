from cda_client.exceptions import ServiceException
from cda_client.rest import RESTResponse
from urllib3 import HTTPResponse
from urllib3._collections import HTTPHeaderDict

from cdapython.exceptions.custom_exception import HTTP_ERROR_API


def test_504_error():
    html = """
        <html>
            <head><title>504 Gateway Time-out</title></head>
            <body>
            <center><h1>504 Gateway Time-out</h1></center>
            <hr><center>nginx</center>
            </body>
        </html>
        """
    headers = HTTPHeaderDict(
        headers={
            "Date": "Wed, 18 Oct 2023 14:22:34 GMT",
            "content-type": "text/html",
            "Content-Length": "160",
            "Connection": "keep-alive",
            "Strict-Transport-Security": "max-age=15724800; includeSubDomains",
        }
    )
    urllib3_http = HTTPResponse(
        status=504, reason="Gateway Time-out", headers=headers, body=html
    )
    http = RESTResponse(urllib3_http)

    service_exception = ServiceException(
        status=504, reason="Gateway Time-out", http_resp=http
    )
    http_error = HTTP_ERROR_API(http_error=service_exception)

    assert http_error.error == "504 Gateway Time-out"
