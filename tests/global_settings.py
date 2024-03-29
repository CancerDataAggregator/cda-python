from cdapython.constant_variables import Constants

localhost = "http://localhost:8080"
production_host = Constants.cda_api_url
table_dev = "gdc-bq-sample.dev"
table_prod = Constants.default_table
integration_host = "http://35.192.60.10:8080/"
integration_table = "gdc-bq-sample.dev"
dev_host = "https://cancerdata.dsde-dev.broadinstitute.org/"

host = integration_host
project = table_dev
