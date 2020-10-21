from django.db import models

from django.contrib.auth.models import AbstractUser, Group

from django_oso.models import AuthorizedModel

class User(AbstractUser):
    @property
    def tag(self):
        return f"@{self.username}"

    def in_group(self, group):
        if group is None:
            return True

        return self.groups.filter(id=group.id).exists()

class Post(AuthorizedModel):
    ACCESS_PUBLIC = 0
    ACCESS_PRIVATE = 1
    ACCESS_LEVEL_CHOICES = [
        (ACCESS_PUBLIC, 'Public'),
        (ACCESS_PRIVATE, 'Private'),
    ]

    contents = models.CharField(max_length=140)

    access_level = models.IntegerField(choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC)

    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=('created_at',))]
