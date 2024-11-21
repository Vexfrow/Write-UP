# WTBF - Grehack 2024

This challenge consist of a simple file containing ascii characters, and the objective is to retrieve a password from this file

![image.png](WTBF%20-%20Grehack%202024%201439b204b34d809998d0fd1b8d722646/image.png)

The file seems very strange as it only contains the following symbols : “+”, “-”, “>”, “<”, “[”, “]”, “,” and “.”

It’s, in fact, a program written in an esoteric language called “Brainfuck”, an efficient language as it’s only use 8 characters, but also a hard-to-understand language.

Note : Brainfuck is abbreviated as “bf”, which is why the challenge is named “WTBF”, it’s a word play between “WTF” and “BF”

So the first step is to transform this program into a much more understandable language. In my case, I use [BFTOC](https://github.com/paulkaefer/bftoc), a Brainfuck to C translator. Thanks to that, I could have a readable program, and thus, start to understand what it does.

This program is composed of two part, the first one only initialized some variable and give them a value. 

Note : Brainfuck looks a lot like a Turing Machine (it is in fact Turing-complete), with a tape, a pointer, and the possibility to increment and decrement the value contained on the tape

![Capture d’écran du 2024-11-21 08-41-39.png](WTBF%20-%20Grehack%202024%201439b204b34d809998d0fd1b8d722646/Capture_dcran_du_2024-11-21_08-41-39.png)

![Capture d’écran du 2024-11-21 08-41-48.png](WTBF%20-%20Grehack%202024%201439b204b34d809998d0fd1b8d722646/Capture_dcran_du_2024-11-21_08-41-48.png)

![Capture d’écran du 2024-11-21 08-41-58.png](WTBF%20-%20Grehack%202024%201439b204b34d809998d0fd1b8d722646/Capture_dcran_du_2024-11-21_08-41-58.png)

When executed, this part gives us the following value on the tape :

```jsx
{0,42,47,48,92,42,0,120,100,54,75,148,102,145,69,199,136,45,75,148,232,114,217,214}
```

The first (from the first 0 to the second) can be interpreted as ASCII code, and it gives the following strings : 

```jsx
*/0\*
```

The second part (from the second 0 to the end) give us nothing for the moment, at least nothing readable. To understand this part, we need to understand what the second part of our program do.

![image.png](WTBF%20-%20Grehack%202024%201439b204b34d809998d0fd1b8d722646/image%201.png)

This part is a little more tricky to understand, because it takes some user input to do some computation, and because the syntax of Brainfuck is very limited.

For example, there is no “If-Else” in Brainfuck, if we want to do computation according to the value of a variable, we can only check if its value is equal to 0, using the following code 

```jsx
[]
```

That correspond to a loop that only stop if the value of the current variable is equal to 0. That what we can see on the program.   

This code do the following action.

- It start at the end of the tape (the last value initiated)
- It takes a user input, let’s say “X”
- It compute “Y = X * 3 + 1”
- Then it compares “Y” with a value on the tape
- If they’re equal, the loop break, and we can pass to another value
- If not, we’re stuck in the loop
- It end when we reach a “0”, the second one on the tape because we start by the end

So it’s easy, right ? We just need to compute X, such as “X = (Y-1)/3” and we’ll get the password.

Let’s try it with a little python script :

```jsx
tab = [214, 217, 114, 232, 148, 75, 45, 136, 199, 69, 145, 102, 148,75, 54, 100, 120]

pas = ""
for i in range(len(tab)) :
    x = (tab[i]-1)/3;
    pas += chr(int(x))

print(pas)
```

It gives us :

```jsx
GH%M1-B0!1!’
```

Which is, quite not what we are expecting for a flag, even though that the “GH” letters are present.

After some research, I found that some of the “X” value computed were not integer but float. 

So what do we do now ? We need to remind that it’s not a program written in C, but in Brainfuck, and that in Brainfuck, there is only uint value. 

This information is important because, what’s happens when we do “0 - 1” with an uint value ? It’s comes back to 255.
And because the comparison in Brainfuck use the fact that we are decrementing each variable we are comparing, we should not compute “X = (Y-1)/3”, but “X = (Y+255)/3” sometimes (when X is a float).

So we just need to alter a little bit our script

```jsx
tab = [214, 217, 114, 232, 148, 75, 45, 136, 199, 69, 145, 102, 148,75, 54, 100, 120]

pas = ""
for i in range(len(tab)) :
    x = (tab[i]-1)/3;
    
    if(round(x)!=x) :
        x = (tab[i]+255)/3;
    pas += chr(int(x))

print(pas)
```

And we finally get the flag :

```jsx
GH{M1nd-Bl0w1ng!}
```

If we use this flag in the program, the string that we found before (***/0\***) is print on the screen, confirming that we found the password.