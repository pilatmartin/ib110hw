######1. (init, >) &rarr; ('mark', '>', RIGHT)

<pre>

| > | a | b | b | a |   |
  <b>^</b>

</pre>
---
######2. (mark, a) &rarr; ('foundA', 'X', RIGHT)

<pre>

| > | a | b | b | a |   |
      <b>^</b>

</pre>
---
######3. (foundA, b) &rarr; ('foundA', 'b', RIGHT)

<pre>

| > | X | b | b | a |   |
          <b>^</b>

</pre>
---
######4. (foundA, b) &rarr; ('foundA', 'b', RIGHT)

<pre>

| > | X | b | b | a |   |
              <b>^</b>

</pre>
---
######5. (foundA, a) &rarr; ('foundA', 'a', RIGHT)

<pre>

| > | X | b | b | a |   |
                  <b>^</b>

</pre>
---
######6. (foundA, ) &rarr; ('checkA', '', LEFT)

<pre>

| > | X | b | b | a |   |
                      <b>^</b>

</pre>
---
######7. (checkA, a) &rarr; ('back', 'X', LEFT)

<pre>

| > | X | b | b | a |   |
                  <b>^</b>

</pre>
---
######8. (back, b) &rarr; ('back', 'b', LEFT)

<pre>

| > | X | b | b | X |   |
              <b>^</b>

</pre>
---
######9. (back, b) &rarr; ('back', 'b', LEFT)

<pre>

| > | X | b | b | X |   |
          <b>^</b>

</pre>
---
######10. (back, X) &rarr; ('mark', 'X', RIGHT)

<pre>

| > | X | b | b | X |   |
      <b>^</b>

</pre>
---
######11. (mark, b) &rarr; ('foundB', 'X', RIGHT)

<pre>

| > | X | b | b | X |   |
          <b>^</b>

</pre>
---
######12. (foundB, b) &rarr; ('foundB', 'b', RIGHT)

<pre>

| > | X | X | b | X |   |
              <b>^</b>

</pre>
---
######13. (foundB, X) &rarr; ('checkB', 'X', LEFT)

<pre>

| > | X | X | b | X |   |
                  <b>^</b>

</pre>
---
######14. (checkB, b) &rarr; ('back', 'X', LEFT)

<pre>

| > | X | X | b | X |   |
              <b>^</b>

</pre>
---
######15. (back, X) &rarr; ('mark', 'X', RIGHT)

<pre>

| > | X | X | X | X |   |
          <b>^</b>

</pre>
---
######16. (mark, X) &rarr; ('accept', 'X', STAY)

<pre>

| > | X | X | X | X |   |
              <b>^</b>

</pre>
---
######16. (accept, X) &rarr; None

<pre>

| > | X | X | X | X |   |
              <b>^</b>

</pre>
---
