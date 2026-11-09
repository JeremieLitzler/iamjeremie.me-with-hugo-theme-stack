---
title: "Using LINQ With Awareness"
description: "How rewriting a GET request reduced execution time from 9.5 seconds to 600ms."
image: 2026-11-09-vibrant-orange-lines-and-dots-form-an-abstract-network-on-a-dark-background.jpg
imageAlt: Vibrant orange lines and dots form an abstract network on a dark background, evoking technology and connectivity
date: 2026-11-09
categories:
  - Software Development
tags:
  - LINQ
  - Csharp
---

Who has ever encountered a bug where an apparently simple `GET` request became a performance bottleneck? I have many times, in various scenarios.

Today, I want to share, for you and my future self, an example where a _LINQ_ query was badly written for the expected usage.

## The Starting Point

{{< blockcontainer jli-notice-note "The business entities and the code have been modified for the article.">}}

{{< /blockcontainer >}}

### The Business Logic

We wanted to list the artists of a gallery that a given collector could view.

The endpoint let the frontend application filter by gallery number through Gridify. In practice, the frontend always applied that filter, and the collector identifier was always provided too.

This was a business need defined by the client. There was no other usage of the endpoint.

### The Code

Let’s see the under-performing code.

The query below was used in a query handler, following the CQS (Command Query Separation) pattern.

The result on a properly seeded database with tons of data: a 9.5 seconds execution time.

```csharp
query = _artistsRepository
   .GetEntities(isActive: true, asNoTracking: true)
   .Where(a => a.GalleryArtists.Any(ga =>
       ga.Gallery.AuthorizedCollectors.Any(c =>
           c.CollectorProfileId == collectorId) && ga.IsActive))
   .OrderBy(x => x.Id)
   .Select(x => new Artist
   {
       Id = x.Id,
       Name = x.Name,
       Address = x.Address,
       Address2 = x.Address2,
       ZipCode = x.ZipCode,
       City = x.City,
       CountryIsoCode = x.CountryIsoCode,
       CountryName = x.Country.Name,
       GalleryCode = x.GalleryArtists.FirstOrDefault().Gallery.Number,
   });

```

Do you see the problem?

I don’t show the pagination code because it simply takes the _Gridify_ object the frontend provides and applies it to the `IQueryable<Artist>`. The gallery number filter is therefore appended to the query afterwards, which is why it isn’t visible above.

In the diagnostic tools, you can see the SQL generated from the above LINQ query is far from optimized with a lot of nesting, probably due to the nested `Any` and the `FirstOrDefault()` in the projection, which becomes a correlated subquery.

Also, I suspect that the filter on `GalleryNumber` is not on a table that defines an index for it. However, the diagnostic tools couldn’t output the full query, given it was so long. Thanks EF…

## My Approach

I started by writing the SQL equivalent to the LINQ query to understand the table relationships and, above all, the filters.

```sql
select
    Artist.Id,
    Artist.Name,
    Artist.Address,
    Artist.Address2,
    Artist.ZipCode,
    Artist.City,
    Artist.CountryIsoCode,
    CountryArtist.Name as CountryName,
    GalleryArtist.GalleryNumber as GalleryCode,
    AuthorizedCollector.CollectorProfileId
from Artist
inner join GalleryArtist
    on Artist.Id = GalleryArtist.ArtistId
    and GalleryArtist.IsActive = 1
inner join Gallery
    on Gallery.Number = GalleryArtist.GalleryNumber
    and Gallery.IsActive = 1
inner join AuthorizedCollector
    on AuthorizedCollector.GalleryNumber = Gallery.Number
    and AuthorizedCollector.IsActive = 1
inner join Country CountryArtist
    on Artist.CountryIsoCode = CountryArtist.IsoCode
    and CountryArtist.IsActive = 1
where GalleryArtist.GalleryNumber = @galleryNumber
and AuthorizedCollector.CollectorProfileId = @collectorId
order by Artist.Id

```

Given that SQL, two things surprised me:

- Executing the query in SSMS was blazing fast.
- The actual filters needed by the frontend showed me an optimization.

In fact, the `GalleryArtist.GalleryNumber` could become `AuthorizedCollector.GalleryNumber`. Though the impact on the SQL was small in execution time, it revealed the solution to fix the performance bottleneck in the LINQ query.

## The Solution

So, the LINQ query became:

```csharp
query = _authorizedCollectorRepository
    .GetEntities(isActive: true, asNoTracking: true)
    .Where(ac => ac.CollectorProfileId == collectorId)
    .SelectMany(ac => ac.Gallery.GalleryArtists)
    .Where(ga => ga.IsActive && ga.Artist.IsActive)
    .Select(ga => new Artist
    {
        Id = ga.Artist.Id,
        Name = ga.Artist.Name,
        Address = ga.Artist.Address,
        Address2 = ga.Artist.Address2,
        ZipCode = ga.Artist.ZipCode,
        City = ga.Artist.City,
        CountryIsoCode = ga.Artist.CountryIsoCode,
        CountryName = ga.Artist.Country.Name,
        GalleryCode = ga.Gallery.Number,
    })
    .Distinct()
    // Required `OrderBy` to use Gridify
    .OrderBy(a => a.Id);

```

The `Distinct()` keeps the behavior of the original query: each artist is returned once, even if the collector has several authorization rows for the gallery. Since the frontend always filters by gallery number, the artist comes back with the code of the requested gallery.

The generated SQL by EF wasn’t exactly the SQL written above, but we definitely found the performance gain we needed.

Why? Probably because we filtered the results on the table `AuthorizedCollector`, containing both the `CollectorProfileId` and `GalleryNumber`, both indexed.

On the same database, the endpoint returned the response within 600 ms.

## My Takeaways

- Understand the business logic and the filters needed first. The filters will direct the choices to query the data and use the proper joins.
- Write tests before you refactor. I had existing tests so I felt comfortable doing my update. Plus, the SQL query I wrote in SSMS gave me the same result before any C# refactoring.
- Start your query from the most selective table, and be wary of nested `Any(...)` and `FirstOrDefault()` in the projection of an `IQueryable<T>`. When in doubt, write the SQL first.

The colleague who wrote the original LINQ query shared that it was the quickest solution to code, and it returned the right data. Performance simply wasn’t the concern at that moment.

In the project context, we were in a hurry to deliver features, so optimization wasn’t the priority. It came later, which is a perfectly normal trade-off.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by U.Lucas Dubé-Cantin (`https://www.pexels.com/photo/abstract-orange-lights-10325707/`)
