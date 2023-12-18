from copy import deepcopy
from typing import Optional, cast

from pystac import Item
from stactools.core.io import ReadHrefModifier, read_text
from stactools.core.io.xml import XmlElement
from stactools.core.utils.antimeridian import Strategy
from stactools.landsat.mtl_metadata import (
    MtlMetadata,
    _parse_mtl_group,
    _mtl_group_to_element,
    MTLGroup,
)
from stactools.landsat.stac import create_item_from_mtl_metadata


def create_item_from_mtl_text(
    href: str,
    use_usgs_geometry: bool = True,
    antimeridian_strategy: Strategy = Strategy.SPLIT,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> Item:
    base_href = "_".join(href.split("_")[:-1])
    text = read_text(href, read_href_modifier)
    lines = iter(text.split("\n"))
    mtl = _parse_mtl_group(lines)
    root_name, root_group = next(iter(mtl.items()))

    if root_name == "L1_METADATA_FILE":
        root_group.setdefault("PRODUCT_CONTENTS", {})
        root_group.setdefault("LEVEL1_PROCESSING_RECORD", {})
        root_group.setdefault("PROJECTION_ATTRIBUTES", {})
        root_group.setdefault("LEVEL1_PROJECTION_PARAMETERS", {})
        root_group.setdefault("IMAGE_ATTRIBUTES", {})
        root_group.setdefault("PRODUCT_CONTENTS", {})

        root_group["PRODUCT_CONTENTS"]["PROCESSING_LEVEL"] = root_group["PRODUCT_METADATA"]["DATA_TYPE"]
        root_group["PRODUCT_CONTENTS"]["LANDSAT_PRODUCT_ID"] = root_group["METADATA_FILE_INFO"]["LANDSAT_PRODUCT_ID"]
        root_group["LEVEL1_PROCESSING_RECORD"]["LANDSAT_SCENE_ID"] = root_group["METADATA_FILE_INFO"]["LANDSAT_SCENE_ID"]
        root_group["PROJECTION_ATTRIBUTES"]["UTM_ZONE"] = root_group["PROJECTION_PARAMETERS"]["UTM_ZONE"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UL_LON_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UL_LON_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UR_LON_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UR_LON_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LL_LON_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LL_LON_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LR_LON_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LR_LON_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UL_LAT_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UL_LAT_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UR_LAT_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UR_LAT_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LL_LAT_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LL_LAT_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LR_LAT_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LR_LAT_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UL_PROJECTION_X_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UL_PROJECTION_X_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UR_PROJECTION_X_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UR_PROJECTION_X_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LL_PROJECTION_X_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LL_PROJECTION_X_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LR_PROJECTION_X_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LR_PROJECTION_X_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UL_PROJECTION_Y_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UL_PROJECTION_Y_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_UR_PROJECTION_Y_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_UR_PROJECTION_Y_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LL_PROJECTION_Y_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LL_PROJECTION_Y_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["CORNER_LR_PROJECTION_Y_PRODUCT"] = root_group["PRODUCT_METADATA"]["CORNER_LR_PROJECTION_Y_PRODUCT"]
        root_group["PROJECTION_ATTRIBUTES"]["REFLECTIVE_LINES"] = root_group["PRODUCT_METADATA"]["REFLECTIVE_LINES"]
        root_group["PROJECTION_ATTRIBUTES"]["REFLECTIVE_SAMPLES"] = root_group["PRODUCT_METADATA"]["REFLECTIVE_SAMPLES"]
        root_group["PROJECTION_ATTRIBUTES"]["THERMAL_LINES"] = root_group["PRODUCT_METADATA"]["THERMAL_LINES"]
        root_group["PROJECTION_ATTRIBUTES"]["THERMAL_SAMPLES"] = root_group["PRODUCT_METADATA"]["THERMAL_SAMPLES"]
        root_group["LEVEL1_PROJECTION_PARAMETERS"]["GRID_CELL_SIZE_REFLECTIVE"] = root_group["PROJECTION_PARAMETERS"]["GRID_CELL_SIZE_REFLECTIVE"]
        root_group["LEVEL1_PROJECTION_PARAMETERS"]["GRID_CELL_SIZE_THERMAL"] = root_group["PROJECTION_PARAMETERS"]["GRID_CELL_SIZE_THERMAL"]
        root_group["IMAGE_ATTRIBUTES"]["DATE_ACQUIRED"] = root_group["PRODUCT_METADATA"]["DATE_ACQUIRED"]
        root_group["IMAGE_ATTRIBUTES"]["SCENE_CENTER_TIME"] = root_group["PRODUCT_METADATA"]["SCENE_CENTER_TIME"]
        root_group["IMAGE_ATTRIBUTES"]["NADIR_OFFNADIR"] = root_group["PRODUCT_METADATA"]["NADIR_OFFNADIR"]
        root_group["IMAGE_ATTRIBUTES"]["WRS_PATH"] = root_group["PRODUCT_METADATA"]["WRS_PATH"]
        root_group["IMAGE_ATTRIBUTES"]["WRS_ROW"] = root_group["PRODUCT_METADATA"]["WRS_ROW"]
        root_group["PRODUCT_CONTENTS"]["COLLECTION_CATEGORY"] = root_group["PRODUCT_METADATA"]["COLLECTION_CATEGORY"]
        root_group["PRODUCT_CONTENTS"]["COLLECTION_NUMBER"] = root_group["METADATA_FILE_INFO"]["COLLECTION_NUMBER"]
        root_group["LEVEL1_RADIOMETRIC_RESCALING"] = deepcopy(root_group["RADIOMETRIC_RESCALING"])

        root_group["IMAGE_ATTRIBUTES"].setdefault("WRS_TYPE", "")

    mtl_metadata = MtlMetadata(
        XmlElement(_mtl_group_to_element(root_name, cast(MTLGroup, root_group))),
        href=href,
    )

    return create_item_from_mtl_metadata(
        base_href,
        mtl_metadata,
        use_usgs_geometry,
        antimeridian_strategy,
        read_href_modifier=read_href_modifier,
    )

