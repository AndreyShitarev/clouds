import os

print("bad pracctice file")
print("User UID:", os.getuid()) // такой код не запумтится на windows
print("APP_TOKEN from ENV:", os.getenv("APP_TOKEN")) 
try:
    with open("/host_root/test/passwordd", "r") as f:
        print("Read host /test/password first line:", f.readline().strip())
except Exception as e:
    print("cant read host file (", e)
