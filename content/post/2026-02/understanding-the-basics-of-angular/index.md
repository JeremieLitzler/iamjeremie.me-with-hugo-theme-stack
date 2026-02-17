---
title: "What I Learned In A 4h Course On Angular"
description: "Angular is a competitor framework to Vue.js. Do you like it?"
image: 2026-02-16-angular-logo-in-the-hand-of-someone.jpg
imageAlt: The Angular logo in the hand of someone
date: 2026-02-16
categories:
  - Web Development
tags:
  - Angular
---

I love Vue.js but learning another JS framework could be useful in the missions I participate in.

I decided to deepen my knowledge of Angular with a 4h YouTube course.

The course is based on Angular 17, but I worked with Angular 19 at the time I followed it, so I became acquainted with the more recent API that Angular provides.

## Installation of the development environment

### Install NodeJS

For Windows, use Scoop:

```powershell
scoop install main/nodejs-lts
```

Note: Install the LTS version to avoid “_Warning: The current version of Node (23.9.0) isn’t supported by Angular._” messages from Angular on the next step.

### Install Angular

```bash
npm install -g @angular/cli
ng version
# Should output the latest Angular version
```

**IMPORTANT:** At the time of writing this, Angular is at v19 while the course was taught in Angular 17 and 18.

### Extensions for VSCode

I personally use the following:

