# Basic SSRF Against the Local Server

**Platform:** PortSwigger Web Security Academy  
**Category:** Server-Side Request Forgery (SSRF)  
**Difficulty:** Apprentice  
**Status:** Completed — lab marked as solved  
**Tools:** Burp Suite Proxy and Repeater

## 1. Objective

Use the product stock-check feature to make the application request its own local admin interface, then use that interface to delete the lab user `carlos`.

Practice only in the intentionally vulnerable PortSwigger lab environment:
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost

## 2. Core concept

**Server-Side Request Forgery (SSRF)** occurs when an application makes a server-side request to a location that can be influenced by user input. If the destination is insufficiently restricted, a user may cause the server to access internal services or functionality that is not intended to be directly accessible.

In this lab, the stock-check feature fetched a URL supplied in the `stockApi` parameter. The vulnerable application made the request; it was not my browser directly requesting `localhost`.

> `localhost` is interpreted from the perspective of the machine making the connection. Here, the request originated from the lab application, so `localhost` referred to the lab server itself.

## 3. What I did

1. Opened the lab in Burp Suite's browser.
2. Opened a product details page and used the stock-check feature for a location.
3. In **Proxy → HTTP history**, found the `POST /product/stock` request. Its response normally contained stock information as text.
4. Sent the request to **Repeater** and identified the `stockApi` parameter as the URL-bearing input.
5. Changed the value and compared the responses.

## 4. Observations and experiments

| `stockApi` value | Response observed | What I learned |
|---|---|---|
| `https://host/admin` | `401`, with a different error response body | The server returned an unauthorized response for this attempt. This alone did not establish whether the target was correct. |
| `https://local/admin` | `500`, with a different error response body | The request caused an error. A `500` by itself does not identify the precise cause. |
| `http://localhost/admin` | `200`; response body contained the admin page HTML and a users list | This was strong evidence that the stock-check feature could retrieve the server's local admin interface. The scheme mattered: the successful URL used HTTP rather than HTTPS. |
| `http://localhost/admin/delete?username=carlos` | `302`; the lab subsequently showed **Lab solved** | The server-side request reached the delete action, and the lab confirmed completion. The status code alone would not be sufficient proof without the lab's success indicator. |

## 5. Successful request path

The vulnerable request was the stock-check request:

```http
POST /product/stock
```

The relevant input was the `stockApi` parameter. In Burp Repeater, I replaced its value with the following URL, keeping the rest of the original request unchanged:

```text
http://localhost/admin
```

The returned HTML revealed the admin interface and the user-deletion route. I then set `stockApi` to:

```text
http://localhost/admin/delete?username=carlos
```

After sending the request, the response was `302` and the lab page confirmed **Lab solved**.

## 6. Request flow and trust boundary

```text
My browser / Burp Repeater
        |
        | POST /product/stock with stockApi value
        v
Vulnerable lab application
        |
        | server-side request to the supplied URL
        v
http://localhost/admin
        |
        | admin HTML returned in the stock-check response
        v
I identify the delete route and supply it through stockApi
        |
        v
Lab admin delete action → lab reports success
```

The security boundary was between **user-controlled input** and the **server's outbound HTTP request**. The application trusted a destination supplied through `stockApi` without adequately restricting access to local administrative functionality.

## 7. Why this matters

Depending on the application's network access and internal services, SSRF can potentially allow an attacker to:

- Read responses from internal-only endpoints.
- Reach administrative interfaces or other services that trust requests from the local machine.
- Trigger actions exposed by those internal endpoints.
- In other environments, interact with back-end systems that are not reachable directly from the attacker's machine.

The impact depends on which destinations the server can reach, how responses are handled, and what authentication and authorization controls exist on the destination service. This lab demonstrates one specific case; it does not prove every SSRF vulnerability has the same impact.

## 8. Defensive lessons

For developers reviewing a URL-fetching feature:

- **Prefer an allowlist.** Where possible, accept only known, necessary destinations instead of arbitrary URLs.
- **Validate the parsed URL.** Restrict schemes to those needed (usually HTTP/HTTPS), and validate hostnames, ports, and URL structure consistently.
- **Validate destination IP addresses.** Consider all resolved A and AAAA addresses, including loopback, private, link-local, multicast, unspecified, and other prohibited or special-purpose ranges.
- **Enforce validation at connection time.** DNS can change between validation and connection. Ensure the actual connection goes to an approved address, while preserving correct TLS certificate verification and hostname/SNI behavior.
- **Handle redirects safely.** Disable redirects when unnecessary; otherwise revalidate every redirect destination before following it.
- **Use network-level controls.** Restrict outbound network access so the application cannot reach sensitive internal services merely because input validation fails.
- **Protect admin functionality independently.** Do not treat a request as trusted only because it appears to come from `localhost`; apply authentication and authorization to sensitive actions.
- **Fail safely and log appropriately.** Avoid returning sensitive internal response details to users, and record blocked destination attempts for investigation.

No single URL filter is a complete defense. Application-level validation and network-level restrictions should work together.

## 9. Evidence to retain

For a useful lab record, retain these non-secret observations:

- The request path and parameter name: `POST /product/stock`, `stockApi`.
- The response differences: `401`, `500`, then `200` with admin HTML.
- The final `302` and the lab's **Lab solved** confirmation.
- A short explanation of why the request originated from the server, not from my own browser.

Do not save session cookies, authentication tokens, or other live credentials in notes or screenshots.

## 10. Review questions

Try answering these without looking at the notes:

1. What makes the stock-check feature an SSRF entry point?
2. Why did `http://localhost/admin` refer to the lab server rather than my laptop?
3. Why was the `200` response body more informative than the status code alone?
4. Why does a `500` response not prove that the intended internal resource was reached?
5. Name two application-level defenses and one network-level defense against SSRF.
6. Why should a URL-fetching feature revalidate redirect destinations and control the actual IP used for the connection?

## 11. Key takeaway

**SSRF is a server-side trust-boundary problem:** user-controlled input influenced where the application made a request. In this lab, that let me retrieve a local admin page and invoke its user-deletion route. The important testing method was to find the URL-bearing parameter, change one variable at a time, inspect the response body as well as the status code, and verify the actual lab outcome.

---
