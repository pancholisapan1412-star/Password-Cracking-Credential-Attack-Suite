from modules.windows_hash_parser import analyze_windows_accounts

sample_data = """
Administrator:500:Enabled:NTLM metadata
Guest:501:Disabled:NTLM metadata
Sapan:1001:Enabled:NTLM metadata
TestUser:1002:Disabled:NTLM metadata
InvalidUser:ABC:Enabled:NTLM metadata
"""

result = analyze_windows_accounts(sample_data)

print("WINDOWS SAM SAMPLE ANALYSIS")

print("Total Records:", result["total_records"])

print("Valid Records:", result["valid_records"])

print("Invalid Records:", result["invalid_records"])

print("Enabled Accounts:", result["enabled_accounts"])

print("Disabled Accounts:", result["disabled_accounts"])

print("\nAccount Details:")

for account in result["accounts"]:
    print(account)

print("\nErrors:")

for error in result["errors"]:
    print(error)