from datetime import date

from django.db import models


class Statistics(models.Model):
    ADCOLONY = "adcolony"
    APPLE_SEARCH_ADS = "apple_search_ads"
    CHARTBOOST = "chartboost"
    FACEBOOK = "facebook"
    GOOGLE = "google"
    UNITYADS = "unityads"
    VUNGLE = "vungle"
    CHANNEL_CHOICES = (
        (ADCOLONY, ADCOLONY),
        (APPLE_SEARCH_ADS, APPLE_SEARCH_ADS),
        (CHARTBOOST, CHARTBOOST),
        (FACEBOOK, FACEBOOK),
        (GOOGLE, GOOGLE),
        (UNITYADS, UNITYADS),
        (VUNGLE, VUNGLE),
    )

    CANADA = "CA"
    GERMANY = "DE"
    FRANCE = "FR"
    ENGLAND = "GB"
    USA = "US"
    COUNTRY_CHOICES = (
        (CANADA, "Canada"),
        (GERMANY, "Germany"),
        (FRANCE, "France"),
        (ENGLAND, "England"),
        (USA, "USA"),
    )

    IOS = 'ios'
    ANDROID = 'android'
    OS_CHOICES = (
        (IOS, IOS),
        (ANDROID, ANDROID),
    )

    date = models.DateField(default=date.today)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES)
    os = models.CharField(max_length=30, choices=OS_CHOICES)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self) -> str:
        return (
            f'{self.date},{self.channel},{self.country},{self.os},'
            f'{self.impressions},{self.clicks},{self.installs},'
            f'{self.spend},{self.revenue}'
        )

    class Meta:
        ordering = ('date',)
        verbose_name = 'statistics'
        verbose_name_plural = 'statistics'
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'channel', 'country', 'os'],
                name='unique report entry'
            )
        ]
