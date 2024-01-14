from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject)
    birthDate = models.DateField()
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    birthPlace = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    password = models.CharField(max_length=100)
    birthDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"