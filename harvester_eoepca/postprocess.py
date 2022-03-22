import json
import logging
from urllib.parse import urlparse

import boto3
from harvester.abc import Postprocessor
from pystac.stac_io import DefaultStacIO, StacIO
from stactools.sentinel2.stac import create_item
from stactools.sentinel2.product_metadata import ProductMetadata
from stactools.sentinel2.constants import PRODUCT_METADATA_ASSET_KEY


LOGGER: logging.Logger = logging.getLogger(__name__)


class CREODIASS3StacIO(DefaultStacIO):
    """ This subclass of the StacIO class interfaces with the
        CREODIAS S3 data interface to access the files stored there.
    """
    def __init__(self):
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id='access',
            aws_secret_access_key='access',
            endpoint_url='http://data.cloudferro.com',
            region_name='RegionOne',
            use_ssl=False,
        )

    def read_text_from_href(self, href: str) -> str:
        parsed = urlparse(href)
        if parsed.scheme == "s3":
            bucket = parsed.netloc
            key = parsed.path[1:]
            obj = self.s3.Object(bucket, key)
            result = obj.get()["Body"].read()
            return result.decode("utf-8")
        else:
            return super().read_text_from_href(href)


class CREODIASOpenSearchSentinel2Postprocessor(Postprocessor):
    """ Takes the result of a Sentinel-2 OpenSearch search and enriches the
        result to create a full STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)
        path = item['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        stac_item = create_item(path).to_dict(include_self_link=False)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(json.dumps(stac_item, indent=4))

        # reset the
        stac_item["id"] = ProductMetadata(
            stac_item["assets"][PRODUCT_METADATA_ASSET_KEY]["href"]
        ).product_id
        return stac_item
