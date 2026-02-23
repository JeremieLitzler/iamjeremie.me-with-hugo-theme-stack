---
title: "About RxJS With Angular"
description: "RxJS is a library for reactive programming in JavaScript, handling asynchronous data streams using observables."
image: 2026-02-23-a-pair-of-vintage-binoculars.jpg
imageAlt: A pair of vintage binoculars
date: 2026-02-23
categories:
  - Web Development
tags:
  - Angular
  - RxJs
---

Following the [course on Angular 18](../understanding-the-basics-of-angular/index.md), I decided to dive deeper into the RxJs concepts and usage.

Thanks to [Sergio from SimpleTech](https://www.youtube.com/@SimpleTechProd), I understand better the ways to use it.

Let’s dive in!

## The Beginning

### What Is RxJS

It stands for _Reactive Extensions for JavaScript_. This library enables asynchronous events to be processed reactively. To understand all this, you need to understand 2 things:

1. What are asynchronous events
2. What is reactivity

You can define asynchronous events as events that can occur at any time, such as a click on a button, a response to an HTTP request or the typing of letters.

The aim is to create more dynamic interfaces and code that is easier to understand and maintain. We all came across the callback hell, didn’t we?

Now, how does this work with RxJS?

RxJS provides an API called `Observable`. It corresponds to a kind of wrapper around asynchronous events, so for example, a wrapper around an HTTP call or a click or keystroke events.

To subscribe to an observable, we’ll use the subscribe method, to which we’ll pass an _Observer_ as a parameter.

You can view an Observer as a collection of one or more of the following methods:

- the `next` method: this is used to receive the events in parameters that our observable will send.
- the `error` method: the observable can send to this method that there has been an error and that it should stop executing. The `error` method takes the error object as a parameter.
- the `complete` method: the observable indicates that it has finished executing and will no longer emit a value.

## The Code Example

Let’s take that the following code example, heavily commented to help you understand:

```tsx
import { Component, OnDestroy } from "@angular/core";
import { Observable, Subscriber, Subscription } from "rxjs";

@Component({
  selector: "app-rx-js-demos",
  imports: [],
  templateUrl: "./rx-js-demos.component.html",
  styleUrl: "./rx-js-demos.component.css",
})
export class RxJsDemosComponent implements OnDestroy {
  // This variable holds the Subscription object returned by
  // the `subscribe()` method.
  speakerSubscription: Subscription | null = null;

  letterSpoken = "";
  constructor() {
    // Initialize the speaker$ observable
    // The Observable named with an ending "$"
    // as naming convention with RxJS
    const speaker$ = new Observable<string>(
      (subscriber: Subscriber<string>) => {
        const textToSend = "Hello RxJS";
        // Loop through the letters of `textToSend`
        // and emit an event with the next method
        // every 250 ms.
        for (let i = 0; i < textToSend.length; i++) {
          setTimeout(
            () => {
              subscriber.next(textToSend[i]);
            },
            (i + 1) * 250,
          );
        }
        // Once the loop is over, emit the event that
        // the observable is complete and will not emit
        // any new event.
        // PS: You need to comment the following timeout,
        // triggering the error event, so the complete can trigger.
        setTimeout(() => {
          subscriber.complete();
        }, textToSend.length * 1000);

        // The following emit an error event.
        setTimeout(
          () => subscriber.error(),
          Math.random() * textToSend.length * 1000,
        );
      },
    );

    // The observer "captures" the events of the observable.
    const speakerObserver = {
      // On `next`, we concatenate the value, e.g. a letter from
      // `textToSend`, to the variable `letters`.
      next: (value: string) => {
        this.letterSpoken = value;
      },
      // On `complete`, we log that the complete event was
      // triggered.
      complete: () => {
        console.log("Speaker has finished!");
      },
      // On `error`, we log that the error event was
      // triggered.
      error: () => {
        console.error("Speaker choked...");
      },
    };

    // This kickstarts the Observable to emit its events
    // as described above.
    // We assign speakerSubscription to allow unsubscription
    // when the componenent is destroyed (see `ngOnDestroy`)
    this.speakerSubscription = speaker$.subscribe(speakerObserver);
  }

  ngOnDestroy(): void {
    // This prevents memory leaks. Forgetting to unsubscribe
    // from Observable can generate complex bugs to resolve.
    this.speakerSubscription?.unsubscribe();
  }
}
```

If we printed the `letterSpoken`, we would see all the letters displayed one at a time.

```html
<p>{{ letterSpoken }}</p>
```

We can achieve the same behavior with a `AsyncPipe` from `@angular/common`:

```tsx
import { AsyncPipe } from "@angular/common";
import { Component } from "@angular/core";
import { FormControl, ReactiveFormsModule } from "@angular/forms";
import { Observable, Subscriber, Subscription } from "rxjs";

@Component({
  selector: "app-rx-js-demos",
  imports: [AsyncPipe, ReactiveFormsModule],
  templateUrl: "./rx-js-demos.component.html",
  styleUrl: "./rx-js-demos.component.css",
})
export class RxJsDemosComponent {
  // Declare the Observable as null by default
  anotherSpeaker$: Observable<string> | null = null;

  constructor() {
    // Define the Observable behavior
    this.anotherSpeaker$ = new Observable<string>(
      (subscriber: Subscriber<string>) => {
        const textToSend = "Hello RxJS";
        for (let i = 0; i < textToSend.length; i++) {
          setTimeout(
            () => {
              subscriber.next(textToSend[i]);
            },
            (i + 1) * 250,
          );
        }
        setTimeout(() => {
          subscriber.complete();
        }, textToSend.length * 1000);
      },
    );
  }
}
```

Then we can use the Observable directly in the HTML:

```html
<!-- async  -->
<p>{{ anotherSpeaker$ | async }}</p>
```

But where are the `subscribe` and `unsubsribe` calls?

`AsyncPipe` takes care of this for us:

1. It does the subscription,
2. It retrieves the values sent
3. And when the template is no longer in use, it will even take care of the unsubscription for us.

Now let’s try this with a form input and display the text typed underneath it.

The TypeScript would become:

```tsx
import { AsyncPipe } from "@angular/common";
import { Component } from "@angular/core";
import { FormControl, ReactiveFormsModule } from "@angular/forms";

@Component({
  selector: "app-rx-js-demos",
  imports: [AsyncPipe, ReactiveFormsModule],
  templateUrl: "./rx-js-demos.component.html",
  styleUrl: "./rx-js-demos.component.css",
})
export class RxJsDemosComponent {
  // Defines the input
  textFormControl = new FormControl("");
  // Defines the Observable, coming from the `valueChanges`
  textTyped$ = this.textFormControl.valueChanges;
}
```

Then, in the template, you have:

```html
<div><input [formControl]="textFormControl" /></div>
<p>{{ textTyped$ | async }}</p>
```

As you type into the input, `textTyped$` updates. `async` from `AsyncPipe` handle the subscribe and unsubscribe and fills the p tag with the value.

## RxJS Operators

We can use a variety of operators as its website lists:

- [Creation Operators](https://rxjs.dev/guide/operators#creation-operators-1)
- [Join Creation Operators](https://rxjs.dev/guide/operators#join-creation-operators)
- [Transformation Operators](https://rxjs.dev/guide/operators#transformation-operators)
- [Filtering Operators](https://rxjs.dev/guide/operators#filtering-operators)
- [Join Operators](https://rxjs.dev/guide/operators#join-operators)
- [Multicasting Operators](https://rxjs.dev/guide/operators#multicasting-operators)
- [Error Handling Operators](https://rxjs.dev/guide/operators#error-handling-operators)
- [Utility Operators](https://rxjs.dev/guide/operators#utility-operators)

### Starting Example That Doesn’t Work

Let’s say we want to want to build a search component to filter a person list.

We have:

- this TypeScript code:

  ```tsx
  import { Component, inject, OnDestroy } from "@angular/core";
  import {
    FormControl,
    FormsModule,
    ReactiveFormsModule,
  } from "@angular/forms";
  import { CommonModule } from "@angular/common";
  import { PersonService } from "../../services/person/person.service";
  import { Person } from "../../interfaces/person.interface";
  import { Subscription } from "rxjs";

  @Component({
    selector: "app-search-page",
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, FormsModule],
    templateUrl: "./search.component.html",
    styleUrls: ["./search.component.css"],
  })
  export class SearchPageComponent implements OnDestroy {
    private personService = inject(PersonService);

    searchTextFormControl = new FormControl<string>("");
    subscriptions: Subscription = new Subscription();
    searchResult: Person[] = [];

    constructor() {
      const textValueChangeSubscription =
        // As the search is typed...
        this.searchTextFormControl.valueChanges.subscribe(
          (value: string | null) => {
            const searchTerm = value ? value : "";
            const searchSubscription = this.personService
              // we call the search method of PersonService ...
              .search(searchTerm)
              .subscribe((result: Person[]) => {
                // ... and update the searchResult variable
                // which update the UI
                this.searchResult = result;
              });
            this.subscriptions.add(searchSubscription);
          },
        );
      this.subscriptions.add(textValueChangeSubscription);
    }

    ngOnDestroy(): void {
      this.subscriptions.unsubscribe();
    }
  }
  ```

- this HTML code:

  ```html
  <div>
    <input
      [formControl]="searchTextFormControl"
      placeholder="Search for a last name or first name..."
    />
    <div>Number of results: {{ searchResult.length }}</div>
    <ul>
      @for (person of searchResult; track person) {
      <li>
        {{ person.firstName }} {{ person.firstName }} - {{ person.birthDate |
        date: "shortDate" : "" : "fr-FR" }}
      </li>
      }
    </ul>
  </div>
  ```

- A service to query some static data:

  ```tsx
  import { Injectable } from "@angular/core";
  import { Observable } from "rxjs";
  import { Person } from "../../interfaces/person.interface";

  @Injectable({
    providedIn: "root",
  })
  export class PersonService {
    private DATA: Person[] = [
      /* Details ommited for the sake of brievity */
    ];

    search(term: string): Observable<Person[]> {
      // The delay will allow to get results after a variable
      // lapse of time.
      const delay = Math.round(Math.random() * 400) + 100;
      const filteredData = this.DATA.filter(
        (item: Person) =>
          item.firstName.toLowerCase().includes(term.toLowerCase()) ||
          item.lastName.toLowerCase().includes(term.toLowerCase()),
      );
      return new Observable((observer) => {
        setTimeout(() => {
          observer.next(filteredData);
          observer.complete();
        }, delay);
      });
    }
  }
  ```

But when we use it, we notice 2 things:

1. Nothing is displayed by default. This shouldn’t happen.
2. The search result for `a` returns values that shouldn’t appear…

Why?

The way the component code is written, e.g., with nested `subscribe`, doesn’t guarantee that the result will contain the expected result because values from the preceding execution will collide with the newest result sets.

### The Better Implementation

The previously described issues give us the opportunity to understand the `pipe` method. To me, it feels like calling `fetch` and being able to chain several `then` methods, as long as you return a Promise at the end of each `then`.

A `then` is equivalent to the operator you’ll use inside `pipe`.

Let’s take a look at the refactored code:

```tsx
import { Component, inject } from "@angular/core";
import { FormControl, FormsModule, ReactiveFormsModule } from "@angular/forms";
import { CommonModule, AsyncPipe } from "@angular/common";
import { PersonService } from "../../services/person/person.service";
import { Person } from "../../interfaces/person.interface";
import { switchMap, Observable } from "rxjs";

@Component({
  selector: "app-search-page",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, AsyncPipe],
  templateUrl: "./search.component.html",
  styleUrls: ["./search.component.css"],
})
export class SearchPageComponent {
  private personService = inject(PersonService);

  searchTextFormControl = new FormControl<string>("");
  searchResult$: Observable<Person[]> =
    // `valueChanges` is equivalent to `subscribe()`
    // which allows to use `pipe()`
    this.searchTextFormControl.valueChanges.pipe(
      switchMap((searchTerm: string | null) => {
        return this.personService.search(searchTerm ?? "");
      }),
    );
}
```

The operator `switchMap` takes the values of an Observable and returns a new Observable from those values. It takes care of canceling any previous Observable.

In the example, it returns an Observable from the `PersonService` using the current search term. But if you type something new (second search) before the first call to PersonService finishes, then the first call is canceled.

Then, the HTML code becomes:

```html
<!-- We need to use `async` in order to use the value of `searchResult$` -->
@for (person of searchResult$ | async; track person) {
<li>
  {{ person.firstName }} {{ person.lastName }} - {{ person.birthDate | date:
  "shortDate" : "" : "fr-FR" }}
</li>
}
```

### Chaining Operators

The other problem in the example is that the starting point shows nothing when the input is empty. We should have all the persons displayed.

Using the operator `startWith`, we can fix that. This operator allows to emit an initial value:

```tsx
import { switchMap, Observable, startWith } from "rxjs";
export class SearchPageComponent {
  searchResult$: Observable<Person[]> =
    this.searchTextFormControl.valueChanges.pipe(
      startWith(""), // empty search
      switchMap((searchTerm: string | null) => {
        return this.personService.search(searchTerm ?? "");
      }),
    );
}
```

{{< blockcontainer jli-notice-warning "⚠️ The order matters">}}

Put the operators in the order your business logic should run!

{{< /blockcontainer >}}

Let’s look at two last operators to give the `PersonService` some air and improve the UX 🌟

```tsx
import { switchMap, Observable, startWith, debounceTime, tap } from 'rxjs';
export class SearchPageComponent {
  searchResult$: Observable<Person[]> =
  searchResult$: Observable<Person[]> =
    this.searchTextFormControl.valueChanges.pipe(
      // Wait 500 ms before starting a new search.
      // Prevents calling the service as the user
      // types his/her search.
      debounceTime(500),
      startWith(''),
      // UX: Starting the search, but no result yet...
      tap(() => (this.loading = true)),
      switchMap((searchTerm: string | null) => {
        return this.personService.search(searchTerm ?? '');
      }),
      // UX: The search result is available!
      tap(() => (this.loading = false)),
    );
}
```

In the HTML, it looks like this:

```html
<!-- display the loader... -->
@if (loading) {
<p style="text-align: center">Loading...</p>
<!-- ... until the data becomes available -->
} @else {
<ul>
  @for (person of searchResult$ | async; track person) {
  <li>
    {{ person.firstName }} {{ person.lastName }} - {{ person.birthDate | date:
    "shortDate" : "" : "fr-FR" }}
  </li>
  }
</ul>
}
```

## An Observable Dependent on Another

In the component, we added a result count, but it was broken after the first refactor. This is the opportunity to showcase a new Observable depending on our existing one:

```tsx
import { switchMap, Observable, startWith, debounceTime, tap, map } from "rxjs";
export class SearchPageComponent {
  searchResultCount$: Observable<number> = this.searchResult$.pipe(
    map((searchResult) => searchResult.length),
  );
}
```

Once the `searchResult$` Observable resolves, we can evaluate `searchResultCount$` and use it in the HTML:

```html
<div>Number of results: {{ searchResultCount$ | async }}</div>
```

## Conclusion

What did you learn? RxJs makes sense now? Thanks to Sergio, it was the case for me and I’m forward to putting this into practice on some projects.

As always…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [ClickerHappy](https://www.pexels.com/photo/black-binocular-on-round-device-63901/).
