######1. (init, ('>', '')) &rarr; ('copy', ('>', ''), (RIGHT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
  <b>^</b>

<b>Tape 1:</b>
|   |
  <b>^</b>

</pre>
---
######2. (copy, ('a', '')) &rarr; ('copy', ('a', 'a'), (RIGHT, RIGHT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
      <b>^</b>

<b>Tape 1:</b>
|   |
  <b>^</b>

</pre>
---
######3. (copy, ('b', '')) &rarr; ('copy', ('b', 'b'), (RIGHT, RIGHT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
          <b>^</b>

<b>Tape 1:</b>
| a |   |
      <b>^</b>

</pre>
---
######4. (copy, ('b', '')) &rarr; ('copy', ('b', 'b'), (RIGHT, RIGHT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
              <b>^</b>

<b>Tape 1:</b>
| a | b |   |
          <b>^</b>

</pre>
---
######5. (copy, ('a', '')) &rarr; ('copy', ('a', 'a'), (RIGHT, RIGHT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                  <b>^</b>

<b>Tape 1:</b>
| a | b | b |   |
              <b>^</b>

</pre>
---
######6. (copy, ('', '')) &rarr; ('goToStart', ('', ''), (LEFT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                      <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######7. (goToStart, ('a', '')) &rarr; ('goToStart', ('a', ''), (LEFT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                  <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######8. (goToStart, ('b', '')) &rarr; ('goToStart', ('b', ''), (LEFT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
              <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######9. (goToStart, ('b', '')) &rarr; ('goToStart', ('b', ''), (LEFT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
          <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######10. (goToStart, ('a', '')) &rarr; ('goToStart', ('a', ''), (LEFT, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
      <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######11. (goToStart, ('>', '')) &rarr; ('check', ('>', ''), (RIGHT, LEFT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
  <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
                  <b>^</b>

</pre>
---
######12. (check, ('a', 'a')) &rarr; ('check', ('a', 'a'), (RIGHT, LEFT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
      <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
              <b>^</b>

</pre>
---
######13. (check, ('b', 'b')) &rarr; ('check', ('b', 'b'), (RIGHT, LEFT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
          <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
          <b>^</b>

</pre>
---
######14. (check, ('b', 'b')) &rarr; ('check', ('b', 'b'), (RIGHT, LEFT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
              <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
      <b>^</b>

</pre>
---
######15. (check, ('a', 'a')) &rarr; ('check', ('a', 'a'), (RIGHT, LEFT))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                  <b>^</b>

<b>Tape 1:</b>
| a | b | b | a |   |
  <b>^</b>

</pre>
---
######16. (check, ('', '')) &rarr; ('accept', ('', ''), (STAY, STAY))
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                      <b>^</b>

<b>Tape 1:</b>
|   | a | b | b | a |   |
  <b>^</b>

</pre>
---
######16. (accept, ('', '')) &rarr; None
<pre>
<b>Tape 0:</b>
| > | a | b | b | a |   |
                      <b>^</b>

<b>Tape 1:</b>
|   | a | b | b | a |   |
  <b>^</b>

</pre>
---