- [https://marketplace.visualstudio.com/items?itemName=1tontech.angular-material](https://marketplace.visualstudio.com/items?itemName=1tontech.angular-material)
- [https://marketplace.visualstudio.com/items?itemName=alexiv.vscode-angular2-files](https://marketplace.visualstudio.com/items?itemName=alexiv.vscode-angular2-files)
- [https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)
- [https://marketplace.visualstudio.com/items?itemName=cyrilletuzi.angular-schematics](https://marketplace.visualstudio.com/items?itemName=cyrilletuzi.angular-schematics)
- [https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [https://marketplace.visualstudio.com/items?itemName=editorconfig.editorconfig](https://marketplace.visualstudio.com/items?itemName=editorconfig.editorconfig)
- [https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)
- [https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag)
- [https://marketplace.visualstudio.com/items?itemName=gruntfuggly.todo-tree](https://marketplace.visualstudio.com/items?itemName=gruntfuggly.todo-tree)
- [https://marketplace.visualstudio.com/items?itemName=humao.rest-client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
- [https://marketplace.visualstudio.com/items?itemName=infinity1207.angular2-switcher](https://marketplace.visualstudio.com/items?itemName=infinity1207.angular2-switcher)
- [https://marketplace.visualstudio.com/items?itemName=john-crowson.angular-file-changer](https://marketplace.visualstudio.com/items?itemName=john-crowson.angular-file-changer)
- [https://marketplace.visualstudio.com/items?itemName=loiane.angular-extension-pack](https://marketplace.visualstudio.com/items?itemName=loiane.angular-extension-pack)
- [https://marketplace.visualstudio.com/items?itemName=obenjiro.arrr](https://marketplace.visualstudio.com/items?itemName=obenjiro.arrr)
- [https://marketplace.visualstudio.com/items?itemName=patbenatar.advanced-new-file](https://marketplace.visualstudio.com/items?itemName=patbenatar.advanced-new-file)
- [https://marketplace.visualstudio.com/items?itemName=pucelle.vscode-css-navigation](https://marketplace.visualstudio.com/items?itemName=pucelle.vscode-css-navigation)
- [https://marketplace.visualstudio.com/items?itemName=quicktype.quicktype](https://marketplace.visualstudio.com/items?itemName=quicktype.quicktype)
- [https://marketplace.visualstudio.com/items?itemName=rctay.karma-problem-matcher](https://marketplace.visualstudio.com/items?itemName=rctay.karma-problem-matcher)
- [https://marketplace.visualstudio.com/items?itemName=segerdekort.angular-cli](https://marketplace.visualstudio.com/items?itemName=segerdekort.angular-cli)
- [https://marketplace.visualstudio.com/items?itemName=simontest.simontest](https://marketplace.visualstudio.com/items?itemName=simontest.simontest)
- [https://marketplace.visualstudio.com/items?itemName=steoates.autoimport](https://marketplace.visualstudio.com/items?itemName=steoates.autoimport)
- [https://marketplace.visualstudio.com/items?itemName=stringham.move-ts](https://marketplace.visualstudio.com/items?itemName=stringham.move-ts)
- [https://marketplace.visualstudio.com/items?itemName=techer.open-in-browser](https://marketplace.visualstudio.com/items?itemName=techer.open-in-browser)
- [https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost](https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost)

### Create a project

```bash
ng new project-name
```

See [my notes about the discountinued `assets` folder under `src`](https://github.com/JeremieLitzler/angular-course-with-simpletech/blob/main/playing-cards/public/assets/README.md).

## The components

To create a component, use this command:

```bash
# short form of ng generate component components/playing-card
ng g c components/playing-card
```

The above creates a new subfolder `components/playing-card` under `app`. The scaffolded component is defined with the `.css`, `.html`, `ts` and `spec.ts` files.

To skip the test file generation, simply the flag `--skip-tests` on the above command.

## Inputs And Signal Inputs

The first manner to declare inputs is the decorator:

```tsx
  @Input() name: string = 'Default Name';
```

You can then use it in the parent component that uses it:

```html
<app-playing-card name="My custom name" />
```

However I learned that if you define an input with a different type than a `string`, then you must use the `[ ]`.

For example:

```html
<app-playing-card [hp]="20" />
```

It can also contain a simple JavaScript expression:

```html
<!-- will output 54 as HP value -->
<app-playing-card [hp]="20+34" />
```

Similarly, we can pass on objects:

```html
<app-playing-card [card]="pik" />
```

To work, you should use the best practice to create a `model` class that you use to initialize `pik` and set the input type of `app-playing-card` to the class name.

For example, I could have this class:

```tsx
export class Card {
  // the type is inferred since we only use primitives in this example
  name = "Default Card Name";
  hp = 40;
  figureCaption = "Default Card figure caption";
  attackName = "Default Attack name";
  attackStrength = 60;
  attackDesc = "Default Attack description";
}
```

I use it to declare `pik` in my `app.component`:

```tsx
export class AppComponent {
  // The "!" is used for what?
  pik!: Card;

  constructor() {
    this.pik = {
      name: "Pikachou",
      hp: 100,
      attackDesc: "Pikachou strikes !!!",
      attackName: "Strike",
      attackStrength: 40,
      figureCaption: "The famous one",
    };
  }
}
```

{{< blockcontainer jli-notice-note "About `!`">}}
The `!` is the definite assignment assertion operator.

It tells TypeScript’s compiler: “_I know this property looks like not initialized, but trust me—it will be assigned a value before it’s used._”

Without it, TypeScript would error because the object `pik` is declared but not immediately initialized at the declaration. Since you’re assigning it to the constructor, the `!` suppresses that error.

{{< /blockcontainer >}}

And I use it to type the input of my child’s component:

```tsx
export class PlayingCardComponent {
  @Input() card: Card = new Card();
}
```

Another feature using the `@Input` decorator is its configuration: you could make the card input required:

```tsx
  @Input({
    required: true,
  })
  card: Card = new Card();
```

And TypeScript would tell you the following:

![Example of TypeScript error](example-of-typescript-error.png)

You can customize the attribute name with `alias` or transform your input object into `transform`, but I don’t see a good use case to give an example for it.

Now, since Angular 17, you can use the signal inputs the following way:

```tsx
export class PlayingCardComponent {
  card: InputSignal<Card> = input(new Card());
}
```

In the HTML, you’ll need to add `()` to access the input properties.

```html
<!-- With @Input() -->
<div id="name">{{ card.name }}</div>
<!-- With signal input -->
<div id="name">{{ card().name }}</div>
```

## Outputs, signal outputs and models

When we need to communicate data from a child component to its parent, we can use the `@Output` decorator. We also call it emitted events.

A very simple example would look like this:

```tsx
  // in your child component TS file
  // You declare the output
  @Output() searchButtonClicked = new EventEmitter();

  // You declare the method that triggers the emit.
  searchClick() {
    this.searchButtonClicked.emit();
  }
```

In your child’s component HTML file, you can add the `searchClick` to a button:

```html
<button (click)="searchClick()">
  <img src="assets/icons/lucide--search.svg" alt="Search icon" />
</button>
```

Then, on your parent component TS file, you add a property `searchClickCount` initialized to 0 and you can listen to events and print out the updated `searchClickCount` value.

```html
<app-search-bar (searchButtonClicked)="increaseCount()" />
<p>Search click count: {{ searchClickCount }}</p>
```

Now, often, we pass data up and in the above example, we don’t.

Let’s say we want to show the searched term on the parent component.

First we need to update the child component TS file:

```tsx
  @Input() searchTerm = '';
  @Output() searchTermChange = new EventEmitter<string>();

  updateSearch(value: string) {
    this.searchTermChange.emit(value);
  }
```

Then we update the child component HTML file to use `searchTerm` with the directive `[ngModel]`:

```html
<input
  type="text"
  placeholder="Search..."
  [ngModel]="searchTerm"
  (ngModelChange)="updateSearch($event)"
/>
```

Finally, we add the `searchedTerm = $event` property to the parent component to complete the **two-ways data binding** and we finish with updating the parent component HTML file:

```html
<app-search-bar
  (searchButtonClicked)="increaseCount()"
  [searchTerm]="searchedTerm"
  (searchTermChange)="searchedTerm = $event"
/>
```

However, we can shorten that code to the following:

```html
<app-search-bar [(searchTerm)]="searchedTerm" />
<p>Search term: {{ searchedTerm }}</p>
```

This is only possible because the output in the child component is named like the input with the prefix `Change`. Angular will tell you if you use the short version incorrectly.

Similarly to inputs, from Angular 17.3, you can use the new method with output signals:

```tsx
searchTerm = input<string>();
searchTermChange = output<string>();
searchButtonClicked = output();
```

All the rest of the code doesn’t change.

Since Angular 17.2, you could also simplify ever more the code using `model`. In your TS file, the child component would become:

```tsx
  searchTerm = model<string>();
  updateSearch(value: string) {
    this.searchTerm.set(value);
  }
```

In the HTML, you can change the code to the following thanks to the two-ways data binding with `[(ngModel)]` directive:

```html
<input type="text" placeholder="Search..." [(ngModel)]="searchTerm" />
```

With that, you can remove the `updateSearch` method.

## Detecting changes

Angular has several lifecycle hooks on components that help you to initialize a component and execute logic on changes.

You can find the [full list in the documentation](https://angular.dev/guide/components/lifecycle).

### Default Strategy vs `OnPush`

By default, when a event is triggered on a component, Angular checks all the component tree.

This could causes performance issue on a large application.

That when you can use the `OnPush` strategy. This limits Angular to only check OnPush components when their inputs change, an event occurs within them, or a bound observable emits — skipping unnecessary checks otherwise.

Sergio, author of the course I followed, explains it very well [in his course](https://youtu.be/U71TQN68QGU?si=lBZl7qu4OXhGMMWa&t=5610). If you don’t speak french, enable the auto-translate subtitles on YouTube.

### Signals In Angular

Coming from Vue.js, I feel like that Angular took the best of Vue’s reactivity with the signal primitives that you can use from Angular 16:

- `signal()` ≈ `ref()` in Vue, both create reactive primitives.
- `computed(() => {})`: is it a copy-paste from Vue? At least, it works the same.
- `effect()` ≈ `watchEffect()` (not watch) which runs automatically when dependencies change

For example, let’s say we store a selected index into a signal and an object into a computed that changes as the index changes:

```tsx
  selectedIndex = signal<number>(1);
  selectedCard = computed<Card>(
    () => this.cards[this.selectedIndex()],
  );

  // No direct assignement but a use of `set` on the signal property.
  toggleCard() {
    this.selectedIndex.set(
      (this.selectedIndex() + 1) % this.cards.length,
    );
  }
```

Then, in the HTML, we can change:

```html
<!-- without signal or computed -->
<app-playing-card [card]="cards[selectedIndex]" />
```

to

```html
<!-- with signal or computed -->
<app-playing-card [card]="selectedCard()" />
```

Using signals makes the code cleaner and shorter. For example, the TypeScript was the following using the historic method:

```tsx
import {
  Component,
  input,
  OnChanges,
  OnInit,
  SimpleChanges,
} from "@angular/core";
import { Card } from "../../models/card.model";
import { CardTypeProperties } from "../../utils/card.utils";

@Component({
  selector: "app-playing-card",
  imports: [],
  templateUrl: "./playing-card.component.html",
  styleUrl: "./playing-card.component.css",
})
export class PlayingCardComponent implements OnInit, OnChanges {
  card = input(new Card());
  cardTypeIcon!: string;
  backgroundColor!: string;

  ngOnInit(): void {
    this.setIcon();
    this.setBackgroundColor();
  }
  ngOnChanges(changes: SimpleChanges): void {
    if (!changes["card"]) {
      return;
    }
    if (
      changes["card"].previousValue?.type === changes["card"].currentValue.type
    ) {
      return;
    }
    this.setIcon();
    this.setBackgroundColor();
  }

  setIcon() {
    this.cardTypeIcon = CardTypeProperties[this.card().type].iconUrl;
  }
  setBackgroundColor() {
    console.log(`color is ${CardTypeProperties[this.card().type].color}`);
    this.backgroundColor = CardTypeProperties[this.card().type].color;
  }
}
```

With signals and keeping the same functionnality, we have:

```tsx
import { Component, computed, input } from "@angular/core";
import { Card } from "../../models/card.model";
import { CardTypeProperties } from "../../utils/card.utils";

@Component({
  selector: "app-playing-card",
  imports: [],
  templateUrl: "./playing-card.component.html",
  styleUrl: "./playing-card.component.css",
})
export class PlayingCardComponent {
  card = input(new Card());
  cardTypeIcon = computed(() => CardTypeProperties[this.card().type].iconUrl);
  backgroundColor = computed(() => CardTypeProperties[this.card().type].color);
}
```

### Why Signals Then

Eventually, Angular will drop out the change detection, performed currently with the library `zone.js`, and use signals to check only the components that we need on events.

This will improve greatly the performance of large applications!

## Loops and conditions

### Using Loops

Nothing extraordinary for simple usage. Make sure to import `CommonModule` in your TS file and then use the `*ngFor` directive as follows:

```html
<div class="cards">
  <app-playing-card *ngFor="let card of filteredCards()" [card]="card" />
</div>
```

### Using Conditions

With conditions, we can use different approaches:

- several `*ngIf` directives

  ```html
  <p *ngIf="filteredCards().length === 0" style="text-align: center">
    No card found
  </p>
  <p *ngIf="filteredCards().length > 0" style="text-align: center">
    Found {{ filteredCards().length }} card{{ filteredCards().length > 1 ? "s" :
    "" }}!
  </p>
  ```

- a single `*ngIf` with a `<ng-template>` element. It makes me think named slots, but it isn’t the same.

  ```html
  <p
    *ngIf="filteredCards().length === 0; else resultsFound"
    style="text-align: center"
  >
    No cards found
  </p>
  <ng-template #resultsFound>
    <p style="text-align: center">
      Found {{ filteredCards().length }} card{{ filteredCards().length > 1 ? "s"
      : "" }}!
    </p>
  </ng-template>
  ```

- a single `*ngIf` with several `<ng-template>` elements

  ```html
  <p
    *ngIf="filteredCards().length === 0; then empty; else resultsFound"
    style="text-align: center"
  ></p>
  <ng-template #empty>
    <p style="text-align: center">No cards found</p>
  </ng-template>
  <ng-template #resultsFound>
    <p style="text-align: center">
      Found {{ filteredCards().length }} card{{ filteredCards().length > 1 ? "s"
      : "" }}!
    </p>
  </ng-template>
  ```

### New Syntax For Conditions

With Angular 17, new syntax brought the ability to write cleaner and clearer code.

If we take the last example above with the condition, we could now write:

```html
@if (filteredCards().length === 0) {
<p style="text-align: center">No cards found</p>
} @else {
<p style="text-align: center">
  Found {{ filteredCards().length }} card{{ filteredCards().length > 1 ? "s" :
  "" }}!
</p>
}
```

Similarly, we rewrite the loop:

```html
@for (card of filteredCards(); track card) {
<app-playing-card [card]="card" />
}
```

What does the `track` mean? Angular uses it to _track_ DOM updates to the minimum when the data changes.

Regarding `@for`, you can use it alongside with `@empty’ so that our previous code the `@if...@else` becomes:

```html
<div class="cards">
  @for (card of filteredCards(); track card) {
  <app-playing-card [card]="card" />
  } @empty {
  <!-- if empty -->
  <p style="text-align: center">No cards found</p>
  }
</div>
@if (filteredCards().length > 0) {
<p style="text-align: center">
  Found {{ filteredCards().length }} card{{ filteredCards().length > 1 ? "s" :
  "" }}!
</p>
}
```

`@for` provides a few extra variables you can use: `$index`, `$first`, `$last`, `$odd`, `$event` and `$count`. [Read the documentation](https://angular.dev/api/core/@for#index-and-other-contextual-variables) for more details.

If you were to code nested `@for`, accessing those built-in variables could become tricky. You can name each variable for a `@for` after the `track` like so:

```html
@for (card of filteredCards(); track card; let i = $index;) {
<app-playing-card [card]="card" />
}
```

The same exists on `*ngFor` but you must declare a local variable if you need to use them. Please [read the documentation](https://angular.dev/api/common/NgFor#local-variables) for more information on the topic.

## Services

A service in Angular allows to separate the UI logic from the data and business logic.

We use services as injectable singletons.

You can create the service using the CLI:

```bash
ng g s services/card
```

Before Angular 14, you could inject services into components through the constructors, hence the name _Constructor Dependency Injection_ that many software engineers use when implementing _S.O.L.I.D_ principles.

```tsx
export class AppComponent {
  constructor(private cardService: CardService) {
    this.cardService.init(); // Outputs "CardService is ready!"
  }
}
```

However, that method makes inheritance complex. Instead, you can now use the new method `inject`:

```tsx
export class AppComponent {
  cardService = inject(CardService);
  constructor() {
    this.cardService.init(); // Outputs "CardService is ready!"
  }
}
```

Angular’s services bridge the components to the data source, whatever it could be for your application.

It can contain [CRUD methods](https://www.google.com/search?q=CRUD) or any business logic to prepare data for your components.

For example:

```tsx
  getAll() {
    return this.cards.map((m) => m.copy());
  }

  get(id: number) {
    const match = this.cards.find((m) => m.id === id);
    return match ? match.copy() : undefined;
  }

  add(card: Card) {
    const newCard = card.copy();
    newCard.id = this.currentIndex;
    this.cards.push(newCard.copy());
    this.currentIndex++;
    this._save();

    return newCard;
  }

  update(card: Card) {
    const updatedCard = card.copy();
    const cardIndex = this.cards.findIndex(
      (originalCard) => originalCard.id === card.id,
    );

    if (cardIndex !== -1) {
      this.cards[cardIndex] = updatedCard.copy();
      this._save();
    } else {
      console.warn(
        `No card found for id=<${card.id}>. Caching or UI refresh issue?`,
      );
    }

    return updatedCard;
  }

  delete(id: number) {
    const cardIndex = this.cards.findIndex(
      (originalCard) => originalCard.id === id,
    );

    if (cardIndex !== -1) {
      delete this.cards[cardIndex];
      this._save();
    } else {
      console.warn(
        `No card found for id=<${id}>. Caching or UI refresh issue?`,
      );
    }
  }
```

## Routes

It felt very similar to [Vue Router I use in Vue](https://router.vuejs.org/), though since I followed [the 2024 Masterclass of VueSchool](https://vueschool.io/the-vuejs-3-master-class), I like the [Nuxt](https://nuxt.com/) approach with [Unplugin Vue Router](https://www.npmjs.com/package/unplugin-vue-router) that uses file-based routing.

### Adding a Route

The application creation process provides you with a `app.routes.ts` file that remains empty by default.

You add a route with the following:

```tsx
import { Routes } from "@angular/router";
import { CardListComponent } from "./pages/card-list/card-list.component";

export const routes: Routes = [
  {
    path: "home",
    component: CardListComponent,
  },
];
```

Then you add to `import: []` on the `app.component.ts` the `RouterOutlet` to add it to the `app.component.html`:

```html
<router-outlet></router-outlet>
```

If you need to redirect a path to another, let’s say `/` to `/home`, you can add another route like so:

```tsx
  {
    path: '',
    redirectTo: 'home',
    // first path match fully the redirect path
    pathMatch: 'full',
  },
```

### What about handling routes not found

```tsx
  {
    path: '**',
    component: NotFoundComponent,
  },
```

However, just like with Vue Router, the order matters so put this route to the bottom of the list… 😁

### Handling Parameters on a Route

Again, very similar to Vue Router:

```tsx
  {
    // route for an existing card
    path: 'card/:id',
    component: CardComponent,
  },
```

But what if you have similar routes? For example, the one above and this one below:

```tsx
  {
    // route for a new card
    path: 'card',
    component: CardComponent,
  },
```

Well, you can group them in the following manner:

```tsx
  {
    path: 'card',
    children: [
      // route for new card
      { path: '', component: CardComponent },
      // route for an existing card
      {
        path: ':id',
        component: CardComponent,
      },
    ],
  },
```

### How Do You Read Route Parameters

Given the `/card/:id` route defined previously, you need to load the current route by injecting the `ActivatedRoute` into the target `CardComponent` component:

```tsx
  private route = inject(ActivatedRoute);
```

With that `route` variable, you can parse from the `params` property the `id`:

```tsx
  cardId = signal<number | undefined>(undefined);

  ngOnInit(): void {
    const params = this.route.snapshot.params;
    this.cardId.set(params['id'] ? parseInt(params['id']) : undefined);
  }
```

You can then use the `cardId` signal in the HTML file.

### How Do You Navigate to a Route

Let’s take an example with a “Next” navigation button on the `/card/:id` route. We want to increment the `cardId` on each click.

The `next()` method that we’ll use in the HTML file would like this:

```tsx
  next() {
    let nextId = this.cardId() || 0;
    nextId++;
    this.router.navigate([`/card/${nextId}`]);
  }
```

But… you may notice an issue. When you click the first next, the route changes, but not the HTML. And if you click again, nothing changes.

Why?

Because we use a _snapshot_ of the `params` and it isn’t subscribed to. Also, Angular doesn’t execute the `ngOnInit` again. Therefore, `cardId` doesn’t get updated.

To solve this, I hinted at the solution: we need to subscribe (topic detailed in more depth below) to the route’s `params` change.

Though, I’ll provide the solution in the following code snippet:

```tsx
  routeSubscription: Subscription | null = null;

  ngOnInit(): void {
    this.routeSubscription = this.route.params.subscribe((params) => {
      this.cardId.set(params['id'] ? parseInt(params['id']) : undefined);
    });
  }
  // The ngOnDestroy is required to avoid memory leaks...
  ngOnDestroy(): void {
    this.routeSubscription = null;
  }
```

With that code, the HTML gets updated and you can click next infinitely.

## Reactive forms

We have several types of form handling in Angular:

- Template Driven Forms: With this method, we use the two-binding with `ngModel` in the HTML file.
- Reactive Forms: With this method, the behavior of the form is declared in the TS file.

Let’s look at the _Reactive Form_ method.

### The Basics

To start, we need to add the `ReactiveFormsModule` module to the TS file to start adding a new `FormControl` that represents the individual inputs:

```tsx
name = new FormControl("", [Validators.required]);
hp = new FormControl(0, [
  Validators.required,
  Validators.min(1),
  Validators.max(200),
]);
```

The default is required and you can add validators using `Validators` class provided by Angular Forms.

While we’re in the TS file, let’s add the `submit` method that receives the data submitted:

```tsx
  submit(event: Event) {
    event.preventDefault();
    console.log(`${this.name.value} ; ${this.hp.value}`);
  }
```

Now, in the HTML file, we can declare the new form:

```html
<form (submit)="submit($event)">
  <div class="form-field">
    <label for="name">Name</label>
    <input id="name" name="name" type="text" [formControl]="name" />
    @if (name.invalid && (name.dirty || name.touched)) {
    <p class="error">This field is required</p>
    }
  </div>
  <div class="form-field">
    <label for="hp">HP</label>
    <input id="hp" name="hp" type="number" [formControl]="hp" />
    @if (hp.invalid && (hp.dirty || hp.touched)) {
    <p class="error">This field is invalid</p>
    }
  </div>

  <button type="submit" [disabled]="name.invalid || hp.invalid">Save</button>
</form>
```

In the code above, from bottom to top:

- the submit button is disabled as long as the two fields aren’t valid.
- on each field, we bind the form control to the input
- the form element binds the submit method to the submit event.

You probably want to tell me that it isn’t practical to check each field on the submit button. That’s where `FormGroup` comes into the scene!

### `FormGroup` Usage

For the sake of making the article short, I’ll limit the example to two fields:

- In the TS file, you define the form group:

  ```tsx
  form = new FormGroup({
    name: new FormControl("", [Validators.required]),
    hp: new FormControl(0, [
      Validators.required,
      Validators.min(1),
      Validators.max(200),
    ]),
  });
  ```

- In the HTML file, you need to adapt a few things:

  ```html
  <!-- first, add `[formGroup]="form"` to the form element -->
  <form [formGroup]="form" (submit)="submit($event)">
    <div class="form-field">
      <label for="name">Name</label>
      <!-- next, change `[formControl]` to `formControlName` -->
      <input id="name" name="name" type="text" formControlName="name" />
      <!-- the method `isFieldValid` groups the logic of the previous to avoid repetition -->
      @if (isFieldValid("name")) {
      <p class="error">This field is required</p>
      }
    </div>
    <div class="form-field">
      <label for="hp">HP</label>
      <input id="hp" name="hp" type="number" formControlName="hp" />
      @if (isFieldValid("hp")) {
      <p class="error">This field is invalid</p>
      }
    </div>
    <!-- finally, we can use `form.invalid` to check form's validity -->
    <button type="submit" [disabled]="form.invalid">Save</button>
  </form>
  ```

### `FormBuilder` Usage

To simplify the TypeScript code, we could also use the `FormBuilder` service.

For that, let’s import it first:

```tsx
  private formBuilder = inject(FormBuilder);
```

Then, you can refractor the form group as follows:

```tsx
form = this.formBuilder.group({
  name: ["", [Validators.required]],
  hp: [0, [Validators.required, Validators.min(1), Validators.max(200)]],
});
```

### Build Select Input

If you need a drop-down input with a select element, you need to:

- declare the source of data
- add the `select` element with a `for loop` to add the options

  ```html
  <label for="type">Type</label>
  <select id="type" name="type" type="number" formControlName="type">
    @for (type of cardTypes; track type) {
    <option [value]="type.Id">{{ type.Name }}</option>
    }
  </select>
  ```

### Handling File Input

In the case of a file input, you’ll need to handle the file change with a custom method. The HTML listens to the `(change)` event:

```html
<label for="image">Image</label>
<input id="image" name="image" type="file" (change)="onFileChange($event)" />
```

And the `onFileChange` takes care of updating the target form field:

```tsx
  onFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const reader = new FileReader();
    if (target.files && target.files.length) {
      const [file] = target.files;
      reader.readAsDataURL(file);
      reader.onload = () => {
        // you can use `patchValue` to assign the value of the field.
        // you can use it on multiple fields
        this.form.patchValue({ image: reader.result as string });
      };
    }
  }
```

### Handle Multiple Validators

The simple way to achieve this could happen with the following:

```html
@if (isFieldValid('hp')) { @if (formGroup.get('hp')?.hasError('required')) {
<div class="error">A valid number is required.</div>
} @if (formGroup.get('hp')?.hasError('min')) {
<div class="error">This field needs to be bigger than 0.</div>
} @if (formGroup.get('hp')?.hasError('max')) {
<div class="error">This field needs to be smaller or equal to 200.</div>
} }
```

## Angular Material

Angular Material is Google’s official UI component library for Angular that implements Material Design principles.

You can install it with the following command:

```bash
ng add @angular/material
```

And you’ll need to answer some questions:

```bash
✔ Choose a prebuilt theme name, or "custom" for a custom theme (list of 4 presets)
✔ Set up global Angular Material typography styles?
```

Then, head to [Angular Material website](https://material.angular.io/components/categories) to make your pick.

In the example so far, we can update the `text` inputs, the `number` inputs and the `select` input.

To do so, we need:

- to import the modules necessary:

  ```tsx
    imports: [
      /* The existing modules or components */
      /* ... */
      /* And add the following for Material compenents */
      MatButtonModule,
      MatInputModule,
      MatSelectModule,
    ],

  ```

- to implement the modules into the HTML:

  ```html
  <!-- for the text and number inputs -->
  <mat-form-field>
    <!-- replaces the `<div class="form-field">` -->
    <mat-label for="name">Name</mat-label
    ><!-- replaces the `<label>` -->
    <!-- add the `matInput` attribute -->
    <input matInput id="name" name="name" type="text" formControlName="name" />
    @if (isFieldValid("name")) {
    <!-- replaces the `<p class="error">` -->
    <mat-error>This field is required</mat-error>
    }
  </mat-form-field>
  <mat-form-field>
    <mat-label for="type">Type</mat-label>
    <!-- replaces the `<select>` -->
    <mat-select id="type" name="type" type="number" formControlName="type">
      @for (type of cardTypes; track type) {
      <!-- replaces the `<option>` -->
      <mat-option [value]="type">{{ type }}</mat-option>
      }
    </mat-select>
    @if (isFieldValid("type")) {
    <mat-error>This field is invalid</mat-error>
    }
  </mat-form-field>
  ```

Now, Angular Material doesn’t provide any components for file input. Sergio takes the smart option to show a button to simulate the click on “Choose file” while hiding the input of type `file`.

```html
<!-- You add the button -->
<button mat-raised-button type="button" (click)="imageInput.click()">
  {{ getUploadImageButtonLabel(imageInput) }}
</button>
<!-- You add the `#imageInput` to allow the button to act on the input file -->
<input
  #imageInput
  id="image"
  name="image"
  type="file"
  hidden
  (change)="onFileChange($event)"
/>
```

Then, we implement the method update the button:

```tsx
  getUploadImageButtonLabel(imageInput: HTMLInputElement) {
    const fileUploaded = imageInput.files?.[0]?.name;
    if (fileUploaded) {
      return `Uploaded file: ${imageInput.files?.[0]?.name}`;
    } else {
      return 'Upload file: ...';
    }
  }
```

## Authentication management

### Introduction

We need to start by adding a provider, since the authentication will require using a REST API through an HTTP client.

To perform this, let’s add that provider to `app.config.ts`:

```tsx
import { provideHttpClient } from "@angular/common/http";
export const appConfig: ApplicationConfig = {
  providers: [
    /* After the other providers */
    provideHttpClient(),
  ],
};
```

### Create the `AuthService`

Next step, you create a new `AuthService` and you import the `HttpClient` and use it in your new service:

```tsx
export class AuthService {
  private http = inject(HttpClient);
  // While, you are at it, add the base URL of the Authentication API
  // Here I'm using Sergio Python API available here: https://gitlab.com/simpletechprod1/playing_cards_backend
  // PS: I recommend using GitBash to run the command of its README to run the API locally.
  private AUTH_BASE_URL = "http://localhost:8000";
}
```

Next, we add the `user` property to the service that will be a signal of type `User | null | undefined`.

```tsx
user = signal<User | null | undefined>(undefined);
```

In authentication, we usually need:

- a method `login` that receives the credentials.
- a method `logout` that terminates the session.
- a method `getUser` that retrieves the user’s information.

Let’s code their signature:

```tsx
  login(credentials: ICredentials): Observable<User | null | undefined> {
    // The return type "Observable" allows to get notified
    // when the login happens successfully... or not
  }

  getUser(): Observable<User | null | undefined> {
    // The return type "Observable" allows to get notified
    // when the API return the data... or not
  }

  logout() {

  }
```

We need to add the interface `ICredentials`:

```tsx
// Add it to the top of the AuthService
export interface ICredentials {
  username: string;
  password: string;
}
// See below ofr its usage in the method login
export interface ILoginResult {
  token: string;
  user: User;
}
```

And the model `User` :

```tsx
// Add the file `user.model.ts` to `/app/models`
export class User {
  username = "";
  firstName = "";
  lastName = "";
}
```

We continue with the call to the login method of the API. Sergio’s API uses a login method that returns a token that we need to store in local storage so we can use it later.

```tsx
return (
  this.http
    // Execute a POST request with
    // - the endpoint as first parameter
    // - the payload as second parameter
    .post<ILoginResult>(`${this.BASE_URL}/sessions/login/`, credentials)
    // `.pipe` allows to chain operations following an Observable result
    .pipe(
      // `tap` allows to take the Observable result and execute some specific code,
      // without changing the Observable result itself
      // ILoginResult is an interface containing `token` and `user` to make TypeScript
      // happy.
      tap((result: ILoginResult) => {
        console.log("authService > login > tap > result", result);
        // We store the token to local storage
        localStorage.setItem(
          LocalStorageDatabaseNameKeys.SESSION_TOKEN_DB,
          result.token,
        );
        // and set the user in the user signal
        const user = Object.assign(new User(), result.user);
        this.user.set(user);
      }),
      // `map` allows to take a Obvervable value and transform it into something else.
      // Below, we simply returns the user.
      map(() => this.user()),
    )
);
```

Why are there three types of `login` and `getUser` methods?

- `undefined` identifies the use case “We don’t know yet if user is logged in”.
- `null` identifies the use case “We know the user isn’t logged in”.
- `User` identifies the use case “User is logged in”.

Now, here is the implementation of the `getUser` and `logout` methods:

```tsx
  // Very similar to login, but we simply get the user
  getUser(): Observable<User | null | undefined> {
    return this.http.get<User>(`${this.BASE_URL}/sessions/me/`).pipe(
      tap((result: User) => {
        const user = Object.assign(new User(), result);
        this.user.set(user);
      }),
      map(() => {
        return this.user();
      }),
    );
  }

  logout() {
    // No `map` because we have no data to return
    return this.http.get(`${this.BASE_URL}/sessions/logout/`).pipe(
      tap(() => {
        localStorage.removeItem(LocalStorageDatabaseNameKeys.SESSION_TOKEN_DB);
        this.user.set(null);
      }),
    );
  }
```

PS: The `tap` method is a RxJS operator that performs side effects (like logging or debugging) without modifying the emitted values in an observable stream.

### Use the `AuthService` on the Login Component

First, we need to inject the dependencies:

- the new `AuthService` to use the `login` method
- the router to handle the navigation if the login action is successful.

```tsx
  private authService = inject(AuthService);
  private router = inject(Router);
```

Then, let’s implement the `login` method:

```tsx
  // the form group with the credentials
  loginFormGroup = this.formBuilder.group({
    username: ['', [Validators.required]],
    password: ['', [Validators.required]],
  });

  // the variable to store the Subscription on the login method
  loginSubscription: Subscription | null = null;

  // the variable to store the failed login
  invalidCredentials = false;

  ngOnDestroy(): void {
    this.loginSubscription?.unsubscribe();
  }

  login() {
    this.loginSubscription = this.authService
      .login(this.loginFormGroup.value as ICredentials)
      .subscribe({
        next: (result: User | null | undefined) => {
          console.log(`next`, result);
          this.navigateHome();
        },
        error: () => {
          this.invalidCredentials = true;
        },
      });
  }

  navigateHome() {
    this.router.navigate(['home']);
  }
```

If you wonder about the `logout`, it’s very simple:

```tsx
  // You would put in the app.component.ts if you'd add a menu in this HTML
  // of the same component.
  private logoutSubscription: Subscription | null = null;

  ngOnDestroy(): void {
    this.logoutSubscription?.unsubscribe();
  }

  logout() {
    this.logoutSubscription = this.authService.logout().subscribe({
      next: () => this.navigateToLogin(),
      error: (err) => {
        console.error(err);
      },
    });
  }
```

However, you might have noticed the `logout` endpoint doesn’t take any parameters. So how do you tell the REST API who’s logging out?

### Interceptors

Interceptors allow to modify a HTTP request to add, for example, an HTTP header.

This is what we need to do if we want to call the REST API because it expects the token received on login.

To create a new interceptor, run the Angular command below:

```bash
ng generate interceptor interceptors/auth-token
```

In the authentication system that Sergio provides, the backend requires an HTTP header `Authorization: Token {token value}`.

The interceptor acts as a proxy to add some data to HTTP requests, in our case an HTTP header:

```tsx
import { HttpInterceptorFn } from "@angular/common/http";
import { LocalStorageDatabaseNameKeys } from "../constants/local.storage.database.name.keys";

export const authTokenInterceptor: HttpInterceptorFn = (req, next) => {
  // Custom starts here...
  // Let's retrieve the token
  const token = localStorage.getItem(
    LocalStorageDatabaseNameKeys.SESSION_TOKEN_DB,
  );

  // If the token is found...
  let requestToSend = req;
  if (token) {
    // Let's modify the request's headers to add the one we need
    const headers = req.headers.set("Authorization", `Token ${token}`);
    // And clone the request with the updated headers
    requestToSend = req.clone({ headers });
  }

  // and run the `next` with the modified request
  return next(requestToSend);
};
```

Now, any request to the REST API receives the token in the header and the logout endpoint can retrieve it to log out the session associated.

One last step remains to complete all this work: tell the HTTP client how to use the interceptor we created.

We do so by updating the `provideHttpClient` to use it:

```tsx
    provideHttpClient(withInterceptors([authTokenInterceptor])),
```

We’re almost done! The last thing to code is to prevent users from seeing the pages requiring “authenticated” status.

### Guards

Guards will help us with the last part.

Guards run on a selected use case. Those use cases are listed when creating one:

```bash
ng generate guard guards/is-logged-in

? Which type of guard would you like to create?
❯◉ CanActivate
 ◯ CanActivateChild
 ◯ CanDeactivate
 ◯ CanMatch
```

In our use case, when a route _activates_, we need to run some code to check if the current user can browse the page.

```tsx
export const isLoggedInGuard: CanActivateFn = () => {
  // Similar to components, we inject our needed dependencies
  const authService = inject(AuthService);
  const router = inject(Router);
  // Then, we check the user's values...
  // If the user is undefined, let's get the user
  if (authService.user() === undefined) {
    return (
      authService
        .getUser()
        // Since `getUser` return an Observable, we need to
        // use pipe and map to return the `true` is the user
        // exists.
        .pipe(
          map(() => true),
          // otherwise, we navigate the user to the login route
          catchError(() => router.navigate(["login"])),
        )
    );
  }

  // the user is null, so we navigate the user to the login route
  if (authService.user() === null) {
    router.navigate(["login"]);
  }

  // the user is known, so he can navigate to the requested route.
  return true;
};
```

To use the guard, we need to update the routes:

```tsx
import { isLoggedInGuard } from "./guards/is-logged-in.guard";

export const routes: Routes = [
  /* One example */
  {
    path: "home",
    component: CardListComponent,
    canActivate: [isLoggedInGuard],
  },
];
```

## REST API integration

Now that we have implemented the authentication API, implementing a data API won’t be hard.

I’ll just share a best practice about the communication between the Angular application and the API you consume.

### Update the Existing Service With API Calls

In our example application, the API returns cards so first, we’ll need to create a `interfaces/card.interface.ts` to define the contract between the Frontend and the Backend:

```tsx
import { CardType } from "../utils/card.utils";

export interface ICard {
  id?: number;
  name: string;
  image: string;
  type: CardType;
  hp: number;
  figureCaption: string;
  attackName: string;
  attackStrength: number;
  attackDescription: string;
}
```

Then, we modify the `card.model.ts` file so that:

- it implements the interface.

  ```tsx
  export class Card implements ICard {}
  ```

- it defines a static method to convert a card in JSON format to a `Card` instance.

  ```tsx
    static fromJson(cardJson: ICard): Card {
      return Object.assign(new Card(), cardJson);
    }
  ```

- it defines a method to convert a `Card` instance to a card in JSON format.

  ```tsx
    toJson(): ICard {
      const cardJson: ICard = Object.assign({}, this);
      // The `id` must be removed since it is either necessary (Create)
      // or it is present in the endpoint URI (Update).
      delete cardJson.id;
      return cardJson;
    }
  ```

Then, we can update the `CardService` to query the REST API:

```tsx
  private http = inject(HttpClient);
  getAll() {
    console.log('Call GET /cards/');

    return this.http
      .get<ICard[]>(`${AppConstants.API_BASE_URL}/cards/`)
      .pipe(
        map((cardJsonArray) => {
          return cardJsonArray.map<Card>((itemJson) =>
            Card.fromJson(itemJson),
          );
        }),
      );
  }

  get(id: number | undefined) {
    console.log('Call GET /cards/:id/', id);
    return this.http
      .get<ICard>(`${AppConstants.API_BASE_URL}/cards/${id}/`)
      .pipe(map((cardJson) => Card.fromJson(cardJson)));
  }

  add(card: Card) {
    return this.http
      .post<ICard>(
        `${AppConstants.API_BASE_URL}/cards/`,
        card.toJson(),
      )
      .pipe(map((cardJson) => Card.fromJson(cardJson)));
  }

  update(card: Card) {
    console.log('Call PUT /cards/:id/');
    return this.http
      .put<ICard>(
        `${AppConstants.API_BASE_URL}/cards/${card.id}/`,
        card.toJson(),
      )
      .pipe(map((cardJson) => Card.fromJson(cardJson)));
  }

  delete(id: number | undefined): Observable<void> {
    return this.http.delete<void>(
      `${AppConstants.API_BASE_URL}/cards/${id}/`,
    );
  }
```

### Update the List Components

In the card-list components, we have this:

```tsx
  cards = signal<Card[]>([]);

  constructor() {
    this.cards.set(this.cardService.getAll());
  }
```

But ESLint tells us:

```plaintext
Argument of type 'Observable<Card[]>' is not assignable to parameter of type 'Card[]'.
```

We could use a `subscribe` on the `getAll` result to convert the `Observable<Card[]>` into `Card[]`, but Angular actually provides a simpler method called `toSignal`:

```tsx
import { toSignal } from "@angular/core/rxjs-interop";
export class CardListComponent {
  cardService = inject(CardService);
  cards = toSignal(this.cardService.getAll());
  /* ... rest of the code */
}
```

And, consequently, you can remove the constructor code.

### Update the Single Card Component

In this case, the code adaptation requires a different approach, but again, to avoid nested `subscribe`, Sergio showcases the use of `switchMap` in a `pipe`:

```tsx
this.routeSubscription = this.route.params
  .pipe(
    // `switchMap` allows to take an Observable and create another
    // that we can use it on the next step.
    switchMap((params) => {
      if (params["id"]) {
        this.cardId.set(params["id"] ? parseInt(params["id"]) : undefined);
        return this.cardService.get(this.cardId());
      }
      // `of` creates an Observable with the value provided,
      // e.g. null in the code below
      return of(null);
    }),
  )
  // receives either the result of `cardService.get` or null
  .subscribe((cardFound) => {
    if (cardFound) {
      this.card = cardFound;
      this.form.patchValue(this.card);
    }
  });
```

This way, we only need to unsubscribe one subscription.

On the `submit` method, we need to adapt the code:

```tsx
  saveSubscription: Subscription | null = null;

  ngOnDestroy(): void {
    /* ... previous code... */
    this.saveSubscription?.unsubscribe();
  }

  submit(event: Event) {
    event.preventDefault();
    console.log(this.card);
    // to avoid having two subscriptions, let's create a local variable...
    let saveObservable = null;
    if (this.cardId() === -1 || !this.cardId()) {
      saveObservable = this.cardService.add(this.card);
    } else {
      this.card.id = this.cardId() as number;
      saveObservable = this.cardService.update(this.card);
    }
    // ... and subscribe to it :
    this.saveSubscription = saveObservable.subscribe(() =>
      // this time, on successful subscribe, we navigate to the next page.
      this.router.navigate(['/home']),
    );
  }

```

On the `deleteCard`, we also need to adapt the code:

```tsx
  deleteSubscription: Subscription | null = null;

  ngOnDestroy(): void {
    /* ... previous code... */
    this.deleteSubscription?.unsubscribe();
  }

  deleteCard() {
    const dialogRef = this.dialog.open(
      CardDeleteConfirmationDialogComponent,
    );
    this.deleteSubscription = dialogRef
      .afterClosed()
      .pipe(
        filter((confirmation) => confirmation),
        switchMap(() => this.cardService.delete(this.cardId())),
      )
      .subscribe(() => this.navigateBack());
  }
```

## Conclusion

I personally prefer Vue’s syntax. But compared to React, it feels more structured to use Angular.

Regarding [the course on YouTube](https://www.youtube.com/watch?v=U71TQN68QGU), I think Sergio did a great job and I think I learned all I needed to really understand the basics about Angular.

Also, having a background experience with Vue 3, I understood the signal concepts faster, as I could link the equivalent syntax and API with Vue.

I need to practice now, especially in regards to the `pipe`, `subscribe`, `tap`, `map` and so on. He teaches RxJs part in another video I’ll review soon.

### Deeper Dive Into RxJs and co

At the end of the course, Sergio shares a tip about the best practices when you handle several subscriptions in a single component.

In fact, instead of using one subscription per use case, we can declare only one variable of type `Subscription` for all:

```tsx
subscriptions: Subscription = new Subscription();
```

Then, in each use case, we perform the following:

```tsx
  ngOnInit(): void {
    const routeSubscription = this.route.params
      .pipe( /* Omitted the details */ )
      .subscribe( /* Omitted the details */ );
    this.subscriptions.add(routeSubscription);
    const formSubscription = this.form.valueChanges.subscribe(/* Omitted the details */);
    this.subscriptions.add(formSubscription);
  }
  submit(event: Event) {
    /* ... preceeding business logic ... */
    this.subscriptions.add(
      saveObservable.subscribe(() => this.router.navigate(['/home'])),
    );
  }
  deleteCard() {
    /* ... preceeding business logic ... */
    const deleteSubscription = dialogRef
      .afterClosed()
      .pipe(/*Omitted the details */)
      .subscribe(() => this.navigateBack());

    this.subscriptions.add(deleteSubscription)
  }
```

And we update the `ngOnDestroy` body to this:

```tsx
this.subscriptions.unsubscribe();
```

For more on the topic, I recommend Sergio’s vlogs on the topic.

- [Intro à RxJS - Observables, Observers, Subscriptions](https://www.youtube.com/watch?v=fQeZSSK2SOM)
- [RxJS / Angular : Opérateurs et exemples concrets](https://www.youtube.com/watch?v=hh3Xdukr42g)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [RealToughCandy.com](https://www.pexels.com/photo/hand-holding-shield-shaped-red-sticker-11035543/).
