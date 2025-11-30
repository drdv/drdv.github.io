#
# Keep this here as I didn't add the following to the post.
#

# --------------------------------------------------------------------------------------
# foldr
# --------------------------------------------------------------------------------------
car = $(firstword $1)
cdr = $(wordlist 2,$(words $1),$1)

# as with foldl, it is better to have two nested let to handle spaces
foldr = $(if $3,$\
			$(let a e,$\
				$(call car,$3) $\
				$(call foldr,$1,$2,$(call cdr,$3)),$\
				$(call or,$1)),$\
			$2)

$(info $(call foldr,$$a$$e$$a,.,a b c))

# --------------------------------------------------------------------------------------
# while
# --------------------------------------------------------------------------------------
# spaces are handled as well
while = $(let string,$3,$\
			$(let cond,$1,$\
				$(let f,$2,$\
					$(if \
						$(call or,$(cond)),$\
						$(call while,$(cond),$(f),$(call or,$(f))),$\
						$(string)))))

$(info \
	$(call while,$\
		$$(findstring ||,$$(string)),$\
		$$(subst ||,|,$$(string)),$\
		this|is|||a|||||test))

all:;@:
