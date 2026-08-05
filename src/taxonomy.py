import pandas as pd


# ============================================
# Taxonomy Mapping
# ============================================

def create_taxonomy_mapping(taxonomy):

    taxonomy_keep = taxonomy[
        taxonomy["Keep"] == "Yes"
    ]

    mapping = taxonomy_keep.set_index(
        "Category"
    ).to_dict("index")

    return mapping

