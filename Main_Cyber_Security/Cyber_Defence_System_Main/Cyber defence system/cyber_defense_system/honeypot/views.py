from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .models import AttackLog, RegisteredUser
from .forms import LoginForm, RegisterForm


def home(request):
    """Home page with navigation to honeypot and dashboard"""
    return render(request, 'index.html')


def honeypot_login(request):
    """Enhanced login page with registration and attack detection"""
    login_form = LoginForm()
    register_form = RegisterForm()
    message = ""
    
    if request.method == 'POST':
        # Determine if this is a registration or login attempt
        if 'register' in request.POST:
            # Registration logic
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                
                # Check if username already exists
                if RegisteredUser.objects.filter(username=username).exists():
                    register_form.add_error('username', 'Username already exists')
                else:
                    # Create new user
                    RegisteredUser.objects.create(username=username, password=password)
                    message = "Registration successful! Please login."
                    register_form = RegisterForm()  # Reset form
        else:
            # Login logic
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # Get login information
                ip_address = request.META.get('REMOTE_ADDR')
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                website = login_form.cleaned_data.get('website', '')  # Hidden honeypot field
                form_submit_time = float(request.POST.get('form_submit_time', 0))
                user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
                
                # STEP 1: Check for attack patterns FIRST
                attack_patterns = [
                    "'", ";", "--", "or 1=1", "' OR '1'='1", "union select", 
                    "drop table", "insert into", "delete from", "update set",
                    "<script>", "</script>", "javascript:", "onerror=", "onload=", "alert("
                ]
                
                enumeration_usernames = ['guest', 'admin', 'administrator']
                combined_input = (username + " " + password).lower()
                
                attack_detected = False
                attack_type = "Brute Force"
                
                # Check for attack patterns
                for pattern in attack_patterns:
                    if pattern in combined_input:
                        attack_detected = True
                        if "'" in pattern or ";" in pattern or "--" in pattern or "or 1=1" in pattern:
                            attack_type = "SQL Injection"
                        elif "<script>" in pattern or "javascript:" in pattern:
                            attack_type = "XSS Attempt"
                        break
                
                # Check for username enumeration
                if not attack_detected and username.lower() in enumeration_usernames:
                    attack_detected = True
                    attack_type = "Username Enumeration"
                
                                
                # Check honeypot field
                if not attack_detected and website.strip():
                    attack_detected = True
                    attack_type = "Honeypot Trigger"
                
                # Rainbow Table Attack Detection
                if not attack_detected:
                    # Check for multiple different password attempts for same username from same IP
                    recent_attempts = AttackLog.objects.filter(
                        ip_address=ip_address,
                        username_attempted=username,
                        timestamp__gte=timezone.now() - timedelta(minutes=5)
                    ).count()
                    
                    if recent_attempts >= 5:
                        attack_detected = True
                        attack_type = "Rainbow Table Attack"
                
                # Password Spray Attack Detection
                if not attack_detected:
                    # Check for single common password used across many different usernames from same IP
                    spray_passwords = ['password', '123456', 'admin', 'welcome', 'password123']
                    spray_attempts = AttackLog.objects.filter(
                        ip_address=ip_address,
                        password_attempted__in=spray_passwords,
                        timestamp__gte=timezone.now() - timedelta(minutes=10)
                    ).count()
                    
                    if spray_attempts >= 3:
                        attack_detected = True
                        attack_type = "Password Spray Attack"
                
                # Dictionary Attack Detection (selective - only obvious attacks)
                if not attack_detected:
                    # Only flag extremely common passwords with common usernames
                    extremely_common_passwords = [
                        '123456', 'password', '123456789', '12345678', '12345', '1234567',
                        '1234567890', '1234', 'qwerty', 'abc123', 'password123', 'admin',
                        'letmein', 'welcome', 'monkey', 'dragon', 'master', 'sunshine'
                    ]
                    
                    # Only trigger if password is extremely common AND username is suspicious
                    if (password.lower() in extremely_common_passwords and 
                        username.lower() in ['admin', 'root', 'administrator', 'guest', 'test']):
                        attack_detected = True
                        attack_type = "Dictionary Attack"
                    
                    # Also flag extremely weak passwords (length < 5, all same character)
                    elif (len(password) < 5 and len(set(password)) == 1):
                        attack_detected = True
                        attack_type = "Dictionary Attack"
                
                # Hybrid Attack Detection (selective - only obvious patterns)
                if not attack_detected:
                    import re
                    
                    # Only check for very obvious hybrid attack patterns
                    obvious_hybrid_patterns = [
                        # Clear attack patterns: common base words + numbers
                        r'^(admin|root|password|welcome|test|login|user)\d{2,4}$',
                        r'^\d{2,4}(admin|root|password|welcome|test|login|user)$',
                        # Only obvious leet speak
                        r'^(p[4@]ssw[0o]rd|[@4]dm[1i]n|w[3e]lc[0o]m[3e])$',
                        # Only very common keyboard patterns
                        r'^(qwerty123|123qwerty|asdf123|123asdf|zxcv123|123zxcv)$'
                    ]
                    
                    for pattern in obvious_hybrid_patterns:
                        if re.search(pattern, password.lower()):
                            attack_detected = True
                            attack_type = "Hybrid Attack"
                            break
                
                # Check for bot indicators
                if not attack_detected:
                    bot_indicators = ["curl", "python", "requests", "selenium", "postman", "wget", "bot", "crawler"]
                    user_agent_lower = user_agent.lower()
                    for indicator in bot_indicators:
                        if indicator in user_agent_lower:
                            attack_detected = True
                            attack_type = "Bot Attack"
                            break
                
                # IF attack detected: log as attacker and return generic error
                if attack_detected:
                    now = timezone.now()
                    AttackLog.objects.create(
                        ip_address=ip_address,
                        username_attempted=username,
                        password_attempted=password,
                        timestamp=now,
                        user_agent=user_agent,
                        attack_type=attack_type,
                        threat_score=15,
                        user_type="Attacker",
                        attack_reason=f"<li>{attack_type} detected</li>",
                        is_attacker=True
                    )
                    login_form.add_error(None, "Invalid credentials.")
                    return render(request, 'honeypot_login.html', {
                        'login_form': login_form,
                        'register_form': register_form,
                        'message': message
                    })
                
                # STEP 2: Check if user is registered
                try:
                    registered_user = RegisteredUser.objects.get(username=username)
                    
                    # Check if user is blocked
                    if registered_user.is_blocked:
                        login_form.add_error(None, "Invalid credentials.")
                        return render(request, 'honeypot_login.html', {
                            'login_form': login_form,
                            'register_form': register_form,
                            'message': message
                        })
                    
                    # STEP 3: Check password
                    if registered_user.password == password:
                        # Successful login - reset failed attempts
                        registered_user.failed_attempts = 0
                        registered_user.save()
                        return redirect("https://artisan-market-place.onrender.com/")
                    else:
                        # Wrong password - increase failed attempts
                        registered_user.failed_attempts += 1
                        
                        # Check if failed attempts >= 3 (classify as attacker)
                        if registered_user.failed_attempts >= 3:
                            registered_user.is_blocked = True
                            registered_user.save()
                            
                            # Log as brute force attacker
                            now = timezone.now()
                            AttackLog.objects.create(
                                ip_address=ip_address,
                                username_attempted=username,
                                password_attempted=password,
                                timestamp=now,
                                user_agent=user_agent,
                                attack_type="Brute Force",
                                threat_score=12,
                                user_type="Attacker",
                                attack_reason="<li>Multiple failed login attempts (Brute Force)</li>",
                                is_attacker=True
                            )
                            login_form.add_error(None, "Invalid credentials.")
                        else:
                            registered_user.save()
                            login_form.add_error(None, "Invalid credentials.")
                        
                except RegisteredUser.DoesNotExist:
                    # User not registered - show "Please register first"
                    login_form.add_error(None, "Please register first")
    
    return render(request, 'honeypot_login.html', {
        'login_form': login_form,
        'register_form': register_form,
        'message': message
    })


