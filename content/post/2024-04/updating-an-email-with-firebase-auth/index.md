---
title: "Updating an e-mail with Firebase Auth"
description: "Long ago, the workflow to change an e-mail address with Firebase Authentification was simple, but less secure. With Firebase 9, it changed and you need to verify the e-mail address when updating it. I’ll show you how it works..."
image: images/2024-04-10-a-few-mailboxes.jpg
imageAlt: "Some physical mailboxes of different design styles"
date: 2024-04-12
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Firebase
---

Performing this task wasn’t easy.

To be honest, Google hasn’t documented very clearly the Firebase Authentification API. However, thanks to Stackoverflow (as always!), I manage to solve this and be able to update the e-mail address of an existing authenticated user (e-mail and password method) .

## Introduction

While the API still provide a `updateEmail` method, it doesn’t update a non-verified e-mail address. So instead, you need to perform a two-step process:

- The user makes a request to change the e-mail.
- The user confirms the e-mail modification.

## How to create an e-mail account for testing purposes

To test that, you need to e-mail account.

For testing purposes only, I recommend **Yopmail**. It allows you to create _throwaway_ e-mail addresses in seconds.

Just go to [their website](https://yopmail.com/) and use [the random e-mail address generator](https://yopmail.com/email-generator).

It guarantees that you don’t have someone use the same e-mail address as you and sees some of sensitive information.

## The code and workflow

### Send the request to change the e-mail

The workflow may differ from an application to another, so I will share the code that calls the Firebase Authentification API:

```tsx
/**
 * This instantiate the firebaseApp
 * @see https://github.com/JeremieLitzler/vueschool-course/blob/forum-vite/src/services/fireBaseConnector.ts
 */
import { firebaseApp } from "@/services/fireBaseConnector";

import { getAuth, verifyBeforeUpdateEmail } from "firebase/auth";

const auth = getAuth(firebaseApp);

/**
 * Send Firebase a request to get a verifyAndUpdateEmail link for a user.
 *
 * The `continueUrl` contains the link to the /account/edit route
 * from where the request is made.
 *
 * The query string parameters are used to have a smooth UX:
 * - `verifiedEmail`: used on the login page (/account/edit
 * requires authentification) and the /account/edit page
 * once reauthenticated.
 * - `showReconnectMessage`: used on the login page to show a
 * clear message about the email address to use to login.
 * - `oobCode`: not used but could be to secure the request
 * if the code was saved in the firestore document corresponding
 * to the updated user.
 *
 * The try&catch is necessary to show a login form on
 * /account/edit if Firebase requests reauthentication.
 *
 * Don't forget to add VITE_BASE_URL in your CD.
 *
 * @param newEmail The new email to set on the authenticated user
 * @returns The result of the request : success (boolean) and the
 * Firebase error (if any)
 */
const secureUpdateEmail = async (newEmail: string) => {
  const oobCode = uniqueIdHelper().newUniqueId;
  const continueUrl = `${import.meta.env.VITE_BASE_URL}/account/edit?${
    AppQueryStringParam.verifiedEmail
  }=${newEmail}&${AppQueryStringParam.oobCode}=${oobCode}&${
    AppQueryStringParam.showReconnectMessage
  }=true`;
  console.log("secureUpdateEmail>continueUrl", continueUrl);

  return verifyBeforeUpdateEmail(auth.currentUser!, newEmail, {
    url: `${continueUrl}`,
    handleCodeInApp: true,
  })
    .then(() => {
      return { success: true, errorMessage: null };
    })
    .catch((error) => {
      return { success: false, errorMessage: error };
    });
};
```

### Confirm the e-mail modification

Once the user requested the verification, Firebase sends an e-mail to the new e-mail address.

While you can configure the e-mail template, in the free tier, you’re limited to what you customize.

Once the user clicks the link, he brought to a Firebase page. Once Firebase has completed the verification and update, the use can click _Continue_. This is where the `continueUrl` is used.

In the demo application below, the custom `continueUrl` allows to guide the user through the steps to complete the update.

While Firebase update the e-mail address in the users database, you probably need to update the Firestore document where you store the user’s other information.

## Live demo

You can visit the [project website](https://vueschool-masterclass-vite.netlify.app/) I built while taking part in [the Vueschool.io Masterclass (version 1)](https://vueschool.io/the-vuejs-master-class).

To test it, you’ll need to:

- Create an account with a Yopmail e-mail address.
- Go to the _View profile_ in the top right corner by clicking the user menu.
- Click _Edit profile_ and change the e-mail address in the form.

For the next steps, I’ll let you follow the flow of actions.

You’ll need to open the Yopmail mailbox use the bottom provided by Yopmail after generating the random e-mail address. There, you’ll be able to open the verification e-mail.

The full code is available [on GitHub](https://github.com/JeremieLitzler/vueschool-course/tree/forum-vite).

I hope you enjoyed this article. If you have any question, as always, [reach out](../../../page/contact-me/index.md) and I’ll see if I can help you.

Credit: Hero photo by [Mathyas Kurmann](https://unsplash.com/@mathyaskurmann?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/six-assorted-color-mail-boxes-fb7yNPbT0l8?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
