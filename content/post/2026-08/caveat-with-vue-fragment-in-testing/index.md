---
title: "Caveat With Vue Fragment In Testing"
description: "A real bug in how the test used Vue Test Utils to read text out of a multi-root Fragment component."
image: 2026-08-05-caveat-with-vue-fragment-in-testing.jpg
imageAlt: A single puzzle piece separated from the rest of the picture
date: 2026-08-05
categories:
  - Web Development
tags:
  - Vue.js
  - Vue Test Utils
  - Testing
  - JavaScript
---

Out of 484 tests, exactly one failed. I was implementing a small, self-contained Vue component, and the failure looked simple: a sentence that should have had spaces around a link didn’t.

I debugged the issue with a `console.log` and then I found a lead. Let’s review the root cause of all that.

## The Component and the Missing Spaces

The component in question, `OrgRestrictionNotice.vue`, renders one fixed sentence with a link in the middle of it:

```vue
<template>
  Le dépôt choisi se trouve sous une organisation n'autorisant pas
  l'authentification avec votre compte et le dépôt choisi. Veuillez visiter ce
  <AppLink :to="settingsUrl">lien</AppLink>
  pour autoriser l'accès.
</template>
```

The test asserted the rendered text matched that sentence exactly:

```ts
// FIXED_SENTENCE is the text-only sentence of the above template.
expect(wrapper.text().replace(/\s+/g, " ").trim()).toBe(FIXED_SENTENCE);
```

It failed with this diff:

```plaintext
Expected: "...Veuillez visiter ce lien pour autoriser l'accès."
Received: "...Veuillez visiter celienpour autoriser l'accès."
```

No spaces at all around the link. Why?

## The Culprit

If the compiled output looked fine, the bug had to be downstream of it—in how the test read the text back out. So I went looking in [Vue Test Utils’ own source](https://github.com/vuejs/test-utils/blob/main/src/utils.ts) for what `wrapper.text()` actually does. Its `textContent` helper is:

```ts
export function textContent(element: Node): string {
  return element.nodeType !== Node.COMMENT_NODE
    ? (element.textContent?.trim() ?? "")
    : "";
}
```

And [the `text()` method on the wrapper itself](https://github.com/vuejs/test-utils/blob/main/src/baseWrapper.ts) is just:

```ts
text() {
  return this.getRootNodes().map(textContent).join('')
}
```

There it was. `getRootNodes()` returns every root-level node of the mounted component. `.map(textContent)` trims each one _individually_. `.join('')` glues the results back together with no separator at all.

`OrgRestrictionNotice.vue` has no wrapping element, so under [Vue 3’s official support for fragments](https://v3-migration.vuejs.org/new/fragments), its template compiles to three sibling root nodes: a text node, the `<AppLink>` (rendered as `<a>`), and another text node. `wrapper.text()` trims each of those three separately—stripping the trailing space off the first text node and the leading space off the third—then concatenates them with nothing in between. It didn’t matter what the template contained; any component with a bare text node touching its own root boundary would lose that space under `wrapper.text()`.

## The Actual Fix

Once I understood the mechanism, the fix was straightforward: stop asserting `wrapper.text()` on the component in isolation, and mount it the way it’s actually used—inside a single-root host:

```ts
const SingleRootHost = defineComponent({
  components: { OrgRestrictionNotice },
  props: { owner: { type: String, required: true } },
  template: '<p role="alert"><OrgRestrictionNotice :owner="owner" /></p>',
});

function mountNotice(owner: string) {
  return mount(SingleRootHost, {
    props: { owner },
    global: { plugins: [router], components: { AppLink } },
  });
}
```

With one root node, `getRootNodes()` returns exactly one element, `textContent` trims only its outer edges, and the interior spacing survives the round-trip intact. All 484 tests passed. The component itself never needed to change.

## Conclusion

I spent some time to diagnosis the issue and, to be honest, Claude didn’t help. It cycled to try to "fix" a component that worked fine because the symptom looked exactly like a template whitespace bug. Maybe a Context 7 MCP with the Vue and Vue Testing documentation would have helped.

I learned an important lesson on that occasion and I’m sure that if you reached that sentence, right now, you did as well.

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Ann H on Pexels (`https://www.pexels.com/photo/pink-jigsaw-puzzle-piece-3482441/`).
