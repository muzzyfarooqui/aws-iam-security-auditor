# AWS IAM Security Audit Report

## Assessment Information

**Environment:** Internal AWS Lab Environment

**Assessment Type:** AWS Identity and Access Management (IAM) Security Assessment

**Purpose:**  
Evaluate a simulated AWS environment for identity and access management security risks. Identify misconfigurations, assess risk, recommend remediation, and improve the overall security posture of the environment.

---

# Assessment Scope

The assessment includes:

- IAM Users
- IAM Groups
- IAM Policies
- Multi-Factor Authentication (MFA)
- IAM Access Keys
- Amazon S3 Permissions

---

# Executive Summary

The AWS IAM security assessment identified four significant identity and access management risks within the simulated environment. These included excessive administrative permissions assigned to developer and intern accounts, missing Multi-Factor Authentication (MFA), and improper offboarding of a former employee with active credentials.

The findings were prioritized based on their potential impact on the AWS environment. Each issue was remediated by implementing least-privilege IAM policies, enabling MFA, removing unnecessary administrative permissions, and revoking former employee access.

After remediation, an automated IAM security auditor was developed using Python and `boto3` to evaluate IAM users for missing MFA, unauthorized `AdministratorAccess`, and unauthorized active access keys.

Controlled security misconfigurations were introduced to validate each automated check. The auditor successfully detected the test violations and confirmed that the environment returned to a clean state after remediation.

---

# Findings

---

## Finding 001

### Title

Intern account assigned AdministratorAccess

### Severity

High

### Evidence

The IAM user `intern` is a member of the `Administrators` group, which grants the AWS managed policy `AdministratorAccess`.

### Risk

If the intern account is compromised, an attacker could gain unrestricted administrative access to AWS resources. This could result in unauthorized changes, deletion of infrastructure, or exposure of sensitive company data.

### Recommendation

Create a dedicated `Interns` IAM group and assign only the permissions required for the intern's responsibilities following the principle of least privilege. Remove the `intern` user from the `Administrators` group.

### Remediation Performed

Created a dedicated `Interns` IAM group and a custom `InternsS3ReadOnly` policy using JSON. Attached the custom policy to the `Interns` group, removed the `intern` user from the `Administrators` group, and added the user to the `Interns` group.

### Verification

Reviewed the `intern` user in IAM and verified that the account is no longer a member of the `Administrators` group and no longer receives `AdministratorAccess`. Confirmed that the user now receives the custom `InternsS3ReadOnly` policy through the `Interns` group.

### Status

Remediated

---

## Finding 002

### Title

Developer account assigned AdministratorAccess

### Severity

High

### Evidence

The IAM user `developer1` is a member of the `Administrators` group, which grants the AWS managed policy `AdministratorAccess`.

### Risk

The developer account has unrestricted administrative access even though a developer typically requires access only to the AWS resources necessary for their work. If the account is compromised, an attacker could gain full administrative control of the AWS environment, increasing the risk of unauthorized changes, infrastructure disruption, or data exposure.

### Recommendation

Create a dedicated `Developers` IAM group and assign only the permissions required for development activities. Remove the `developer1` account from the `Administrators` group and implement least-privilege access based on job responsibilities.

### Remediation Performed

Created a dedicated `Developers` IAM group and a custom `DevelopersS3LeastPrivilege` policy using JSON. Attached the custom policy to the `Developers` group, removed the `developer1` user from the `Administrators` group, and added the user to the `Developers` group.

### Verification

Reviewed the `developer1` user in IAM and verified that the account is no longer a member of the `Administrators` group and no longer receives `AdministratorAccess`. Confirmed that the user now receives the custom `DevelopersS3LeastPrivilege` policy through the `Developers` group.

### Status

Remediated

---

## Finding 003

### Title

IAM users with console access did not have Multi-Factor Authentication (MFA) enabled

### Severity

Critical

### Evidence

The IAM users reviewed during the assessment did not have Multi-Factor Authentication (MFA) enabled. This included privileged accounts such as `cloud-admin`.

### Risk

Without MFA, an attacker who obtains a user's password could gain unauthorized access to the AWS environment. This significantly increases the risk of unauthorized administrative access, infrastructure modification, and exposure of sensitive company data.

