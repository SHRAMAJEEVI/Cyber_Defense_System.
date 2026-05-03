from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from honeypot.models import AttackLog
import random


class Command(BaseCommand):
    help = 'Generate test attack logs for demonstration'

    def handle(self, *args, **options):
        # Clear existing logs
        AttackLog.objects.all().delete()
        
        # Expanded sample data for more variety
        ips = [
            '192.168.1.100', '10.0.0.15', '172.16.0.5', '203.0.113.1',
            '198.51.100.10', '192.0.2.50', '172.20.10.1', '10.1.1.1',
            '203.0.113.100', '198.51.100.200', '192.0.2.150', '172.16.0.25',
            '185.220.101.182', '185.220.102.182', '199.87.154.223', '199.87.154.234'
        ]
        
        usernames = ['admin', 'root', 'administrator', 'user', 'test', 'guest', 'oracle', 'postgres', 
                     'mysql', 'sa', 'nginx', 'apache', 'ftp', 'ssh', 'mail', 'webmaster', 'demo']
        
        passwords = ['password', '123456', 'admin', 'root', 'password123', 'qwerty', 'letmein', 'secret',
                     '12345678', 'abc123', 'password1', 'admin123', 'root123', 'test123', 'guest123',
                     'welcome', 'login', 'access', 'default', 'changeme', 'temp123']
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        ]
        
        attack_types = ['Brute Force', 'SQL Injection', 'XSS Attempt', 'Directory Traversal', 'Command Injection',
                       'Credential Stuffing', 'Password Spray', 'Dictionary Attack', 'Hybrid Attack']
        
        logs_created = 0
        used_combinations = set()
        
        # Generate unique logs with different timestamps
        for days_ago in range(30, 0, -1):  # 30 days ago to today
            for hour in range(24):  # Each hour
                for minute in range(0, 60, 15):  # Every 15 minutes
                    # Create unique combination
                    ip = random.choice(ips)
                    username = random.choice(usernames)
                    password = random.choice(passwords)
                    user_agent = random.choice(user_agents)
                    attack_type = random.choice(attack_types)
                    
                    # Create unique identifier
                    combo_id = f"{ip}_{username}_{password}_{days_ago}_{hour}_{minute}"
                    
                    if combo_id not in used_combinations:
                        timestamp = timezone.now() - timedelta(days=days_ago, hours=hour, minutes=minute)
                        
                        AttackLog.objects.create(
                            ip_address=ip,
                            username_attempted=username,
                            password_attempted=password,
                            timestamp=timestamp,
                            user_agent=user_agent,
                            attack_type=attack_type
                        )
                        used_combinations.add(combo_id)
                        logs_created += 1
                        
                        # Stop if we have enough logs
                        if logs_created >= 200:
                            break
                
                if logs_created >= 200:
                    break
            
            if logs_created >= 200:
                break
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {logs_created} unique test attack logs')
        )
