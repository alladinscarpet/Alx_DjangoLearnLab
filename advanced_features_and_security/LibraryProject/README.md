### 3. Implementing HTTPS and Secure Redirects in Django


#### Objective
Enhance the security of your Django application by configuring it to handle secure HTTPS connections and enforce HTTPS redirects for all HTTP requests.  
This task will ensure that your application adheres to best practices for secure web communication.

---

#### Task Description
Configure your Django application to support and enforce HTTPS, protecting the data transmitted between the client and the server.  
This includes setting up HTTPS redirects, configuring security-related headers, and ensuring that your site is served securely.

---

#### Steps

1. **Configure Django for HTTPS Support**

   Adjust your Django settings to strengthen the security of your application by enforcing HTTPS connections.

   - **Security Settings to Adjust:**
     - **`SECURE_SSL_REDIRECT`**: Set to `True` to redirect all non-HTTPS requests to HTTPS.
     - **`SECURE_HSTS_SECONDS`**: Set an appropriate value (e.g., `31536000` for one year) to instruct browsers to only access the site via HTTPS for the specified time.
     - **`SECURE_HSTS_INCLUDE_SUBDOMAINS`** and **`SECURE_HSTS_PRELOAD`**: Set to `True` to include all subdomains in the HSTS policy and to allow preloading.

2. **Enforce Secure Cookies**

   Modify cookie settings to enhance security by ensuring that cookies are only sent over secure HTTPS connections.

   - **Cookie Settings to Configure:**
     - **`SESSION_COOKIE_SECURE`**: Set to `True` to ensure session cookies are only transmitted over HTTPS.
     - **`CSRF_COOKIE_SECURE`**: Set to `True` to ensure CSRF cookies are only transmitted over HTTPS.

3. **Implement Secure Headers**

   Add additional HTTP headers to further secure your application from various types of attacks like clickjacking and XSS.

   - **Headers to Implement:**
     - **`X_FRAME_OPTIONS`**: Set to `"DENY"` to prevent your site from being framed and protect against clickjacking.
     - **`SECURE_CONTENT_TYPE_NOSNIFF`**: Set to `True` to prevent browsers from MIME-sniffing a response away from the declared content-type.
     - **`SECURE_BROWSER_XSS_FILTER`**: Set to `True` to enable the browser's XSS filtering and help prevent cross-site scripting attacks.

4. **Update Deployment Configuration**

   Ensure that your deployment environment is configured to support HTTPS by setting up SSL/TLS certificates.  
   This might involve updating your web server configuration (e.g., Apache or Nginx) to include SSL directives and certificate files.

5. **Documentation and Review**

   Document the changes made to secure the application, particularly how HTTPS and related security settings are implemented and enforced.  
   Review all settings to ensure they are correctly configured for your production environment.

---

#### Deliverables

1. **`settings.py`**: Documented changes with detailed comments on each security setting configured.
2. **Deployment Configuration**: Instructions or scripts used to configure your web server for HTTPS, included as part of your deployment documentation.
3. **Security Review**: A brief report detailing the security measures implemented, how they contribute to securing the application, and any potential areas for improvement.