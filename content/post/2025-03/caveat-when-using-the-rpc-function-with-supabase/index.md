---
title: "Caveat when using the RPC function with Supabase"
description: "Using the RPC method on the Supabase client requires an additional step and TypeScript is involved."
image: 2025-03-12-illuminated-road-work-cone.jpg
imageAlt: An illuminated red road work cone
date: 2025-03-12
categories:
  - Web Development
tags:
  - Supabase
  - Postgres
  - TypeScript
---

On January 27th, I shared a tip to [use Postgres functions](../../2025-01/the-order-by-clause-with-dates-in-supabase/index.md) to perform an advanced ordering on a table.

Let me show you the error I didn’t catch right away.

## The Issue

On all the code related to the `allEntitiesQuery`, many TypeScript errors showed up.

I saw the first issue in the datatable’s columns definition where TypeScript was telling me that the properties of `AllEntitiesType` didn’t exist.

![Code example with TypeScript error](code-example-with-typescript-error.png)

## The Cause

Supabase’s RPC returns the correct type according to the function’s return type, as defined in your database schema ([source](https://www.restack.io/docs/supabase-knowledge-supabase-rpc-typescript-guide)).

In my case, I set `RETURNS SETOF json AS $$` and so it did:

![Code example with proper type](code-example-with-proper-type.png)

Since you can call the function with the table name as an input parameter, the returned type made sense to me.

But how do I fix the TypeScript errors?

## The Fix

To fix this, you need to use Supabase generated types and create a new custom type:

```tsx
import type { Database } from "@/types/DatabaseTypes";

export type EntityRecordWithRpc =
  Database["public"]["Tables"]["entities"]["Row"];
```

Then, you update the returned type to `as unknown as PostgrestSingleResponse<EntityRecordWithRpc[]>` on the `allEntitiesQuery`.

The TypeScript requires the `as unknown` cast first before the `as PostgrestSingleResponse<EntityRecordWithRpc[]>` because neither type sufficiently overlaps with the other (See [rule _ts(2352)_](https://medium.com/@maciej.osytek/downcasting-in-typescript-how-to-avoid-the-ts-2352-error-632a7b122b16)).

Next, replace all references of `AllEntitiesTypes` to `EntityRecordWithRpc`.

Finish with another run of the build script. It should show resolution of all TypeScript errors!

## Conclusion

My takeaway: I need to add a CI step to run the `npm run build` on each PR. A topic for another article. Stay tuned!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Mido Makasardi ©️](https://www.pexels.com/photo/red-led-traffic-cone-2743739/)
