from django.db import models

class TemperatureRecord(models.Model):
    t0 = models.FloatField()
    h0 = models.FloatField()
    t1 = models.FloatField()
    h1 = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return "TR(%s, t0=%5.2f t1=%5.2f h0=%5.2f h1=%5.2f)" % (
            self.time.isoformat(),
            self.t0, self.t1, self.h0, self.h1
        )
