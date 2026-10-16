# Burp Repeater Experiment Evidence

> **Purpose:** Record reproducible observations from controlled HTTP experiments in Burp Suite Repeater.
>
> **Separation of concerns:** This file is the evidence log. Keep concepts and general lessons in `notes/web-security.md`.

## Lab details

- **Date performed:** `2026-10-14`
- **Tester:** `Yug`
- **Tool:** Burp Suite Community Edition — Repeater
- **Target:** `http://127.0.0.1:8000/`
- **Scope:** Local practice server only
- **Server command:**

  ```bash
  cd ~/cyber-lab/projects/attack-surface
  python3 -m http.server 8000 --bind 127.0.0.1 --directory site
  ```

## Method

1. Send a request from **Proxy → HTTP history** to **Repeater**.
2. Send the original request first and preserve it as the baseline.
3. Change **one variable at a time**.
4. Send the modified request and compare its response with the baseline.
5. Record observations separately from hypotheses and conclusions.
6. Save screenshots that clearly show the request and corresponding response. Avoid recording cookies, credentials, tokens, or unrelated private data.

## Evidence index

Screenshots are marked as captured based on the tester's confirmation. The filenames below are the names recorded for this lab; make sure each file is actually saved in the evidence directory before committing.

| ID | Experiment | Evidence filename(s) | Captured? |
|---|---|---|---|
| E01 | Baseline: `GET /` | `E01-baseline-root.png` | Yes |
| E02 | Path: `/` vs `/index.html` | `E02-path-comparison.png` | Yes |
| E03 | Nonexistent path | `E03-nonexistent-path.png` | Yes |
| E04 | Query value change | `E04-query-parameter1.png`, `E04-query-parameter2.png` | Yes |
| E05 | `User-Agent` value change | `E05-user-agent1.png`, `E05-user-agent2.png` | Yes |
| E06 | `GET` vs `HEAD` | `E06-get-vs-head.png` | Yes |

Screenshots are supporting evidence; written request/response records are also useful. Do not create placeholder screenshots.

---

## E01 — Baseline request: `GET /`

- **Question:** What response does the server return for the root path?
- **Request:** `GET /`
- **Observed status:** `200 OK`
- **Server header (as recorded):** `SimpleHTTP/0.6 Python/3.12.3`
- **Content-Length:** `135`
- **Date header recorded:** `Wed, 14 Oct 2026 15:39:15 GMT`
- **Evidence file:** `E01-baseline-root.png`
- **Conclusion:** The root request returned `200 OK` in this observation.

## E02 — Path comparison: `/` versus `/index.html`

- **Question:** Does changing only the path change the response?
- **Baseline request:** `GET /`
- **Modified request:** `GET /index.html`
- **Only request variable changed:** Path
- **Baseline result (as recorded):** `200 OK`; server header `SimpleHttp/0.6 Python/3.12.3`; body note `In file`
- **Modified result (as recorded):** `200 OK`; server header `SimpleHttp/0.6 Python/3.12.3`; body note `In file`
- **Recorded request difference:** Only the path changed.
- **Evidence file:** `E02-path-comparison.png`

## E03 — Nonexistent path

- **Question:** How does the server respond to a path that does not exist?
- **Request:** `GET /missing`
- **Only request variable changed from baseline:** Path
- **Observed status:** `404 File not found`
- **Server header (as recorded):** `SimpleHttp/0.6 Python/3.12.3`
- **Body/error-message note:** `In file`
- **Evidence file:** `E03-nonexistent-path.png`
- **Conclusion:** The tested path returned a 404 response. An error response by itself does not prove that a security vulnerability exists.

## E04 — Query parameter value

- **Question:** Does changing the query parameter value produce an observable response difference?
- **Baseline request:** `GET /?source=attack-surface`
- **Modified request:** `GET /?source=proxy-lab`
- **Only request variable changed:** The `source` value
- **Recorded request difference:** Only the `source` value changed.
- **Response comparison:** Same
- **Evidence files:** `E04-query-parameter1.png`, `E04-query-parameter2.png`
- **Caution:** Acceptance of a parameter does not establish that the application uses it.

## E05 — `User-Agent` header

- **Question:** Does changing only the `User-Agent` header change the response?
- **Baseline value:** `CyberLab-Session3/1.0`
- **Modified value:** `CyberLab-Session3/2.0`
- **Only request variable changed:** `User-Agent`
- **Recorded request difference:** Only the `User-Agent` value changed.
- **Response comparison:** Same
- **Evidence files:** `E05-user-agent1.png`, `E05-user-agent2.png`

## E06 — `GET` versus `HEAD`

- **Question:** How does the response to `HEAD` compare with `GET`?
- **Baseline request:** `GET /`
- **Modified request:** `HEAD /`
- **Only request variable changed:** HTTP method
- **Recorded observation:** `HEAD` returned no response body.
- **Evidence file:** `E06-get-vs-head.png`
- **Still to compare:** Status code and response headers, including `Content-Type` and `Content-Length` if present.
- **Conclusion:** The recorded observation is consistent with the expected purpose of `HEAD`, but compare the status and headers in the captured response before drawing a fuller conclusion.

## Session summary

- **Most useful observation:** The root request returned `200 OK`; the nonexistent `/missing` path returned `404 File not found`; the `HEAD` response was recorded as having no body.
- **What this evidence does not prove:** These observations do not establish that the server is secure or vulnerable. A lack of visible response differences does not prove that a request value is ignored in every context.
- **Related notes:** `../notes/web-security.md`
