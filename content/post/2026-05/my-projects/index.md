

---
title: "My Ongoing Projects"
description: "A selection of personal projects I built to solve real problems and sharpen my skills with various technical stacks and AI."
image: 2026-05-04-portfolio_feature_terminal_strip.svg
imageAlt: Portfolio Feature Terminal Strip
date: 2026-05-04
categories:
  - Software Development
tags:
  - Vue
  - Python
  - Netlify
  - GitHub Actions
  - Claude Code
---

## Social Media Sharing Assistant

**What:** A single-page application that automates the formatting and preparation of blog articles for sharing across X, LinkedIn, Medium and Substack. Given an article URL and a target platform, it extracts the relevant content, generates UTM-tagged links and produces ready-to-copy text for each platform.

**Why:** Sharing a single blog post to four platforms meant navigating back and forth, copying the same information repeatedly and manually adapting formatting — especially time-consuming for Medium and Substack. This tool cuts that process down to two inputs and a clipboard click.

**Who:** Built for my own use as the author of two bilingual blogs (English and French).

**How:** The app fetches the article HTML via a Netlify Functions proxy (to bypass CORS), parses the consistent Hugo-generated structure, and renders platform-specific outputs in the browser.

**Stack:** Vue.js, TypeScript, Vite, Netlify Functions, Tailwind CSS

[Live website](https://share.madebyjeremie.fr/) · [View on GitHub](https://github.com/JeremieLitzler/SocialMediaPublisherApp)


## Coup de Pompe — French Gas Station Price Tracker

**What:** A web app that scrapes fuel prices from the French government website (prix-carburants.gouv.fr) for a user-defined list of gas stations and displays them side by side in a sortable table.

**Why:** Comparing fuel prices across nearby stations required opening each page individually. This tool puts all the prices in one view so I can spot the cheapest option at a glance.

**Who:** Anyone in France who regularly fills up and wants to track a handful of local stations.

**How:** The user manages a list of station URLs stored in IndexedDB. On load, a Netlify serverless function fetches each station's HTML, the client parses the price table, and the results are presented in a filterable Vue component.

**Stack:** Vue.js, TypeScript, Vite, Netlify Functions, Tailwind CSS, IndexedDB

[Live website](https://coupdepompe.madebyjeremie.fr/) · [View on GitHub](https://github.com/JeremieLitzler/french-gas-stations-scraper)

---

## Dead Link Probe

**What:** A CLI tool that crawls a website via breadth-first search, discovers every internal and external link, checks their HTTP status in parallel, and outputs a CSV report plus a Markdown summary of broken links.

**Why:** Maintaining two blogs means hundreds of internal and external links that can silently break over time. A scheduled scan catches 404s, redirects and server errors before readers do.

**Who:** Any website owner who wants automated dead-link detection without relying on a third-party SaaS.

**How:** The crawler walks internal pages single-threaded (BFS), collecting all link/referrer pairs. A thread pool then fires HEAD requests against every discovered URL (falling back to GET on 405). Results are written to a timestamped scan folder. A GitHub Actions workflow runs nightly and commits results to a dedicated data branch. Optional email notifications via Resend alert the operator when non-200 statuses are found.

**Stack:** Python 3 (standard library only for core logic), GitHub Actions, Resend SDK for notifications

[Live website](https://www.deadlinkprobe.com/) · [View on GitHub](https://github.com/JeremieLitzler/deadlinkprobe)

---

## IFU Generator (CH → FR)

**What:** A set of Python scripts that generate the French tax declaration data (IFU equivalent) for investment accounts held at Yuh/Swissquote and Wise Assets. It produces detailed CSVs and a unified Markdown summary with the exact figures needed to fill in tax forms 2074, 2086 and 2042.

**Why:** French-resident cross-border workers (_frontaliers_) investing through Swiss or international brokers receive no IFU from their broker. Computing capital gains using the PMP method (weighted average cost basis) with ECB exchange rates by hand is tedious and error-prone — especially across multiple brokers and currencies (CHF, USD, EUR).

**Who:** French residents working in Switzerland who hold investment accounts at Yuh/Swissquote or Wise Assets and need to declare capital gains, dividends and positions to the French tax authorities.

**How:** The scripts parse broker CSV exports, apply the PMP method as defined by article 150-0 D of the French tax code, fetch ECB exchange rates (with weekend/holiday fallback to last business day), and produce per-broker and unified outputs ready for the annual declaration.

**Stack:** Python 3, ECB exchange rate API, shell scripts

Live website: _under construction_ · [View on GitHub](https://github.com/JeremieLitzler/ifu-generator-ch-to-fr)
