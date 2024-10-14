import random
from faker import Faker
from django.core.management.base import BaseCommand
from job.models import Job  # Make sure to use the correct app name and import your Job model
from users.models import User  # Import User model

class Command(BaseCommand):
    help = 'Generate 1000 fake job entries'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.filter(user_type=User.EMPLOYER)  # You can customize this to select specific users if needed
        employement_types = [Job.EMPLOYEMENT_TYPE_FULL_TIME, Job.EMPLOYEMENT_TYPE_PART_TIME, Job.EMPLOYEMENT_TYPE_FREELANCING, Job.EMPLOYEMENT_TYPE_CONTRACT]
        countries = [Job.INDIA]
        count = 1000

        for _ in range(count):
            # Generate a structured job description similar to previous examples
            job_description = f"""
            Summary: As a {fake.job()}, you will {fake.sentence(nb_words=10)}. You will {fake.sentence(nb_words=10)} and ensure {fake.sentence(nb_words=8)}. Your role will involve collaborating with {fake.word()} and {fake.word()} to solve challenges.

            Roles & Responsibilities:
            - {fake.sentence(nb_words=12)}
            - {fake.sentence(nb_words=12)}
            - {fake.sentence(nb_words=12)}
            - {fake.sentence(nb_words=12)}
            - {fake.sentence(nb_words=12)}

            Professional & Technical Skills:
            - Must have skills: Proficiency in {fake.word()}
            - Strong understanding of {fake.sentence(nb_words=6)}
            - Familiarity with {fake.word()} development practices
            - Experience with version control systems such as Git
            - Knowledge of database systems and SQL

            Additional Information:
            - This position is based at our {fake.city()} office.
            - A 15 years full-time education is required.
            """
            
            job = Job(
                slug=fake.slug(),
                job_title=fake.job(),
                role=fake.bs(),
                job_description=job_description.strip(),
                experience=f"{random.randint(1, 10)} years",
                salary=str(random.randint(30000, 150000)),
                no_of_openings=random.randint(1, 10),
                industry=fake.company(),
                functional_area=fake.word(),
                employement_type=random.choice(employement_types),
                country=random.choice(countries),
                place=fake.city(),
                visit_count=random.randint(1, 1000),
                job_applied_count=random.randint(1, 500),
                user=random.choice(users),  # Assuming you have some users in the DB
                publish=fake.boolean(),
                recommended_job=fake.boolean(),
            )
            job.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} fake jobs'))
