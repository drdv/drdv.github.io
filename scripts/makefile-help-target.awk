# --------------------------------------------------------------------------
# Script I use in Makefiles as follows:
#
# ## show this help
# ##   can have multi-line description
# help:
# 	@awk -f makefile-help-target.awk $(MAKEFILE_LIST)
#
# Target is displayed in:
#   BLUE if its description starts with ##
#   RED  if its description starts with ##!
# --------------------------------------------------------------------------

BEGIN {
  # comman-line arguments (pass to awk using -v MAX_PREVIEW=...)
  MAX_PREVIEW = (MAX_PREVIEW == "" ? 15 : MAX_PREVIEW)

  BLUE = "\033[34m"
  RED = "\033[31m"
  END_COLOR = "\033[0m"
  DISPLAY_PATTERN = "%s%-" MAX_PREVIEW "s%s %s\n"

  separator = sprintf("%*s", 50, "")
  gsub(/ /, "-", separator) # gsub works inplace
  printf "%s\nAvailable targets:\n%s\n", separator, separator

  description = ""
}

# Capture the line if it is a description
/^##/ {
  if (description) {
    # handle multiple description lines
    description = description "\n" sprintf("%" MAX_PREVIEW + 2 "s", "") substr($0, 4)
  } else {
    description = $0
  }
}

# Process target
/^[a-zA-Z0-9_-]+:/ {
  if (description) {
    if (substr(description, 3, 1) == "!") {
      color = RED
      description_offset = 4
    } else {
      color = BLUE
      description_offset = 3
    }

    n = length($1) - 1 # the "-1" is to skip the :
    printf DISPLAY_PATTERN, color,                        \
        substr($1, 1, n < MAX_PREVIEW ? n : MAX_PREVIEW), \
        END_COLOR,                                        \
        substr(description, description_offset)
    description = "" # forget the previous description
  }
}
