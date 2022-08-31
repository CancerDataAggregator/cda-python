from cdapython import Q
from unittest import mock
from tests.fake_result import FakeResultData
from cdapython.results.result import Result
from pandas import DataFrame
# from tests.global_settings import host, integration_host, table

result = [
    {
        'id': '17f8307e-3b45-46b5-add9-bcee96ae5fd7',
        'identifier': [
            {'system': 'IDC', 'value': '17f8307e-3b45-46b5-add9-bcee96ae5fd7'}
        ],
        'label': 'tasets-idc/17f8307e-3b45-46b5-add9-bcee96ae5fd7.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:17f8307e-3b45-46b5-add9-bcee96ae5fd7',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '87b1b0c3-7ae7-46b7-a86c-170640e371a9',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AN-A0G0__tcga_brca',
        'subject_id': 'TCGA-AN-A0G0'
    },
    {
        'id': '40b05074-1aef-45b2-b033-0667c33cbf06',
        'identifier': [
            {'system': 'IDC', 'value': '40b05074-1aef-45b2-b033-0667c33cbf06'}
        ],
        'label': 'tasets-idc/40b05074-1aef-45b2-b033-0667c33cbf06.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:40b05074-1aef-45b2-b033-0667c33cbf06',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '21593970-7af2-4b66-a993-376942462ab8',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AR-A24H__tcga_brca',
        'subject_id': 'TCGA-AR-A24H'
    },
    {
        'id': 'c29fbfd3-69ab-4c59-ade7-eb3ed16f2611',
        'identifier': [
            {'system': 'IDC', 'value': 'c29fbfd3-69ab-4c59-ade7-eb3ed16f2611'}
        ],
        'label': 'tasets-idc/c29fbfd3-69ab-4c59-ade7-eb3ed16f2611.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:c29fbfd3-69ab-4c59-ade7-eb3ed16f2611',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '3fb06ce9-ad47-49d4-b630-307790051a02',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '825bfe58-9c52-477c-85d6-35728523a039',
        'identifier': [
            {'system': 'IDC', 'value': '825bfe58-9c52-477c-85d6-35728523a039'}
        ],
        'label': 'tasets-idc/825bfe58-9c52-477c-85d6-35728523a039.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:825bfe58-9c52-477c-85d6-35728523a039',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '608d2cd4-5945-4d10-a44a-dc89e5dcc21d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-C8-A12P__tcga_brca',
        'subject_id': 'TCGA-C8-A12P'
    },
    {
        'id': '9ab94faf-20da-4f07-9bf7-b2681c9111c8',
        'identifier': [
            {'system': 'IDC', 'value': '9ab94faf-20da-4f07-9bf7-b2681c9111c8'}
        ],
        'label': 'tasets-idc/9ab94faf-20da-4f07-9bf7-b2681c9111c8.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:9ab94faf-20da-4f07-9bf7-b2681c9111c8',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'ac7f4915-58fd-4ead-86a1-3c0c50fcfbd5',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0DL__tcga_brca',
        'subject_id': 'TCGA-BH-A0DL'
    },
    {
        'id': '2a390a7b-6e9a-4211-9953-6c538c2ddcb4',
        'identifier': [
            {'system': 'IDC', 'value': '2a390a7b-6e9a-4211-9953-6c538c2ddcb4'}
        ],
        'label': 'tasets-idc/2a390a7b-6e9a-4211-9953-6c538c2ddcb4.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:2a390a7b-6e9a-4211-9953-6c538c2ddcb4',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '97845efa-1dd1-4739-8991-bec0fc5bdf0c',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AN-A0XL__tcga_brca',
        'subject_id': 'TCGA-AN-A0XL'
    },
    {
        'id': '74e59768-b745-4c78-a39a-3cb15a829714',
        'identifier': [
            {'system': 'IDC', 'value': '74e59768-b745-4c78-a39a-3cb15a829714'}
        ],
        'label': 'tasets-idc/74e59768-b745-4c78-a39a-3cb15a829714.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:74e59768-b745-4c78-a39a-3cb15a829714',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '39b7c366-1119-4575-819b-15973ad9afbc',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': '90d43d11-73f3-4387-88de-316bc1d64ca6',
        'identifier': [
            {'system': 'IDC', 'value': '90d43d11-73f3-4387-88de-316bc1d64ca6'}
        ],
        'label': 'tasets-idc/90d43d11-73f3-4387-88de-316bc1d64ca6.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:90d43d11-73f3-4387-88de-316bc1d64ca6',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'fa4fb2cb-c76a-479a-99e3-98ddd4a85d09',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E9-A22E__tcga_brca',
        'subject_id': 'TCGA-E9-A22E'
    },
    {
        'id': 'cd236963-2d73-469c-b829-af8c8d3e21df',
        'identifier': [
            {'system': 'IDC', 'value': 'cd236963-2d73-469c-b829-af8c8d3e21df'}
        ],
        'label': 'tasets-idc/cd236963-2d73-469c-b829-af8c8d3e21df.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:cd236963-2d73-469c-b829-af8c8d3e21df',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '8e6b78ba-295b-4df4-bd54-6a8290d9661d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A18N__tcga_brca',
        'subject_id': 'TCGA-BH-A18N'
    },
    {
        'id': '645bcccd-e905-44d2-ba9f-b609e763fc11',
        'identifier': [
            {'system': 'IDC', 'value': '645bcccd-e905-44d2-ba9f-b609e763fc11'}
        ],
        'label': 'tasets-idc/645bcccd-e905-44d2-ba9f-b609e763fc11.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:645bcccd-e905-44d2-ba9f-b609e763fc11',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '6a5cff9f-4e84-47ff-876d-de1401b85363',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A1LE__tcga_brca',
        'subject_id': 'TCGA-E2-A1LE'
    },
    {
        'id': '689d2907-c279-4baa-8c67-4ee13cde4923',
        'identifier': [
            {'system': 'IDC', 'value': '689d2907-c279-4baa-8c67-4ee13cde4923'}
        ],
        'label': 'tasets-idc/689d2907-c279-4baa-8c67-4ee13cde4923.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:689d2907-c279-4baa-8c67-4ee13cde4923',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '7ae16e00-99f1-4534-8ef3-8e53071620be',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': '1c0638d9-7443-4e64-b37a-b762949e7864',
        'identifier': [
            {'system': 'IDC', 'value': '1c0638d9-7443-4e64-b37a-b762949e7864'}
        ],
        'label': 'tasets-idc/1c0638d9-7443-4e64-b37a-b762949e7864.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1c0638d9-7443-4e64-b37a-b762949e7864',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '5ad746d9-7d2d-481c-8188-e849c763ea47',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0DS__tcga_brca',
        'subject_id': 'TCGA-BH-A0DS'
    },
    {
        'id': 'f38c40cd-a815-4c5e-9065-f5bef24b7d1f',
        'identifier': [
            {'system': 'IDC', 'value': 'f38c40cd-a815-4c5e-9065-f5bef24b7d1f'}
        ],
        'label': 'tasets-idc/f38c40cd-a815-4c5e-9065-f5bef24b7d1f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:f38c40cd-a815-4c5e-9065-f5bef24b7d1f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '7d08aa88-9833-455b-8b33-91d4db9d3fa4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-B6-A1KC__tcga_brca',
        'subject_id': 'TCGA-B6-A1KC'
    },
    {
        'id': 'd1a292e0-890d-48d3-86f6-765ae6c314ee',
        'identifier': [
            {'system': 'IDC', 'value': 'd1a292e0-890d-48d3-86f6-765ae6c314ee'}
        ],
        'label': 'tasets-idc/d1a292e0-890d-48d3-86f6-765ae6c314ee.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:d1a292e0-890d-48d3-86f6-765ae6c314ee',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '02c6258e-afc3-4dcd-9c15-cb03efb89b99',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A7-A0DA__tcga_brca',
        'subject_id': 'TCGA-A7-A0DA'
    },
    {
        'id': 'f50ab3f1-69f9-40b4-9b92-a16b4405df40',
        'identifier': [
            {'system': 'IDC', 'value': 'f50ab3f1-69f9-40b4-9b92-a16b4405df40'}
        ],
        'label': 'tasets-idc/f50ab3f1-69f9-40b4-9b92-a16b4405df40.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:f50ab3f1-69f9-40b4-9b92-a16b4405df40',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '522f9e08-08f7-41e3-9393-60ae936a3873',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-D8-A1JE__tcga_brca',
        'subject_id': 'TCGA-D8-A1JE'
    },
    {
        'id': 'd9d21482-89b8-4404-a824-706e55494b22',
        'identifier': [
            {'system': 'IDC', 'value': 'd9d21482-89b8-4404-a824-706e55494b22'}
        ],
        'label': 'tasets-idc/d9d21482-89b8-4404-a824-706e55494b22.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:d9d21482-89b8-4404-a824-706e55494b22',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'ad49783c-e4e9-4b84-8bc6-6de4a4317265',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A9RU__tcga_brca',
        'subject_id': 'TCGA-E2-A9RU'
    },
    {
        'id': '39619198-fec8-4cb4-96ea-9fdd78dbec29',
        'identifier': [
            {'system': 'IDC', 'value': '39619198-fec8-4cb4-96ea-9fdd78dbec29'}
        ],
        'label': 'tasets-idc/39619198-fec8-4cb4-96ea-9fdd78dbec29.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:39619198-fec8-4cb4-96ea-9fdd78dbec29',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'd5249781-fd76-445c-8201-17c1bb8ca62a',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A1-A0SG__tcga_brca',
        'subject_id': 'TCGA-A1-A0SG'
    },
    {
        'id': '2bad6a6a-4fc3-4a28-9726-30139ad69532',
        'identifier': [
            {'system': 'IDC', 'value': '2bad6a6a-4fc3-4a28-9726-30139ad69532'}
        ],
        'label': 'tasets-idc/2bad6a6a-4fc3-4a28-9726-30139ad69532.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:2bad6a6a-4fc3-4a28-9726-30139ad69532',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '5c3afba9-4d58-48df-844c-fc843678fa8b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0HP__tcga_brca',
        'subject_id': 'TCGA-BH-A0HP'
    },
    {
        'id': 'b715908c-f36d-4044-9c76-60a1baee6ae0',
        'identifier': [
            {'system': 'IDC', 'value': 'b715908c-f36d-4044-9c76-60a1baee6ae0'}
        ],
        'label': 'tasets-idc/b715908c-f36d-4044-9c76-60a1baee6ae0.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:b715908c-f36d-4044-9c76-60a1baee6ae0',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '62131fa5-1b07-4d14-ab6c-544c168c9289',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-EW-A1OY__tcga_brca',
        'subject_id': 'TCGA-EW-A1OY'
    },
    {
        'id': 'ea7f1430-3d1a-4360-b2c2-0d6e70ad8273',
        'identifier': [
            {'system': 'IDC', 'value': 'ea7f1430-3d1a-4360-b2c2-0d6e70ad8273'}
        ],
        'label': 'tasets-idc/ea7f1430-3d1a-4360-b2c2-0d6e70ad8273.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:ea7f1430-3d1a-4360-b2c2-0d6e70ad8273',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '1bb6f2e6-5977-4415-9040-4905a0c1cb82',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A083__tcga_brca',
        'subject_id': 'TCGA-A8-A083'
    },
    {
        'id': 'ec3429b4-446f-48c2-b574-6f50fd30763b',
        'identifier': [
            {'system': 'IDC', 'value': 'ec3429b4-446f-48c2-b574-6f50fd30763b'}
        ],
        'label': 'tasets-idc/ec3429b4-446f-48c2-b574-6f50fd30763b.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:ec3429b4-446f-48c2-b574-6f50fd30763b',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'd0841c64-d1b0-4a64-90b0-62c90e85e91f',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0EA__tcga_brca',
        'subject_id': 'TCGA-BH-A0EA'
    },
    {
        'id': '34ddf37d-a04e-4cc5-b1c5-1407ce17aba0',
        'identifier': [
            {'system': 'IDC', 'value': '34ddf37d-a04e-4cc5-b1c5-1407ce17aba0'}
        ],
        'label': 'tasets-idc/34ddf37d-a04e-4cc5-b1c5-1407ce17aba0.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:34ddf37d-a04e-4cc5-b1c5-1407ce17aba0',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '7c7ba05b-140f-4f8e-a806-ad93d101cadb',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-Z7-A8R5__tcga_brca',
        'subject_id': 'TCGA-Z7-A8R5'
    },
    {
        'id': '6956347a-23f8-4f58-aec1-452dee5c758f',
        'identifier': [
            {'system': 'IDC', 'value': '6956347a-23f8-4f58-aec1-452dee5c758f'}
        ],
        'label': 'tasets-idc/6956347a-23f8-4f58-aec1-452dee5c758f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:6956347a-23f8-4f58-aec1-452dee5c758f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'b9548879-f3c2-4324-94fc-88fe5f836a23',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-EW-A1OY__tcga_brca',
        'subject_id': 'TCGA-EW-A1OY'
    },
    {
        'id': 'e228a304-7fc0-49bf-b38a-54a6ab164c0b',
        'identifier': [
            {'system': 'IDC', 'value': 'e228a304-7fc0-49bf-b38a-54a6ab164c0b'}
        ],
        'label': 'tasets-idc/e228a304-7fc0-49bf-b38a-54a6ab164c0b.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:e228a304-7fc0-49bf-b38a-54a6ab164c0b',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '9dd3dcce-97b4-4683-a94f-77b778da13fc',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AN-A046__tcga_brca',
        'subject_id': 'TCGA-AN-A046'
    },
    {
        'id': '1a7a28e3-5fbe-461e-b8fb-a6ae10473b04',
        'identifier': [
            {'system': 'IDC', 'value': '1a7a28e3-5fbe-461e-b8fb-a6ae10473b04'}
        ],
        'label': 'tasets-idc/1a7a28e3-5fbe-461e-b8fb-a6ae10473b04.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1a7a28e3-5fbe-461e-b8fb-a6ae10473b04',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '1d927b1a-6d3c-473c-9179-abb63b774a76',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A105__tcga_brca',
        'subject_id': 'TCGA-E2-A105'
    },
    {
        'id': 'ab2ed030-a4f3-4e0c-b86b-183fcdc6866f',
        'identifier': [
            {'system': 'IDC', 'value': 'ab2ed030-a4f3-4e0c-b86b-183fcdc6866f'}
        ],
        'label': 'tasets-idc/ab2ed030-a4f3-4e0c-b86b-183fcdc6866f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:ab2ed030-a4f3-4e0c-b86b-183fcdc6866f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '45f6c82e-0897-4bb3-b9d5-5e545ca943f8',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-PE-A5DD__tcga_brca',
        'subject_id': 'TCGA-PE-A5DD'
    },
    {
        'id': 'b052d830-c9ee-428e-8abb-e472dfdc4ea2',
        'identifier': [
            {'system': 'IDC', 'value': 'b052d830-c9ee-428e-8abb-e472dfdc4ea2'}
        ],
        'label': 'tasets-idc/b052d830-c9ee-428e-8abb-e472dfdc4ea2.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:b052d830-c9ee-428e-8abb-e472dfdc4ea2',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '693405ad-f617-4f28-9ba3-c70d13800304',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': 'c8173f69-947b-480d-a37c-1785892d5482',
        'identifier': [
            {'system': 'IDC', 'value': 'c8173f69-947b-480d-a37c-1785892d5482'}
        ],
        'label': 'tasets-idc/c8173f69-947b-480d-a37c-1785892d5482.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:c8173f69-947b-480d-a37c-1785892d5482',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'e0a4b350-f413-47a3-b5e1-fe35272bf683',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-D8-A1XJ__tcga_brca',
        'subject_id': 'TCGA-D8-A1XJ'
    },
    {
        'id': '8fd5c4f5-5f81-4d3d-b412-f2eb878cc2b5',
        'identifier': [
            {'system': 'IDC', 'value': '8fd5c4f5-5f81-4d3d-b412-f2eb878cc2b5'}
        ],
        'label': 'tasets-idc/8fd5c4f5-5f81-4d3d-b412-f2eb878cc2b5.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:8fd5c4f5-5f81-4d3d-b412-f2eb878cc2b5',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'e06ad7c9-bc69-4358-8f65-20e6a3dd0c9c',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A10B__tcga_brca',
        'subject_id': 'TCGA-E2-A10B'
    },
    {
        'id': '10b79ef5-7fdc-4d3c-8d5a-9188467bc0b9',
        'identifier': [
            {'system': 'IDC', 'value': '10b79ef5-7fdc-4d3c-8d5a-9188467bc0b9'}
        ],
        'label': 'tasets-idc/10b79ef5-7fdc-4d3c-8d5a-9188467bc0b9.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:10b79ef5-7fdc-4d3c-8d5a-9188467bc0b9',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '1c430260-f930-4221-8426-833c3c1a93f2',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0HB__tcga_brca',
        'subject_id': 'TCGA-BH-A0HB'
    },
    {
        'id': '229cb42d-0033-443c-9fa4-2c94ab549e9f',
        'identifier': [
            {'system': 'IDC', 'value': '229cb42d-0033-443c-9fa4-2c94ab549e9f'}
        ],
        'label': 'tasets-idc/229cb42d-0033-443c-9fa4-2c94ab549e9f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:229cb42d-0033-443c-9fa4-2c94ab549e9f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '0fdc052f-9a23-4584-a5f6-7d89196b4eb4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-B6-A0RM__tcga_brca',
        'subject_id': 'TCGA-B6-A0RM'
    },
    {
        'id': 'b85f687d-48b1-46ca-921d-1d899f09131c',
        'identifier': [
            {'system': 'IDC', 'value': 'b85f687d-48b1-46ca-921d-1d899f09131c'}
        ],
        'label': 'tasets-idc/b85f687d-48b1-46ca-921d-1d899f09131c.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:b85f687d-48b1-46ca-921d-1d899f09131c',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '701b44f4-76d4-4cf2-9347-4fcea7dc4280',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AQ-A04H__tcga_brca',
        'subject_id': 'TCGA-AQ-A04H'
    },
    {
        'id': '8feba546-cbbc-40ba-9a71-a84841582056',
        'identifier': [
            {'system': 'IDC', 'value': '8feba546-cbbc-40ba-9a71-a84841582056'}
        ],
        'label': 'tasets-idc/8feba546-cbbc-40ba-9a71-a84841582056.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:8feba546-cbbc-40ba-9a71-a84841582056',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'b9e1fea7-93b8-423b-a630-cf55cd7183b5',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-5T-A9QA__tcga_brca',
        'subject_id': 'TCGA-5T-A9QA'
    },
    {
        'id': '8dab4f3b-0d4a-4175-8bd6-324c929e0b15',
        'identifier': [
            {'system': 'IDC', 'value': '8dab4f3b-0d4a-4175-8bd6-324c929e0b15'}
        ],
        'label': 'tasets-idc/8dab4f3b-0d4a-4175-8bd6-324c929e0b15.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:8dab4f3b-0d4a-4175-8bd6-324c929e0b15',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '9c5bfbf0-949b-4121-abb5-c73b7e0ca182',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-D8-A1XQ__tcga_brca',
        'subject_id': 'TCGA-D8-A1XQ'
    },
    {
        'id': '5ee83c6e-7ced-4bfb-83e1-56e6f0e45d0e',
        'identifier': [
            {'system': 'IDC', 'value': '5ee83c6e-7ced-4bfb-83e1-56e6f0e45d0e'}
        ],
        'label': 'tasets-idc/5ee83c6e-7ced-4bfb-83e1-56e6f0e45d0e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:5ee83c6e-7ced-4bfb-83e1-56e6f0e45d0e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'd114c824-618d-47b9-9283-15d42131cd16',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-LD-A74U__tcga_brca',
        'subject_id': 'TCGA-LD-A74U'
    },
    {
        'id': '7b48468e-1d8a-4c36-90db-f60bc6dc4e3f',
        'identifier': [
            {'system': 'IDC', 'value': '7b48468e-1d8a-4c36-90db-f60bc6dc4e3f'}
        ],
        'label': 'tasets-idc/7b48468e-1d8a-4c36-90db-f60bc6dc4e3f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:7b48468e-1d8a-4c36-90db-f60bc6dc4e3f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'd39adca0-115b-4834-8700-e7f55be137b4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '7a602ed7-1d77-4aba-9df5-a313608ccc8a',
        'identifier': [
            {'system': 'IDC', 'value': '7a602ed7-1d77-4aba-9df5-a313608ccc8a'}
        ],
        'label': 'tasets-idc/7a602ed7-1d77-4aba-9df5-a313608ccc8a.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:7a602ed7-1d77-4aba-9df5-a313608ccc8a',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '6566cfa2-7360-42e7-a0fb-075aa69edbaf',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A07G__tcga_brca',
        'subject_id': 'TCGA-A8-A07G'
    },
    {
        'id': '06718c07-00e2-4cc9-806d-53503e61b15d',
        'identifier': [
            {'system': 'IDC', 'value': '06718c07-00e2-4cc9-806d-53503e61b15d'}
        ],
        'label': 'tasets-idc/06718c07-00e2-4cc9-806d-53503e61b15d.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:06718c07-00e2-4cc9-806d-53503e61b15d',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '537619e9-9661-47ea-8602-4d6d34404cac',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-GM-A2DM__tcga_brca',
        'subject_id': 'TCGA-GM-A2DM'
    },
    {
        'id': 'f133e432-f1d6-46a5-bc5b-6884ebfa738e',
        'identifier': [
            {'system': 'IDC', 'value': 'f133e432-f1d6-46a5-bc5b-6884ebfa738e'}
        ],
        'label': 'tasets-idc/f133e432-f1d6-46a5-bc5b-6884ebfa738e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:f133e432-f1d6-46a5-bc5b-6884ebfa738e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'a0ff90a0-cd9a-497f-910b-304945b9eacf',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-C8-A12P__tcga_brca',
        'subject_id': 'TCGA-C8-A12P'
    },
    {
        'id': '1b695c91-3663-4a13-86b6-35772db1171a',
        'identifier': [
            {'system': 'IDC', 'value': '1b695c91-3663-4a13-86b6-35772db1171a'}
        ],
        'label': 'tasets-idc/1b695c91-3663-4a13-86b6-35772db1171a.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1b695c91-3663-4a13-86b6-35772db1171a',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '1507973e-09f5-4636-bc9a-4091ba04f778',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-EW-A424__tcga_brca',
        'subject_id': 'TCGA-EW-A424'
    },
    {
        'id': '0c9fd109-1753-46df-8ab8-0efd1b4e3d6d',
        'identifier': [
            {'system': 'IDC', 'value': '0c9fd109-1753-46df-8ab8-0efd1b4e3d6d'}
        ],
        'label': 'tasets-idc/0c9fd109-1753-46df-8ab8-0efd1b4e3d6d.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:0c9fd109-1753-46df-8ab8-0efd1b4e3d6d',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'b65f0589-386c-42b9-9707-4f8626c69794',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '4bafd8c2-8645-400c-a4b6-877663949eb2',
        'identifier': [
            {'system': 'IDC', 'value': '4bafd8c2-8645-400c-a4b6-877663949eb2'}
        ],
        'label': 'tasets-idc/4bafd8c2-8645-400c-a4b6-877663949eb2.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:4bafd8c2-8645-400c-a4b6-877663949eb2',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'f6e0e7be-9fe7-4ed6-b1ef-1d98667bb13d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AR-A0U4__tcga_brca',
        'subject_id': 'TCGA-AR-A0U4'
    },
    {
        'id': 'fe867bb2-7eba-4cc4-b497-32d79d87a541',
        'identifier': [
            {'system': 'IDC', 'value': 'fe867bb2-7eba-4cc4-b497-32d79d87a541'}
        ],
        'label': 'tasets-idc/fe867bb2-7eba-4cc4-b497-32d79d87a541.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:fe867bb2-7eba-4cc4-b497-32d79d87a541',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'e06159a9-a02b-4c78-bc0f-5503056c44f5',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-OL-A97C__tcga_brca',
        'subject_id': 'TCGA-OL-A97C'
    },
    {
        'id': '13d42c72-3054-4102-8ece-bd6b5d41cda0',
        'identifier': [
            {'system': 'IDC', 'value': '13d42c72-3054-4102-8ece-bd6b5d41cda0'}
        ],
        'label': 'tasets-idc/13d42c72-3054-4102-8ece-bd6b5d41cda0.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:13d42c72-3054-4102-8ece-bd6b5d41cda0',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '5138a786-9939-423d-ad4e-d76d2fbc2410',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': 'c3bb83d5-7658-4f00-bea2-c2864ba929a9',
        'identifier': [
            {'system': 'IDC', 'value': 'c3bb83d5-7658-4f00-bea2-c2864ba929a9'}
        ],
        'label': 'tasets-idc/c3bb83d5-7658-4f00-bea2-c2864ba929a9.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:c3bb83d5-7658-4f00-bea2-c2864ba929a9',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '8216fbc9-8280-47f8-9f8e-94e0778132ed',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0B4__tcga_brca',
        'subject_id': 'TCGA-BH-A0B4'
    },
    {
        'id': 'da7644a1-8071-4993-be04-af1dbf6380e3',
        'identifier': [
            {'system': 'IDC', 'value': 'da7644a1-8071-4993-be04-af1dbf6380e3'}
        ],
        'label': 'tasets-idc/da7644a1-8071-4993-be04-af1dbf6380e3.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:da7644a1-8071-4993-be04-af1dbf6380e3',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '8d629b29-7a9f-4551-acce-949ef378dfe2',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A04N__tcga_brca',
        'subject_id': 'TCGA-A2-A04N'
    },
    {
        'id': 'eb7cb12c-6725-4562-974f-43733db50970',
        'identifier': [
            {'system': 'IDC', 'value': 'eb7cb12c-6725-4562-974f-43733db50970'}
        ],
        'label': 'tasets-idc/eb7cb12c-6725-4562-974f-43733db50970.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:eb7cb12c-6725-4562-974f-43733db50970',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'a47051d8-88b6-4bb0-8773-eeeb889dc7b6',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A1FX__tcga_brca',
        'subject_id': 'TCGA-A2-A1FX'
    },
    {
        'id': '30709eb4-9df7-443d-9006-f7491fc508a1',
        'identifier': [
            {'system': 'IDC', 'value': '30709eb4-9df7-443d-9006-f7491fc508a1'}
        ],
        'label': 'tasets-idc/30709eb4-9df7-443d-9006-f7491fc508a1.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:30709eb4-9df7-443d-9006-f7491fc508a1',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '39b7c366-1119-4575-819b-15973ad9afbc',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': '475a39f0-df35-424e-8c3b-3bae8d2a64af',
        'identifier': [
            {'system': 'IDC', 'value': '475a39f0-df35-424e-8c3b-3bae8d2a64af'}
        ],
        'label': 'tasets-idc/475a39f0-df35-424e-8c3b-3bae8d2a64af.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:475a39f0-df35-424e-8c3b-3bae8d2a64af',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '94ffe3af-fd40-4fd1-a893-e19c98072fdf',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-C8-A138__tcga_brca',
        'subject_id': 'TCGA-C8-A138'
    },
    {
        'id': '5128f01f-0181-44cb-8271-81f3f1cbcfed',
        'identifier': [
            {'system': 'IDC', 'value': '5128f01f-0181-44cb-8271-81f3f1cbcfed'}
        ],
        'label': 'tasets-idc/5128f01f-0181-44cb-8271-81f3f1cbcfed.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:5128f01f-0181-44cb-8271-81f3f1cbcfed',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '7239d59e-8057-4fe1-884f-848f6a53b44e',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AQ-A04H__tcga_brca',
        'subject_id': 'TCGA-AQ-A04H'
    },
    {
        'id': '44cfa3ff-ef63-4d07-838f-5336c02f9095',
        'identifier': [
            {'system': 'IDC', 'value': '44cfa3ff-ef63-4d07-838f-5336c02f9095'}
        ],
        'label': 'tasets-idc/44cfa3ff-ef63-4d07-838f-5336c02f9095.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:44cfa3ff-ef63-4d07-838f-5336c02f9095',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '53ed7df4-74a6-456b-926c-a9f1eba60145',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-C8-A12N__tcga_brca',
        'subject_id': 'TCGA-C8-A12N'
    },
    {
        'id': 'a51c6bf8-c762-4824-a66d-4d23da231fe1',
        'identifier': [
            {'system': 'IDC', 'value': 'a51c6bf8-c762-4824-a66d-4d23da231fe1'}
        ],
        'label': 'tasets-idc/a51c6bf8-c762-4824-a66d-4d23da231fe1.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:a51c6bf8-c762-4824-a66d-4d23da231fe1',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '8ff55e4c-f634-49e2-9ba4-f634267fba94',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A7-A13E__tcga_brca',
        'subject_id': 'TCGA-A7-A13E'
    },
    {
        'id': 'be8b916d-e971-42ea-803c-e9ab6d61014c',
        'identifier': [
            {'system': 'IDC', 'value': 'be8b916d-e971-42ea-803c-e9ab6d61014c'}
        ],
        'label': 'tasets-idc/be8b916d-e971-42ea-803c-e9ab6d61014c.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:be8b916d-e971-42ea-803c-e9ab6d61014c',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'f224a9d1-c20a-41dc-97cf-6712754dff05',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A14Q__tcga_brca',
        'subject_id': 'TCGA-E2-A14Q'
    },
    {
        'id': '4deff8f7-cd90-46c1-a154-c7dd4d851aa5',
        'identifier': [
            {'system': 'IDC', 'value': '4deff8f7-cd90-46c1-a154-c7dd4d851aa5'}
        ],
        'label': 'tasets-idc/4deff8f7-cd90-46c1-a154-c7dd4d851aa5.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:4deff8f7-cd90-46c1-a154-c7dd4d851aa5',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'dc627984-adb6-4bac-b630-32c42569aaa7',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A18U__tcga_brca',
        'subject_id': 'TCGA-BH-A18U'
    },
    {
        'id': '082e1e0b-eec6-45d6-bdec-01587e699e37',
        'identifier': [
            {'system': 'IDC', 'value': '082e1e0b-eec6-45d6-bdec-01587e699e37'}
        ],
        'label': 'tasets-idc/082e1e0b-eec6-45d6-bdec-01587e699e37.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:082e1e0b-eec6-45d6-bdec-01587e699e37',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '6e917e5f-ac03-48a0-95c5-6d4370a330b1',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A09N__tcga_brca',
        'subject_id': 'TCGA-A8-A09N'
    },
    {
        'id': '1ce9b89e-4d48-44f5-b4d7-8745ece3aa6f',
        'identifier': [
            {'system': 'IDC', 'value': '1ce9b89e-4d48-44f5-b4d7-8745ece3aa6f'}
        ],
        'label': 'tasets-idc/1ce9b89e-4d48-44f5-b4d7-8745ece3aa6f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1ce9b89e-4d48-44f5-b4d7-8745ece3aa6f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'f0505ed8-eca7-4116-8f98-6530eb2f7654',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A18J__tcga_brca',
        'subject_id': 'TCGA-BH-A18J'
    },
    {
        'id': '2ae4e8b8-fd47-406b-95df-d6e7e4225b2b',
        'identifier': [
            {'system': 'IDC', 'value': '2ae4e8b8-fd47-406b-95df-d6e7e4225b2b'}
        ],
        'label': 'tasets-idc/2ae4e8b8-fd47-406b-95df-d6e7e4225b2b.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:2ae4e8b8-fd47-406b-95df-d6e7e4225b2b',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '87f2859b-4d8e-473c-a556-aa6defc1be69',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A0A4__tcga_brca',
        'subject_id': 'TCGA-A8-A0A4'
    },
    {
        'id': '88d36bf6-003f-4f13-881b-d623d459afb4',
        'identifier': [
            {'system': 'IDC', 'value': '88d36bf6-003f-4f13-881b-d623d459afb4'}
        ],
        'label': 'tasets-idc/88d36bf6-003f-4f13-881b-d623d459afb4.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:88d36bf6-003f-4f13-881b-d623d459afb4',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'f6d5db0b-8481-41ff-afdc-6c56bb9aa00b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-XX-A89A__tcga_brca',
        'subject_id': 'TCGA-XX-A89A'
    },
    {
        'id': '45e3152b-d4ea-40dc-a06d-cccdaecfe90f',
        'identifier': [
            {'system': 'IDC', 'value': '45e3152b-d4ea-40dc-a06d-cccdaecfe90f'}
        ],
        'label': 'tasets-idc/45e3152b-d4ea-40dc-a06d-cccdaecfe90f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:45e3152b-d4ea-40dc-a06d-cccdaecfe90f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'd9903216-0f55-43ca-9501-bf965b3f6daf',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A08T__tcga_brca',
        'subject_id': 'TCGA-A8-A08T'
    },
    {
        'id': '8cca939a-e9e1-4663-a7ec-a86727343e07',
        'identifier': [
            {'system': 'IDC', 'value': '8cca939a-e9e1-4663-a7ec-a86727343e07'}
        ],
        'label': 'tasets-idc/8cca939a-e9e1-4663-a7ec-a86727343e07.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:8cca939a-e9e1-4663-a7ec-a86727343e07',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '7fbe823f-63ae-4aca-b620-207e562473de',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-S3-AA15__tcga_brca',
        'subject_id': 'TCGA-S3-AA15'
    },
    {
        'id': '51e5561c-1899-42d9-b67e-3e1c99db0978',
        'identifier': [
            {'system': 'IDC', 'value': '51e5561c-1899-42d9-b67e-3e1c99db0978'}
        ],
        'label': 'tasets-idc/51e5561c-1899-42d9-b67e-3e1c99db0978.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:51e5561c-1899-42d9-b67e-3e1c99db0978',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '47ba721e-626f-48b9-a454-b081a7183f3b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '6ad4e4c4-7545-43a9-9a24-2266dd1418ec',
        'identifier': [
            {'system': 'IDC', 'value': '6ad4e4c4-7545-43a9-9a24-2266dd1418ec'}
        ],
        'label': 'tasets-idc/6ad4e4c4-7545-43a9-9a24-2266dd1418ec.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:6ad4e4c4-7545-43a9-9a24-2266dd1418ec',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '7f33b148-a77b-4204-9ab0-c27d412acd85',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': '3a7c4502-c817-4bb2-96cf-a52f6e607d20',
        'identifier': [
            {'system': 'IDC', 'value': '3a7c4502-c817-4bb2-96cf-a52f6e607d20'}
        ],
        'label': 'tasets-idc/3a7c4502-c817-4bb2-96cf-a52f6e607d20.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:3a7c4502-c817-4bb2-96cf-a52f6e607d20',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'faa514f0-2b24-4091-ba55-141e4e41baf8',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-B6-A0I9__tcga_brca',
        'subject_id': 'TCGA-B6-A0I9'
    },
    {
        'id': '48a4ad41-7ace-44f0-9a2c-2b43f9733c8c',
        'identifier': [
            {'system': 'IDC', 'value': '48a4ad41-7ace-44f0-9a2c-2b43f9733c8c'}
        ],
        'label': 'tasets-idc/48a4ad41-7ace-44f0-9a2c-2b43f9733c8c.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:48a4ad41-7ace-44f0-9a2c-2b43f9733c8c',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'c9801a7c-3e4a-4b87-b241-f362fcc1ae03',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A0BZ__tcga_brca',
        'subject_id': 'TCGA-BH-A0BZ'
    },
    {
        'id': 'e792090f-b9c4-4cff-9bbc-ac5e2acc126c',
        'identifier': [
            {'system': 'IDC', 'value': 'e792090f-b9c4-4cff-9bbc-ac5e2acc126c'}
        ],
        'label': 'tasets-idc/e792090f-b9c4-4cff-9bbc-ac5e2acc126c.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:e792090f-b9c4-4cff-9bbc-ac5e2acc126c',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'f29647e7-0209-4cc9-877d-0c2ab8aea87d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A0CY__tcga_brca',
        'subject_id': 'TCGA-A2-A0CY'
    },
    {
        'id': 'a663fef3-24db-4ddd-8cfb-1ffc70775cb2',
        'identifier': [
            {'system': 'IDC', 'value': 'a663fef3-24db-4ddd-8cfb-1ffc70775cb2'}
        ],
        'label': 'tasets-idc/a663fef3-24db-4ddd-8cfb-1ffc70775cb2.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:a663fef3-24db-4ddd-8cfb-1ffc70775cb2',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'd39adca0-115b-4834-8700-e7f55be137b4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': 'b1151c0a-1d0b-4f27-a6f8-ec52ac290896',
        'identifier': [
            {'system': 'IDC', 'value': 'b1151c0a-1d0b-4f27-a6f8-ec52ac290896'}
        ],
        'label': 'tasets-idc/b1151c0a-1d0b-4f27-a6f8-ec52ac290896.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:b1151c0a-1d0b-4f27-a6f8-ec52ac290896',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '37b934c0-a9ed-45f0-b89f-50d13cae0915',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A14Q__tcga_brca',
        'subject_id': 'TCGA-E2-A14Q'
    },
    {
        'id': '7aa97b6d-2d97-4d67-935a-0ba67842a7c6',
        'identifier': [
            {'system': 'IDC', 'value': '7aa97b6d-2d97-4d67-935a-0ba67842a7c6'}
        ],
        'label': 'tasets-idc/7aa97b6d-2d97-4d67-935a-0ba67842a7c6.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:7aa97b6d-2d97-4d67-935a-0ba67842a7c6',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '8d379ee8-6b66-4174-9185-9a0d4447234a',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A09C__tcga_brca',
        'subject_id': 'TCGA-A8-A09C'
    },
    {
        'id': '1447c301-279a-4865-9f12-4695bbba6abb',
        'identifier': [
            {'system': 'IDC', 'value': '1447c301-279a-4865-9f12-4695bbba6abb'}
        ],
        'label': 'tasets-idc/1447c301-279a-4865-9f12-4695bbba6abb.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1447c301-279a-4865-9f12-4695bbba6abb',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': 'bc70512a-9f48-4925-a282-b554f6a0dcc7',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '2def34e5-b677-46dc-ad90-a9e9cf952b0f',
        'identifier': [
            {'system': 'IDC', 'value': '2def34e5-b677-46dc-ad90-a9e9cf952b0f'}
        ],
        'label': 'tasets-idc/2def34e5-b677-46dc-ad90-a9e9cf952b0f.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:2def34e5-b677-46dc-ad90-a9e9cf952b0f',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'f7c2a70d-66c5-4c69-80c2-1d61c5a9bea2',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-LL-A7T0__tcga_brca',
        'subject_id': 'TCGA-LL-A7T0'
    },
    {
        'id': '879140be-caae-4f75-b5d7-7dbf789dc841',
        'identifier': [
            {'system': 'IDC', 'value': '879140be-caae-4f75-b5d7-7dbf789dc841'}
        ],
        'label': 'tasets-idc/879140be-caae-4f75-b5d7-7dbf789dc841.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:879140be-caae-4f75-b5d7-7dbf789dc841',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '7ae16e00-99f1-4534-8ef3-8e53071620be',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': 'aa71a04e-6446-4e48-81cc-35490d7eb054',
        'identifier': [
            {'system': 'IDC', 'value': 'aa71a04e-6446-4e48-81cc-35490d7eb054'}
        ],
        'label': 'tasets-idc/aa71a04e-6446-4e48-81cc-35490d7eb054.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:aa71a04e-6446-4e48-81cc-35490d7eb054',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '83e03929-250e-426e-b57e-8a8c3914d02b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AO-A0JI__tcga_brca',
        'subject_id': 'TCGA-AO-A0JI'
    },
    {
        'id': '66a6322f-afa2-4db3-8b11-da345a37cb3a',
        'identifier': [
            {'system': 'IDC', 'value': '66a6322f-afa2-4db3-8b11-da345a37cb3a'}
        ],
        'label': 'tasets-idc/66a6322f-afa2-4db3-8b11-da345a37cb3a.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:66a6322f-afa2-4db3-8b11-da345a37cb3a',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'c3d525f4-7505-4b36-b1f0-4d69a91c3a7e',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AR-A1AK__tcga_brca',
        'subject_id': 'TCGA-AR-A1AK'
    },
    {
        'id': '917100da-14b6-4233-84a6-afd084499ba4',
        'identifier': [
            {'system': 'IDC', 'value': '917100da-14b6-4233-84a6-afd084499ba4'}
        ],
        'label': 'tasets-idc/917100da-14b6-4233-84a6-afd084499ba4.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:917100da-14b6-4233-84a6-afd084499ba4',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '052b366e-b6ea-42a0-98a8-3100af26d175',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A105__tcga_brca',
        'subject_id': 'TCGA-E2-A105'
    },
    {
        'id': '2c2d0fec-e86a-4be3-b962-dbb6ad554323',
        'identifier': [
            {'system': 'IDC', 'value': '2c2d0fec-e86a-4be3-b962-dbb6ad554323'}
        ],
        'label': 'tasets-idc/2c2d0fec-e86a-4be3-b962-dbb6ad554323.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:2c2d0fec-e86a-4be3-b962-dbb6ad554323',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '655a2d3a-107c-4970-953d-53416a497479',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AN-A0FV__tcga_brca',
        'subject_id': 'TCGA-AN-A0FV'
    },
    {
        'id': '4918a870-a422-41c6-95da-76325acbe956',
        'identifier': [
            {'system': 'IDC', 'value': '4918a870-a422-41c6-95da-76325acbe956'}
        ],
        'label': 'tasets-idc/4918a870-a422-41c6-95da-76325acbe956.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:4918a870-a422-41c6-95da-76325acbe956',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'a5a3d3c2-f38f-4839-b40d-5310ae2b286b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A07L__tcga_brca',
        'subject_id': 'TCGA-A8-A07L'
    },
    {
        'id': 'db2ccc2c-aa78-4df2-be12-ea3689b6fbf0',
        'identifier': [
            {'system': 'IDC', 'value': 'db2ccc2c-aa78-4df2-be12-ea3689b6fbf0'}
        ],
        'label': 'tasets-idc/db2ccc2c-aa78-4df2-be12-ea3689b6fbf0.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:db2ccc2c-aa78-4df2-be12-ea3689b6fbf0',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '0cd2d4fc-d622-4daa-aef1-5e42d368ad1c',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AR-A24N__tcga_brca',
        'subject_id': 'TCGA-AR-A24N'
    },
    {
        'id': '761a4985-4977-43c3-a7c5-b0c2980fab3e',
        'identifier': [
            {'system': 'IDC', 'value': '761a4985-4977-43c3-a7c5-b0c2980fab3e'}
        ],
        'label': 'tasets-idc/761a4985-4977-43c3-a7c5-b0c2980fab3e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:761a4985-4977-43c3-a7c5-b0c2980fab3e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'cf26bad9-bc2a-413e-8899-df07615b94b2',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A1ET__tcga_brca',
        'subject_id': 'TCGA-BH-A1ET'
    },
    {
        'id': '4ccd1cec-12a1-4598-a3e4-93aa438451e9',
        'identifier': [
            {'system': 'IDC', 'value': '4ccd1cec-12a1-4598-a3e4-93aa438451e9'}
        ],
        'label': 'tasets-idc/4ccd1cec-12a1-4598-a3e4-93aa438451e9.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:4ccd1cec-12a1-4598-a3e4-93aa438451e9',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '05540d21-3f87-4dfb-8dbe-3034ba1cdf0d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-D8-A3Z5__tcga_brca',
        'subject_id': 'TCGA-D8-A3Z5'
    },
    {
        'id': '249da761-52d5-4fc8-a12e-5c2517247251',
        'identifier': [
            {'system': 'IDC', 'value': '249da761-52d5-4fc8-a12e-5c2517247251'}
        ],
        'label': 'tasets-idc/249da761-52d5-4fc8-a12e-5c2517247251.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:249da761-52d5-4fc8-a12e-5c2517247251',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '396a687e-ad37-443f-9622-72c423cb389e',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A0YD__tcga_brca',
        'subject_id': 'TCGA-A2-A0YD'
    },
    {
        'id': 'e07661d3-6773-47e3-b75f-52cc512e32eb',
        'identifier': [
            {'system': 'IDC', 'value': 'e07661d3-6773-47e3-b75f-52cc512e32eb'}
        ],
        'label': 'tasets-idc/e07661d3-6773-47e3-b75f-52cc512e32eb.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:e07661d3-6773-47e3-b75f-52cc512e32eb',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '936e5785-9059-4c1c-b90a-eedce6f8fbd4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-S3-A6ZG__tcga_brca',
        'subject_id': 'TCGA-S3-A6ZG'
    },
    {
        'id': '58cd613f-443f-441c-8848-ff4aff22a598',
        'identifier': [
            {'system': 'IDC', 'value': '58cd613f-443f-441c-8848-ff4aff22a598'}
        ],
        'label': 'tasets-idc/58cd613f-443f-441c-8848-ff4aff22a598.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:58cd613f-443f-441c-8848-ff4aff22a598',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '2049089a-d8fb-4266-b142-3b2aa355b0aa',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-BH-A18R__tcga_brca',
        'subject_id': 'TCGA-BH-A18R'
    },
    {
        'id': '643a5d40-6927-46e2-9067-fa7033646c63',
        'identifier': [
            {'system': 'IDC', 'value': '643a5d40-6927-46e2-9067-fa7033646c63'}
        ],
        'label': 'tasets-idc/643a5d40-6927-46e2-9067-fa7033646c63.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:643a5d40-6927-46e2-9067-fa7033646c63',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '58f3c040-c0dc-4836-bf3d-99ba191e4215',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-GM-A2DC__tcga_brca',
        'subject_id': 'TCGA-GM-A2DC'
    },
    {
        'id': 'ba021b3c-1842-49d5-a498-29729bc61b7a',
        'identifier': [
            {'system': 'IDC', 'value': 'ba021b3c-1842-49d5-a498-29729bc61b7a'}
        ],
        'label': 'tasets-idc/ba021b3c-1842-49d5-a498-29729bc61b7a.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:ba021b3c-1842-49d5-a498-29729bc61b7a',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '18454a90-c561-4864-ba71-a07bac1cf98c',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E9-A1NG__tcga_brca',
        'subject_id': 'TCGA-E9-A1NG'
    },
    {
        'id': '5ec361b9-a2fb-4aed-9fa6-e2a828f585df',
        'identifier': [
            {'system': 'IDC', 'value': '5ec361b9-a2fb-4aed-9fa6-e2a828f585df'}
        ],
        'label': 'tasets-idc/5ec361b9-a2fb-4aed-9fa6-e2a828f585df.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:5ec361b9-a2fb-4aed-9fa6-e2a828f585df',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '6c397f31-25f9-4701-803e-5f12402daf0d',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A097__tcga_brca',
        'subject_id': 'TCGA-A8-A097'
    },
    {
        'id': '85fc1f2e-bb89-4952-ab12-01861f6e8f35',
        'identifier': [
            {'system': 'IDC', 'value': '85fc1f2e-bb89-4952-ab12-01861f6e8f35'}
        ],
        'label': 'tasets-idc/85fc1f2e-bb89-4952-ab12-01861f6e8f35.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:85fc1f2e-bb89-4952-ab12-01861f6e8f35',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '1d927b1a-6d3c-473c-9179-abb63b774a76',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A105__tcga_brca',
        'subject_id': 'TCGA-E2-A105'
    },
    {
        'id': 'a9d4af7f-37a0-4ef7-98a8-16a3ec24a46c',
        'identifier': [
            {'system': 'IDC', 'value': 'a9d4af7f-37a0-4ef7-98a8-16a3ec24a46c'}
        ],
        'label': 'tasets-idc/a9d4af7f-37a0-4ef7-98a8-16a3ec24a46c.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:a9d4af7f-37a0-4ef7-98a8-16a3ec24a46c',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '5bb1f160-c05d-4f70-a5ae-99c38804d134',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A0EV__tcga_brca',
        'subject_id': 'TCGA-A2-A0EV'
    },
    {
        'id': '512a8542-b554-42f2-b882-1f99d63e93b9',
        'identifier': [
            {'system': 'IDC', 'value': '512a8542-b554-42f2-b882-1f99d63e93b9'}
        ],
        'label': 'tasets-idc/512a8542-b554-42f2-b882-1f99d63e93b9.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:512a8542-b554-42f2-b882-1f99d63e93b9',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '5483cdf7-c65f-447f-85c3-8f80ddfe4c0b',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A06Z__tcga_brca',
        'subject_id': 'TCGA-A8-A06Z'
    },
    {
        'id': '632f29c8-72dc-4e9f-9bb6-146d4b201378',
        'identifier': [
            {'system': 'IDC', 'value': '632f29c8-72dc-4e9f-9bb6-146d4b201378'}
        ],
        'label': 'tasets-idc/632f29c8-72dc-4e9f-9bb6-146d4b201378.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:632f29c8-72dc-4e9f-9bb6-146d4b201378',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'cca97bb2-2863-454a-a347-5ba93bd2e285',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AR-A0U4__tcga_brca',
        'subject_id': 'TCGA-AR-A0U4'
    },
    {
        'id': '5a1728b2-5278-4af6-b0f8-1b4ec1b54913',
        'identifier': [
            {'system': 'IDC', 'value': '5a1728b2-5278-4af6-b0f8-1b4ec1b54913'}
        ],
        'label': 'tasets-idc/5a1728b2-5278-4af6-b0f8-1b4ec1b54913.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:5a1728b2-5278-4af6-b0f8-1b4ec1b54913',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'b08f5951-be66-4547-80be-6e8ef5481b82',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E9-A1NF__tcga_brca',
        'subject_id': 'TCGA-E9-A1NF'
    },
    {
        'id': '1a7701e6-74bc-483e-9e3f-4445b9770c25',
        'identifier': [
            {'system': 'IDC', 'value': '1a7701e6-74bc-483e-9e3f-4445b9770c25'}
        ],
        'label': 'tasets-idc/1a7701e6-74bc-483e-9e3f-4445b9770c25.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1a7701e6-74bc-483e-9e3f-4445b9770c25',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '21eb422e-3a47-47b2-94fb-677620e292b0',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-D8-A1JT__tcga_brca',
        'subject_id': 'TCGA-D8-A1JT'
    },
    {
        'id': '0113fcd0-80b0-4411-919c-694c78673d2b',
        'identifier': [
            {'system': 'IDC', 'value': '0113fcd0-80b0-4411-919c-694c78673d2b'}
        ],
        'label': 'tasets-idc/0113fcd0-80b0-4411-919c-694c78673d2b.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:0113fcd0-80b0-4411-919c-694c78673d2b',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '562199cf-7584-4b6d-ad00-6cbdf88a8de4',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A2-A0YI__tcga_brca',
        'subject_id': 'TCGA-A2-A0YI'
    },
    {
        'id': '1287f3ad-8c7b-409a-beed-df28afef3267',
        'identifier': [
            {'system': 'IDC', 'value': '1287f3ad-8c7b-409a-beed-df28afef3267'}
        ],
        'label': 'tasets-idc/1287f3ad-8c7b-409a-beed-df28afef3267.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:1287f3ad-8c7b-409a-beed-df28afef3267',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'dacfb6c5-5ba6-426d-88e6-49ba1a56f0b6',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A8-A0A7__tcga_brca',
        'subject_id': 'TCGA-A8-A0A7'
    },
    {
        'id': '820c0de4-6311-4eed-8209-ff574c174f3e',
        'identifier': [
            {'system': 'IDC', 'value': '820c0de4-6311-4eed-8209-ff574c174f3e'}
        ],
        'label': 'tasets-idc/820c0de4-6311-4eed-8209-ff574c174f3e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:820c0de4-6311-4eed-8209-ff574c174f3e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'ea0d48d9-8761-435a-bec6-92ab6d4d3ef0',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-A7-A4SD__tcga_brca',
        'subject_id': 'TCGA-A7-A4SD'
    },
    {
        'id': 'f2526368-e536-4485-9b1d-0d95bce89459',
        'identifier': [
            {'system': 'IDC', 'value': 'f2526368-e536-4485-9b1d-0d95bce89459'}
        ],
        'label': 'tasets-idc/f2526368-e536-4485-9b1d-0d95bce89459.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:f2526368-e536-4485-9b1d-0d95bce89459',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': 'ce4359c0-de27-474b-8e1e-2d1f3bde1181',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-GM-A2DD__tcga_brca',
        'subject_id': 'TCGA-GM-A2DD'
    },
    {
        'id': 'efbd881c-9fea-4d40-9233-13ba3eb35bcb',
        'identifier': [
            {'system': 'IDC', 'value': 'efbd881c-9fea-4d40-9233-13ba3eb35bcb'}
        ],
        'label': 'tasets-idc/efbd881c-9fea-4d40-9233-13ba3eb35bcb.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:efbd881c-9fea-4d40-9233-13ba3eb35bcb',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '39b7c366-1119-4575-819b-15973ad9afbc',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A107__tcga_brca',
        'subject_id': 'TCGA-E2-A107'
    },
    {
        'id': 'ec755eaf-eae5-4dce-abd5-fd4ea130fa9e',
        'identifier': [
            {'system': 'IDC', 'value': 'ec755eaf-eae5-4dce-abd5-fd4ea130fa9e'}
        ],
        'label': 'tasets-idc/ec755eaf-eae5-4dce-abd5-fd4ea130fa9e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:ec755eaf-eae5-4dce-abd5-fd4ea130fa9e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '28dee278-ed0a-4a1c-9751-4ace27f0c2c7',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-AQ-A04H__tcga_brca',
        'subject_id': 'TCGA-AQ-A04H'
    },
    {
        'id': 'cd39361c-2672-4b31-95f9-93b60efb2d7e',
        'identifier': [
            {'system': 'IDC', 'value': 'cd39361c-2672-4b31-95f9-93b60efb2d7e'}
        ],
        'label': 'tasets-idc/cd39361c-2672-4b31-95f9-93b60efb2d7e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:cd39361c-2672-4b31-95f9-93b60efb2d7e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '1bbff807-e2dc-4aaa-a13d-a6eec0907863',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E2-A15P__tcga_brca',
        'subject_id': 'TCGA-E2-A15P'
    },
    {
        'id': 'b4cde411-e3d3-4ce9-b9e0-2612cff51d2e',
        'identifier': [
            {'system': 'IDC', 'value': 'b4cde411-e3d3-4ce9-b9e0-2612cff51d2e'}
        ],
        'label': 'tasets-idc/b4cde411-e3d3-4ce9-b9e0-2612cff51d2e.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:b4cde411-e3d3-4ce9-b9e0-2612cff51d2e',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'MR',
        'dbgap_accession_number': None,
        'imaging_series': '41128946-2b5b-4d06-b86f-a472e1da39e0',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-EW-A1OY__tcga_brca',
        'subject_id': 'TCGA-EW-A1OY'
    },
    {
        'id': 'f98dbdd4-36f5-4c13-9d3b-37d44621b0db',
        'identifier': [
            {'system': 'IDC', 'value': 'f98dbdd4-36f5-4c13-9d3b-37d44621b0db'}
        ],
        'label': 'tasets-idc/f98dbdd4-36f5-4c13-9d3b-37d44621b0db.dcm',
        'data_category': 'Imaging',
        'data_type': None,
        'file_format': 'DICOM',
        'associated_project': 'tcga_brca',
        'drs_uri': 'drs://dg.4DFC:f98dbdd4-36f5-4c13-9d3b-37d44621b0db',
        'byte_size': None,
        'checksum': None,
        'data_modality': 'Imaging',
        'imaging_modality': 'SM',
        'dbgap_accession_number': None,
        'imaging_series': '14e01140-9fbb-4331-bb48-4ce4c8eea0d7',
        'researchsubject_specimen_id': '',
        'researchsubject_id': 'TCGA-E9-A1NF__tcga_brca',
        'subject_id': 'TCGA-E9-A1NF'
    }
]

fake = FakeResultData(result)
fake_result = Result(
                    api_response=fake.api_response,
                    query_id=fake.query_id,
                    offset=fake.offset,
                    limit=fake.limit,
                    api_instance=fake.api_instance,
                    show_sql=fake.show_sql,
                    show_count=fake.show_count,
                    format_type=fake.format_type,
                )
@mock.patch("cdapython.Q.run", return_value=fake_result)
def test_Down_house(a):
    q1 = Q('File.associated_project = "tcga_brca"')
    q2 = Q('File.associated_project = "TCGA-BRCA"')
    q3 = Q("days_to_birth < -50*365")
    q4 = Q('File.data_category = "Imaging"')
    q = q4.AND(q3.AND(q1.OR(q2)))
    t = q.file.run()
    qsub = t
    assert t is not None
    assert isinstance(t.to_list(), list) is True
    assert isinstance(qsub.to_dataframe(), DataFrame) is True



