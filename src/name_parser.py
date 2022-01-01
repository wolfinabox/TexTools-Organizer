from typing import Tuple, Union
import pyparsing as pp


# All images end with one of these characters, respresenting the type of image
IMAGE_TYPES = {
    "d": "albedo",
    "e": "color",
    "n": "normal",
    "o": "occlusion",
    "s": "specular",
}

PART_TYPES = {
    "sho": "feet",
    "dwn": "legs",
    "glv": "gloves",
    "top": "chest",
    "met": "head",
    "b": "body",  # special case
    "t": "tail",  # special case
    "z": "ears",  # special case
    "fac": "face",
    "etc": "faceacc",
    "iri": "iris",
    "hir": "hair",
    "acc": "hairacc",
}

# DOCUMENTATION
# Clothing seems to be "mt_", then the item ID or something, then the descriptor ("top_"), then the "part"? ("a_" or "b_", maybe more?), then the image type

# CLOTHING EXAMPLES
# Head: mt_c0101e0175_met_a_d mt_c0101e5031_met_a_d mt_c0101e0003_met_a_d mt_c0101e0228_met_a_d
# Body: (mt_c0101e0745_top_a_d, mt_c0101e0745_top_b_d) mt_c0101e0463_top_a_d mt_c0101e0006_top_a_d mt_c0101e0172_top_a_d
# Gloves: mt_c0101e0461_glv_a_d mt_c0101e0649_glv_a_d mt_c0101e0747_glv_a_d mt_c0101e0387_glv_a_d
# Legs: mt_c0201e0748_dwn_a_d mt_c0101e0463_dwn_a_d mt_c0101e0042_dwn_a_d mt_c0101e0003_dwn_a_d
# Feet: mt_c0101e0375_sho_a_d mt_c0101e0745_sho_a_d mt_c0101e0005_sho_a_d mt_c0101e0387_sho_a_d

clothing_parser = (
    pp.Literal("mt").suppress()
    + pp.Literal("_").suppress()
    + (
        pp.Word(pp.alphanums, exact=5) + pp.Literal("e") + pp.Word(pp.nums, exact=4)
    ).set_results_name("id")
    + pp.Literal("_").suppress()
    + pp.Word(pp.alphas, exact=3).set_results_name("part_type")
    + pp.Literal("_").suppress()
    + pp.Char(pp.alphas).set_results_name("part_subtype")
    + pp.Literal("_").suppress()
    + pp.Char("denos").set_results_name(
        "image_type"
    )  # "denos" being the 5 ending characters representing image type... for future reference
    + pp.Word(pp.alphas + ".")
)

# CHARACTER EXAMPLES
# Body: mt_c0201b0001_a_d mt_c0201b0001_a_d
# Ears: (inner,outer): (mt_c1801z0001_a_d, mt_c1801z0001_fac_a_d) (mt_c1701z0001_a_d, mt_c1701z0001_fac_a_d)
# ====== Grouped into "face" when exporting ========================================================
# Face: mt_c1301f0001_fac_a_d mt_c0501f0001_fac_a_d mt_c1101f0001_fac_a_d mt_c0801f0003_fac_a_d
# Faceacc: mt_c1301f0001_etc_a_d mt_c0501f0001_etc_a_d mt_c1101f0001_etc_a_d mt_c0801f0003_etc_a_d
# Eye: mt_c1301f0001_etc_b_d mt_c0501f0001_etc_b_d mt_c1101f0001_etc_b_d mt_c0801f0003_etc_b_d
# Iris: mt_c1301f0001_iri_a_d mt_c0501f0001_iri_a_d mt_c1101f0001_iri_a_d mt_c0801f0003_iri_a_d
# =================================================================================================
# Hair: mt_c0201h0157_hir_a_d mt_c1701h0002_hir_a_d mt_c0301h0001_hir_a_d
# Hairacc: mt_c0201h0157_acc_b_d mt_c0301h0001_acc_b_d
# Tail mt_c1401t0001_a_d mt_c1401t0002_a_d mt_c1401t0003_a_d mt_c0801t0001_a_d mt_c0801t0002_a_d
character_parser = (
    pp.Suppress(pp.Literal("mt") + pp.Literal("_"))
    + (
        pp.Word(pp.alphanums, exact=5)
        + pp.Char(pp.alphas).set_results_name("part_group")
        + pp.Word(pp.nums, exact=4)
    ).set_results_name("id")
    + pp.Literal("_").suppress()
    + pp.Optional(
        pp.Word(pp.alphas, exact=3).set_results_name("part_type")
        + pp.Literal("_").suppress()
    )
    + pp.Char(pp.alphas).set_results_name("part_subtype")
    + pp.Literal("_").suppress()
    + pp.Char("denos").set_results_name(
        "image_type"
    )  # "denos" being the 5 ending characters representing image type... for future reference
    + pp.Word(pp.alphas + ".")
)


def parse_filename(file: str) -> Union[Tuple[str, str, str], Tuple[None, None, None]]:
    # try to parse clothing
    part_type, part_subtype, image_type = None, None, None
    try:
        result = clothing_parser.parse_string(file, parse_all=True)
        part_type = PART_TYPES.get(result.get("part_type"))
        part_subtype = result.get("part_subtype")
        image_type = IMAGE_TYPES.get(result.get("image_type"))
    except pp.exceptions.ParseException:
        # otherwise, try to parse character part
        try:
            result = character_parser.parse_string(file, parse_all=True)
            part_type = PART_TYPES.get(
                result.get("part_type", result.get("part_group"))
            )
            part_subtype = str(ord(result.get("part_subtype")) - 96) #'a' to '1', 'b' to '2' etc
            image_type = IMAGE_TYPES.get(result.get("image_type"))
        except pp.exceptions.ParseException:
            # invalid file name
            return None, None, None

    return part_type, part_subtype, image_type
