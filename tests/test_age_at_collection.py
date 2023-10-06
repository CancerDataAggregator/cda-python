from unittest import mock

from pandas import DataFrame

from cdapython import Q
from cdapython.results.result import Result
from tests.fake_result import FakeResultData
from tests.patcher import Q_import_path_str

# from tests.global_settings import host, table

result = [
    {
        "id": "093d1bd8-56b2-4dac-a9c3-a476016d8bb7",
        "identifier": [
            {"system": "GDC", "value": "093d1bd8-56b2-4dac-a9c3-a476016d8bb7"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-3U-A98D",
        "researchsubject_id": "c5d4d4b4-2c9e-4865-8860-68327356d461",
    },
    {
        "id": "099fb7bd-9b77-4101-96a2-917ce0a7c52f",
        "identifier": [
            {"system": "GDC", "value": "099fb7bd-9b77-4101-96a2-917ce0a7c52f"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "38d1076c-b832-5c6f-a8e4-561b1f6ac58f",
        "subject_id": "TCGA-UT-A88E",
        "researchsubject_id": "77c64e5d-da34-467a-a8d3-c79060700e4f",
    },
    {
        "id": "174dc55d-2b8d-47e5-8d8a-65f4f71877c7",
        "identifier": [
            {"system": "GDC", "value": "174dc55d-2b8d-47e5-8d8a-65f4f71877c7"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-N5-A4RO",
        "researchsubject_id": "4f4906dc-7ebd-47f1-a8f5-b35d3950e740",
    },
    {
        "id": "179b5e00-22b9-5b66-9702-6eff092d855e",
        "identifier": [
            {"system": "GDC", "value": "179b5e00-22b9-5b66-9702-6eff092d855e"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "f7902358-c99e-4276-b2b9-9891d83d9c87",
        "subject_id": "TCGA-W5-AA2Z",
        "researchsubject_id": "20ec1cd9-7bdb-4eb9-9d20-65795580f1f5",
    },
    {
        "id": "5637bb83-c619-4652-8b71-ae44f2058bd7",
        "identifier": [
            {"system": "GDC", "value": "5637bb83-c619-4652-8b71-ae44f2058bd7"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-VD-A8KK",
        "researchsubject_id": "8e6d3005-445a-4b7f-95ec-a988a121c628",
    },
    {
        "id": "5deabbe3-26e5-4215-b434-2d9d9434666f",
        "identifier": [
            {"system": "GDC", "value": "5deabbe3-26e5-4215-b434-2d9d9434666f"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-TS-A7P7",
        "researchsubject_id": "c9c7366b-8826-4bd2-a3dc-5883e34c1502",
    },
    {
        "id": "66bff15e-a9f7-4dd2-8f5d-0565d3dde1ee",
        "identifier": [
            {"system": "GDC", "value": "66bff15e-a9f7-4dd2-8f5d-0565d3dde1ee"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-3X-AAVA",
        "researchsubject_id": "fe57b639-db7a-460f-adfe-552f1e034e46",
    },
    {
        "id": "7962e9ff-6738-4389-a01a-55b3424085eb",
        "identifier": [
            {"system": "GDC", "value": "7962e9ff-6738-4389-a01a-55b3424085eb"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "9332e4c8-ce71-595c-bc99-b2fcdb41b7a5",
        "subject_id": "TCGA-V4-A9EA",
        "researchsubject_id": "a9fe64a9-6d22-4e9f-96f3-f16af7d298f8",
    },
    {
        "id": "c6ed9122-95c4-49e0-9a6e-6007dc226e60",
        "identifier": [
            {"system": "GDC", "value": "c6ed9122-95c4-49e0-9a6e-6007dc226e60"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "b9187852-b740-58fb-9f13-c5cb72ac9122",
        "subject_id": "TCGA-NA-A4QV",
        "researchsubject_id": "cdde118f-4673-4e7e-b965-1f9fe007050d",
    },
    {
        "id": "da81b06e-63c7-488d-9e9b-8c6fc5bf3f95",
        "identifier": [
            {"system": "GDC", "value": "da81b06e-63c7-488d-9e9b-8c6fc5bf3f95"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-TS-A7OU",
        "researchsubject_id": "880befcf-2bb1-4d37-b65b-5f2970bfb18b",
    },
    {
        "id": "e02b1e5e-fda6-56bd-8b8b-b3234f8741ff",
        "identifier": [
            {"system": "GDC", "value": "e02b1e5e-fda6-56bd-8b8b-b3234f8741ff"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "b0c4f7ae-8bd4-4d0d-b073-bd0fb7d2fdbf",
        "subject_id": "TCGA-NQ-A638",
        "researchsubject_id": "5a197d56-e835-4f96-ad85-04ae9f6aff32",
    },
    {
        "id": "e750bb67-8e8f-4908-a44c-8537097c56d5",
        "identifier": [
            {"system": "GDC", "value": "e750bb67-8e8f-4908-a44c-8537097c56d5"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-FF-8061",
        "researchsubject_id": "c8cde9ea-89e9-4ee8-8a46-417a48f6d3ab",
    },
    {
        "id": "0400595a-fd55-42d1-89f4-09c1f2158aa9",
        "identifier": [
            {"system": "GDC", "value": "0400595a-fd55-42d1-89f4-09c1f2158aa9"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-W5-AA2I",
        "researchsubject_id": "3c8ca064-a4a7-416f-a069-4324d4a72038",
    },
    {
        "id": "05ab05c4-3e2a-488e-b82a-6a0b225202c6",
        "identifier": [
            {"system": "GDC", "value": "05ab05c4-3e2a-488e-b82a-6a0b225202c6"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "f9cb3449-102b-5e0b-873a-296aa3265757",
        "subject_id": "TCGA-W5-AA2R",
        "researchsubject_id": "20bf79af-3b0f-477d-b619-5597d42f5d5e",
    },
    {
        "id": "0e4cbb19-9737-57a4-87cc-478513725f46",
        "identifier": [
            {"system": "GDC", "value": "0e4cbb19-9737-57a4-87cc-478513725f46"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "85179f76-e88a-416e-a5f9-51cd2d589563",
        "subject_id": "TCGA-MQ-A6BQ",
        "researchsubject_id": "d3a6accc-5c45-4e70-baf5-2188af53e0db",
    },
    {
        "id": "51c6ed77-f3b7-11e8-a44b-0a9c39d33490",
        "identifier": [
            {"system": "PDC", "value": "51c6ed77-f3b7-11e8-a44b-0a9c39d33490"}
        ],
        "associated_project": "PJ25730263",
        "days_to_collection": 0,
        "primary_disease_type": "Chromophobe Renal Cell Carcinoma",
        "anatomical_site": "Kidney",
        "source_material_type": "Normal",
        "specimen_type": "aliquot",
        "derived_from_specimen": "c2ab1d90-f3b3-11e8-a44b-0a9c39d33490",
        "subject_id": "CA25730263-5",
        "researchsubject_id": "bdc07b2c-f3a7-11e8-a44b-0a9c39d33490",
    },
    {
        "id": "705fb351-a316-4bf9-ad49-0a5a36fa4aa8",
        "identifier": [
            {"system": "GDC", "value": "705fb351-a316-4bf9-ad49-0a5a36fa4aa8"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-VD-A8KJ",
        "researchsubject_id": "7289bc25-2551-4c6d-b2fa-c7e13859b9b3",
    },
    {
        "id": "7d74f26c-af76-4030-bc2c-6c20aa367a9d",
        "identifier": [
            {"system": "GDC", "value": "7d74f26c-af76-4030-bc2c-6c20aa367a9d"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "e02b1e5e-fda6-56bd-8b8b-b3234f8741ff",
        "subject_id": "TCGA-NQ-A638",
        "researchsubject_id": "5a197d56-e835-4f96-ad85-04ae9f6aff32",
    },
    {
        "id": "8941ded5-3f5c-540e-bb60-62377329c468",
        "identifier": [
            {"system": "GDC", "value": "8941ded5-3f5c-540e-bb60-62377329c468"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "c8a0e3bb-c68d-45b1-95ef-d7a91c5598c6",
        "subject_id": "TCGA-N8-A4PI",
        "researchsubject_id": "8c8d4495-1a1d-4942-b0f0-1445fd05dfce",
    },
    {
        "id": "899d669a-30d7-53dd-808d-eaffdcbc0ad3",
        "identifier": [
            {"system": "GDC", "value": "899d669a-30d7-53dd-808d-eaffdcbc0ad3"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "2fd7d6d4-4a06-460a-80c5-8cb341624b0d",
        "subject_id": "TCGA-V4-A9EZ",
        "researchsubject_id": "39e494bc-7710-4f9f-98b0-0f509f7aef1a",
    },
    {
        "id": "90c14622-9db9-40c5-abda-f145d4dac8b0",
        "identifier": [
            {"system": "GDC", "value": "90c14622-9db9-40c5-abda-f145d4dac8b0"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "db11e487-0c39-5faf-b9f7-9242fff65b61",
        "subject_id": "TCGA-V4-A9F1",
        "researchsubject_id": "94f3d9b0-0ee4-4f6a-a8ff-ce7a4d8fab76",
    },
    {
        "id": "91577f7d-b7c1-47c8-84ed-f01924e1ab9e",
        "identifier": [
            {"system": "GDC", "value": "91577f7d-b7c1-47c8-84ed-f01924e1ab9e"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "e3d6f821-da73-5c45-8bb3-820448593159",
        "subject_id": "TCGA-QM-A5NM",
        "researchsubject_id": "485b221f-f40f-46a0-a9cf-023f807e6146",
    },
    {
        "id": "9d7189eb-e34b-546b-b0ee-20be03534e4e",
        "identifier": [
            {"system": "GDC", "value": "9d7189eb-e34b-546b-b0ee-20be03534e4e"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "924d5195-e53c-48d9-b971-c1f1863f4a70",
        "subject_id": "TCGA-WC-A880",
        "researchsubject_id": "d8e15178-d8c5-4e4e-895c-57ffe5bc80c2",
    },
    {
        "id": "a41f6020-0288-4077-a3c6-dbeb9bbd17a4",
        "identifier": [
            {"system": "GDC", "value": "a41f6020-0288-4077-a3c6-dbeb9bbd17a4"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "0211cbd0-d541-5a62-b9bb-2bc30ddd5547",
        "subject_id": "TCGA-GR-7351",
        "researchsubject_id": "7a589441-11ef-4158-87e7-3951d86bc2aa",
    },
    {
        "id": "ae54a3b1-9b99-4670-8e5a-eaf70b7fab6c",
        "identifier": [
            {"system": "GDC", "value": "ae54a3b1-9b99-4670-8e5a-eaf70b7fab6c"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "85a48253-1ec8-5249-9bfc-52e3a0158a6c",
        "subject_id": "TCGA-UD-AAC7",
        "researchsubject_id": "0ac27bc8-346e-4006-a701-d9676fb91cb7",
    },
    {
        "id": "b8374753-5a7e-5201-aed6-b5cf24667329",
        "identifier": [
            {"system": "GDC", "value": "b8374753-5a7e-5201-aed6-b5cf24667329"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "fe0115fe-0489-4fbd-a009-a850c944f0b6",
        "subject_id": "TCGA-VD-A8KA",
        "researchsubject_id": "af04ca52-8b71-497e-8135-6ddfca9ab221",
    },
    {
        "id": "e4fce342-b5cb-4bd7-b73d-6d9e0772e982",
        "identifier": [
            {"system": "GDC", "value": "e4fce342-b5cb-4bd7-b73d-6d9e0772e982"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "7cd49cfc-123c-5378-a311-169dd5cd6e19",
        "subject_id": "TCGA-N6-A4VE",
        "researchsubject_id": "4f0124a6-4a5b-4e42-b9ff-d7de51d2148c",
    },
    {
        "id": "0e5b0458-32bc-5714-a6ea-914059b39c10",
        "identifier": [
            {"system": "GDC", "value": "0e5b0458-32bc-5714-a6ea-914059b39c10"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "3e24a631-82cf-4bd8-a8d1-95332b784707",
        "subject_id": "TCGA-V4-A9ES",
        "researchsubject_id": "c510a423-6ab1-431e-9248-d2ac91fdedba",
    },
    {
        "id": "3b0becd5-e452-47ba-969e-a0864cf06d69",
        "identifier": [
            {"system": "GDC", "value": "3b0becd5-e452-47ba-969e-a0864cf06d69"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "b41a87f9-ac08-563e-b673-3552f3db3467",
        "subject_id": "TCGA-N6-A4V9",
        "researchsubject_id": "75a43851-8fa0-4259-b843-88dc6fbce270",
    },
    {
        "id": "445e09ef-dae4-4f0f-a8bc-ba06580cd04c",
        "identifier": [
            {"system": "GDC", "value": "445e09ef-dae4-4f0f-a8bc-ba06580cd04c"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "cfd3f333-c41e-5fc4-91ca-ae477f5af4bb",
        "subject_id": "TCGA-3X-AAV9",
        "researchsubject_id": "41b97b11-acaa-4fbc-b3b0-0abc1bcac13b",
    },
    {
        "id": "6945a38e-86be-42b5-a819-4027263267a9",
        "identifier": [
            {"system": "GDC", "value": "6945a38e-86be-42b5-a819-4027263267a9"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-G8-6906",
        "researchsubject_id": "3f5a897d-1eaa-4d4c-8324-27ac07c90927",
    },
    {
        "id": "6b4dd908-74fe-4704-b0f9-b01d6e465416",
        "identifier": [
            {"system": "GDC", "value": "6b4dd908-74fe-4704-b0f9-b01d6e465416"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "4a2fb34c-525f-54b3-951e-1a15528feaba",
        "subject_id": "TCGA-TS-A7P6",
        "researchsubject_id": "74f63637-cc7c-4539-a57e-783c8f62fb95",
    },
    {
        "id": "7578f5fb-be2d-463b-80e6-7c2eba7d6871",
        "identifier": [
            {"system": "GDC", "value": "7578f5fb-be2d-463b-80e6-7c2eba7d6871"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "3634b7b5-bdfd-58c5-9316-3521c4519e48",
        "subject_id": "TCGA-V4-A9EJ",
        "researchsubject_id": "d9ccba9b-6bf0-44d9-8097-a97ab747f0bd",
    },
    {
        "id": "7916f287-1847-5919-9100-cbacf48b26ff",
        "identifier": [
            {"system": "GDC", "value": "7916f287-1847-5919-9100-cbacf48b26ff"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "3affcaf3-c3f0-494b-8d7c-6f557c9268c4",
        "subject_id": "TCGA-3H-AB3S",
        "researchsubject_id": "1c848577-c3a4-4830-abfa-549992172396",
    },
    {
        "id": "be245e88-4fb3-5f4e-b623-983d13fa0835",
        "identifier": [
            {"system": "GDC", "value": "be245e88-4fb3-5f4e-b623-983d13fa0835"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "2f9ec645-f158-4d59-a094-b0229bca8cda",
        "subject_id": "TCGA-LK-A4O5",
        "researchsubject_id": "9ad7575d-2ad4-4fda-8176-55145396f04a",
    },
    {
        "id": "c7a99bd8-f3b3-11e8-a44b-0a9c39d33490",
        "identifier": [
            {"system": "PDC", "value": "c7a99bd8-f3b3-11e8-a44b-0a9c39d33490"}
        ],
        "associated_project": "PJ25730263",
        "days_to_collection": 0,
        "primary_disease_type": "Clear Cell Renal Cell Carcinoma",
        "anatomical_site": "Kidney",
        "source_material_type": "Normal",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "CA25730263-6",
        "researchsubject_id": "bf5e9985-f3a7-11e8-a44b-0a9c39d33490",
    },
    {
        "id": "f14916d4-d46f-485c-8788-f733cbcabb3f",
        "identifier": [
            {"system": "GDC", "value": "f14916d4-d46f-485c-8788-f733cbcabb3f"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "709fdb7f-017b-57f6-a5a4-9395f3e484e1",
        "subject_id": "TCGA-N5-A59F",
        "researchsubject_id": "158fd4c2-68dc-4ca4-8130-d5589c80d825",
    },
    {
        "id": "04ec6a09-9745-457f-9838-5bb9ac128e2b",
        "identifier": [
            {"system": "GDC", "value": "04ec6a09-9745-457f-9838-5bb9ac128e2b"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "ea16d28f-68d1-5577-8678-132e8c7e8ec5",
        "subject_id": "TCGA-YS-A95C",
        "researchsubject_id": "ca9031aa-87e5-4d5b-a526-3615efac3077",
    },
    {
        "id": "0f22f03d-6e84-486f-930f-33387f8d1191",
        "identifier": [
            {"system": "GDC", "value": "0f22f03d-6e84-486f-930f-33387f8d1191"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "c134757a-2247-5ddf-9f16-0a06b94e406c",
        "subject_id": "TCGA-FF-8062",
        "researchsubject_id": "0e9fcccc-0630-408d-a121-2c6413824cb7",
    },
    {
        "id": "198ede78-c8b9-4b97-8953-8353d185cb4f",
        "identifier": [
            {"system": "GDC", "value": "198ede78-c8b9-4b97-8953-8353d185cb4f"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "baccfb6d-8635-5105-a8ef-f76078fd57e5",
        "subject_id": "TCGA-VD-A8KH",
        "researchsubject_id": "39af6e0f-908c-4b2b-97b8-a4d1966e47e1",
    },
    {
        "id": "1ca4a177-b74b-4473-8108-1321149111d5",
        "identifier": [
            {"system": "GDC", "value": "1ca4a177-b74b-4473-8108-1321149111d5"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-FA-A6HO",
        "researchsubject_id": "69f23725-adca-48ac-9b33-80a7aae24cfe",
    },
    {
        "id": "386427c9-9d6b-4919-bb97-3f14a0fc32a2",
        "identifier": [
            {"system": "GDC", "value": "386427c9-9d6b-4919-bb97-3f14a0fc32a2"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-UD-AABZ",
        "researchsubject_id": "97408569-ef36-46d6-941a-aca9e0ab297e",
    },
    {
        "id": "3900eb03-d09e-45b7-8de3-5d68797bc74e",
        "identifier": [
            {"system": "GDC", "value": "3900eb03-d09e-45b7-8de3-5d68797bc74e"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "4ddae085-6c77-52db-8f16-6825aec5a6fd",
        "subject_id": "TCGA-N5-A4RO",
        "researchsubject_id": "4f4906dc-7ebd-47f1-a8f5-b35d3950e740",
    },
    {
        "id": "3b09723f-b1c0-4ad8-9730-78924f9477a1",
        "identifier": [
            {"system": "GDC", "value": "3b09723f-b1c0-4ad8-9730-78924f9477a1"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-UT-A88C",
        "researchsubject_id": "b1f27fa2-133c-42c0-b69e-815af67e2a7e",
    },
    {
        "id": "4bc6f9d0-f3b7-11e8-a44b-0a9c39d33490",
        "identifier": [
            {"system": "PDC", "value": "4bc6f9d0-f3b7-11e8-a44b-0a9c39d33490"}
        ],
        "associated_project": "PJ25730263",
        "days_to_collection": 0,
        "primary_disease_type": "Clear Cell Renal Cell Carcinoma",
        "anatomical_site": "Kidney",
        "source_material_type": "Normal",
        "specimen_type": "aliquot",
        "derived_from_specimen": "b906b0bc-f3b3-11e8-a44b-0a9c39d33490",
        "subject_id": "CA25730263-3",
        "researchsubject_id": "baa9907d-f3a7-11e8-a44b-0a9c39d33490",
    },
    {
        "id": "5941da1b-5752-4cd9-bb93-8c0049e56907",
        "identifier": [
            {"system": "GDC", "value": "5941da1b-5752-4cd9-bb93-8c0049e56907"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-ZH-A8Y6",
        "researchsubject_id": "5166d82f-7b22-4101-bea9-6056e5a74c48",
    },
    {
        "id": "85a48253-1ec8-5249-9bfc-52e3a0158a6c",
        "identifier": [
            {"system": "GDC", "value": "85a48253-1ec8-5249-9bfc-52e3a0158a6c"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "60d9c4b3-bb9a-4999-acbc-4e4ea2d94a2a",
        "subject_id": "TCGA-UD-AAC7",
        "researchsubject_id": "0ac27bc8-346e-4006-a701-d9676fb91cb7",
    },
    {
        "id": "9e23dc1f-79b3-4106-9921-9e6b14a1240c",
        "identifier": [
            {"system": "GDC", "value": "9e23dc1f-79b3-4106-9921-9e6b14a1240c"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-VB-A8QN",
        "researchsubject_id": "a6923479-4e68-4ea8-87ed-e9642b9d43d5",
    },
    {
        "id": "d1f86158-1f77-52f3-9386-84e8fe27fe1f",
        "identifier": [
            {"system": "GDC", "value": "d1f86158-1f77-52f3-9386-84e8fe27fe1f"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "cb3f6d59-4f03-44f1-af48-8d9a9c8852e8",
        "subject_id": "TCGA-TS-A7P8",
        "researchsubject_id": "92c1f122-2f48-47a7-b3b8-c1792a1f4f32",
    },
    {
        "id": "e5c6583d-5e30-4f1f-8579-830b65341f15",
        "identifier": [
            {"system": "GDC", "value": "e5c6583d-5e30-4f1f-8579-830b65341f15"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "8aa07e59-eda2-59f3-a779-f0cc80c6bdb3",
        "subject_id": "TCGA-SC-A6LP",
        "researchsubject_id": "dc6720dd-5028-49d3-8508-a7936e7b3faa",
    },
    {
        "id": "0b9de402-ab8c-474c-bb86-b4df06747548",
        "identifier": [
            {"system": "GDC", "value": "0b9de402-ab8c-474c-bb86-b4df06747548"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-VD-A8KN",
        "researchsubject_id": "b26cb5f2-4ff0-4476-8d02-7256ace7d8a3",
    },
    {
        "id": "43f2a5fb-f07a-4a1f-96f7-d7010f6aa520",
        "identifier": [
            {"system": "GDC", "value": "43f2a5fb-f07a-4a1f-96f7-d7010f6aa520"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-G8-6907",
        "researchsubject_id": "31bbad4e-3789-42ec-9faa-1cb86970f723",
    },
    {
        "id": "4c9771c0-6633-4750-9213-98991f44b175",
        "identifier": [
            {"system": "GDC", "value": "4c9771c0-6633-4750-9213-98991f44b175"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "a46db0cc-6128-5ba0-abf9-93eb4b0af585",
        "subject_id": "TCGA-FF-8047",
        "researchsubject_id": "f978cb0f-d319-4c01-b4c5-23ae1403a106",
    },
    {
        "id": "a5145ae3-55e7-5f85-8ccc-0d75c853a9d0",
        "identifier": [
            {"system": "GDC", "value": "a5145ae3-55e7-5f85-8ccc-0d75c853a9d0"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "a939be8d-5de4-45ef-ba45-cdbc498720c6",
        "subject_id": "TCGA-RZ-AB0B",
        "researchsubject_id": "2bf47a88-df0a-4102-af2e-998c3d252b9c",
    },
    {
        "id": "a9f85697-ede4-522a-8aa5-db34b1f471a0",
        "identifier": [
            {"system": "GDC", "value": "a9f85697-ede4-522a-8aa5-db34b1f471a0"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "561c17e5-6e23-4dda-b4f3-9dccb27fd4ef",
        "subject_id": "TCGA-W5-AA31",
        "researchsubject_id": "2d6e20b2-82c7-4c12-92d0-93282b0a9031",
    },
    {
        "id": "c2002a2a-35a9-4e94-a378-516a9fd154df",
        "identifier": [
            {"system": "GDC", "value": "c2002a2a-35a9-4e94-a378-516a9fd154df"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-3H-AB3M",
        "researchsubject_id": "ebe927e6-0a7e-4c97-ad73-f3c302cca7bc",
    },
    {
        "id": "c261a1e7-a6fa-5b81-82aa-b33f7f77b868",
        "identifier": [
            {"system": "GDC", "value": "c261a1e7-a6fa-5b81-82aa-b33f7f77b868"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "f19c7920-20a8-4f52-b299-636363d12709",
        "subject_id": "TCGA-4G-AAZT",
        "researchsubject_id": "b10c64c2-7fd2-4210-b975-034affb14b57",
    },
    {
        "id": "c9315478-c4de-45a7-8efc-395b20001382",
        "identifier": [
            {"system": "GDC", "value": "c9315478-c4de-45a7-8efc-395b20001382"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "f5cc3073-f524-5542-9e21-5ef069fbe7eb",
        "subject_id": "TCGA-V4-A9EO",
        "researchsubject_id": "bcb87378-9f43-45e4-bdf2-f6dfa6ac5b8c",
    },
    {
        "id": "fe13e029-f2d0-5393-9519-4393dcefb9d3",
        "identifier": [
            {"system": "GDC", "value": "fe13e029-f2d0-5393-9519-4393dcefb9d3"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "6585428e-f319-4931-92bb-58f4926a62f8",
        "subject_id": "TCGA-YZ-A982",
        "researchsubject_id": "cba920f4-c57f-47bc-958d-9b7872df01c8",
    },
    {
        "id": "14b7f6bf-db60-5eb4-9bbb-30dee88aa078",
        "identifier": [
            {"system": "GDC", "value": "14b7f6bf-db60-5eb4-9bbb-30dee88aa078"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "c66d8642-d402-430b-9d4c-9268e192d55a",
        "subject_id": "TCGA-3H-AB3U",
        "researchsubject_id": "c328f661-c109-4e01-b819-299a75bd4348",
    },
    {
        "id": "219266d5-fc4a-4652-90fa-f831ca0cb55b",
        "identifier": [
            {"system": "GDC", "value": "219266d5-fc4a-4652-90fa-f831ca0cb55b"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-3X-AAVC",
        "researchsubject_id": "ff4131c9-537c-46cc-b495-9af60d431f5e",
    },
    {
        "id": "2b7492b8-3e5f-4001-ab11-a44fb377f7a0",
        "identifier": [
            {"system": "GDC", "value": "2b7492b8-3e5f-4001-ab11-a44fb377f7a0"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "1b8b5ff2-3e51-5acc-8e15-a6a26604d36a",
        "subject_id": "TCGA-V4-A9F3",
        "researchsubject_id": "e21d8018-8fe9-4c92-8b36-28d7d3f7df2b",
    },
    {
        "id": "2e4726a6-25c8-452e-9317-bf9952da1e02",
        "identifier": [
            {"system": "GDC", "value": "2e4726a6-25c8-452e-9317-bf9952da1e02"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "6649a2df-a5b0-58a4-9740-d0a267bdd0da",
        "subject_id": "TCGA-NF-A4WX",
        "researchsubject_id": "64d00705-5070-4338-9433-ba74424528b3",
    },
    {
        "id": "339749f2-52fa-58d7-94a0-4f928aa3213d",
        "identifier": [
            {"system": "GDC", "value": "339749f2-52fa-58d7-94a0-4f928aa3213d"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "be3a399f-10c9-44bc-8204-e6d025179cc6",
        "subject_id": "TCGA-FF-8042",
        "researchsubject_id": "f0a326d2-1f3e-4a5d-bca8-32aaccc52338",
    },
    {
        "id": "578fd2fe-8d2c-44e8-99e0-43dfb26e9082",
        "identifier": [
            {"system": "GDC", "value": "578fd2fe-8d2c-44e8-99e0-43dfb26e9082"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-N5-A4RN",
        "researchsubject_id": "1d2937e8-6104-4330-b7dc-7bcd79dac927",
    },
    {
        "id": "5c89811b-9851-41e7-a0c2-a0e5e3090a54",
        "identifier": [
            {"system": "GDC", "value": "5c89811b-9851-41e7-a0c2-a0e5e3090a54"}
        ],
        "associated_project": "CPTAC-3",
        "days_to_collection": 1,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "aliquot",
        "derived_from_specimen": "8f284629-9df1-542e-b26c-636c6648368b",
        "subject_id": "C3L-00001",
        "researchsubject_id": "13310f38-a002-437e-8de2-332b0b10d0c0",
    },
    {
        "id": "69c5c759-5921-4db3-9922-463c227ba630",
        "identifier": [
            {"system": "GDC", "value": "69c5c759-5921-4db3-9922-463c227ba630"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "8eeba3b5-aaa2-557f-bc0f-1f2bab578dd6",
        "subject_id": "TCGA-UT-A88C",
        "researchsubject_id": "b1f27fa2-133c-42c0-b69e-815af67e2a7e",
    },
    {
        "id": "7057906c-860f-4b36-b27d-cf9fe4e9b72e",
        "identifier": [
            {"system": "GDC", "value": "7057906c-860f-4b36-b27d-cf9fe4e9b72e"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "fdf30c4c-0258-5a93-8bb8-af6ec51d9498",
        "subject_id": "TCGA-N8-A4PQ",
        "researchsubject_id": "51f6692d-a05b-474b-ba99-637c8bc49b30",
    },
    {
        "id": "85ee6197-f39b-504c-bfc9-82ba97e0dd83",
        "identifier": [
            {"system": "GDC", "value": "85ee6197-f39b-504c-bfc9-82ba97e0dd83"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "f7d6c999-1da6-4eca-82cb-f9507173f7c5",
        "subject_id": "TCGA-W5-AA36",
        "researchsubject_id": "f2d42e03-ca8d-4b57-ae39-0cc8f37b1b67",
    },
    {
        "id": "a2d32037-8c33-5f5b-807c-8707d3b3e6dd",
        "identifier": [
            {"system": "GDC", "value": "a2d32037-8c33-5f5b-807c-8707d3b3e6dd"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "e06abef6-e028-4a90-a814-4ee8e4780c39",
        "subject_id": "TCGA-N7-A4Y5",
        "researchsubject_id": "245e4254-dbc1-45bd-b5df-504d8c3822de",
    },
    {
        "id": "a63004e2-b18d-565b-986f-1005174aeb39",
        "identifier": [
            {"system": "GDC", "value": "a63004e2-b18d-565b-986f-1005174aeb39"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "08075e77-066c-4451-98e8-533251de4b5d",
        "subject_id": "TCGA-N8-A4PN",
        "researchsubject_id": "8b7c42cd-fc2a-4023-843e-a411821f94ff",
    },
    {
        "id": "ad9501f0-b1f5-5198-a79b-41fb11a57eac",
        "identifier": [
            {"system": "GDC", "value": "ad9501f0-b1f5-5198-a79b-41fb11a57eac"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "46b90d0c-3b18-4890-99f0-eacb15c9f7d9",
        "subject_id": "TCGA-LK-A4O7",
        "researchsubject_id": "e4469259-2504-4987-88a4-02cae33f46f2",
    },
    {
        "id": "b340ab01-48a4-4dd3-9f47-78a6dc8b623b",
        "identifier": [
            {"system": "GDC", "value": "b340ab01-48a4-4dd3-9f47-78a6dc8b623b"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-N5-A4RA",
        "researchsubject_id": "2aa77a19-efde-478a-a113-c0af75708b31",
    },
    {
        "id": "bf5e2e03-51ec-4384-b18e-f3aa7aeefbba",
        "identifier": [
            {"system": "GDC", "value": "bf5e2e03-51ec-4384-b18e-f3aa7aeefbba"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "bba279a7-98d8-5ce4-8b93-3be0ac747fd4",
        "subject_id": "TCGA-G8-6325",
        "researchsubject_id": "ea54dbad-1b23-41cc-9378-d4002a8fca51",
    },
    {
        "id": "cc15090f-de9f-51bb-bb25-3fac35a2f50b",
        "identifier": [
            {"system": "GDC", "value": "cc15090f-de9f-51bb-bb25-3fac35a2f50b"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "c3c968b8-cb14-4e06-befc-2222d6b89bb7",
        "subject_id": "TCGA-V4-A9EY",
        "researchsubject_id": "15d19ccc-52b8-41f6-b1c1-2cc55691aed5",
    },
    {
        "id": "e9310374-101c-5052-b7fe-6b39cbd1df3f",
        "identifier": [
            {"system": "GDC", "value": "e9310374-101c-5052-b7fe-6b39cbd1df3f"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "a3c4b16b-600d-4e63-a308-02524370b88b",
        "subject_id": "TCGA-V4-A9EI",
        "researchsubject_id": "b533e555-90cf-4657-80c6-15b67da8ad26",
    },
    {
        "id": "ecbb48af-5558-45e5-af60-f7e131b7c136",
        "identifier": [
            {"system": "GDC", "value": "ecbb48af-5558-45e5-af60-f7e131b7c136"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-V4-A9EX",
        "researchsubject_id": "892e7630-b11e-47bd-987c-327d33258e11",
    },
    {
        "id": "f69c9efc-2ac8-4799-80c8-c8ea7a187a29",
        "identifier": [
            {"system": "GDC", "value": "f69c9efc-2ac8-4799-80c8-c8ea7a187a29"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-NF-A4WX",
        "researchsubject_id": "64d00705-5070-4338-9433-ba74424528b3",
    },
    {
        "id": "17d5cdf3-823e-4246-ad3b-22ae1871072a",
        "identifier": [
            {"system": "GDC", "value": "17d5cdf3-823e-4246-ad3b-22ae1871072a"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-GR-A4D6",
        "researchsubject_id": "c1c06604-5ae2-4a53-b9c0-eb210d38e3f0",
    },
    {
        "id": "42206439-b0a5-5b23-8171-5df555cb5c2b",
        "identifier": [
            {"system": "GDC", "value": "42206439-b0a5-5b23-8171-5df555cb5c2b"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "578fd2fe-8d2c-44e8-99e0-43dfb26e9082",
        "subject_id": "TCGA-N5-A4RN",
        "researchsubject_id": "1d2937e8-6104-4330-b7dc-7bcd79dac927",
    },
    {
        "id": "844321d7-8bd0-43bd-a82b-a76c820a243e",
        "identifier": [
            {"system": "GDC", "value": "844321d7-8bd0-43bd-a82b-a76c820a243e"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "0c17eed6-318a-5d24-be77-8bc02f336219",
        "subject_id": "TCGA-GS-A9TT",
        "researchsubject_id": "33365d22-cb83-4d8e-a2d1-06b675f75f6e",
    },
    {
        "id": "8fa7ff5d-413a-40e3-acc9-4282119e9c29",
        "identifier": [
            {"system": "GDC", "value": "8fa7ff5d-413a-40e3-acc9-4282119e9c29"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "a884cdb4-4592-55bc-9d21-66ef15d3a51f",
        "subject_id": "TCGA-W5-AA33",
        "researchsubject_id": "5fb3affa-3661-48e8-a1cc-b533c862e8c5",
    },
    {
        "id": "a6ca56f6-ea14-58a7-8eec-2e63943de3dd",
        "identifier": [
            {"system": "GDC", "value": "a6ca56f6-ea14-58a7-8eec-2e63943de3dd"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "cec34d49-4caf-4cad-846a-80d19be9d732",
        "subject_id": "TCGA-NA-A4R1",
        "researchsubject_id": "98315e03-ffe8-449c-8f92-7fd2c0f20b79",
    },
    {
        "id": "a7778b54-2664-45ec-a754-ed2cac544116",
        "identifier": [
            {"system": "GDC", "value": "a7778b54-2664-45ec-a754-ed2cac544116"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-UT-A97Y",
        "researchsubject_id": "c9ce1f62-2df1-4974-868b-d075781ce282",
    },
    {
        "id": "bca86e17-388c-4826-a269-0f3785dda81d",
        "identifier": [
            {"system": "GDC", "value": "bca86e17-388c-4826-a269-0f3785dda81d"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-TS-A7P1",
        "researchsubject_id": "554f4424-bb94-4958-a316-6d7d4eb4181b",
    },
    {
        "id": "e10f831f-7c8f-5e9e-8088-f477e0cd1b23",
        "identifier": [
            {"system": "GDC", "value": "e10f831f-7c8f-5e9e-8088-f477e0cd1b23"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "f18df67e-7fc2-45b7-a98a-d09551ab9481",
        "subject_id": "TCGA-V4-A9EH",
        "researchsubject_id": "5e54122f-1c4d-45cc-8842-cd1c1df0eed8",
    },
    {
        "id": "ef257a6b-5a93-54c8-865d-3b39b5af6a3a",
        "identifier": [
            {"system": "GDC", "value": "ef257a6b-5a93-54c8-865d-3b39b5af6a3a"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "cc78b3b8-ecf5-47ae-9576-1cd229b7e54e",
        "subject_id": "TCGA-N8-A4PO",
        "researchsubject_id": "2aad74b4-8d66-4563-8958-88d83f86556d",
    },
    {
        "id": "fdd6404f-7f19-596b-b1dd-0db0752030a9",
        "identifier": [
            {"system": "GDC", "value": "fdd6404f-7f19-596b-b1dd-0db0752030a9"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "836eb39b-9cd7-4686-9f73-26b069e81f0f",
        "subject_id": "TCGA-N5-A4RV",
        "researchsubject_id": "3af5b391-e72f-463d-a086-a86c6c30a51a",
    },
    {
        "id": "193e69da-ceb6-4563-83b1-eeb7ecf57da0",
        "identifier": [
            {"system": "GDC", "value": "193e69da-ceb6-4563-83b1-eeb7ecf57da0"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "bcfc2771-8c89-5d6c-8870-ec2d5519b66d",
        "subject_id": "TCGA-QM-A5NM",
        "researchsubject_id": "485b221f-f40f-46a0-a9cf-023f807e6146",
    },
    {
        "id": "1b568320-8384-4628-88a1-1ca30d33e71a",
        "identifier": [
            {"system": "GDC", "value": "1b568320-8384-4628-88a1-1ca30d33e71a"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-MQ-A6BR",
        "researchsubject_id": "00397ce0-a931-46dd-9407-c1c6a14c39f1",
    },
    {
        "id": "1eaa0397-c65f-544d-8bcf-d17163ff434e",
        "identifier": [
            {"system": "GDC", "value": "1eaa0397-c65f-544d-8bcf-d17163ff434e"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "6c8f89c2-a9b4-46dc-b2d5-c25ebeb5485a",
        "subject_id": "TCGA-V4-A9ED",
        "researchsubject_id": "367869f9-bbe7-4e57-a16f-f2b63f2de697",
    },
    {
        "id": "2b226f92-2bc9-4307-b1e9-805abac68a51",
        "identifier": [
            {"system": "GDC", "value": "2b226f92-2bc9-4307-b1e9-805abac68a51"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "0702edbe-216d-556e-865a-48a56892b7df",
        "subject_id": "TCGA-MQ-A6BN",
        "researchsubject_id": "4d9f1899-4a41-4e57-bdad-b12eb0d47629",
    },
    {
        "id": "2b2e106f-4378-4767-b82e-77bb3e7b23f0",
        "identifier": [
            {"system": "GDC", "value": "2b2e106f-4378-4767-b82e-77bb3e7b23f0"}
        ],
        "associated_project": "TCGA-UVM",
        "days_to_collection": 0,
        "primary_disease_type": "Nevi and Melanomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "9d7189eb-e34b-546b-b0ee-20be03534e4e",
        "subject_id": "TCGA-WC-A880",
        "researchsubject_id": "d8e15178-d8c5-4e4e-895c-57ffe5bc80c2",
    },
    {
        "id": "51dcb9cd-8248-4067-b243-f0d30c67eeed",
        "identifier": [
            {"system": "GDC", "value": "51dcb9cd-8248-4067-b243-f0d30c67eeed"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "ea0ff8a0-f3de-5087-86ac-af525a8bc1df",
        "subject_id": "TCGA-ZH-A8Y5",
        "researchsubject_id": "9d9109f5-5917-4126-8e34-8a7e4632e913",
    },
    {
        "id": "56144c3d-4fa3-487e-ae9d-2686167f0926",
        "identifier": [
            {"system": "GDC", "value": "56144c3d-4fa3-487e-ae9d-2686167f0926"}
        ],
        "associated_project": "TCGA-CHOL",
        "days_to_collection": 0,
        "primary_disease_type": "Adenomas and Adenocarcinomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "a46cddb8-b24e-5077-9dd6-7184e953f1c2",
        "subject_id": "TCGA-3X-AAVB",
        "researchsubject_id": "3824cd6d-c85c-4b21-819a-932d1afef976",
    },
    {
        "id": "5b9fb6dc-6cbd-486b-92ba-c8b919ff8eb7",
        "identifier": [
            {"system": "GDC", "value": "5b9fb6dc-6cbd-486b-92ba-c8b919ff8eb7"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "d53fb49c-0c51-5e24-9810-dd228578199c",
        "subject_id": "TCGA-N5-A4RT",
        "researchsubject_id": "1791e250-70ac-439c-828b-15ba811935cc",
    },
    {
        "id": "632596b1-2620-5225-814a-6cc258ce35a3",
        "identifier": [
            {"system": "GDC", "value": "632596b1-2620-5225-814a-6cc258ce35a3"}
        ],
        "associated_project": "TCGA-MESO",
        "days_to_collection": 0,
        "primary_disease_type": "Mesothelial Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "portion",
        "derived_from_specimen": "530132c7-ff21-400a-b3ef-1c92b5bce6cb",
        "subject_id": "TCGA-LK-A4O6",
        "researchsubject_id": "d940e476-fb0a-4cc3-8ab5-691156e7c09b",
    },
    {
        "id": "836eb39b-9cd7-4686-9f73-26b069e81f0f",
        "identifier": [
            {"system": "GDC", "value": "836eb39b-9cd7-4686-9f73-26b069e81f0f"}
        ],
        "associated_project": "TCGA-UCS",
        "days_to_collection": 0,
        "primary_disease_type": "Complex Mixed and Stromal Neoplasms",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-N5-A4RV",
        "researchsubject_id": "3af5b391-e72f-463d-a086-a86c6c30a51a",
    },
    {
        "id": "b7901bd4-a92a-4f6b-8102-ab28ca9d1472",
        "identifier": [
            {"system": "GDC", "value": "b7901bd4-a92a-4f6b-8102-ab28ca9d1472"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "slide",
        "derived_from_specimen": "857c0da5-dc93-5476-9627-bf532cc8b9d4",
        "subject_id": "TCGA-RQ-AAAT",
        "researchsubject_id": "4dd86ebd-ef16-4b2b-9ea0-5d1d7afef257",
    },
    {
        "id": "d979de82-00ac-430e-a18a-a0502a30a678",
        "identifier": [
            {"system": "GDC", "value": "d979de82-00ac-430e-a18a-a0502a30a678"}
        ],
        "associated_project": "TCGA-DLBC",
        "days_to_collection": 0,
        "primary_disease_type": "Mature B-Cell Lymphomas",
        "anatomical_site": None,
        "source_material_type": "Primary Tumor",
        "specimen_type": "sample",
        "derived_from_specimen": "initial specimen",
        "subject_id": "TCGA-GR-7353",
        "researchsubject_id": "c3d662ee-48d0-454a-bb0c-77d3338d3747",
    },
]

fake = FakeResultData(result)
fake_result = Result(
    api_response=fake.api_response,
    offset=fake.offset,
    limit=fake.limit,
    api_instance=fake.api_instance,
    show_sql=fake.show_sql,
    show_count=fake.show_count,
    format_type=fake.format_type,
)


@mock.patch(Q_import_path_str(method="run"), return_value=fake_result)
def test_age_at_collection(a):
    p = Q("age_at_collection <= 10")
    qsub = p.specimen.run()
    assert isinstance(qsub.to_list(), list) is True
    assert isinstance(qsub.to_dataframe(), DataFrame) is True
