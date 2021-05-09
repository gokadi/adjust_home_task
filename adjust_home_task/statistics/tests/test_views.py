import json

import pytest
from django.template.response import SimpleTemplateResponse
from pytest_mock import MockFixture

from adjust_home_task.statistics.views import get_report

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture(autouse=True, scope="module")
def mock_fetching_from_google(module_mocker):
    module_mocker.patch('adjust_home_task.statistics.utils.filter_statistics')
    module_mocker.patch('adjust_home_task.statistics.utils.group_statistics')
    module_mocker.patch('adjust_home_task.statistics.utils.sort_statistics')
    module_mocker.patch('adjust_home_task.statistics.utils.get_report_data')


class TestGetReport:
    def test_get_report_non_get_method_405(self, mocker: MockFixture):
        response = get_report(mocker.Mock(method='POST'))

        assert response.status_code == 405

    def test_get_report_invalid_params_should_return_400(
        self, mocker: MockFixture
    ):
        response = get_report(
            mocker.Mock(method='GET', GET={'group_by': 'bad value'})
        )

        assert response

    def test_get_report_valid_params_download_mode(self, mocker: MockFixture):
        response = get_report(
            mocker.Mock(method='GET', GET={'view_mode': 'download'})
        )

        assert (
            'attachment; filename="report_' in response['Content-Disposition']
        )

    def test_get_report_valid_params_ui_mode(self, mocker: MockFixture):
        response = get_report(
            mocker.Mock(method='GET', GET={'view_mode': 'ui'})
        )

        assert isinstance(response, SimpleTemplateResponse)
        assert response.template_name == 'report.html'

    def test_get_report_valid_params_api_mode(self, mocker: MockFixture):
        response = get_report(mocker.Mock(method='GET', GET={}))

        assert response.content == bytes(
            json.dumps({
                'report': 'date,channel,country,os,impressions,clicks,'
                          'installs,spend,revenue,cpi\n'
            }),
            encoding='utf-8'
        )
