import json
import logging
from os.path import basename, splitext, normpath, join
from urllib.parse import urlparse

import boto3
import botocore
from harvester.abc import Postprocessor
import pystac
from pystac.stac_io import DefaultStacIO, StacIO
from stactools.sentinel2.stac import create_item
from stactools.sentinel2.product_metadata import ProductMetadata
from stactools.sentinel2.constants import PRODUCT_METADATA_ASSET_KEY
from stactools.landsat.stac import create_stac_item


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

    def exists(self, path):
        """ Checks whether the given object exists on the storage
        """
        parsed = urlparse(path)
        try:
            CREODIASS3StacIO().s3.Object(parsed.netloc, parsed.path[1:]).load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise


class CREODIASOpenSearchSentinel2Postprocessor(Postprocessor):
    """ Takes the result of a Sentinel-2 OpenSearch search and enriches the
        result to create a full STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)
        path = item['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        stac_item: pystac.Item = create_item(path)

        # see if we the thumbnail exists, if yes, add it to the STAC Item
        ql_path = join(path, f"{splitext(basename(normpath(path)))[0]}-ql.jpg")
        if CREODIASS3StacIO().exists(ql_path):
            stac_item.add_asset(
                "thumbnail",
                pystac.Asset(
                    ql_path,
                    media_type="image/jpeg",
                    roles=["thumbnail"],
                ),
            )

        out_item = stac_item.to_dict(include_self_link=False)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(json.dumps(out_item, indent=4))

        LOGGER.info("START...")
        LOGGER.info(json.dumps(out_item, indent=4))
        LOGGER.info("...END")

        # reset the
        out_item["id"] = ProductMetadata(
            out_item["assets"][PRODUCT_METADATA_ASSET_KEY]["href"]
        ).product_id
        return out_item


class CREODIASOpenSearchLandsat8Postprocessor(Postprocessor):
    """ Takes the result of a Landsat-8 OpenSearch search and creates from
        it a STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)

        # Product identifier
        product_identifier = item['properties']['productIdentifier'].replace('/eodata/', 's3://EODATA/')
        short_product_identifier = product_identifier[product_identifier.rfind("/")+1:]

        # Landsat MTL metadata file
        mtl_xml_file = product_identifier + '/' + short_product_identifier + '_MTL.xml'
        LOGGER.info(f"mtl_xml_file: {mtl_xml_file}")

        # STAC item
        stac_item: pystac.Item = create_stac_item(mtl_xml_file)
        out_item = stac_item.to_dict(include_self_link=False)

        # Fix-up the STAC role of the asset
        # ref. https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#asset-roles
        assets = out_item["assets"]
        for asset_name in assets:
            asset = assets[asset_name]
            if asset_name == "thumbnail":
                asset["roles"] = ["thumbnail"]
            elif asset_name == "reduced_resolution_browse":
                asset["roles"] = ["overview"]
            elif asset["type"].startswith("image/"):
                asset["roles"] = ["data"]
                asset["href"] = asset["href"].replace("_SR", "")
            else:
                asset["roles"] = ["metadata"]

        LOGGER.info("START...")
        LOGGER.info(json.dumps(out_item, indent=4))
        LOGGER.info("...END")

        return out_item
