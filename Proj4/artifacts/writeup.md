Name: []

## Question 1

In the following code-snippet from `Num2Bits`, it looks like `sum_of_bits`
might be a sum of products of signals, making the subsequent constraint not
rank-1. Explain why `sum_of_bits` is actually a _linear combination_ of
signals.

```
        sum_of_bits += (2 ** i) * bits[i];
```

## Answer 1
This is a linear combination instead of a quadratic expression because (2**i) is a constant and this is equivalent in writing (bits[i] + bits[i]+....+bits[i]) (2**i) times. The laws of linear expression guides that a linear expression can be written using multiplication of variables by constants. 

## Question 2

Explain, in your own words, the meaning of the `<==` operator.

## Answer 2
The '<==' operator means that not only you are assigning the value of a signal to only be only the quadratic expressions of an operation. And you are also constraining the final signal to must equal to the result of the operation because it is much safer. However you can't use it for complex operations outside of quadratic expressions such as division or power. 


## Question 3

Suppose you're reading a `circom` program and you see the following:

```
    signal input a;
    signal input b;
    signal input c;
    (a & 1) * b === c;
```

Explain why this is invalid.

## Answer 3

This is invalid because you are using constraints with a complex operations (a&1), which is not allowed for constraints. 
