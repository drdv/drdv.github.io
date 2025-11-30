---
draft: false
date: 2025-11-13
categories:
  - GNU Make
slug: 202511-make-double-colon-rules
---

# `GNU Make`: double-colon rules

Consider an integration testing setup where the command to test appears on the first
line of a text file, followed by the expected output. I used to run all tests using:

```Makefile
TESTS := test-html test-latex test-semicolon ...

.PHONY: $(TESTS)
$(TESTS): COMMAND = $(shell head -n 1 $(TEST_DIR/$@))
$(TESTS): EXPECTED = ... $(TEST_DIR/$@)
$(TESTS): RESULT = ...
$(TESTS):
	compare $(EXPECTED) with $(RESULT)
```

but the other day I had the following problem: one of the tests required additional
post-processing.

<!-- more -->

Long story short: I switched to using [double-colon
rules](https://www.gnu.org/software/make/manual/html_node/Double_002dColon.html):

```Makefile
$(TESTS):: COMMAND = ... $(TEST_DIR/$@)
$(TESTS):: EXPECTED = ... $(TEST_DIR/$@)
$(TESTS):: RESULT = ...
$(TESTS)::
	compare $(EXPECTED) with $(RESULT)

test-latex::
	post-processing
```

The key difference from normal (single-colon) rules is that, instead of having just one,
we can associate multiple recipes with a target, which are executed sequentially in the
order they are defined.

There might be downsides I am not aware of, but this seems like a convenient and
extensible solution to the above problem. I no longer need to come up with new target
names or reorganise tests to ensure that all post-processing steps are executed. All I
have to do is "register" additional recipes with a target -- much like hooks -- which
`Make` runs automatically whenever needed. The "whenever needed" part can be controlled
by means of specifying dependencies to my `test-latex::` target.

The docs say:

> Double-colon rules are somewhat obscure and not often very useful; they provide a
> mechanism for cases in which the method used to update a target differs depending on
> which prerequisite files caused the update, and such cases are rare.

This might be true when the target is a real file but in the context of `.PHONY` targets
(where the side-effect is the intended effect), double-colon rules seem to provide a
useful mechanism that let me let `Make` do its job.

And another quote from the docs:

> Double-colon rules with the same target are in fact completely separate from one
> another. Each double-colon rule is processed individually, just as rules with different
> targets are processed.

Maybe I am parsing this the wrong way but different targets can have different
target-specific variables, while target-specific variables used in the recipes of
double-colon rules (associated with the same target) are shared:

```Makefile
t:: A = 1
t::; @echo $(A)
t:: A = 2
t::; @echo $(A)
t:: A = 3
```
outputs

```
3
3
```
