---
title: "How does SSL certificates work?"
description: "They are used to secure all our online activities, preventing hackers and malicious people to steal sensitive information."
image: images/2024-09-02-handshake-between-two-individuals.jpg
imageAlt: Handshake between two individuals
date: 2024-09-02
categories:
  - Web Development
tags:
  - Security
---

## Why Do We Need SSL Certificates

SSL certificates allow:

1. **Encryption of data:** SSL certificates encrypt data transferred between the server and the client, ensuring that malicious individuals can’t intercept or tamper sensitive information (e.g., credit card numbers, personal details).
2. **Authentication:** they authenticate the identity of the website, assuring users that they’re communicating with the legitimate website and not an impostor. This prevents man-in-the-middle attacks.
3. **Data Integrity:** SSL certificates ensure that no one alter data sent and received during transmission. If data is tampered with, the connection is terminated.
4. **Trust and Reputation:** Websites with SSL certificates display a padlock icon and use “https” in the URL, which builds trust with users. Some browsers also flag non-SSL sites as “Not Secure,” which can deter users.
5. **Compliance:** Many regulatory standards (e.g., PCI DSS for payment processing) require websites to use SSL to protect sensitive data.

By providing encryption, authentication, and integrity, SSL certificates are essential for secure online communications and transactions, building trust between users and websites.

## Creating an SSL Certificate

Below, you will find the detailed steps to create certificate.

### Generating the Private Key and CSR (Certificate Signing Request)

The **Private Key** corresponds to a long, random string of characters. This key is kept secret and stored on the server.

Then, you build the **CSR** using the private key, the website owner creates a CSR, which includes information about the website and the owner.

### Submitting of CSR to a CA for Validation

The website owner submits the CSR to a trusted CA, which verifies the provided information. The CA checks the authenticity of the organization or individual requesting the certificate.

Depending on the type of SSL certificate, the CA may perform various levels of validation. This can range from checking domain ownership (for Domain Validated certificates) to verifying organizational details (for Organization Validated certificates) and even conducting a thorough vetting process (for Extended Validation certificates).

### Certificate Issuance

Once the CA validates the information, it issues an SSL certificate, which includes the website’s public key and the CA’s digital signature. This certificate is sent back to the website owner.

### Installation of the Certificate

The website owner installs the SSL certificate on their web server. The server can now establish secure connections with clients (browsers).

## How SSL Certificates Work

To secure a connection between a client (typically a user on a web browser) and a server (a machine that replies to content requests), it takes a few steps, required to exchange any data in a encrypted manner.

First, the client initiates a connection: when a user accesses a website with SSL, their browser requests the server to identify itself.

Then, the server sends a copy of the SSL certificate, which includes the public key and the CA’s digital signature.

Then the browser verifies the certificate against a list of trusted CAs. It verifies that the certificate is from a trusted source, hasn’t expired, and is used for the intended purpose.

Finally, the client starts the encryption key exchange: if the certificate is trusted, the browser generates a session key, encrypts it with the server’s public key, and sends it to the server. Only the server can decrypt this session key using its private key.

Now, both the browser and the server now have a shared session key, which they use to encrypt all subsequent data exchanged during the session.

Below is a sequence chart that demonstrates the steps involved in how SSL certificates work during a typical SSL handshake between a client (browser) and a server (website).

```text
Client (Browser)               Server (Website)
   |                                |
   |--- 1. Client Hello ----------->|
   |                                |
   |<-- 2. Server Hello ------------|
   |<-- 3. Server Certificate ------|
   |<-- 4. Server Key Exchange -----|
   |<-- 5. Server Hello Done -------|
   |                                |
   |--- 6. Client Key Exchange ---->|
   |--- 7. Client Finished -------->|
   |                                |
   |<-- 8. Server Finished ---------|
   |                                |
   |--- 9. Encrypted Data --------->|
   |<-- 10. Encrypted Data ---------|

```

### Steps Explained In Simple Terms

Imagine you’re passing secret notes in a classroom. Here’s how random numbers (like the ones used in SSL) would make this more secure:

