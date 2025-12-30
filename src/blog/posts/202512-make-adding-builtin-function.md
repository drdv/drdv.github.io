---
draft: false
date: 2025-12-03
categories:
  - GNU Make
slug: 202512-make-adding-builtin-function
description: An example of how to add a built-in function to GNU Make.
---

# `GNU Make`: Adding a built-in function

I saw [this](https://lists.gnu.org/archive/html/help-make/2025-12/msg00000.html)
question on the help-make mailing list and I decided to see how easy it would be to
register a new built-in function in GNU Make. It turned out to be quite easy (in
comparison, it took me more time to write this post). I then found out that there is a
section "Anatomy of a Built-In Function" in "The GNU Make Book" by John Graham-Cumming
which helped me to see alternatives.

<!-- more -->

## The sources

```Bash
curl -O https://ftp.gnu.org/gnu/make/make-4.4.tar.gz && tar xvf make-4.4.tar.gz
cd make-4.4 && ./configure && make
```

## The function

```c
static char *
func_location (char *o, char **argv, const char *funcname UNUSED)
{
  const floc *flocp = reading_file;
  if (flocp && flocp->filenm) {
    const char *mode = argv[0];
    if (!strcmp(mode, "file")) {
      return variable_buffer_output(o, flocp->filenm, strlen(flocp->filenm));
    } else if (!strcmp(mode, "line")) {
      char buf[21];
      snprintf(buf, sizeof(buf), "%lu", flocp->lineno + flocp->offset);
      return variable_buffer_output(o, buf, strlen(buf));
    }
  }
  return o;
}
```

All built-in functions have the same signature:

+ `o`: a pointer to the buffer where the result of the macro expansion would be substituted
+ `argv`: an array of arguments
+ `funcname`: a label (which we don't use).

The logic of the code is not important[^1] -- a string containing filename/line number
is formed and `variable_buffer_output(...)` is called to insert it into the output
buffer. We then add `func_location` to `src/function.c` and include it into a hash table
of built-in functions (where we specify that there would be exactly one argument which
would be expanded as per usual):

```c
static struct function_table_entry function_table_init[] =
{
 /*         Name            MIN MAX EXP? Function */
  FT_ENTRY ("abspath",       0,  1,  1,  func_abspath),
  // ...
  FT_ENTRY ("location",      1,  1,  1,  func_location),
};
```

Then we run `make` in `make-4.4` again and we are done.

## The example

So now we have a function that takes one argument (either `file` or `line`). We define
two recursively expanded variables (`__FILE__` and `__LINE__`) for convenience:

```Makefile title="Makefile.test" linenums="1"
__FILE__ = $(location file)
__LINE__ = $(location line)

.PHONY: all tell-lines

all: tell-lines other

# empty/commented lines before the first recipe line are accounted for
	@echo "[one logical line  ] $(__FILE__):$(__LINE__)" \
	"($(__LINE__))"

# all other empty/commented lines in a recipe are ignored
	@echo "[after empty lines ] $(__FILE__):$(__LINE__)"

# the line number of the first recipe line is correct
tell-lines:
	@printf "tell-lines at %s:%d\n" $(__FILE__) $(__LINE__)

include Makefile.other
```

```Makefile title="Makefile.other" linenums="1"
.PHONY: other
other:
	@echo "[from included file] $(__FILE__):$(__LINE__)"
```

Running `make -f Makefile.test` outputs:
```
tell-lines at Makefile.test:17
[from included file] Makefile.other:3
[one logical line  ] Makefile.test:9 (9)
[after empty lines ] Makefile.test:10
```

As noted in the comments above, the line numbers indicate "[logical
lines](https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html)" and
empty/commented lines after the first recipe line are not accounted for (my guess is
that this is a consequence of "[how makefiles are
parsed](https://www.gnu.org/software/make/manual/html_node/Parsing-Makefiles.html)").

!!! note "Comments"

    Got feedback? Leave it [here](https://github.com/drdv/drdv.github.io/discussions/4).

[^1]: I am sure I don't handle some edge-cases -- but that's beyond the point.
