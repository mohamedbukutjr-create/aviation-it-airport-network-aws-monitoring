#!/bin/bash
dnf update -y
dnf install -y httpd
cat > /var/www/html/index.html <<'HTML'
<html>
<head><title>Mock Airline Operations App</title></head>
<body>
<h1>Mock Airline Operations App</h1>
<p>Status: ONLINE</p>
<p>Services: Check-in, Baggage Events, Gate Operations</p>
</body>
</html>
HTML
systemctl enable httpd
systemctl start httpd
