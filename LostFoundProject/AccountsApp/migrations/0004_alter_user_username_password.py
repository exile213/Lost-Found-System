from django.db import migrations, models
import django.contrib.auth.validators

class Migration(migrations.Migration):

    dependencies = [
        ('AccountsApp', '0003_remove_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                null=True,
                blank=True,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='username'
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(
                max_length=128,
                null=True,
                blank=True,
                verbose_name='password'
            ),
        ),
    ] 