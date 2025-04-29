---
title: "Enhancing DX with Bash Aliases"
description: "You have many CLI in your project? Let’s enable autocomplete the commands."
image: 2025-04-30-example-of-autocomplete.jpg
imageAlt: Example of autocomplete
date: 2025-04-30
categories:
  - Software Development
tags:
  - Bash
---

You’re using the same commands often but they are long or you don’t remember their syntax? I have a solution for you!

## Bash Aliases

It’s called _bash aliases_ to do the same thing that you can perform with npm scripts, but with a better DX (Developer Experience):

- create a `.bashrc` at the repo root.
- define your aliases, for example:

```bash
alias sp-init='supabase init'
alias sp-login='supabase login'
alias sp-link-env='source .env && echo "linking to $SUPABASE_PROJECT_ID ... using password=$SUPABASE_PROJECT_PASSWORD" && supabase link --project-ref $SUPABASE_PROJECT_ID'
alias sp-gen-types='source .env && supabase gen types --lang=typescript --project-id "$SUPABASE_PROJECT_ID" --schema public > src/types/database.types.ts'
alias sp-db-migrate-new='supabase migration new "$1"'
alias sp-dbreset='supabase db reset --linked'
alias sp-dbseed='node --env-file=.env database/sedding.js'
alias sp-dbrs='sp-dbreset && node --env-file=.env database/sedding.js'
```

## Usage

Run `source .bashrc` from within the terminal in the repository’s root.

Then, run any alias with it name and use `TAB` to list them if you cannot remember one exactly.

To check the aliases are loaded, run `alias` in the terminal.

PS: you'll also have many other predefined aliases in your environment.

To reload the aliases after a change, run `source .bashrc` each time.

I've tested that in Git bash for Windows. On MacOS or Linux, it works just as well.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
