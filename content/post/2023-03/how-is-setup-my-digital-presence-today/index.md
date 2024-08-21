---
title: "How is my digital presence setup?"
description: "In 2023, there are a lot of solutions to build your digital presence. In this article, I will share my current setup and why I use it."
date: 2023-03-30
image: images/2023-03-30-a-laptop-and-notebook-on-a-desk.jpg
imageAlt: A laptop and a notebook on a desk
categories:
  - Digital Business
---

In 2023, there are a lot of solutions to build your digital presence. In this article, I will share my current setup and why I use what I use.

<!-- more -->

## For websites

{{< blockcontainer jli-notice-note "Pour la version française de cet article" >}}

[C'est par ici](https://jeremielitzler.fr/2023/03/comment-j-organise-mon-activite-digitale/).

{{< /blockcontainer >}}

I use three solutions, which I pick depending on the following criteria.

For my personal use, I use the VuePress option more and more because of the clear win on hosting cost.

Yet, I use the second option to host my clients' websites and the third for my WordPress demo websites.

All my domain names are registered with OVH. I had a couple registered with Infomaniak, but I’m dropping them this year.

### VuePress hosted on Netlify and GitHub

I have been looking for a lightweight and cost-effective solution to build and host websites for a long time.

I tried simple HTML files, custom PHP application and WordPress.

Even if I use WordPress for my clients because it gives flexibility for them to update content themselves, I didn’t want using it for my personal needs.

As a software engineer, I wanted something quick, easy and with the least dependences possible.

I discovered VuePress as I started learning about VueJS in 2021.

At first, I used a custom theme of VuePress 2, based on the default theme. Then I discovered [Mr Hope’s theme](https://theme-hope.vuejs.press/) which provides all the features I need.

It allows me to:

- customize the styles, navigation, features I need
- write articles quickly in [Markdown](https://en.wikipedia.org/wiki/Markdown) which VuePress transforms into static HTML files
- deploy automatically the website with little efforts.

I have built a [template repository with multilangual support](https://github.com/Puzzlout/TemplateVuepress/) with a minimum setup if you’re interested. Or [contact me if you need help](../../../page/contact-me/index.md).

Today I use this for:

- this current website you are on, which is my personal blog
- [this demo website for a quinoa producer](https://inflorescences-quinoa.fr/) in Normandy (north west of France)
- [my business idea about teach people to learn how to save on their energy bills](https://www.passonslecap.fr/).
- [my historical business website site](https://puzzlout.com/) which I recently migrated over from a custom build with Gulp and flat hmtl files.

In all these usecases, the **cost is limited to the custom domain name** if the `my-website.netlify.app`isn’t enough.

### WordPress and Divi hosted on Infomaniak

I use WordPress and the Divi builder through [Infomaniak hosting](https://www.infomaniak.com/goto/fr/my-easy-site?utm_term=5ff70313bf816) for clients.

It’s very cost-effective with an hosting plan starting at **about 112 euros per year** (depending on the sale offers at a given moment).

It includes a domain, a email account and a web hosting with the Divi builder for free.

The manager dashboard is great and more intuitive than OVH’s.

The features available really appeals to me who likes to script deployments. Even though I can’t do all I can on Cloudways ([see below](#wordpress-and-divi-on-cloudways)), I can do enough to automate a lot of steps when deploying a WordPress site for a client.

Also, the fact that Divi comes for free when you purchase a hosting plan is a good plus.

In terms of cost, you will need to pay for the domain and hosting. For a `.fr`domain and the bare minimum hosting, it costs about **112 euros per year**, which may be more than OVH or GoDaddy or IONOS, but the features and performance of Infomaniak beat them clear and square.

At the moment, I use this setup for:

- [L'ensemble instrumental Tournon-Tain](https://ensembleinstrumentaltournontain.fr/) (a symphonic orchestra in the city where I live).
- [Gilles Fauriat's website](https://fauriat-ardeche.fr/) who is a stonecutter near Annonay, France.

{{< blockcontainer jli-notice-tip "Plus Infomaniak is really working on their impact on the environment" >}}

See about their environmental [on their website](https://www.infomaniak.com/en/ecology).

{{< /blockcontainer >}}

[Contact me if you need help or advice](../../../page/contact-me/index.md) to get started.

### WordPress and Divi on Cloudways

I use WordPress and the Divi builder (which I purchased) and I host on a [Virtual Private Server (VPS) from Cloudways hosting](https://www.cloudways.com/en/?id=174912) all my demo WordPress websites:

- [A music orchestra demo](https://music-demo-wp.puzzlout.com/)
- [A florist business](https://fleuriste-demo.puzzlout.com/)
- [A school dance demo](https://ecole-de-danse-demo.puzzlout.com/)
- [A blank template](https://blank-template-fr.madebyjeremie.fr/)
- [A storefront demo for local farmer market (with Woocommerce but payment)](https://magasin-producteurs-demo.puzzlout.com/)
- [A storefront demo for local farmer market (with Woocommerce and payment possible)](https://boutique-producteurs-demo.puzzlout.com/)
- [A driving school demo](https://auto-moto-ecole.puzzlout.com/)

Why Cloudways for those demo websites? Because Infomaniak is more expensive and less performant for half a dozen demo WordPress sites than a VPS.

It costs me **$11.34 per month** to keep on a minimal VPS running. Cloudways take care of all the server maintenance for me.

I only need to update the WordPress sites now and then.

I have built a custom workflow to deploy those websites using bash scripts. It’s very similar to Infomaniak scripts.

I really like Cloudways because you have access to many features that are usually locked with shared hosting.

Compared to Infomaniak's shared hosting, the different is that you own your server and nobody else works on it. At Infomaniak, a VPS cost 30 euros per month at minimum (and yes, it has more power than the 1 GB Digital Ocean droplet).

[Contact me](../../../page/contact-me/index.md) if you’re interested about the deploy scripts or using Cloudways.

## For newsletters

At the moment, I use Substack only.

Why?

Because it’s free and customizable to reflect your brand.

There are two drawbacks so far:

- The localization isn’t great: when you speak another language than English, you can’t set everything in your language.
- Even if the membership feature is easy to set up (connecting with your Stripe account), you can only setup subscription in US dollars.

I’m hoping for an update soon to solve the first issue soon.

For the membership issue, read on.

## For memberships

I’ve got no subscribers as of March 30, 2023. But I'm working on that thanks to [Darius Foroux's Digital Business school training](https://members.dariusforoux.com/digitalbusiness-school).

However, I have a Stripe account with products in English and French. For those who, one day, will be kind to [support my work with one-time donation or a monthly/yearly subscription](../../../page/sponsor-me/index.md), it is all ready.

At the moment, my personal website, for example, is using payment links that allows anyone to pay in 4 different currencies.

Maybe this will change in 2023.

If you want to follow my progress in the search of the best solution, consider subscribing.
