from django.db import models

class Industry(models.Model):
    """Represents an industry such as IT, Finance, Healthcare, etc."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the unique name of the industry, e.g., 'Finance', 'IT'.",
        verbose_name="Industry Name",
        error_messages={
            'unique': "An industry with this name already exists.",
            'blank': "Industry name cannot be blank."
        }
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description providing an overview of the industry.",
        verbose_name="Industry Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Status",
        help_text="Check this box if the industry is currently active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    def __str__(self):
        return self.name


class FunctionalArea(models.Model):
    """Represents functional areas within an industry, like Development, Project Management, etc."""
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name='functional_areas',
        verbose_name="Associated Industry"
    )
    name = models.CharField(
        max_length=200,
        help_text="Enter the name of the functional area, e.g., 'Development'.",
        verbose_name="Functional Area Name",
        error_messages={
            'blank': "Functional area name cannot be blank."
        }
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description providing an overview of this functional area.",
        verbose_name="Functional Area Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Status",
        help_text="Check this box if the functional area is currently active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    def __str__(self):
        return f"{self.name} - {self.industry.name}"


class Role(models.Model):
    """Represents specific roles within a functional area, such as Frontend Developer, QA Engineer, etc."""
    functional_area = models.ForeignKey(
        FunctionalArea,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name="Associated Functional Area"
    )
    name = models.CharField(
        max_length=200,
        help_text="Enter the specific title of the role, e.g., 'QA Engineer'.",
        verbose_name="Role Name",
        error_messages={
            'blank': "Role title cannot be blank."
        }
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description of the role's responsibilities.",
        verbose_name="Role Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Status",
        help_text="Check this box if the role is currently active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )

    def __str__(self):
        return f"{self.name} ({self.functional_area.name})"
