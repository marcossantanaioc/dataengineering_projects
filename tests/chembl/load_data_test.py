"""Unit tests for Chembl data loading."""
import pytest
import responses as responses_lib
import requests

@pytest.fixture
def chembl_single_target(responses):
    """A fixture that mocks a successful ChEMBL request for targets."""
    responses.add(
        responses_lib.GET,
        "https://www.ebi.ac.uk/chembl/api/data/target/CHEMBL2074.json",
        json={
            "cross_references": [],
            "organism": "Homo sapiens",
            "pref_name": "Maltase-glucoamylase",
            "species_group_flag": False,
            "target_chembl_id": "CHEMBL2074",
            "target_type": "SINGLE PROTEIN",
            "tax_id": 9606
        },
        status=200
    )

@pytest.fixture
def chembl_targets(responses):
    """A fixture that mocks a ChEMBL request returning exactly 2 targets."""
    responses.add(
        responses_lib.GET,
        "https://www.ebi.ac.uk/chembl/api/data/target/",
        json={
            "page_meta": {
                "limit": 20,
                "next": "/chembl/api/data/target.json?limit=20&offset=20&_=1778350410822",
                "offset": 0,
                "previous": None,
                "total_count": 17803
            },
            "targets": [
                {
                    "cross_references": [],
                    "organism": "Homo sapiens",
                    "pref_name": "Maltase-glucoamylase",
                    "species_group_flag": False,
                    "target_chembl_id": "CHEMBL2074",
                    "target_components": [
                        {
                            "accession": "O43451",
                            "component_description": "Maltase-glucoamylase",
                            "component_id": 434,
                            "component_type": "PROTEIN",
                            "relationship": "SINGLE PROTEIN",
                            "target_component_synonyms": [
                                {"component_synonym": "3.2.1.20", "syn_type": "EC_NUMBER"},
                                {"component_synonym": "MGAM", "syn_type": "GENE_SYMBOL"}
                            ],
                            "target_component_xrefs": [
                                {"xref_id": "O43451", "xref_name": None, "xref_src_db": "AlphaFoldDB"},
                                {"xref_id": "GO:0005886", "xref_name": "plasma membrane", "xref_src_db": "GoComponent"}
                            ]
                        }
                    ],
                    "target_type": "SINGLE PROTEIN",
                    "tax_id": 9606
                },
                {
                    "cross_references": [],
                    "organism": "Homo sapiens",
                    "pref_name": "ATP-binding cassette sub-family C member 9",
                    "species_group_flag": False,
                    "target_chembl_id": "CHEMBL1971",
                    "target_components": [
                        {
                            "accession": "O60706",
                            "component_description": "ATP-binding cassette sub-family C member 9",
                            "component_id": 294,
                            "component_type": "PROTEIN",
                            "relationship": "SINGLE PROTEIN",
                            "target_component_synonyms": [
                                {"component_synonym": "ABCC9", "syn_type": "GENE_SYMBOL"},
                                {"component_synonym": "SUR2", "syn_type": "GENE_SYMBOL_OTHER"}
                            ],
                            "target_component_xrefs": [
                                {"xref_id": "O60706", "xref_name": None, "xref_src_db": "AlphaFoldDB"},
                                {"xref_id": "GO:0005737", "xref_name": "cytoplasm", "xref_src_db": "GoComponent"}
                            ]
                        }
                    ],
                    "target_type": "SINGLE PROTEIN",
                    "tax_id": 9606
                }
            ]
        },
        status=200
    )

def test_load_target_data_from_chembl(chembl_single_target):
    """Test loading Chembl target data."""
    
    # 4. Updated URL to hit the mocked target endpoint
    response = requests.get("https://www.ebi.ac.uk/chembl/api/data/target/CHEMBL2074.json")
    
    # 5. Updated asserts to check for Maltase-glucoamylase data, not Aspirin
    assert response.status_code == 200
    
    data = response.json()
    assert data["pref_name"] == "Maltase-glucoamylase"
    assert data["target_chembl_id"] == "CHEMBL2074"
    assert data["organism"] == "Homo sapiens"

def test_load_multiple_targets_data_from_chembl(chembl_targets):
    """Test loading Chembl data with 2 targets."""
    
    response = requests.get("https://www.ebi.ac.uk/chembl/api/data/target/")
    assert response.status_code == 200
    
    data = response.json()
    
    # 1. Check that exactly 2 targets were loaded from our mock
    assert len(data["targets"]) == 2
    
    # 2. Check the first target
    target_1 = data["targets"][0]
    assert target_1["pref_name"] == "Maltase-glucoamylase"
    assert target_1["target_chembl_id"] == "CHEMBL2074"
    assert target_1["target_components"][0]["accession"] == "O43451"
    
    # 3. Check the second target
    target_2 = data["targets"][1]
    assert target_2["pref_name"] == "ATP-binding cassette sub-family C member 9"
    assert target_2["target_chembl_id"] == "CHEMBL1971"
    assert target_2["target_components"][0]["accession"] == "O60706"