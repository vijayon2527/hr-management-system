import random
from faker import Faker
from django.core.management.base import BaseCommand
from job.models import Job, Industry, FunctionalArea, Role  # Adjust imports based on your app structure
from users.models import User  # Import User model

class Command(BaseCommand):
    help = 'Generate 1000 fake job entries with dynamic industry, functional area, and role'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetching employer-type users
        users = User.objects.filter(user_type=User.EMPLOYER)

        # Employment types list
        employment_types = [
            Job.EMPLOYMENT_TYPE_FULL_TIME,
            Job.EMPLOYMENT_TYPE_PART_TIME,
            Job.EMPLOYMENT_TYPE_FREELANCING,
            Job.EMPLOYMENT_TYPE_CONTRACT,
        ]

        # Country list
        countries = [Job.INDIA]  # You can add more countries here if needed

        count = 1000  # The number of fake jobs to generate

        # Ensure industries, functional areas, and roles are present in the database
        industries = list(Industry.objects.all())
        functional_areas = list(FunctionalArea.objects.all())
        roles = list(Role.objects.all())

        # Check if the required data is missing from the database
        if not industries or not functional_areas or not roles:
            self.stdout.write(self.style.ERROR(
                'Industries, Functional Areas, or Roles are missing in the database. Please populate them first.'
            ))
            return

        # Creating the fake jobs
        for _ in range(count):
            # Randomly select an industry, functional area, and role
            industry = random.choice(industries)
            functional_area = random.choice(
                FunctionalArea.objects.filter(industry=industry)  # Select functional areas for the chosen industry
            )
            role = random.choice(
                Role.objects.filter(functional_area=functional_area)  # Select roles for the chosen functional area
            )

            # Generate a fake job description
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

            # Creating the Job object with the dynamically generated data
            job = Job(
                slug=fake.slug(),
                job_title=fake.job(),
                role=role,  # Assign the Role instance
                job_description=job_description.strip(),
                min_salary=str(random.randint(30000, 150000)),
                max_salary=str(random.randint(150000, 200000)),
                min_experience=str(random.randint(1,2)),
                max_experience=str(random.randint(3,7)),
                
                no_of_openings=random.randint(1, 10),
                industry=industry,  # Assign the Industry instance
                functional_area=functional_area,  # Assign the FunctionalArea instance
                employment_type=random.choice(employment_types),
                country=random.choice(countries),
                city=fake.city(),
                visit_count=random.randint(1, 1000),
                job_applied_count=random.randint(1, 500),
                user=random.choice(users),  # Assign a random employer
                publish=fake.boolean(),
                recommended_job=fake.boolean(),
            )
            # Save the generated job entry
            job.save()

        # Success message once all jobs are generated
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} fake jobs with dynamic data!'))
