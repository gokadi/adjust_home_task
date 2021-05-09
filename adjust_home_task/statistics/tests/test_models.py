import pytest
from mixer.backend.django import mixer

from adjust_home_task.statistics.models import Statistics

pytestmark = pytest.mark.django_db(transaction=True)


class TestStatistics:
    def test_str(self):
        statistics = mixer.blend(Statistics)

        assert (
            str(statistics) == (
                f'{statistics.date},{statistics.channel},'
                f'{statistics.country},{statistics.os},'
                f'{statistics.impressions},{statistics.clicks},'
                f'{statistics.installs},{statistics.spend},'
                f'{statistics.revenue}'
            )
        )
