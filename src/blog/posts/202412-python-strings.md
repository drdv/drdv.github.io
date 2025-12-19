---
draft: false
date: 2024-12-06
categories:
  - python
slug: 202412-python-strings
---

# Anatomy of python strings

From the [docs](https://docs.python.org/3.12/library/stdtypes.html#textseq): "Strings
are immutable sequences of Unicode code points". This requires a bit of unpacking ...

<!-- more -->

## Terminology

From the sea of technical lingo, I will mostly use three concepts (and often abuse
terminology):

**Symbol**

:   A symbol is an entity that conveys meaning in a given context. It can be seen as a
    "meme" in that it represents an idea or recognized concept. For example, it can be a
    single character or unit of text as perceived by a human reader (regardless of the
    underlying primitive blocks from which it is formed). The digit `1` is a symbol, so
    is that letter `é`, and so is the emoji 👨‍👩‍👧‍👦.

**Character**

:   A primitive building block for symbols. It is common to refer to a visible (i.e., a
    user-perceived) character as a *grapheme*.

**Code point**

:   Unicode code points are unsigned integers[^hex] that map one to one with (primitive)
    characters. That is, to each character in the Unicode character set there is a
    corresponding integer code point as its index.

[^hex]: Often expressed as a hexadecimal number.

For example, the code point `97` corresponds to the grapheme `e`. Every (primitive)
character can be seen as a symbol, but the opposite is not true because there are many
symbols that do not have an assigned code point. That is, some symbols are defined in
terms of a sequence of characters (and thus, of code points). Such symbols are commonly
referred to as *grapheme clusters*. An example of a grapheme cluster is 👨‍👩‍👧‍👦 (as we
will [see](#example-a-family) shortly, it consists of 7 characters 4 of which are
graphemes).

## Redundancy of representation

``` mermaid
flowchart LR
    subgraph G0 [symbol]
		symbol{"é"}
    end
    subgraph G1 [as one code point]
		one_code_point["é (U+00E9)"]
    end
    subgraph G2 [as two code points]
		dispatch@{ shape: framed-circle }
		dispatch --> two_code_point_1["e (U+0065)"]
		dispatch --> two_code_point_2["́  (U+0301)"]
    end
	symbol --> dispatch
	symbol --> one_code_point

	style symbol font-size:20px
	style one_code_point font-size:18px
	style two_code_point_1 font-size:18px
	style two_code_point_2 font-size:18px
```

In Unicode, the symbol é can be encoded in two ways (see [Unicode
equivalence](https://en.wikipedia.org/wiki/Unicode_equivalence)). First, it has a
dedicated code point (which defines it as a "primitive" grapheme). Second, it can be
represented as a combination of e and an acute accent (which makes it a grapheme cluster
as well).

``` python
s1 = "é"  # using one code point (U+00E9)
s2 = "é"  # using two code points (equivalent to s2 = "e\u0301")

assert s1 != s2
assert len(s1) == 1
assert len(s2) == 2

for char in s2:
	code_point = ord(char)
	print(f"{code_point} ({hex(code_point)})")
```

<div class="result" markdown>
Output: (1)
{ .annotate }

1.  `M-x describe-char` in `emacs` gives:

    === "on é (one code point)"
		``` { . .no-copy hl_lines="1 14 17" }
					 position: 1 of 1 (0%), column: 0
					character: é (displayed as é) (codepoint 233, #o351, #xe9)
					  charset: iso-8859-1 (Latin-1 (ISO/IEC 8859-1))
		code point in charset: 0xE9
					   script: latin
					   syntax: w 	which means: word
					 category: .:Base, L:Strong L2R, c:Chinese, j:Japanese, l:Latin, v:Viet
					 to input: type "C-x 8 RET e9" or "C-x 8 RET LATIN SMALL LETTER E WITH ACUTE"
				  buffer code: #xC3 #xA9
					file code: #xC3 #xA9 (encoded by coding system utf-8-unix)
					  display: terminal code #xC3 #xA9

		Character code properties: customize what to show
		  name: LATIN SMALL LETTER E WITH ACUTE
		  old-name: LATIN SMALL LETTER E ACUTE
		  general-category: Ll (Letter, Lowercase)
		  decomposition: (101 769) ('e' ' ')
		```

	=== "on é (two code points)"
		``` { . .no-copy hl_lines="1 13 14 15" }
					 position: 1 of 2 (0%), column: 0
					character: e (displayed as e) (codepoint 101, #o145, #x65)
					  charset: ascii (ASCII (ISO646 IRV))
		code point in charset: 0x65
					   script: latin
					   syntax: w 	which means: word
					 category: .:Base, L:Strong L2R, a:ASCII, l:Latin, r:Roman
					 to input: type "C-x 8 RET 65" or "C-x 8 RET LATIN SMALL LETTER E"
				  buffer code: #x65
					file code: #x65 (encoded by coding system utf-8-unix)
					  display: composed to form "e " (see below)

		Composed with the following character(s) " " by these characters:
		 e (#x65) LATIN SMALL LETTER E
		   (#x301) COMBINING ACUTE ACCENT

		Character code properties: customize what to show
		  name: LATIN SMALL LETTER E
		  general-category: Ll (Letter, Lowercase)
		  decomposition: (101) ('e')
		```

``` { . .no-copy }
101 (0x65)
769 (0x301)
```
</div>

## Example: a family

``` mermaid
flowchart TD
	%%{init: {'themeVariables': {'title': 'My Flowchart Title'}}}%%
	family1["👩‍👧"]
	family2["👩‍👩‍👧"]
	family3["👨‍👩‍👧‍👦"]
	family4["👪︎"]
	family5["👨‍👦‍👦"]
	C@{ shape: framed-circle, label: "Stop" }
	C --> cp1["👨"]
	C --> cp2["U+200d"]
	C --> cp3["👩"]
	C --> cp4["U+200d"]
	C --> cp5["👧"]
	C --> cp6["U+200d"]
	C --> cp7["👦"]
	family3 --> C

	cp1-.->cp1-hex["U+1f468"]
	cp3-.->cp3-hex["U+1f469"]
	cp5-.->cp5-hex["U+1f467"]
	cp7-.->cp7-hex["U+1f466"]

	style family1 font-size:50px
	style family2 font-size:50px
	style family3 font-size:50px
	style family4 font-size:50px
	style family5 font-size:50px
	style cp1 font-size:30px
	style cp2 font-size:30px
	style cp3 font-size:30px
	style cp4 font-size:30px
	style cp5 font-size:30px
	style cp6 font-size:30px
	style cp7 font-size:30px
	style cp1-hex font-size:30px
	style cp3-hex font-size:30px
	style cp5-hex font-size:30px
	style cp7-hex font-size:30px
```

There are various emoji symbols that portray a family. They have different semantics,
which is reflected by the code points used to form them. In the representation of the
middle one (depicted on the lower levels), there are 4 primitive graphemes glued
together with the [zero-width joiner](https://en.wikipedia.org/wiki/Zero-width_joiner)
character `U+200d`. We can use `#!python list("👨‍👩‍👧‍👦")` to get a list of characters
associated with the code points that form 👨‍👩‍👧‍👦.

## Indexing

Consider the string `#!python sentense = "This 👨‍👩‍👧‍👦 is my family!"`. As python
strings are (stored as) sequences of code points, `#!python sentense[:6]` would give
`#!python "This 👨"` because 👨 corresponds to the first (also called a *base*) code
point of 👨‍👩‍👧‍👦. As can be expected `#!python sentense[:8]` returns `#!python "This
👨‍👩"`, where the zero-width joiner is not visible[^rendering].

[^rendering]: The string might be rendered as `#!python "This 👨\u200d👩"`.

The situation can get tricky with symbols that may have different Unicode
representations. For example `#!python len("L'idée a été réévaluée.")` is 23, while
`#!python len("L'idée a été réévaluée.")` is 29 because all symbols é in the latter
string are encoded using two code points. One can imagine strings with a mix of
representations for the same symbols which can be difficult to handle in an ad hoc
manner.

## Grapheme clustering

The Unicode standard defines [rules](https://www.unicode.org/reports/tr29) for
identifying sequences of code points that are meant to form a particular symbol (i.e.,
grapheme cluster). Finding [symbol
boundaries](https://unicode.org/reports/tr29/#Grapheme_Cluster_Boundaries) is a common
problem e.g., in text editors and terminal emulators. As an example, consider the
following functionality from the `grapheme`[^grapheme-install] package:

[^grapheme-install]: `pip install grapheme`

``` python
import grapheme

sentense = "This 👨‍👩‍👧‍👦 is my family!"

assert len(sentense) == 26
assert grapheme.length(sentense) == 20
assert not grapheme.startswith(sentense, sentense[:6])
```

## Normalization

The `unicodedata` package is a part of python's standard library and can be used to
normalize a string. That is, to detect symbols for which alternative Unicode encodings
exist and to convert them to a given [canonical](https://www.unicode.org/reports/tr15)
form.

``` { .python .annotate }
import unicodedata

s1 = "L'idée a été réévaluée."
assert len(s1) == 23

# each "é" becomes "e\u0301"
s2 = unicodedata.normalize("NFD", s1) # canonical decomposition
assert len(s2) == 29 # (1)!

s3 = unicodedata.normalize("NFC", s2) # canonical composition
assert len(s3) == 23
assert s1 == s3
assert s1 != s2
```

1.  While the representation of symbols resulting from the `NDF` canonical decomposition
	may contain more code points, it allows for greater flexibility of text processing
	in many contexts, e.g., string pattern matching.

## Memory footprint

The above discussion is mostly abstract in that it makes no assumptions on how code
points (ranging from `0` to `1114111`) are to be stored in memory. Starting from [PEP
393](https://peps.python.org/pep-0393/), python addresses the memory storage problem in
a pragmatic way by handling **four cases** which depend only on one parameter: the
largest code point occurring in the string.

``` { .python }
import sys
import unicodedata

s1 = "L'idée a été réévaluée."
s2 = unicodedata.normalize("NFD", s1)

m1, m2 = max(s1), max(s2)
print(f"[s1]: {ord(m1)} ( {m1} ) #bytes = {sys.getsizeof(s1)}")
print(f"[s2]: {ord(m2)} ( {m2}  ) #bytes = {sys.getsizeof(s2)}")
```

<div class="result" markdown>
Output:

``` { . .no-copy }
[s1]: 233 ( é ) #bytes = 80
[s2]: 769 ( ́  ) #bytes = 116
```
</div>

The largest code point for the `s2` string corresponds to the combining acute accent,
while for the `s1` string it corresponds to `é`.

The four cases are:

\begin{align}
	\texttt{code_point_bytes}(s) = \begin{cases}
		1, & \text{if $\mu(s) < 2^7$}.\\
		1, & \text{if $\mu(s) < 2^8$}.\\
		2, & \text{if $\mu(s) < 2^{16}$}.\\
		4, & \text{otherwise}.
	\end{cases}
\end{align}

where $\mu(s)$ denotes the largest code point in the string $s$. The memory required to
store $s$ is

$$
\texttt{struct_bytes}(s) + (\texttt{len}(s) + 1) \cdot \texttt{code_point_bytes}(s),
$$

where $\texttt{len}(s)$ is the number of code points in $s$ and, the size of the
`C-struct` that holds the data is given by[^c_struct_size]

\begin{align}
	\texttt{struct_bytes}(s) = \begin{cases}
		40, & \text{if $\mu(s) < 2^7$}.\\
		56, & \text{otherwise}.
	\end{cases}
\end{align}

[^c_struct_size]: Assuming a `x86_64` architecture (see the `string_bytes` function for
more details).

The above logic is implemented in the `string_bytes` function below[^PyUnicode_New].

[^PyUnicode_New]: Based on `#!c PyObject * PyUnicode_New(Py_ssize_t size, Py_UCS4 maxchar)`
in `unicodeobject.c`.

??? info "`#!python def string_bytes(s):`"

	``` python
	def string_bytes(s):
		numb_code_points, max_code_points = len(s), ord(max(s))

	    # C-structs in cpython/Objects/unicodeobject.c
		# ----------------------------------------------
		# ASCII     (use PyASCIIObject):
		#   2 x ssize_t       = 16
		#   6 x unsigned int  = 24
		# otherwise (use PyCompactUnicodeObject):
		#   1 x PyASCIIObject = 40
		#   1 x ssize_t       = 8
		#   1 x char *        = 8
		# assuming a x86_64 architecture
		struct_bytes = 56
		if max_code_points < 2**7:
			code_point_bytes = 1
			struct_bytes = 40
		elif max_code_points < 2**8:
			code_point_bytes = 1
		elif max_code_points < 2**16:
			code_point_bytes = 2
		else:
			code_point_bytes = 4

		# `+ 1` for zero termination
		# the result is identical with sys.getsizeof(s)
		return struct_bytes + (numb_code_points + 1) * code_point_bytes
	```

For the above example, `s1` is `56 + (23 + 1) * 1 = 80` bytes because it falls in the
second case as its largest code point is 233. The string `s2`, on the other hand, falls
in the third case because the acute accent has a code point above 255 (so its size is
`56 + (29 + 1) * 2 = 116` bytes).

Three clear advantages of the [PEP 393](https://peps.python.org/pep-0393/) approach:

* an optimized ASCII implementation can be used for the most common (ASCII) case
* the constant number of bytes per code point[^smallest_constant_representation] results
  in constant-time indexing and facilitates other operations
+ can handle natively strings containing [non-BMP
  characters](https://en.wikipedia.org/wiki/Plane_(Unicode)), i.e., code points greater
  than $2^{16} - 1$.

[^smallest_constant_representation]: The smallest possible is always chosen.

On the flip-side, concatenating a single emoji to an ASCII string increases the size x
4.

## Code units

The building block used to actually store a code point in memory is often called a *code
unit*. For example, consider the acute accent (`U+0301`):

``` mermaid
flowchart TD
	%%{init: {'themeVariables': {'title': 'My Flowchart Title'}}}%%

	s["U+0301"]
	s --> utf8["UTF-8"]
	s --> utf16["UTF-16"]
	s --> utf32["UTF-32"]

	C@{ shape: framed-circle, label: "Stop" }
	C -.-> utf8-1["CC"]
	C -.-> utf8-2["81"]

	utf8 -.-> C
	utf16 -.-> utf16-1["0103"]
	utf32 -.-> utf16-2["01030000"]

	style utf8 stroke-width:2px,stroke-dasharray: 5 5
	style utf16 stroke-width:2px,stroke-dasharray: 5 5
	style utf32 stroke-width:2px,stroke-dasharray: 5 5
```


* with a `utf-8` encoding there are two 8-bit code units (`0xCC` and `0x81`)
* with a `utf-16` encoding there is one 16-bit code unit
* with a `utf-32` encoding there is one 32-bit code unit .

Note that, in the above example, the code units for `utf-16` and `utf-32` are stored
using little-endian.

### Four string encodings

A different encoding is used in each of the four cases discussed above.

* case 1 $\left(\mu(s) < 2^7\right)$: ASCII (which is equivalent to UTF-8 in this range)
* case 2 $\left(\mu(s) < 2^8\right)$: UCS1 (i.e., LATIN-1)
* case 3 $\left(\mu(s) < 2^{16}\right)$: UCS2 (i.e., UTF-16)
* case 4 $\left(\mu(s) \geq 2^{16}\right)$: UCS4 (i.e., UTF-32).

For example, the string `#!python mess` in the snippet below has 8 code points and
$\mu(\texttt{mess}) = 65039$, hence we are in case 3 in which UTF-16 encoding should be
used. At the end, the encoding computed manually is compared[^memory-comparison-hack]
with the actual memory occupied by our string.

[^memory-comparison-hack]: We used a `CPython` implementation of `python 3.12`.

``` { .python }
mess = "I♥️日本ГО©"

assert len(mess) == 8
assert ord(max(mess)) == 65039  # case 3: 255 < 65039 < 65536

# utf-16-le stands for utf-16 with little-endian
encoding = b''.join([char.encode("utf-16-le") for char in mess]).hex()

assert string_bytes(mess) == 74  # 56 + (8 + 1) * 2
assert len(encoding) == 32  # i.e., 16 bytes as it is in hex
assert encoding == "490065260ffee5652c6713041e04a900"

# --------------------------------------------------------------------------
# compare to groundtruth (this is a hack!)
# --------------------------------------------------------------------------
import ctypes
import sys

def memory_dump(string):
	address = id(string)  # assuming CPython
	buffer = (ctypes.c_char * sys.getsizeof(string)).from_address(address)
	return bytes(buffer)

# [56:] removes what we called struct_bytes above (in CPython they come first)
# [:-2] removes the zero termination bytes
assert memory_dump(mess)[56:-2].hex() == encoding
# --------------------------------------------------------------------------
```

### Bytes objects

As we have seen, the code units used to store a python string in memory depend on the
string itself and are abstracted away from the user. While this is a good thing in many
cases, sometimes we need more fine-grained control. [To this
end](https://peps.python.org/pep-0358/#motivation), python provides the *"bytes" object*
(an immutable sequences of single bytes). Actually we already used it in the previous
example as it is the return type of
[`str.encode`](https://docs.python.org/3.12/library/stdtypes.html#str.encode).

Let us consider the string `#!python a_man = "a👨"`. By now we know that it is stored using
4 bytes per code point. Using `#!python a_man.encode("utf-32")` we obtain:

* `#!python "a"`: `97, 0, 0, 0`
* `#!python "👨"`: `104, 244, 1, 0`.

If we relax the constraint of constant number of bytes per code point, we can dedicate
less space to our string. Using `#!python a_man.encode("utf-16")` we obtain:

* `#!python "a"`: `97, 0`
* `#!python "👨"`: `61, 216, 104, 220`

or using `#!python a_man.encode("utf-8")`:

* `#!python "a"`: `97`
* `#!python "👨"`: `240, 159, 145, 168`.

All above representations have their applications. For example UTF-8 provides
compatibility with ASCII and efficient data storage, while UTF-16 and UTF-32 allow for
faster processing of a larger range of characters. Having the possibility to
easily/efficiently change representations is convenient.

Bytes do not necessarily have to be associated with individual code points, as is the
case when using `#!python str.encode`. For example, suppose we want to express the
string `#!python "a1b1"` as a byte object, where each pair of characters represents a
byte in hex (i.e., `0xA1` followed by `0xB1`). In this case, using `#!python
list("a1b1".encode())` is not appropriate, as it would return `[97, 49, 98, 49]`, which
are the ASCII codes for the characters `a`, `1`, `b`, and `1`, respectively. Instead, we
should consider the additional structure and use `#!python list(bytes.fromhex("a1b1"))`,
which results in `[161, 177]`.

Bytes objects can also be used in other contexts. For instance, `#!python
(1).to_bytes(4, byteorder='little')` returns the byte representation of the integer 1
(in little-endian).

## Immutability

The design decision to have immutable string in python has far-reaching implication
related to e.g., hashing, performance optimizations, garbage collection, thread safety
etc. In addition to all this, having immutable strings was a prerequisite for the
approach in [PEP 393](https://peps.python.org/pep-0393/).

!!! note "Comments"

    Got feedback? Leave it [here](https://github.com/drdv/drdv.github.io/discussions/7).
