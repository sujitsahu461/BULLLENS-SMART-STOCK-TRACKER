import subprocess, os

print("Removing old .git...")
os.system('rmdir /s /q .git')

print("Initializing git...")
subprocess.run(['git', 'init'])

print("Adding remote...")
subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/sujitsahu461/BULLLENS-SMART-STOCK-TRACKER.git'])

print("Setting branch to main...")
subprocess.run(['git', 'branch', '-M', 'main'])

print("Adding files (respecting .gitignore)...")
subprocess.run(['git', 'add', '.'])

print("Committing...")
subprocess.run(['git', 'commit', '-m', 'Complete project including UI fixes and ML endpoints'])

print("Pushing to remote...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], capture_output=True)
print(res.stdout.decode('utf-8', errors='replace') + res.stderr.decode('utf-8', errors='replace'))
