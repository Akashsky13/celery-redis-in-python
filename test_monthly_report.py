from tasks import send_monthly_report
from datetime import datetime, timedelta

# Calculate the ETA (30 seconds from now)
eta_time = datetime.utcnow() + timedelta(seconds=20)

# Apply the task asynchronously with eta parameter
result = send_monthly_report.apply_async(eta=eta_time)

# Print the task ID and state to verify it was scheduled correctly
print(f'Task ID: {result.id}')
print(f'Task ETA: {eta_time}')