def dashboard(request):
    """Admin dashboard with attack statistics and classification breakdown"""
    # Get basic statistics
    total_attacks = AttackLog.objects.count()
    unique_ips = AttackLog.objects.values('ip_address').distinct().count()
    
    # Get classification statistics
    normal_users = AttackLog.objects.filter(user_type='Normal').count()
    suspicious_users = AttackLog.objects.filter(user_type='Suspicious').count()
    attackers = AttackLog.objects.filter(user_type='Attacker').count()
    
    # Get attacks in different time periods
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    recent_attacks = AttackLog.objects.filter(timestamp__gte=last_24h).count()
    weekly_attacks = AttackLog.objects.filter(timestamp__gte=last_7d).count()
    monthly_attacks = AttackLog.objects.filter(timestamp__gte=last_30d).count()
    
    # Latest attacks with classification
    latest_attacks = AttackLog.objects.all()[:10]
    
    # Classification breakdown for table
    classification_table = AttackLog.objects.all().order_by('-timestamp')[:20]
    
    # Detect brute force attacks (more than 5 attempts from same IP)
    brute_force_ips = AttackLog.objects.values('ip_address').annotate(
        attempt_count=Count('id')
    ).filter(attempt_count__gt=5).order_by('-attempt_count')
    
    # Get daily attack data for chart
    last_7d_data = []
    for i in range(7):
        day_start = now - timedelta(days=i+1)
        day_end = now - timedelta(days=i)
        count = AttackLog.objects.filter(
            timestamp__gte=day_start,
            timestamp__lt=day_end
        ).count()
        last_7d_data.append({
            'day': day_start.strftime('%m/%d'),
            'count': count
        })
    
    # Get attack type breakdown
    attack_types = AttackLog.objects.values('attack_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Get top attacker IPs
    top_ips = AttackLog.objects.values('ip_address').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Get most targeted usernames
    top_usernames = AttackLog.objects.values('username_attempted').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Calculate attack rate (attacks per hour in last 24h)
    if recent_attacks > 0:
        attack_rate = round(recent_attacks / 24, 1)
    else:
        attack_rate = 0
    
    # Get most active hour
    most_active_hour = AttackLog.objects.extra(
        select={'hour': "strftime('%%H', timestamp)"}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    context = {
        'total_attacks': total_attacks,
        'unique_ips': unique_ips,
        'normal_users': normal_users,
        'suspicious_users': suspicious_users,
        'attackers': attackers,
        'recent_attacks': recent_attacks,
        'weekly_attacks': weekly_attacks,
        'monthly_attacks': monthly_attacks,
        'latest_attacks': latest_attacks,
        'classification_table': classification_table,
        'brute_force_ips': brute_force_ips,
        'daily_data': list(reversed(last_7d_data)),
        'attack_types': list(attack_types),
        'top_ips': list(top_ips),
        'top_usernames': list(top_usernames),
        'attack_rate': attack_rate,
        'most_active_hour': most_active_hour,
    }
    
    return render(request, 'dashboard.html', context)


def attack_logs(request):
    """Page showing recent attack logs (last 24 hours)"""
    # Get recent logs (last 24 hours)
    last_24h = timezone.now() - timedelta(hours=24)
    logs = AttackLog.objects.filter(timestamp__gte=last_24h).order_by('-timestamp')
    
    # Get filter parameters
    ip_filter = request.GET.get('ip')
    if ip_filter:
        logs = logs.filter(ip_address__icontains=ip_filter)
    
    # Calculate statistics
    unique_ips = logs.values('ip_address').distinct().count()
    unique_users = logs.values('username_attempted').distinct().count()
    attack_types = logs.values('attack_type').distinct().count()
    
    context = {
        'logs': logs,
        'ip_filter': ip_filter or '',
        'unique_ips': unique_ips,
        'unique_users': unique_users,
        'attack_types': attack_types,
        'showing_recent': True,
    }
    
    return render(request, 'logs.html', context)


def previous_logs(request):
    """Page showing old attack logs (before last 24 hours)"""
    # Get logs older than 24 hours
    last_24h = timezone.now() - timedelta(hours=24)
    logs = AttackLog.objects.filter(timestamp__lt=last_24h).order_by('-timestamp')
    
    # Get filter parameters first
    ip_filter = request.GET.get('ip')
    if ip_filter:
        logs = logs.filter(ip_address__icontains=ip_filter)
    
    # Calculate statistics before pagination
    unique_ips = logs.values('ip_address').distinct().count()
    unique_users = logs.values('username_attempted').distinct().count()
    attack_types = logs.values('attack_type').distinct().count()
    
    # Pagination after filtering
    paginator = Paginator(logs, 25)  # 25 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'logs': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'ip_filter': ip_filter or '',
        'unique_ips': unique_ips,
        'unique_users': unique_users,
        'attack_types': attack_types,
        'showing_recent': False,
        'total_old_logs': logs.count(),
    }
    
    return render(request, 'logs.html', context)


def attacker_types(request):
    """Page displaying detailed information about different types of attackers"""
    
    attacker_data = [
        {
            'name': 'SQL Injection Attackers',
            'icon': 'fa-database',
            'color': '#ff006e',
            'description': 'Attackers who attempt to inject malicious SQL code into database queries.',
            'patterns': ["'", ';', '--', 'or 1=1', "' OR '1'='1", 'union select', 'drop table'],
            'motivation': 'Data theft, database manipulation, information extraction',
            'detection': 'Pattern matching in input fields',
            'threat_level': 'High',
            'examples': [
                "username: admin' OR '1'='1",
                "password: '; DROP TABLE users; --"
            ]
        },
        {
            'name': 'XSS Attackers',
            'icon': 'fa-code',
            'color': '#ff4081',
            'description': 'Attackers who inject malicious scripts into web pages viewed by other users.',
            'patterns': ['<script>', '</script>', 'javascript:', 'onerror=', 'onload=', 'alert('],
            'motivation': 'Session hijacking, defacement, phishing, malware distribution',
            'detection': 'Script tag detection in input fields',
            'threat_level': 'High',
            'examples': [
                "username: <script>alert('XSS')</script>",
                "password: javascript:alert('XSS')"
            ]
        },
                {
            'name': 'Dictionary Attackers',
            'icon': 'fa-book',
            'color': '#00ff88',
            'description': 'Attackers who use lists of extremely common passwords to gain unauthorized access.',
            'patterns': ['123456', 'password', 'admin', 'welcome', 'qwerty', 'abc123'],
            'motivation': 'Quick credential theft using common passwords',
            'detection': 'Extremely common password with suspicious username',
            'threat_level': 'Medium',
            'examples': [
                "username: admin, password: password123",
                "username: root, password: 123456"
            ]
        },
        {
            'name': 'Hybrid Attackers',
            'icon': 'fa-random',
            'color': '#00cc6a',
            'description': 'Attackers who combine common words with numbers or symbols to bypass simple security.',
            'patterns': ['admin123', 'password2024', 'p@ssw0rd', 'qwerty123'],
            'motivation': 'Bypass basic password policies',
            'detection': 'Obvious word + number/symbol combinations',
            'threat_level': 'Medium',
            'examples': [
                "username: admin, password: admin123",
                "username: user, password: password2024"
            ]
        },
        {
            'name': 'Brute Force Attackers',
            'icon': 'fa-hammer',
            'color': '#ff6b6b',
            'description': 'Attackers who try many different combinations of usernames and passwords.',
            'patterns': ['Repeated attempts', 'Sequential passwords', 'Common variations'],
            'motivation': 'Systematic credential discovery, account takeover',
            'detection': 'High frequency attempts from same IP',
            'threat_level': 'Medium',
            'examples': [
                "Multiple login attempts with different passwords",
                "Sequential password variations"
            ]
        },
        {
            'name': 'Username Enumeration Attackers',
            'icon': 'fa-search',
            'color': '#f39c12',
            'description': 'Attackers who probe for valid usernames using common administrative accounts.',
            'patterns': ['admin', 'root', 'administrator', 'guest'],
            'motivation': 'User discovery, reconnaissance, targeted attacks',
            'detection': 'Common username matching',
            'threat_level': 'Low-Medium',
            'examples': [
                "username: admin, password: test",
                "username: root, password: password"
            ]
        }
    ]
    
    context = {
        'attacker_data': attacker_data,
        'total_types': len(attacker_data)
    }
    
    return render(request, 'attacker_types.html', context)


def api_stats(request):
    """API endpoint for real-time statistics"""
    total_attacks = AttackLog.objects.count()
    unique_ips = AttackLog.objects.values('ip_address').distinct().count()
    
    # Get attacks in last hour
    last_hour = timezone.now() - timedelta(hours=1)
    recent_attacks = AttackLog.objects.filter(timestamp__gte=last_hour).count()
    
    data = {
        'total_attacks': total_attacks,
        'unique_ips': unique_ips,
        'recent_attacks': recent_attacks,
    }
    
    return JsonResponse(data)
