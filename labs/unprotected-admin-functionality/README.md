# PortSwigger Lab: Unprotected Admin Functionality

**Platform:** PortSwigger Web Security Academy  
**Category:** Access Control  
**Difficulty:** Apprentice  
**Status:** Solved  
**Tools:** Web browser, Burp Suite Community

## 1. Objective

Access an unprotected administrative panel and delete the user `carlos`.

Official lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality

## 2. Vulnerability Overview

The application exposed administrative functionality without enforcing appropriate server-side authorization.

The location of the administrative panel was disclosed through `robots.txt`. This file is intended to provide instructions to web crawlers; it is publicly accessible and must not be treated as a security mechanism.

The core issue was not simply that the administrator path was discoverable. The security failure was that the administrative functionality could be accessed without the required authorization checks.

## 3. Reconnaissance

### Homepage

- Requested the homepage.
- Observed HTTP status: `200 OK`.
- No obvious administrator link was visible in the page.
- Inspected the HTML response for clues.

### JavaScript inspection

The homepage referenced:

`/resources/labheader/js/labHeader.js`

Inspected the script for administrator-related paths. No relevant clue was identified in this resource.

### robots.txt

After verifying the correct lab instance, inspected `/robots.txt`.

The file disclosed the administrator-panel path:

`/administrator-panel`

**Lesson:** `robots.txt` is publicly readable. A `Disallow` entry does not restrict access to a path.

## 4. Exploitation

1. Located the administrative-panel path through `robots.txt`.
2. Navigated directly to `/administrator-panel` on the authorized Academy lab.
3. Accessed the exposed administrative functionality.
4. Located the user `carlos`.
5. Used the panel's delete action to remove the user.
6. Confirmed that the Academy lab was marked as solved.

## 5. Root Cause

The application relied on obscurity instead of enforcing authorization at the server.

Not linking an administrator page from the homepage does not prevent users from requesting its URL directly. Similarly, listing a path in `robots.txt` does not protect it.

## 6. Security Impact

In a real application, an unauthenticated user who can access an unprotected administrator panel might be able to perform privileged actions, depending on the functions exposed.

Potential impacts include:

- Unauthorized account deletion or modification.
- Unauthorized access to administrative information.
- Changes to application settings or user permissions.
- Disruption of normal application operations.

The actual impact must be established by testing the affected functionality within the authorized scope.

## 7. Recommended Remediation

- Enforce server-side authentication and authorization on every administrative endpoint.
- Require an appropriate administrator role before allowing privileged actions.
- Deny access by default when authorization cannot be established.
- Apply authorization checks to both the administrative interface and its underlying action endpoints.
- Do not rely on hidden links, unpredictable URLs, or `robots.txt` for security.
- Add tests verifying that unauthenticated and non-administrator users cannot perform privileged actions.

## 8. Key Takeaways

- Authentication determines who the user is; authorization determines what the user may do.
- A discoverable URL is not itself a vulnerability; missing access control is.
- `robots.txt` is not an access-control mechanism.
- Sensitive operations must be protected on the server, not merely hidden in the interface.
- Security findings should be supported by observed behavior and reproducible evidence.

## 9. Evidence and Limitations

- Lab completion: confirmed.
- Homepage response: `200 OK`.
- Visible administrator link: none observed.
- JavaScript inspection: no administrator-related clue found in the inspected shared lab-header script.
- Administrative path: discovered through `robots.txt` on the verified lab instance.
- Final objective: completed by deleting `carlos`.

This was an intentionally vulnerable training application. The result does not establish that any real-world application has the same vulnerability.

## 10. References

- Official lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
- PortSwigger access-control learning materials: https://portswigger.net/web-security/access-control
