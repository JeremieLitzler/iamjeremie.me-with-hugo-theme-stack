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

They share some surface-level similarities, but they solve different problems. Both a bicycle and a car get you from point A to point B, but you wouldn't use them in the same situations.

## The Command Pattern: Your Personal Remote Control

Imagine you have a universal remote control for your home. When you press the "movie night" button, it doesn't just turn on your TV—it dims the lights, closes the blinds, adjusts the thermostat, and starts your streaming device. The remote doesn't need to know _how_ each device works internally; it just knows what sub-processes to run.

The Command Pattern works the same way. It wraps up a request—like "turn on the TV"—into a neat package (an object) that contains everything needed to execute that request later. This package is portable, reusable, and can be passed around your code like a note with instructions written on it.

### The Key Players in This Pattern

The **client** creates the command and configures it with a receiver—think of the person programming the remote, deciding which button maps to which device.

The **command** is the instruction note itself, declaring what needs to be done.

The **invoker** holds the remote and decides when to press buttons. It triggers commands without knowing what they do internally.

The **receiver** is the device (or object) that carries out the actual work.

**Concrete commands** are the specific buttons on your remote, each wired to perform a particular action on a particular receiver.

What makes the Command Pattern special is that it can do more than just execute actions. Because each command is an object, you can store them in a list (creating an undo history), schedule them for later (like a DVR recording), or replay them in sequence. It's like having a macro recorder for your software.

## Message Bus Systems: The Office Memo Board

Let's take the example of a busy office with different departments: Sales, Marketing, Accounting, and IT. Instead of people running around constantly interrupting each other, the company uses a central bulletin board system. When Sales closes a big deal, they post a memo on the board: "New customer acquired!" The Accounting Department checks the board regularly and sees the memo, so they create an invoice. Marketing sees it too and sends a welcome package. IT provisions a new account. Nobody had to knock on anyone's door.

A message bus system works on the same principle. It's a communication highway where different parts of your software can talk to each other without knowing who's listening or even if anyone's listening at all.

### The Main Components

**Message producers** are the departments posting memos—components that publish messages to the bus.

The **message bus** is the bulletin board itself—the infrastructure that routes messages to interested parties.

**Message consumers** subscribe to specific types of messages on the bus. Unlike the bulletin board analogy (where anyone can scan every memo), consumers in most real implementations register their interest upfront, and the bus pushes matching messages to them. A consumer handling invoices subscribes to "order placed" events and ignores everything else.

Message buses excel at coordinating multiple systems that need to stay loosely connected. When a new component joins the system, it subscribes to relevant message types—no need to rewire existing connections. If a component is removed, the others keep operating normally (though in practice, you'd want to account for the missing functionality).

## Where They Meet and Where They Diverge

Both patterns address a fundamental truth in software design: tight coupling is the enemy of flexibility. When one piece of code knows too much about another, changing one can break the other. Both the Command Pattern and message buses reduce that coupling, but in different ways.

**The Command Pattern** is like a waiter delivering your order. You (the client) decide what you want and make a mental note (command). The waiter (invoker) takes your order on his notepad or tablet and delivers it to the kitchen (receiver) as he goes back to the chef. The focus is on _encapsulating individual actions_ so they can be manipulated, delayed, or reversed.

**A Message Bus** is like a radio broadcast system. The DJ (producer) doesn't know who's listening or how many people tuned in. Listeners (consumers) can tune in or out whenever they want. Multiple stations can broadcast simultaneously, and you can receive from several at once. The focus is on _facilitating communication_ between many independent components without them needing to know about each other.

## The Key Differences That Matter

While the Command Pattern helps you organize and control _what your code does_, a message bus helps you organize _how your code communicates_.

The Command Pattern is agnostic about execution model—commands can run synchronously or asynchronously. In simple implementations, the invoker calls `execute()` directly and waits for the result. But queued commands, scheduled commands, and batch-processed commands are all asynchronous by nature. Message buses, by contrast, are asynchronous by design—producers fire messages and move on without waiting for consumers to process them.

The Command Pattern shines when you need control over execution: undo/redo functionality in a text editor, transaction systems in databases, or job schedulers that need to retry failed operations. Each command is a first-class citizen that can be inspected, modified, or canceled.

Message buses fit well in distributed systems where multiple components need to react to events: e-commerce platforms where an order triggers inventory updates, shipping notifications, and accounting entries, all happening independently. Depending on the implementation, a bus may offer delivery guarantees (persistent queues, acknowledgments, retries) or it may be fire-and-forget. The bus decouples producers from consumers, but doesn't dictate processing order or guarantee who responds.

## When to Use Each

The deciding question is: **do you need control over individual operations, or do you need to decouple the sender from the receivers?**

Choose the Command Pattern when the _operation itself_ is the thing you need to
manage. You want to inspect it, reverse it, replay it, or decide at runtime whether
to execute it at all.

Reach for a message bus when you care about _what happened_ but not about
_who reacts or how_. The producer shouldn't need to change when a new consumer
shows up. Typical cases: an order event that independently triggers inventory,
shipping, and billing; a microservice architecture where teams deploy and scale
their services without coordinating; or any workflow where adding a new downstream
step shouldn't require touching the upstream code.

If you need both — say, distributing work across services (bus) while giving each
service fine-grained control over execution and rollback (commands) — use both.

## Conclusion

The two strategies aren't competitors. Many sophisticated systems use both: a message bus distributes work across multiple servers, and the Command Pattern manages how that work gets executed within each one.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: _Photo by RDNE Stock project on Pexels_
