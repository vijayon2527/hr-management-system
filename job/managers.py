from django.db import models
from django.db.models import Q
import operator
from functools import reduce
from datetime import date, timedelta
from django.shortcuts import get_object_or_404

class SkillQuerySet(models.QuerySet):
    
    def search(self, query, queryset):
        queryset = queryset.filter(Q(name=query))
        return queryset

    def skill_lists(self, query, sorting_value):
        queryset = self.all()
        if sorting_value is not None:
            queryset=queryset.order_by(sorting_value)
        if query is None:
            return queryset
        else:
            return self.search(query, queryset)
        
    def skill_detail(self, pk):
        return get_object_or_404(self, pk=pk)
        
class SkillManager(models.Manager):
    def get_queryset(self):
        return SkillQuerySet(self.model, using=self._db)
    
    def skill_lists(self, query, sorting_value):
        return self.get_queryset().skill_lists(query, sorting_value)
    
    def skill_detail(self, pk):
        return self.get_queryset().skill_detail(pk)
    

class JobQuerySet(models.QuerySet):
    
    def search(self, query, queryset):
        if isinstance(query, list):
            query = (Q(reduce(operator.or_, (Q(place=option) for option in query)))) | \
                    (Q(reduce(operator.or_, (Q(job_title=option) for option in query)))) | \
                    (Q(reduce(operator.or_, (Q(skills__name=option) for option in query))))
            queryset = queryset.filter(query).order_by("-id")
            return queryset

        queryset = queryset.filter(Q(job_title__icontains=query)|
                                    Q(role__icontains=query)|
                                    Q(country__icontains=query)|
                                    Q(place__icontains=query)
                                    )
        return queryset

    def all_job_lists(self, query, sorting_value, user=None):
        queryset = self.filter(user=user).order_by("-id") if user else self.all().order_by("-id")
        if sorting_value:
            queryset = queryset.order_by(sorting_value)
        return self.search(query, queryset) if query else queryset
    
    # def published_job_lists(self, query=None, user=None):
    #     queryset = self.filter(publish=True, user=user).order_by("-id") if user else self.filter(publish=True).order_by("-id")
    #     return self.search(query, queryset) if query else queryset

    def published_job_lists(self, query=None, user=None):
        queryset = self.filter(publish=True).order_by("-id")
        return self.search(query, queryset) if query else queryset
        
    def unpublished_job_lists(self, user=None):
        return self.filter(publish=False, user=user).order_by("-id") if user else self.filter(publish=False).order_by("-id")

    def job_detail(self, slug, user=None):
        return self.get(slug=slug, user=user) if user else self.get(slug=slug)

    def get_filtered_data(self, salary, freshness, experience, country, user=None):
        queryset = self.filter(user=user) if user else self.published_job_lists()
        today =  date.today()
        filter_day = None
        if freshness == 'Last one day':
            filter_day = today-timedelta(days=1)
        
        if freshness == 'Last three days':
            filter_day = today-timedelta(days=3)
        
        if freshness == 'Last seven days':
            filter_day = today-timedelta(days=7)

        if freshness == 'Last fifteen days':
            filter_day = today-timedelta(days=15)
        
        if freshness == 'Last thirty days':
            filter_day = today-timedelta(days=30)

        queryset = self.published_job_lists()
        if freshness:
            queryset = queryset.filter(Q(published_at__gte=filter_day))

        if country:
            query = (Q(reduce(operator.or_, (Q(country__icontains=option) for option in country))))
            queryset = queryset.filter(query)

        # if salary:
        #     queryset = queryset.filter(salary__icontains=salary)

        # if experience:
        #     queryset = queryset.filter(Q(experience__icontains=experience))

        queryset = queryset.order_by('-published_at')
        return queryset
    
    def recommended_jobs(self):
        jobs = self.filter(recommended_job=True)[:24]
        if not jobs:
            jobs = self.published_job_lists()[:8]
        return jobs
    
    def toggle_recommended_jobs(self, slug, user=None):
        job = self.get(slug=slug, user=user)
        if job.recommended_job == True:
            job.recommended_job = False
        else:
            job.recommended_job = True
        job.save()
        return
    

class JobManager(models.Manager):
    
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def all_job_lists(self, query=None, sorting_value=None, user=None):
        return self.get_queryset().all_job_lists(query, sorting_value, user)

    def published_job_lists(self, query=None, user=None):
        return self.get_queryset().published_job_lists(query, user)

    def unpublished_job_lists(self, user=None):
        return self.get_queryset().unpublished_job_lists(user)

    def job_detail(self, slug, user=None):
        return self.get_queryset().job_detail(slug, user)

    def get_filtered_data(self, salary=None, freshness=None, experience=None, country=[], user=None):
        return self.get_queryset().get_filtered_data(salary, freshness, experience, country, user)
    
    def recommended_jobs(self, user=None):
        return self.get_queryset().recommended_jobs(user)

    def toggle_recommended_jobs(self, slug, user=None):
        return self.get_queryset().toggle_recommended_jobs(slug=slug, user=user)


class JobApplicantQuerySet(models.QuerySet):

    def search(self, query, queryset):
        queryset = queryset.filter(Q(user__first_name__icontains=query)|
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
    
    
class JobApplicantManager(models.Manager):
    def get_queryset(self):
        return JobApplicantQuerySet(self.model, using=self._db)
    
    def all_applicant_lists(self, query=None, sorting_value=None):
        return self.get_queryset().all_applicant_lists(query, sorting_value)