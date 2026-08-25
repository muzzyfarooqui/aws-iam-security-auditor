import boto3

iam = boto3.client("iam")

response = iam.list_users()

findings = []

approved_admins = {
    "cloud-admin",
    "muzammil"
}

approved_access_key_users = {
    "muzammil"
}


# IAM USERS
print("\n=== IAM Users ===")

for user in response["Users"]:
    print(user["UserName"])


# MFA CHECK
print("\n=== MFA Check ===")

for user in response["Users"]:
    username = user["UserName"]

    mfa_devices = iam.list_mfa_devices(
        UserName=username
    )

    if len(mfa_devices["MFADevices"]) == 0:
        print(f"❌ {username}: MFA NOT enabled")

        findings.append(
            f"HIGH: {username} does not have MFA enabled"
        )

    else:
        print(f"✅ {username}: MFA enabled")


# ADMINISTRATOR ACCESS CHECK
print("\n=== AdministratorAccess Check ===")

for user in response["Users"]:
    username = user["UserName"]

    groups = iam.list_groups_for_user(
        UserName=username
    )["Groups"]

    has_admin = False

    for group in groups:
        group_name = group["GroupName"]

        policies = iam.list_attached_group_policies(
            GroupName=group_name
        )["AttachedPolicies"]

        for policy in policies:
            if policy["PolicyName"] == "AdministratorAccess":
                has_admin = True

    direct_policies = iam.list_attached_user_policies(
        UserName=username
    )["AttachedPolicies"]

    for policy in direct_policies:
        if policy["PolicyName"] == "AdministratorAccess":
            has_admin = True

    if has_admin:
        if username in approved_admins:
            print(f"✅ {username}: Approved AdministratorAccess")
        else:
            print(
                f"❌ {username}: "
                "Unauthorized AdministratorAccess detected"
            )

            findings.append(
                f"HIGH: {username} has unauthorized AdministratorAccess"
            )

    else:
        print(f"✅ {username}: No AdministratorAccess detected")


# ACCESS KEY CHECK
print("\n=== Access Key Check ===")

for user in response["Users"]:
    username = user["UserName"]

    keys = iam.list_access_keys(
        UserName=username
    )["AccessKeyMetadata"]

    if len(keys) == 0:
        print(f"✅ {username}: No access keys")

    else:
        active_keys = [
            key for key in keys
            if key["Status"] == "Active"
        ]

        if active_keys:
            if username in approved_access_key_users:
                print(f"✅ {username}: Approved active access key")
            else:
                print(
                    f"❌ {username}: "
                    "Unauthorized active access key detected"
                )

                findings.append(
                    f"HIGH: {username} has an unauthorized active access key"
                )

        else:
            print(f"✅ {username}: No active access keys")


# SECURITY FINDINGS SUMMARY
print("\n=== Security Findings Summary ===")

if len(findings) == 0:
    print("✅ No security violations detected.")

else:
    for finding in findings:
        print(f"❌ {finding}")

    print(f"\nTotal findings: {len(findings)}")