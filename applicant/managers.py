from django.db import models
from django.db.models import Q

class ApplicantQuerySet(models.QuerySet):
    def search(self, query, queryset):
        queryset = queryset.filter(Q(user__first_name__icontains=query)|
                                    Q(user__last_name__icontains=query) |
                                    Q(user__mobile__icontains=query) |
                                    Q(user__email__icontains=query) |
                                    Q(notice_period__icontains=query)
                                    )
        return queryset
    
    def all_applicant_lists(self, query, sorting_value):
        queryset = self.all()
        if sorting_value is not None:
            queryset=queryset.order_by(sorting_value)
        if query is None:
            return queryset
        else:
            return self.search(query, queryset)
    
class ApplicantManager(models.Manager):
    def get_queryset(self):
        return ApplicantQuerySet(self.model, using=self._db)
    
    def all_applicant_lists(self, query=None, sorting_value=None):
        return self.get_queryset().all_applicant_lists(query, sorting_value)
    

class ApplicationQuerySet(models.QuerySet):
    def search(self, query, queryset):
        queryset = queryset.filter(Q(applicant__user__first_name__icontains=query)|
                                    Q(applicant__user__last_name__icontains=query) |
                                    Q(applicant__user__mobile__icontains=query) |
                                    Q(applicant__user__email__icontains=query) |
                                    Q(applicant__notice_period__icontains=query)
                                    )
        return queryset
    
    def all_application_lists(self, query, sorting_value, employer=None, status=None):
        queryset = self.all()
        if employer:
            queryset = self.filter(job__user=employer)
        if status:
            queryset = queryset.filter(status=status)
        if sorting_value is not None:
            queryset=queryset.order_by(sorting_value)
        if query is None:
            return queryset
        else:
            return self.search(query, queryset)
    
class ApplicationManager(models.Manager):
    def get_queryset(self):
        return ApplicationQuerySet(self.model, using=self._db)
    
    def all_application_lists(self, query=None, sorting_value=None, employer=None, status=None):
        return self.get_queryset().all_application_lists(query, sorting_value, employer, status)