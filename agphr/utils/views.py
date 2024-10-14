from django.views.generic import RedirectView
from django.urls import reverse
from users.models import User

class RootView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_type = self.request.user.user_type
            if user_type == User.SUPER_ADMIN:
                next_url = 'super_admin:super_admin_analytics'
            elif user_type == User.EMPLOYER:
                next_url = 'employer:employer_dashboard'
            elif user_type == User.APPLICANT_USER:
                next_url = 'applicant:applicant_dashboard'
        else:
            next_url = 'job:job_list'

        try:
            return reverse(next_url)
        except Exception as e:
            print(f"Error resolving URL: {e}")
            return reverse('job:job_list')
