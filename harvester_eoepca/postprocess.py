import json
import logging
from os.path import basename, splitext, normpath, join
from urllib.parse import urlparse

import boto3
import botocore
from harvester.abc import Postprocessor
import pystac
from pystac.stac_io import DefaultStacIO, StacIO
from stactools.sentinel1.grd.stac import create_item as sentinel1_grd_create_item
from stactools.sentinel2.stac import create_item as sentinel2_create_item
from stactools.sentinel2.product_metadata import ProductMetadata
from stactools.sentinel2.constants import PRODUCT_METADATA_ASSET_KEY
from stactools.sentinel3.stac import create_item as sentinel3_create_item
from stactools.landsat.stac import create_item as landsat_create_item
from stactools.landsat.stac import (
    create_item_from_mtl_text as landsat_create_item_from_mtl_text
)


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


class CREODIASOpenSearchSentinel1Postprocessor(Postprocessor):
    """ Takes the result of a Sentinel-1 OpenSearch search and enriches the
        result to create a full STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)
        path = item['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        stac_item: pystac.Item = sentinel1_grd_create_item(path)

        out_item = stac_item.to_dict(include_self_link=False)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(json.dumps(out_item, indent=4))

        # Set the collection
        if 'sar:product_type' in out_item['properties']:
            if out_item['properties']['sar:product_type'] == 'GRD':
                out_item["collection"] = 'S1GRD'

        return out_item


class CREODIASOpenSearchSentinel2Postprocessor(Postprocessor):
    """ Takes the result of a Sentinel-2 OpenSearch search and enriches the
        result to create a full STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)
        path = item['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        stac_item: pystac.Item = sentinel2_create_item(path)

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

        # reset the
        out_item["id"] = ProductMetadata(
            out_item["assets"][PRODUCT_METADATA_ASSET_KEY]["href"]
        ).product_id

        # Set the collection
        if 's2:product_type' in out_item['properties']:
            out_item["collection"] = out_item['properties']['s2:product_type']

        return out_item


class CREODIASOpenSearchSentinel3Postprocessor(Postprocessor):
    """ Takes the result of a Sentinel-3 OpenSearch search and enriches the
        result to create a full STAC item.
    """

    def postprocess(self, item: dict) -> dict:
        StacIO.set_default(CREODIASS3StacIO)
        path = item['properties']['productIdentifier']
        path = path.replace('/eodata/', 's3://EODATA/') + '/'
        stac_item: pystac.Item = sentinel3_create_item(path, skip_nc=True)

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

        # Set the collection
        if 's3:productType' in out_item['properties']:
            out_item["collection"] = out_item['properties']['s3:productType']

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
        mtl_xml_file = f"{product_identifier}/{short_product_identifier}_MTL.xml"
        mtl_text_file = f"{product_identifier}/{short_product_identifier}_MTL.txt"

        stac_io = CREODIASS3StacIO()
        stac_item: pystac.Item
        if stac_io.exists(mtl_xml_file):
            stac_item = landsat_create_item(mtl_xml_file)
            LOGGER.debug(f"mtl_xml_file: {mtl_xml_file}")
        elif stac_io.exists(mtl_text_file):
            stac_item = landsat_create_item_from_mtl_text(mtl_text_file)
            LOGGER.debug(f"mtl_text_file: {mtl_text_file}")
        else:
            raise ValueError("Failed to find xml/text metadata file")

        # STAC item
        out_item = stac_item.to_dict(include_self_link=False)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(json.dumps(out_item, indent=4))

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

        # Set the collection
        platform = out_item["properties"]["platform"]
        preocessing_level = out_item["properties"]["landsat:processing_level"]
        if platform == "landsat-8":
            if preocessing_level == "L1TP":
                out_item["collection"] = "L8MSI1TP"
            elif preocessing_level == "L1GT":
                out_item["collection"] = "L8MSI1GT"

        return out_item


class TitlePostprocessor(Postprocessor):
    """ Adds the title property if not already present and sets it to the items
        ID.
    """

    def postprocess(self, item: dict) -> dict:
        properties = item.get("properties", {})
        if "title" not in properties:
            properties["title"] = item["id"]

        return item
