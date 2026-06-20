from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from honeypot.models import AttackLog
import random


class Command(BaseCommand):
    help = 'Reset all attacks and simulate gradual attack increase'

    def handle(self, *args, **options):
        # Clear existing logs
        AttackLog.objects.all().delete()
        
        # Simple dummy data
        ips = ['192.168.1.100', '10.0.0.15', '172.16.0.5', '203.0.113.1']
        usernames = ['admin', 'root', 'user', 'test']
        passwords = ['password', '123456', 'admin', 'test']
        user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0']
        attack_types = ['Brute Force', 'SQL Injection', 'XSS Attempt']
        
        logs_created = 0
        
        # Simulate gradual attack increase over last 7 days
        for days_ago in range(7, 0, -1):  # 7 days ago to yesterday
            # Increase attacks each day: 1, 2, 3, 5, 8, 12, 20
            if days_ago == 7:
                attacks_today = 1
            elif days_ago == 6:
                attacks_today = 2
            elif days_ago == 5:
                attacks_today = 3
            elif days_ago == 4:
                attacks_today = 5
            elif days_ago == 3:
                attacks_today = 8
            elif days_ago == 2:
                attacks_today = 12
            else:  # yesterday
                attacks_today = 20
            
            # Create attacks for this day
            for i in range(attacks_today):
                timestamp = timezone.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
                
                AttackLog.objects.create(
                    ip_address=random.choice(ips),
                    username_attempted=random.choice(usernames),
                    password_attempted=random.choice(passwords),
                    timestamp=timestamp,
                    user_agent=random.choice(user_agents),
                    attack_type=random.choice(attack_types)
                )
                logs_created += 1
        
        # Add some recent attacks (today)
        for hours_ago in range(12, 0, -1):  # Last 12 hours
            # More recent attacks
            for i in range(random.randint(1, 3)):
                timestamp = timezone.now() - timedelta(hours=hours_ago)
                
                AttackLog.objects.create(
                    ip_address=random.choice(ips),
                    username_attempted=random.choice(usernames),
                    password_attempted=random.choice(passwords),
                    timestamp=timestamp,
                    user_agent=random.choice(user_agents),
                    attack_type=random.choice(attack_types)
                )
                logs_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {logs_created} simulated attacks (starting from 0)')
        )
        
        # Show daily breakdown
        self.stdout.write('\nDaily Attack Simulation:')
        self.stdout.write('Day 7: 1 attack')
        self.stdout.write('Day 6: 2 attacks')
        self.stdout.write('Day 5: 3 attacks')
        self.stdout.write('Day 4: 5 attacks')
        self.stdout.write('Day 3: 8 attacks')
        self.stdout.write('Day 2: 12 attacks')
        self.stdout.write('Day 1: 20 attacks')
        self.stdout.write('Today: ~18 attacks (last 12 hours)')
