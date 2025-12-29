from django.db import models

class PIESCode(models.Model):
    pies_code_id = models.IntegerField(db_column='PIESCodeID', primary_key=True)
    pies_code = models.CharField(db_column='PIESCode', max_length=10)
    description = models.CharField(db_column='Description', max_length=255)

    class Meta:
        db_table = 'PIESCode'
        ordering = ['pies_code_id']

    def __str__(self):
        return f"{self.pies_code} - {self.description}"