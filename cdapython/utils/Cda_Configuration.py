from os import path
from ssl import get_default_verify_paths
from typing import Optional

from cda_client.configuration import Configuration

from cdapython.constant_variables import Constants


class CdaConfiguration(Configuration):
    def __init__(
        self,
        host: Optional[str] = None,
        api_key=None,
        api_key_prefix=None,
        access_token=None,
        username=None,
        password=None,
        discard_unknown_keys=False,
        disabled_client_side_validations="",
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
        ssl_ca_cert=None,
        verify: Optional[bool] = None,
        verbose: Optional[bool] = None,
    ):
        self.verify = verify

        if host is None:
            host = Constants.CDA_API_URL

        self.host = host.strip("/")

        if self.verify is None:
            self.verify_ssl = self._find_ssl_path()

        if self.verify is False:
            if verbose:
                self._unverified_http()
            self.verify_ssl = False

        super().__init__(
            host,
            api_key,
            api_key_prefix,
            access_token,
            username,
            password,
            discard_unknown_keys,
            disabled_client_side_validations,
            server_index,
            server_variables,
            server_operation_index,
            server_operation_variables,
            ssl_ca_cert,
        )

    def _find_ssl_path(self) -> bool:
        """[summary]
        This will look in your local computer for a ssl pem file and
        return True or False if the file is there.
        if value is False Q will accept any TLS certificate presented by a server,
        and will ignore hostname mismatches and expired certificates
        Returns:
            bool: [description]
        """
        openssl_cafile: str
        openssl_dir: str
        openssl_dir, openssl_cafile = path.split(
            get_default_verify_paths().openssl_cafile
        )
        check: bool = True

        if not path.exists(openssl_dir):
            check: bool = False

        if openssl_cafile.find("pem") == -1:
            check: bool = False

        return check

    def _unverified_http(self) -> None:
        print(
            f"""[bold yellow]Unverified HTTPS request is being made to host'{Constants.CDA_API_URL}'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings[/bold yellow]"""
        )
