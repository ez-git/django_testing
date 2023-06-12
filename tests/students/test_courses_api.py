import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def students_factory():
    def factory(**kwargs):
        return baker.make('Student', **kwargs)

    return factory


@pytest.fixture
def courses_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)

    return factory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_url_courses():
    return 'http://127.0.0.1:8000/api/v1/courses/'


@pytest.mark.django_db
def test_first_course(api_client, api_url_courses, courses_factory):
    # создаем курс через фабрику;
    # строим урл и делаем запрос через тестовый клиент;
    # проверяем, что вернулся именно тот курс, который запрашивали;
    course = courses_factory()
    response = api_client.get(f'{api_url_courses}{course.id}/')
    assert response.status_code == 200
    assert course.name == response.json().get('name')


@pytest.mark.django_db
def test_get_courses(api_client, api_url_courses, courses_factory):
    # аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем
    # результат;
    courses = courses_factory(_quantity=10)
    response = api_client.get(api_url_courses)
    assert response.status_code == 200
    response_json = response.json()
    assert len(courses) == len(response_json)
    for list_index, course in enumerate(courses):
        assert course.name == response_json[list_index].get('name')


@pytest.mark.django_db
def test_filter_by_id(api_client, api_url_courses, courses_factory):
    # создаем курсы через фабрику, передать ID одного курса в фильтр,
    # проверить результат запроса с фильтром;
    courses = courses_factory(_quantity=10)
    for list_index, course in enumerate(courses):
        data = {'id': course.id}
        response = api_client.get(api_url_courses, data=data)
        assert response.status_code == 200
        response_json = response.json()
        assert course.name == response_json[0].get('name')


@pytest.mark.django_db
def test_filter_by_name(api_client, api_url_courses, courses_factory):
    courses = courses_factory(_quantity=10)
    for list_index, course in enumerate(courses):
        data = {'name': course.name}
        response = api_client.get(api_url_courses, data=data)
        assert response.status_code == 200
        response_json = response.json()
        assert course.id == response_json[0].get('id')


@pytest.mark.django_db
def test_create_course(api_client, api_url_courses):
    # здесь фабрика не нужна, готовим JSON-данные и создаём курс;
    test_name = 'test_course1'
    data = {'name': test_name}
    response = api_client.post(api_url_courses, data=data)
    assert response.status_code == 201
    assert response.json().get('name') == test_name


@pytest.mark.django_db
def test_refresh_course(api_client, api_url_courses, courses_factory):
    test_name = 'test_course1'
    course = courses_factory()
    data = {'name': test_name}
    response = api_client.patch(f'{api_url_courses}{course.id}/', data=data)
    assert response.status_code == 200
    assert response.json().get('name') == test_name


@pytest.mark.django_db
def test_delete_course(api_client, api_url_courses, courses_factory):
    course = courses_factory()
    response = api_client.delete(f'{api_url_courses}{course.id}/')
    assert response.status_code == 204
