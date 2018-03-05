---
layout: post
title: Simple Data Structures in Go
---

There are plenty of things to like about the Go programming language, but if you're used to working with generics, and, in particular, something like the Java collections framework, you might find it a bit difficult at first to adapt to the lack of these features in Go.

This is a particular issue in timed programming challenges. Sometimes you may find you need queue or a stack, for example - and if you're having to write implementations from scratch yourself - you could be putting yourself at a significant disadvantage compared to your Java-writing competitors.

It turns out there are few tricks, however. Here's a brief overview:

## Lists, Stacks, Queues and Deques

Assume we have a data structure (list) `l`, an element `x`  (here with type `int`), and an index, `i`.

### Slices

```go
// Initialisation
l := []int{1, 2, 3}
// Initialisation - with initial length of 0 and initial capacity for 10 elements
l := make([]int, 0, 10)
```

Slices are Go's "go-to" for most standard data structures. They're pretty efficient and very easy to use. They're essentially references to arrays, and they don't have a fixed length. In many ways, [their implementation](https://blog.golang.org/go-slices-usage-and-internals) is similar to that of Java's `ArrayList`.

NB: You need to be careful when passing slices around - if you want to change the array, passing the slice's value is fine, but if you want to change the slice itself, you'll need to pass a pointer.

Go slices are perfect as **stacks**:

```go
// Push   amortised O(1)
append(l, x)
// Pop    amortised O(1)
length := len(s)
return s[:length - 1], s[length - 1]
```

And also as **queues**:

```go
// Enqueue   amortised O(1)
append(l, x)
// Dequeue   amortised O(1)
return s[1:], s[0]
```

And they also work quite nicely as **lists**:

```go
// Insert   O(n)
l = append(l, 0)
copy(l[i+1:], l[i:])
l[i] = x
// Delete   O(n)
l = l[:i + copy(l[i:], l[i+1:])]
// Iteration
for i, x := range l { /* do something */ }
```

Note that slightly less efficient, but arguably more readable versions of the above are possible using `append` instead of `copy`.

### Buffered Channels

```go
// Initialisation
l := make(chan int, 100)
```

Buffered channels are really just thread-safe **queues**. The one drawback is that you have to provide a channel with an upper capacity limit - but if that's not an issue for you, they can be a very concise and efficient option:

```go
// Enqueue   O(1)
l <- x
// Dequeue   O(1)
return <- l
```

### Containers: Lists

```go
import "container/list"

// Initialisation
l := list.New()
```

Go's [containers package](https://golang.org/pkg/container/) provides a doubly-linked-list interface.

One thing that a slice won't work well for is a **deque** (double ended queue). That's because adding to the front of a slice is quite costly. But this is something that can be solved by a doubly-linked-list:

```go
// PushFront   O(1)
l.PushFront(x)
// PushBack    O(1)
l.PushBack(x)
// PopFront    O(1)
return l.Remove(l.Front()).(int)
// PopBack     O(1)
return l.Remove(l.Back()).(int)
```

Of course, we don't have generics, so how does Go's containers package work? Well, they contain an `interface{}` type, which could be anything. If we want to retrieve something from our container, we need to "assert" the type we're expecting (which is fancy Go talk for typecasting) - that's what the `.(int)` is for.

### Containers: Rings

Rings are circular lists. I'll admit I've never used one before, but I can see how they'd be particularly useful for certain problems such as:

> Given a set of players sitting in a circle that are numbered from 1 up, eliminate them 1-by-1 by first eliminating #1, then #3, and then #6 such that the amount of players that "survive" between each elimination increases by one. Continue around the circle until a final survivor remains.

## Sets and Maps

Assume we have a data structure (map) `m`, a key `k`  (here with type `int`), and a value, `v` (with type `string`).

### Maps

Go maps implement a hash table.

They can be used as **sets**:

```go
// Initialisation
m := map[int]bool{}
// Add        O(1)
m[k] = true
// Contains   O(1)
return m[k]
// Remove     O(1)
delete(m, k)
```

Or **maps**:

```go
// Initialisation
m := map[int]string{}
// Add        O(1)
m[k] = v
// Get        O(1)
if v, ok := l[x]; ok { return v }
// Remove     O(1)
delete(m, k)
// Iteration
for k, v := range m { /* do something */ }
```

## Tree-Based Data Structures

### Containers: Heaps

Go's heap package implements a min-heap. Heaps are useful for **priority queues** and things that need to be **sorted**.

You need to provide a type that implements `heap.Interface`:

```go
// heap.Interface
type Interface interface {
	sort.Interface
	Push(x interface{}) // append x to collection
	Pop() interface{} // remove and return last element
}
// sort.Interface
type Interface interface {
	Len() int // size of the collection
	Less(i, j int) bool // true if elem i < elem j
	Swap(i, j int) // swap elems i and j
}
```

Once you've sorted that, you can use the heap functionality. Let's assume that `&l`  is some kind of collection that implements the above:

```go
// Initialise
heap.Init(&l)
// Push   O(log n)
heap.Push(&l, x)
// Pop    O(log n)
heap.Pop(&l)
```

### DIY

If you've reached this far, and still not found what you're looking for, you're probably trying to implement some other tree-based data structure, and it's probably time to bite the bullet and write it yourself.

I find it's best practice to look up the data structure you're going to implement in your favourite book / web-resource - even if you know your data structures well. You'll definitely make fewer silly mistakes and probably end up saving yourself some time. 

Alternatively, you can always use an open-source implementation, if you can find one.

## References

- [The Go Programming Language Specification](https://golang.org/ref/spec)
- *The Go Blog* [Go Slices: usage and internals](https://blog.golang.org/go-slices-usage-and-internals)
- *Go Wiki* [Slice Tricks](https://github.com/golang/go/wiki/SliceTricks)
- *The Go Blog* [Go maps in action](https://blog.golang.org/go-maps-in-action)
- [Container Package Documentation](https://golang.org/pkg/container/)
- *John Graham-Cumming* [Go Containers](https://github.com/cloudflare/jgc-talks/tree/master/Go_London_User_Group/Go_Containers)
- *Grayson Koonce* [Solving ring-shaped problems with Go's container/ring](https://graysonkoonce.com/solving-ring-shaped-problems-with-golangs-container-ring/)