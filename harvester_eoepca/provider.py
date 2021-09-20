from urllib.parse import urlparse

from requests import Response
from pystac import Item
import boto3
from pystac.stac_io import DefaultStacIO, StacIO
from stactools.sentinel2.stac import create_item
from harvester.endpoint.OpenSearchEndpoint import SearchPage


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


class CREODIASOpenSearchSentinel2Provider:
    """ Takes the result of a Sentinel-2 OpenSearch search and enriches the
        result to create a full STAC item.
    """
    def parse(self, response: Response):
        StacIO.set_default(CREODIASS3StacIO)
        data = response.json()
        items = [
            self._to_item(feature) for feature in data['features']
        ]
        return SearchPage(
            items,
            data['properties']['startIndex'],
            data['properties']['totalResults'],
        )

    def _to_item(self, feature: dict) -> Item:
        """ Picks the `productIdentifier` property of the response feature
            to generate a valid S3 URL, which is consequently passed to the
            stactools.sentinel2 library to generate a STAC Item.
        """
        path = feature['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        return create_item(path).to_dict(include_self_link=False)