- Unique “handshake”: let’s say before passing notes, you (Client) and your friend (Server) agree on a secret handshake. But instead of using the same handshake every time, you both roll a die and use the numbers to create a unique handshake each time. This way, even if someone sees your handshake once, they can’t use that knowledge to pretend to be you next time. In addition, your friend passes on his key to create the one-time code
- Creating a one-time code (Client Key Exchange): after your handshake, you use the numbers you both rolled to create a special code or key (Pre-Master Secret) for your message. This code changes every time (each session) because the die rolls are different. So even if someone cracks one message, they can’t read the next one.
- Freshness check: if you write the current time on your note along with a random number, your friend can be sure it’s a new note and not an old one someone is resending to trick them.
- Preventing guesswork: since the die roll provides a random number, nobody can guess the next one.

### Steps Explained In Details

1. **Client Hello:** the client initiates the handshake by sending a “Client Hello” message to the server. This message includes the client’s SSL/TLS version, the cipher suites supported by the client (encrypt subsequent data, see steps 9 and 10), and a randomly generated number.
2. **Server Hello:** the server responds with a “Server Hello” message. This message includes the server’s SSL/TLS version, the cipher suite chosen by the server from the list provided by the client, and a randomly generated number.
3. **Server Certificate:** next, the server sends its SSL certificate to the client. This certificate contains the server’s public key and is signed by a trusted Certificate Authority (CA).
4. **Server Key Exchange (if required):** if the chosen cipher suite requires a key exchange, the server sends the necessary key exchange parameters.
5. **Server Hello Done:** the server sends a “Server Hello Done” message to indicate that it has completed its part of the initial negotiation.
6. **Client Key Exchange:** the client generates a pre-master secret, encrypts it with the server’s public key (from the server’s certificate), and sends it to the server. Both the client and server use this pre-master secret to generate a master secret.

   The formula for the master secret value is as follows:

   ```text
   MasterSecret = PRF(PreMasterSecret, "master secret",
                      ClientHello.random + ServerHello.random)

   Where:
   PRF = Pseudorandom Function (a cryptographic hash function)
   PreMasterSecret = The secret value generated by the client
   ClientHello.random = The random number sent by the client
   ServerHello.random = The random number sent by the server
   ```

7. **Client Finished:** the client sends a “Client Finished” message, encrypted with the session key derived from the master secret, to indicate that the client part of the handshake is complete.
8. **Server Finished:** the server responds with a “Server Finished” message, also encrypted with the session key, to indicate that the server part of the handshake is complete.
9. **Encrypted Data:** the client and server can now securely exchange data using symmetric encryption, with keys derived from the master secret.
10. **Encrypted Data:** the server responds to the client’s encrypted data. This exchange continues for the duration of the session.

### What Does Interrupt a Session

Many factors can interrupt a session.

For example:

Excellent question. Sessions in SSL/TLS can be interrupted or terminated for various reasons. Let’s explore the main factors that can cause a session to end:

1. Natural session expiration: SSL/TLS sessions have a predetermined lifespan, typically set by the server. Once this time limit is reached, the session naturally expires.

2. Explicit termination: Either the client or server can initiate a proper closure of the connection. This is done through a specific SSL/TLS protocol message called “Close Notify”.

3. Network issues: Sudden loss of network connectivity or significant network latency or packet loss can cut off the session between the client anad server.

4. Server-side actions: Server restart or crash or load balancing that moves the connection to a different server.

5. Client-side actions: Closing the browser or application or putting a mobile device to sleep terminates the ongoing session.

6. Security measures: Detection of potential security threats might cause the server to terminate sessions or simply changing of server’s SSL/TLS certificates.

7. Inactivity timeout: Many servers implement an inactivity timeout to free up resources.

8. Maximum data transfer: some implementations may terminate a session after a certain amount of data has been transferred.

It’s worth noting that in many modern web applications, the concept of a “session” often extends beyond the SSL/TLS session itself. Application-level sessions (like login sessions) may persist across multiple SSL/TLS sessions through mechanisms like session cookies or tokens.

When a session is interrupted, a new handshake process must occur to establish a new secure connection. This involves generating new random numbers, a new Pre-Master Secret, and consequently, new session keys. This ensures that even if an attacker managed to compromise one session, they wouldn’t automatically have access to subsequent sessions.

## Conclusion

Do you understand better how SSL certificates work?

[Feel free to ask questions](../../../page/contact-me/index.md) if you need.
After reading more on the topic and summarizing it here, I do.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Cytonn Photography](https://unsplash.com/@cytonn_photography?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/two-people-shaking-hands-n95VMLxqM2I?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
