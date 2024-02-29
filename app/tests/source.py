from django.urls import reverse

from currency.models import Source


def test_post_source_empty_form_200(client):
    response = client.post(reverse('currency:source-create'))
    assert response.status_code == 200


def test_post_source_empty_form_errors(client):
    response = client.post(reverse('currency:source-create'))
    assert response.context_data['form'].errors == {
        'source_name': ['This field is required.'],
        'source_url': ['This field is required.']
    }


def test_post_source_create(client):
    initial_count = Source.objects.count()
    payload = {
        'source_name': 'source_name',
        'source_url': 'source_url'
    }
    response = client.post(reverse('currency:source-create'), data=payload)
    assert response.status_code == 302
    assert response.headers['Location'] == reverse('currency:source-list')
    assert Source.objects.count() == initial_count + 1
    source = Source.objects.last()
    assert source.source_name == payload['source_name']
    assert source.source_url == payload['source_url']


def test_post_source_update(client):
    source = Source.objects.create(
        source_name='source_name',
        source_url='source_url'
    )
    initial_count = Source.objects.count()
    payload = {
        'source_name': 'source_name_updated',
        'source_url': 'source_url_updated'
    }
    response = client.post(reverse('currency:source-update', kwargs={'pk': source.pk}), data=payload)
    assert response.status_code == 302
    assert response.headers['Location'] == reverse('currency:source-list')
    assert Source.objects.count() == initial_count
    source.refresh_from_db()
    assert source.source_name == payload['source_name']
    assert source.source_url == payload['source_url']


def test_post_source_delete(client):
    source = Source.objects.create(
        source_name='source_name',
        source_url='source_url'
    )
    initial_count = Source.objects.count()
    response = client.post(reverse('currency:source-delete', kwargs={'pk': source.pk}))
    assert response.status_code == 302
    assert response.headers['Location'] == reverse('currency:source-list')
    assert Source.objects.count() == initial_count - 1
    assert not Source.objects.filter(pk=source.pk).exists()


def test_get_source_list(client):
    response = client.get(reverse('currency:source-list'))
    assert response.status_code == 200
    assert response.context_data['object_list'].count() == Source.objects.count()


def test_get_source_details(client):
    source = Source.objects.create(
        source_name='source_name',
        source_url='source_url'
    )
    response = client.get(reverse('currency:source-details', kwargs={'pk': source.pk}))
    assert response.status_code == 200
    assert response.context_data['object'] == source
    assert response.context_data['object'].source_name == source.source_name
    assert response.context_data['object'].source_url == source.source_url