### Recommendation

Enable Multi-Factor Authentication (MFA) for all IAM users with AWS Management Console access, prioritizing privileged administrator accounts. Require MFA during user onboarding and periodically review IAM users to ensure MFA remains enabled.

### Remediation Performed

Enabled Multi-Factor Authentication (MFA) for all assessed IAM users with AWS Management Console access. MFA was first configured for `cloud-admin` because the account has the highest level of privileges, followed by `developer1` and `intern`.

During automated testing, the auditor also identified that the `muzammil` administrative IAM user did not have MFA enabled. MFA was subsequently configured for this account as well.

### Verification

Reviewed each assessed IAM user in the AWS IAM console and confirmed that an MFA device is assigned to `cloud-admin`, `developer1`, `intern`, and `muzammil`. The automated auditor was then executed and confirmed that no users were missing MFA.

### Status

Remediated

---

## Finding 004

### Title

Improper employee offboarding procedures

### Severity

Critical

### Evidence

The IAM user `former-employee` remained active, was a member of the `Administrators` group, and had active programmatic access credentials.

### Risk

Former employees retaining privileged accounts and active credentials present a critical security risk. If the account or access keys are compromised, an attacker could gain unrestricted administrative access to AWS resources, modify infrastructure, or expose sensitive company data.

### Recommendation

Implement an automated employee offboarding process that immediately disables or removes IAM accounts, revokes active access keys, removes users from privileged groups, and verifies that former employees no longer retain access to AWS resources.

### Remediation Performed

Removed the IAM user `former-employee` from the `Administrators` group, deactivated and deleted the user's active access key, disabled console access, and then deleted the IAM user after confirming the account was no longer required.

### Verification

Verified that `former-employee` no longer had `AdministratorAccess` or active programmatic credentials before deleting the IAM user. Confirmed that the `former-employee` identity no longer appears in IAM.

### Status

Remediated

---

# Remediation Summary

| Finding | Status |
| --- | --- |
| Finding 001 | Remediated |
| Finding 002 | Remediated |
| Finding 003 | Remediated |
| Finding 004 | Remediated |

---

# Automated Security Validation

After completing the manual remediation, a Python security auditor was developed using the AWS SDK (`boto3`) to validate IAM security controls automatically.

The auditor checks for:

- IAM users without MFA
- Unauthorized `AdministratorAccess`
- Unauthorized active access keys

Controlled misconfigurations were introduced to verify that the automated checks function correctly.

## MFA Test

MFA was temporarily removed from the `intern` account. The auditor successfully detected the missing MFA configuration and generated a High severity finding. MFA was restored, and a second audit confirmed that the finding was resolved.

## AdministratorAccess Test

The `intern` account was temporarily added to the `Administrators` group. The auditor successfully identified the unauthorized administrative access and generated a High severity finding. The account was removed from the group, and a second audit confirmed that the finding was resolved.

## Access Key Test

A temporary access key was created for the `intern` account. The auditor successfully detected the unauthorized active access key and generated a High severity finding. The key was deleted, and a second audit confirmed that the environment returned to a clean state.

## Final Validation

After all controlled tests were remediated, the automated auditor reported:

```text
=== Security Findings Summary ===
✅ No security violations detected.
```

---

# Lessons Learned

This project demonstrated that identifying a security issue is only one part of a security assessment. Findings must also be supported with evidence, evaluated based on risk, prioritized, remediated, and verified.

The manual audit strengthened my understanding of IAM permissions, Multi-Factor Authentication (MFA), access keys, employee offboarding, and the principle of least privilege. Creating separate IAM groups and custom policies demonstrated how access can be limited based on job responsibilities instead of assigning broad administrative permissions.

Performing the assessment manually before automating it helped me understand what the automated auditor needed to check and why each control was important. The automated MFA scan also identified an account that was missed during the initial manual verification, demonstrating how automation can provide more consistent coverage and reduce human oversight.

Automating the process with Python and `boto3` demonstrated how cloud security checks can be performed consistently across IAM users. Controlled testing also demonstrated the importance of validating security automation by introducing known misconfigurations, confirming detection, remediating the issue, and verifying that the environment returns to a secure state.