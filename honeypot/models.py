from django.db import models


class RegisteredUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # In production, use hashed passwords
    created_at = models.DateTimeField(auto_now_add=True)
    failed_attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} - Created: {self.created_at}"


class AttackLog(models.Model):
    USER_TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('Suspicious', 'Suspicious'),
        ('Attacker', 'Attacker'),
    ]
    
    ip_address = models.CharField(max_length=45)
    username_attempted = models.CharField(max_length=100)
    password_attempted = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    user_agent = models.TextField()
    attack_type = models.CharField(max_length=50, default="Brute Force")
    
    # New fields for classification system
    threat_score = models.IntegerField(default=0)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Normal')
    attack_reason = models.TextField(blank=True, help_text="Reason for classification")
    is_attacker = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        # Prevent exact duplicates within the same minute
        unique_together = [
            ['ip_address', 'username_attempted', 'password_attempted', 'timestamp']
        ]

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp} - {self.user_type}"
