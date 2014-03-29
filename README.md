Chinese-Wubi
============

Chinese Wubi (五笔) input method for Emacs based on `quail` package.

## How to use

Place the `chinese-wubi.el` and the `chinese-wubi-rules.el` in your
load path, and add the following in your `.emacs` file:

```lisp
(require 'chinesewubi)
(register-input-method
 "chinese-wubi" "Chinese-GB" 'quail-use-package "wubi" "wubi")
```

## TODO

1. Currently I use the table the previous author built himself, which is
   only a fraction of the wubi rules.  So I'm converting and merging the
   the wubi tables from IBus, haifeng86 and jidian86.  The resulting
   table will cover most of the rules.
2. The previous author implemented the *user add word* function, but
   I'm not sure whether it works OK, so I've got to check that.
3. Frequency adjusting if possible
4. Submit package to ELPA.

---

package originally created by
[Yuwen Dai](mailto::daiyuwen@freeshell.org) and
[William Xu](mailto:william.xwl@gmail.com).  A brief description could
be found [here](http://daiyuwen.freeshell.org/gb/wubi/wubi.html).
