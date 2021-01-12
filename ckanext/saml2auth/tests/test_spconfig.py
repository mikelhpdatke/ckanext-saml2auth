# encoding: utf-8
import pytest

from ckanext.saml2auth.spconfig import get_config

NAME_ID_FORMAT = u'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent urn:oasis:names:tc:SAML:2.0:nameid-format:transient'


@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.location', u'local')
@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.local_path', '/path/to/idp.xml')
def test_read_metadata_local_config():
    assert get_config()[u'metadata'][u'local'] == ['/path/to/idp.xml']


@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.location', u'remote')
def test_read_metadata_remote_config():
    with pytest.raises(KeyError):
        assert get_config()[u'metadata'][u'local']

    assert get_config()[u'metadata'][u'remote']


@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.location', u'remote')
@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.remote_url', u'https://metadata.com')
@pytest.mark.ckan_config(u'ckanext.saml2auth.idp_metadata.remote_cert', u'/path/to/local.cert')
def test_read_metadata_remote_url():
    with pytest.raises(KeyError):
        assert get_config()[u'metadata'][u'local']

    remote = get_config()[u'metadata'][u'remote'][0]
    assert remote[u'url'] == u'https://metadata.com'
    assert remote[u'cert'] == u'/path/to/local.cert'


@pytest.mark.ckan_config(u'ckanext.saml2auth.want_response_signed', u'False')
@pytest.mark.ckan_config(u'ckanext.saml2auth.want_assertions_signed', u'True')
@pytest.mark.ckan_config(u'ckanext.saml2auth.want_assertions_or_response_signed', u'True')
def test_signed_settings():

    cfg = get_config()
    assert not cfg[u'service'][u'sp'][u'want_response_signed']
    assert cfg[u'service'][u'sp'][u'want_assertions_signed']
    assert cfg[u'service'][u'sp'][u'want_assertions_or_response_signed']


@pytest.mark.ckan_config(u'ckanext.saml2auth.key_file_path', u'/path/to/mykey.pem')
@pytest.mark.ckan_config(u'ckanext.saml2auth.cert_file_path', u'/path/to/mycert.pem')
@pytest.mark.ckan_config(u'ckanext.saml2auth.attribute_map_dir', u'/path/to/attribute_map_dir')
def test_paths():

    cfg = get_config()
    assert cfg[u'key_file'] == u'/path/to/mykey.pem'
    assert cfg[u'cert_file'] == u'/path/to/mycert.pem'
    assert cfg[u'encryption_keypairs'] == [{u'key_file': '/path/to/mykey.pem', u'cert_file': '/path/to/mycert.pem'}]
    assert cfg[u'attribute_map_dir'] == '/path/to/attribute_map_dir'


@pytest.mark.ckan_config(u'ckanext.saml2auth.name_id_format', NAME_ID_FORMAT)
def test_name_id_policy_format_is_a_string():

    name_id_policy_format = get_config()[u'service'][u'sp'][u'name_id_policy_format']
    assert name_id_policy_format  == NAME_ID_FORMAT.split(' ')[0]


@pytest.mark.ckan_config(u'ckanext.saml2auth.entity_id', u'some:entity_id')
def test_read_entity_id():

    entity_id = get_config()[u'entityid']
    assert entity_id == u'some:entity_id'
