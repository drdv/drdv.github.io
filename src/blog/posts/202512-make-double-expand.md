---
draft: false
date: 2025-12-01
categories:
  - GNU Make
slug: 202512-make-double-expand
description: A cool double-expand trick in GNU Make that makes functional programming possible.
---

# `GNU Make`: double-expand

A few days ago I stumbled upon [this](https://www.bhk.com/make/closures.html) article
late in the evening and it kept me awake the whole night! It describes a cool trick that
allows to "double-expand" a macro without using `eval`. The following is a summary of
the main idea, a reflection of why it works and a small extension.

<!-- more -->

## Macro expansion

A macro is a string that expands to another string when referenced. For example the
macro `foo`, can be expanded using `$(foo)`. That is, the string `$(foo)` would be
replaced by the result of an expansion process. A _macro reference_ takes the form of a
dollar sign followed by either a single character or a string enclosed in matching
parenthesis, e.g., `$foo` is the same as `$(f)oo` which is different from `$(foo)`.
Normally, each `$` (that defines the start of a macro reference) expands **exactly**[^1]
one string in a left-to-right depth-first traversal.

Apart from a string substitution, a macro expansion may result in a side-effect, as is
the case, e.g., with `$(info ...)`, which prints its expanded argument(s) on standard
output and returns an empty string. We could think of `info` as a built-in function. In
addition to built-in functions, there is the notion of user-defined functions. Next, I
make an important distinction between the two.

## Functions

A macro reference of the form `$(string srg1,arg2,...)` is interpreted as a built-in
function call, when `string` exists as a key in a hash table of built-in functions. In
such a case, the following comma-separated strings are interpreted as positional
arguments and are either all expanded as per normal, or are left to the function to
expand in a custom way. In the `C` code, this is governed by the `EXP?` column in

```c
static struct function_table_entry function_table_init[] =
{
 /*         Name            MIN MAX EXP? Function */
  FT_ENTRY ("abspath",       0,  1,  1,  func_abspath),
  FT_ENTRY ("addprefix",     2,  2,  1,  func_addsuffix_addprefix),
  // ...
  FT_ENTRY ("foreach",       3,  3,  0,  func_foreach),
  FT_ENTRY ("let",           3,  3,  0,  func_let),
  FT_ENTRY ("call",          1,  0,  1,  func_call),
  // ...
  FT_ENTRY ("intcmp",        2,  5,  0,  func_intcmp),
  FT_ENTRY ("if",            2,  3,  0,  func_if),
  FT_ENTRY ("or",            1,  0,  0,  func_or),
  FT_ENTRY ("and",           1,  0,  0,  func_and),
  FT_ENTRY ("value",         0,  1,  1,  func_value),
};
```

Except for `foreach`, `let`, `intcmp`, `if`, `or` and `and`, all built-in functions have
their arguments expanded.

A user-defined function, on the other hand, is always expanded as a standard macro that
could, potentially, contain some parameters/arguments to be specified later. For
example:

```Makefile
a = a
b = function

my-function = This is $a custom $b.

$(info $(my-function))
$(info $(let a b,my macro,$(my-function)))

all:;@:
```

would output

```
This is a custom function.
This is my custom macro.
```

Instead of `a` and `b` as in the above example, normally we name parameters as `1`, `2`,
etc. and use the built-in `$(call ...)` function:

```Makefile
my-standard-function = This is $1 standard $2.
$(info $(call my-standard-function,a,function))
```

## The `call` function

As with most built-in functions, all arguments of `call` are expanded (see
`function_table_init`). Then it is responsible for two things:

+ detect if what is to be called is actually a built-in function -- in which case it is
  executed directly with the already expanded arguments;
+ if instead, a user-defined function is to be called, the parameters `1, 2, ...` are
  initialised on a local stack and the macro is expanded (something like the above
  `$(let ...)` example).

## Double-expansion

The trick is to use `$(call ...)` to call one of the 6 builtin functions that expand
their own arguments (i.e., for which `EXP? = 0`). For example:

```Makefile
key = value
x = $$(key)

my-function = $(eval _tmp:=$1)$(_tmp)

$(info $(call or,$x))
$(info $(call firstword,$x))
$(info $(call my-function,$x))

all:;@:
```

would output

```
value
$(key)
value
```

In all cases, the argument `$x` is expanded to `$(key)`. Then `or` expands `$(key)` (as
it would normally do if we call directly `$(or $(key))`) which results in `value`.
`firstword`, on the other hand, "knows" that its argument is already expanded and simply
returns the first word (which happens to be the literal string `$(key)`). To achieve the
same double-expansion with a user-defined function, we would have to use `eval` and
define a global variable (as in `my-function`).

## Anonymous functions

Here it is worth reading the [original](https://www.bhk.com/make/closures.html) article.
It presents a nice sequence of examples that rely on the double-expansion trick to
define anonymous functions. Here I present one of them[^2] in order to point out that, as an
alternative to the positional arguments in their "Hack #3", we could use key-value
arguments, that avoid the need to define an `apply` function.

### Fold left

Let us define `foldl` similar to the following
[example](https://github.com/drdv/sicp/blob/e2bc04d437e082f62261f97a8f22bfc47151c97a/sicp2_part1.rkt#L1827-L1832)
in Racket

```Racket
(define (foldl op initial sequence)
  (if (null? sequence)
      initial
      (foldl op
		     (op initial (car sequence))
		     (cdr sequence))))
```

The result is:

```Makefile
car = $(firstword $1)
cdr = $(wordlist 2,$(words $1),$1)

foldl = $(if $3,$\
			$(call foldl,$\
				$1,$\
				$(let a,$2,$\
					$(let e,$(call car,$3),$\
						$(call or,$1))),$\
				$(call cdr,$3)),$\
			$2)

$(info $(call foldl,$$a$$e$$a,.,a b c))

all:;@:
```

While this wouldn't win a code readability contest, it is kind of nice. Note how, after
the initial expansion, argument `1` of `foldl` is equal to `$a$e$a` -- which is what
`or` further expands using the local variables `$a` (the accumulator) and `$e` (the
current element) defined in the two nested `let` blocks. The output is:

```
.a.b.a.c.a.b.a.
```

Our anonymous function `$$a$$e$$a` takes two parameters, which are now fixed to be `a`
and `e`. The reason for using two nested `let` blocks instead of the more readable

```Makefile
$(let a e,$2 $(call car,$3),$(call or,$1))
```

is that the latter option doesn't work when there are spaces in the anonymous function
(e.g., `$$a $$e $$a`) -- this is due to the way lists are defined in `Make`.

### The 6 special functions

As I mentioned, we could use any of the 6 special functions to implement the
double-expansion trick:

```Makefile
key = value
x = $$(key)

$(info $(call or,$x))
$(info $(call and,$x))
$(info $(call if,1,$x))
$(info $(call foreach,,_,$x))
$(info $(call let,,,$x))
$(info $(call intcmp,1,2,$x))

all:;@:
```

The output is:

```
value
value
value
value
value
value
```

I believe the following sentence in the
[docs](https://www.gnu.org/software/make/manual/html_node/Call-Function.html) refers to
the above behaviour:

> The 'call' function expands the PARAM arguments before assigning them
> to temporary variables.  This means that VARIABLE values containing
> references to built-in functions that have special expansion rules, like
> 'foreach' or 'if', may not work as you expect.

!!! note "Comments"

    Got feedback? Leave it [here](https://github.com/drdv/drdv.github.io/discussions/3).

[^1]: But there are exceptions, which are discussed below. Note that `$$` is equivalent
to `$($)`, and only the first `$` defines the start of a macro reference, while the
second `$` is a part of the associated string (which expands to itself).

[^2]: The others can be modified in a similar way.
