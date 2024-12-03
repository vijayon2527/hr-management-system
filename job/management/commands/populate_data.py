from django.core.management.base import BaseCommand
from super_admin.models import Industry, FunctionalArea, Role


class Command(BaseCommand):
    help = "Populates industries, functional areas, and roles with predefined data."

    def handle(self, *args, **kwargs):
        data = {
            "IT": {
                "Software Development": [
                    "Software Engineer/Developer",
                    "Web Developer",
                    "Mobile App Developer",
                    "Full Stack Developer",
                    "Backend Developer",
                    "Frontend Developer",
                ],
                "Data Science and Analytics": [
                    "Data Analyst",
                    "Data Scientist",
                    "Business Intelligence Analyst",
                    "Data Engineer",
                    "Machine Learning Engineer",
                ],
                "Cybersecurity": [
                    "Security Analyst",
                    "Network Security Engineer",
                    "Information Security Specialist",
                    "Cybersecurity Consultant",
                ],
                "Network and Systems Administration": [
                    "Network Administrator",
                    "Systems Administrator",
                    "IT Support Specialist",
                    "Technical Support Engineer",
                ],
                "Cloud Computing": [
                    "Cloud Engineer",
                    "Cloud Consultant",
                    "Cloud Support Associate",
                ],
                "Quality Assurance and Testing": [
                    "Quality Assurance (QA) Engineer",
                    "Software Tester",
                    "Automation Test Engineer",
                ],
                "DevOps": [
                    "DevOps Engineer",
                    "Site Reliability Engineer (SRE)",
                ],
                "Project Management": [
                    "Project Coordinator",
                    "Scrum Master (entry-level)",
                ],
                "UI/UX Design": [
                    "UI Designer",
                    "UX Designer",
                    "Graphic Designer",
                ],
                "Digital Marketing": [
                    "Digital Marketing Executive",
                    "SEO Specialist",
                    "Content Marketing Associate",
                    "Social Media Manager",
                ],
            },
            "Non-IT": {
                "Finance and Accounting": [
                    "Accountant",
                    "Financial Analyst",
                    "Audit Associate",
                    "Tax Consultant",
                ],
                "Human Resources": [
                    "HR Executive",
                    "Recruitment Consultant",
                    "Payroll Executive",
                ],
                "Sales and Marketing": [
                    "Sales Executive",
                    "Marketing Executive",
                    "Business Development Executive",
                    "Brand Ambassador",
                ],
                "Operations Management": [
                    "Operations Executive",
                    "Supply Chain Coordinator",
                    "Logistics Executive",
                ],
                "Customer Service": [
                    "Customer Service Representative",
                    "Call Center Executive",
                    "Client Relations Associate",
                ],
                "Education and Training": [
                    "Teaching Assistant",
                    "Corporate Trainer (entry-level)",
                ],
                "Healthcare": [
                    "Medical Representative",
                    "Healthcare Assistant",
                    "Lab Technician (for BTech in Biotechnology)",
                ],
                "Research and Development": [
                    "Research Assistant",
                    "Laboratory Technician (for BTech in Chemical/Biomedical)",
                ],
                "Retail": [
                    "Store Manager (trainee)",
                    "Retail Sales Associate",
                ],
                "Hospitality and Tourism": [
                    "Front Desk Executive",
                    "Event Coordinator",
                    "Travel Consultant",
                ],
            },
        }

        for industry_name, functional_areas in data.items():
            industry, _ = Industry.objects.get_or_create(name=industry_name)
            for functional_area_name, roles in functional_areas.items():
                functional_area, _ = FunctionalArea.objects.get_or_create(
                    name=functional_area_name, industry=industry
                )
                for role_name in roles:
                    Role.objects.get_or_create(name=role_name, functional_area=functional_area)

        self.stdout.write(self.style.SUCCESS("Industries, functional areas, and roles populated successfully!"))
