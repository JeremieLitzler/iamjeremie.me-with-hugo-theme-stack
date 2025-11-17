---
title: "Command Design Pattern vs Bus Message"
description: "As I was reviewing some OOP concepts, I read about the command pattern and it made me think about bus message. However, they are not the same."
image: 2025-11-17-a-waiter-taking-an-order-from-two-men.jpg
imageAlt: A waiter taking an order from two men
date: 2025-11-17
categories:
  - Software Development
tags:
  - Design Patterns
---

When developers talk about software architecture, two concepts often come up: the Command Pattern and message bus systems.

While they share some similarities, they’re designed to solve different problems. Think of it this way: both a bicycle and a car get you from point A to point B, but you wouldn’t use them in the same situations.

## The Command Pattern: Your Personal Remote Control

Imagine you have a universal remote control for your home. When you press the “movie night” button, it doesn’t just turn on your TV—it dims the lights, closes the blinds, adjusts the thermostat, and starts your streaming device. The remote doesn’t need to know _how_ each device works internally; it just knows which buttons to press.

That’s essentially what the Command Pattern does in software. It wraps up a request—like “turn on the TV”—into a neat package (an object) that contains everything needed to execute that request later. This package is portable, reusable, and can be passed around your code like a note with instructions written on it.

### The Key Players in This Pattern

First, we have the **command itself**. It represents the instruction note that says what needs to be done.

Then, we find the **invoker**, e.g., the person (or code) holding the remote, deciding when to press buttons.

Next, we have the **receiver**. It’s the device (or object) that executes the work.

Then, **concrete commands** can represent other specific buttons on your remote, each wired to perform a specific action.

What makes the Command Pattern special is that it can do more than just execute actions. Because each command is an object, you can store them in a list (creating an undo history), schedule them for later (like a DVR recording), or even replay them in sequence. It’s like having a macro recorder for your software.

## Message Bus Systems: The Office Memo Board

Now, let’s shift gears and think about a different scenario. Picture a busy office with different departments: Sales, Marketing, Accounting, and IT. Instead of people running around constantly interrupting each other, the company uses a central bulletin board system. When Sales closes a big deal, they post a memo on the board: “New customer acquired!” The Accounting Department checks the board regularly and sees the memo, so they create an invoice. Marketing sees it too and sends a welcome package. Finally, IT provisions a new account. Nobody had to knock on anyone’s door.

This is how a message bus system works. It’s a communication highway where different parts of your software can talk to each other without knowing who’s listening or even if anyone’s listening at all.

### The Main Components

First, we find the **message producers**, in the above example, each department posting memos (components that send messages).

Then, we have the **message bus** that we described as the bulletin board itself (the infrastructure that routes messages).

Finally, the **message consumers** represent the components that subscribe to messages. In the above example, the departments reading the memos correspond to those consumers.

Message buses excel at coordinating multiple systems that need to stay loosely connected. When a new department joins the company, it just starts reading relevant memos **to itself** from the board—no need to rewire everyone’s phones. Similarly, if a department leaves, the others keep operating normally.

## Where They Meet and Where They Diverge

Both patterns recognize a fundamental truth in software design: tight coupling is the enemy of flexibility.

When one piece of code knows too much about another, changing one can very often break the other.

Both the Command Pattern and message buses cut that wire, but in different ways:

**The Command Pattern** is like a waiter taking your order. The waiter (invoker) doesn’t cook your food; they write down your request (command object) and deliver it to the kitchen (receiver). You can change your order before it’s cooked, the restaurant can queue orders during busy times, and if there’s a mistake, they can reference your original order slip. The focus is on _encapsulating individual actions_ so they can be manipulated, delayed, or reversed.

**A Message Bus** is like a radio broadcast system. The DJ (producer) doesn’t know who’s listening or how many people tuned in. Listeners (consumers) can tune in or out whenever they want. Multiple stations can broadcast simultaneously, and you can tune in to several stations. The focus is on _facilitating communication_ between many independent components, often at the same time, without them needing to know about each other.

## The Key Differences That Matter

While the Command Pattern helps you organize and control _what your code does_, a message bus helps you organize _how your code communicates_.

Commands typically run synchronous—like handing a task list to your assistant and waiting for them to complete it. Message buses usually execute asynchronous—like sending emails and checking your inbox later to see who responded.

The Command Pattern shines when you need control over execution: undo/redo functionality in a text editor, transaction systems in databases, or job schedulers that need to retry failed operations. Each command is a first-class citizen that can be inspected, modified, or canceled.

Message buses excel in distributed systems where multiple components need to react to events: e-commerce platforms where an order triggers inventory updates, shipping notifications, and accounting entries, all happening independently. The bus ensures messages get delivered, but doesn’t care about the order of processing or who responds.

## When to Use Each

Choose the Command Pattern when you’re building features that require:

- Undo and redo capabilities
- Queuing work for later execution
- Recording operations for audit logs
- Transactional behavior with rollback support

Reach for a message bus when you’re dealing with:

- Multiple systems that need to respond to the same event
- Asynchronous workflows where immediate responses aren’t necessary
- Scalability requirements where components might live on different servers
- Evolving architectures where new features need to plug in without breaking existing code

## The Bottom Line

Think of the Command Pattern as a sophisticated to-do list system for your application—each item is carefully packaged with all the information needed to complete it, and you can shuffle, delay, or undo items as needed. A message bus, on the other hand, is more like a town crier in a medieval village, announcing news to anyone who cares to listen, without worrying about who shows up or what they do with the information.

They’re not competitors; they’re tools for different jobs. In fact, many sophisticated systems use both. You might use a message bus to distribute work across multiple servers, and use the Command Pattern within each server to manage how that work gets executed. Like a well-equipped toolbox, the best software architects know when to reach for each tool.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [RDNE Stock project](https://www.pexels.com/photo/waiter-getting-the-customer-s-orders-4921154/).
