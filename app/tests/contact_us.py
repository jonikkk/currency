from django.urls import reverse


def test_post_contact_us_empty_form_200(client):
    response = client.post(reverse('currency:contactus-create'))
    assert response.status_code == 200


def test_post_contact_us_empty_form_errors(client):
    response = client.post(reverse('currency:contactus-create'))
    assert response.context_data['form'].errors == {

        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_post_contact_us_invalid_email(client):
    payload = {

        'email_from': 'INVALID_EMAIL',
        'subject': 'Subject',
        'message': 'message'
    }
    response = client.post(reverse('currency:contactus-create'), data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email_from': ['Enter a valid email address.']
    }

# def test_post_contact_us_valid_data(client, mailoutbox):
#     initial_count = ContactUs.objects.count()
#     payload = {
#
#         'email_from': 'usr@mail.com',
#         'subject': 'Subject',
#         'message': 'message'
#     }
#     response = client.post(reverse('currency:contactus-create'), data=payload)
#     assert response.status_code == 302
#     assert response.headers['Location'] == '/'
#     assert len(mailoutbox) == 1
#     assert mailoutbox[0].from_email == settings.EMAIL_HOST_USER
#     assert ContactUs.objects.count() == initial_count + 1
