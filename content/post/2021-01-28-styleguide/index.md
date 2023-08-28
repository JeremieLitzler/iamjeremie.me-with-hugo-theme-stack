---
title: Style guide of the site (H1)
description: A set of examples of the various elements in a post and how they will look
date: 2021-01-28
image: '/images/2021-01-28-styleguide.jpg'
imageAlt: A Macintosh computer on a desk
categories:
  - Web Fundamentals

tags:
  - Markdown
  - VuePress
  - Jamstack
---

_Note:_ H1 is included in the frontmatter, property `title`. Check out [the VuePress docs](https://v2.vuepress.vuejs.org/reference/default-theme/frontmatter.html).

## Titre H2

### Titre H3

#### Titre H4

##### Titre H5

A paragraph: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dignissim dui et orci vehicula pellentesque. Mauris ac porta nulla. Vivamus scelerisque imperdiet metus, non egestas ipsum scelerisque a. Maecenas quis blandit dui, viverra scelerisque libero. Duis ac neque nisl. Nulla interdum leo quam, eu blandit leo cursus in. Fusce aliquet lobortis dui, ut varius ligula mollis ut. In a lorem at enim viverra consectetur luctus a diam. Praesent at justo eu ex fringilla tempus nec vel velit. Integer nec suscipit lectus. Nullam sem neque, ullamcorper sit amet viverra in, gravida id ante. Duis cursus aliquet massa.

Quisque pharetra consectetur nulla, vel iaculis eros ultricies vitae. Nullam non eros id lorem volutpat laoreet non in arcu. Duis facilisis pretium libero eu tincidunt. Duis mauris tellus, commodo condimentum nibh scelerisque, tincidunt condimentum felis. Donec blandit, enim vitae vulputate auctor, quam dui molestie tortor, non pretium est orci vel lorem. Duis porta tortor faucibus ipsum efficitur molestie a nec felis. Mauris ullamcorper sed magna ut aliquet. Ut in nibh scelerisque, malesuada erat non, dapibus nibh. Duis aliquam porttitor consequat. Morbi elementum libero sed maximus accumsan.

## A link

[A markdown link](https://iamjeremie.me/).

## An image

![An image](/images/default.jpg)

## A bullet list

- Item 1
- Item 2
  - Item 2.1
  - Item 2.2
- Item 3

## A short quote

> A short quote of a few words

## A long quote

> Quoting text multilines.
>
> And more of the same quote that is long and allows to test how the text wraps in the width of the container.

## A quote of a quote (double level)

> first level of quote
>
> > A double level quote that is long and allows to test how the text wraps in the width of the container.
>
> And first level again

## Code highlighting

```js
import React from 'react';
import uniquePropHOC from './lib/unique-prop-hoc';

// this comment is here to demonstrate an extremely long line length, well beyond what you should probably allow in your own code, though sometimes you'll be highlighting code you can't refactor, which is unfortunate but should be handled gracefully

class Expire extends React.Component {
  constructor(props) {
    super(props);
    this.state = { component: props.children };
  }
  componentDidMount() {
    setTimeout(() => {
      this.setState({
        component: null,
      });
    }, this.props.time || this.props.seconds * 1000);
  }
  render() {
    return this.state.component;
  }
}

export default uniquePropHOC(['time', 'seconds'])(Expire);
```

## Special styles

> A block quote with ~~strikethrough~~ and a URL: [See here](https://reactjs.org).

## Tables

| Col 1 | Col 2           | Col 3                                                |
| ----- | --------------- | ---------------------------------------------------- |
| Value | Very long value | So long that it will scroll horizontally? I hope so! |

Check out [the source on GitHub](https://github.com/JeremieLitzler/journal/blob/main/docs/posts/2021-01-28-styleguide/index.md).

Hero photo by [Jan Losert](https://unsplash.com/@janlosert?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash.
