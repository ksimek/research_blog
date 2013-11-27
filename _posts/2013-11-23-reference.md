---
layout: post
title: "Hessian of Marginal Likelihood"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

Recall  the expression for the i-th element of the gradient of ML w.r.t. indices.

<div>
\[
\begin{align}
g'_i(x) &= \frac{1}{2} z(x)^\top K'(x) z(x) \\
        &= \frac{1}{2} z_i(x) \delta_i^\top(x) z(x) - Z'_i(x) \\
        &= f_i(x) - Z'_i(x)
\end{align}
\]
</div>

Where \\(\delta_i = k'(x_i, x_j)\\), and \\(Z'_i\\) is the derivitive of the normalization constant.

    


The goal today is to derive the second derivitive, H.  Like the first derivitive, it will have two terms,
    
    
<div>
    \[
    H = H_1 - H_2
    \]
</div>

Ultimately, we'll split the second term \\(H_2\\) into two sub-terms:

<div>
    \[
    H = H_1 - H_{2,A} - H_{2,B}
    \]
</div>

Prerequisite: \\(\frac{\partial \delta_i}{\partial x_j}\\)
-------------------------------------------------------

Recall that the elements of \\(\delta_i\\) are the partial derivatives of the kernel function w.r.t. its first input.  The second derivatives \\(\delta_i\\) will be given by the second partial derivatives of the kernel function.

<div>
\[
\begin{align}
\frac{\partial^2 k(x_i, x_j)}{\partial x_i^2} &= 
        x_j - \min(x_i, x_j)  \\
\frac{\partial^2 k(x_i, x_j)}{\partial x_i \partial x_j} &= 
        \min(x_i, x_j) 
\end{align}
\]
</div>

The derivative of the j-th element of \\(\delta_i\\) is derived below.  

<div>
\[
\begin{align}
\frac{\partial \left(\delta_i \right)_j}{\partial x_k} 
    &= \frac{\partial^2 k(x_i, x_j)}{\partial x_i \partial x_k} \\
    &= (x_j - \min(x_i, x_j))\mathbb{1}_{k = i} + \min(x_i, x_j) \mathbb{1}_{k = j} 
\end{align}
\]
</div>

Note that this handles the special cases where k = i = j and \\(k \neq i, k \neq j\\).  

We can generalizing to the full vector \\(\delta_i\\) 

<div>
\[
\begin{align}
\frac{\partial \delta_i }{\partial x_k}  &= A_{i} \mathbb{1}_{k = i}  + B_{ik}\\
A_{i} &= (x_1 - \min(x_i, x_1), \dots, x_j - \min(x_i, x_j), \dots)^\top  \\
B_{ik} &= (0, \dots, \underbrace{\min(x_i, x_k)}_\text{k-th element}, \dots, 0)^\top
\end{align}
\]
</div>

The A term handles the on-diagonal hessian terms, whereas B is included in all terms.   

First term, \\(H_1 = f_i'\\)
------------------

We use the product rule to take the derivitive of \\(f_i = z_i \delta_i \cdot  z\\).

<div>
\[
\begin{align}
\frac{\partial f_i(x)}{\partial x_j} &=
            \left ( \frac{\partial}{\partial x_j} \, z_i(x) \right ) \delta_i^\top(x) z(x)  +
            z_i(x) \left ( \frac{\partial}{\partial x_j}\delta_i^\top(x) \right ) z(x) +
            z_i(x) \, \delta_i^\top(x) \left ( \frac{\partial}{\partial x_j} z(x) \right ) \\
&=
            z_i' (x) \, \delta_i^\top(x) \, z(x)  +
            z_i(x) \, (A_{i}\mathbb{1}_{k = i} + B_{ij})^\top \, z(x) + 
            z_i(x) \, \delta_i^\top(x) \, z'(x) \\
&=
            z_i' (x) \, \delta_i^\top(x) \, z(x)  +
            \mathbb{1}_{k = i} z_i(x) \, A_{i}^\top \, z(x) + z_i(x) \, \min(x_i, x_j) \, z_j(x)  +
            z_i(x) \, \delta_i^\top(x) \, z'(x)
\end{align}
\]
</div>

where 

<div>
\[
\begin{align}
z' = z'_{(j)} = \frac{\partial z(x)}{\partial x_j} &= \frac{\partial}{\partial x_j} S^\top U^{-1}(x) S y \\
        &= S V' S^\top y \\
        &= S^\top U^{-1} U' U^{-1} S y \\
        &= (S^\top U^{-1} S) K' (S^\top U^{-1} S) y
\end{align}
\]
</div>


Our goal is the generalize this to a single expression for the entire hessian matrix.
Note that when \\(i \neq j\\), the third term disappears, so that term will become a diagonal matrix in the hessian expression.
Let \\(\mathcal{Z}' \\) be the jacobian of \\(z\\).  We can express the hessian asWe can express the hessian as

<div>
\[
H_1 = \mathcal{Z}' \odot \left[ \Delta \, z \, (1 \, 1 \, ...) \right] + M \odot \left(z z^\top \right ) + \text{diag}\left\{ z(x) \odot \Delta' z(x) \right\} +  \left[ z \, (1 \, 1 \, ...) \right] \odot \left[ \Delta \, \mathcal{Z}' \right]
\]
</div>

where \\(M\\) is a matrix whose elements \\(m_{ij} = \min(x_i, x_j)\\), 
      
\\(\Delta\\) is a matrix whose rows are composed of the \\(\delta_i\\) vectors,

\\(\Delta'\\) is the matrix whose i-th row is the vector \\(A_i\\),

\\(\odot\\) is the Hadamard matrix product,

and diag() is an operator that converts a vector into a diagonal matrix.
      

Second term, \\(Z_i''(x) = H\_{2,A} + H\_{2,B} \\)
------------------------

Below are the expressions for the zeroth, first, and second derivitives of Z;

<div>
\[
\begin{align}
Z &= 0.5 \log(\det(S K S^\top + I)) \\
\frac{\partial Z}{\partial x_i} &= 0.5 \text{Tr} \left[ U^{-1} U' \right] \\
\frac{\partial^2 Z}{\partial x_i \partial x_j} &= 0.5 \text{Tr} \left[ \frac{\partial U^{-1}}{\partial x_j} U' + U^{-1} \frac{\partial U'}{\partial x_j} \right] \\
        &= 0.5 \text{Tr} \left[ V'_{(j)} U'_{(i)} + U^{-1} U''_{(ij)} \right] \\
        &= 0.5 \left \{ \text{Tr} \left[ V'_{(j)} U'_{(i)} \right] + \text{Tr} \left[ U^{-1} U''_{(ij)} \right] \right\} \\
        &= 0.5 \text{Tr}[A] +0.5 \text{Tr}[B]
\end{align}
\]
</div>

Where

<div>
\[
        A =  V'_{(j)} U'_{(i)} \\  
        B = U^{-1} U''_{(ij)} 
\]
</div>

These two terms correspond to the elements to the two hessian terms, \\(H\_{2,A}\\) and \\(H\_{2,B}\\).

We'll begin by finding \\(Tr[A]\\) and \\(H_{2,A}\\).


Observe that we can rewrite \\(U_{(i)}'\\) as 

<div>
\[
\begin{align}
U'_{(i)} &= S  K'  S^\top \\
U'_{(i)} &= S  (B + B^\top)  S^\top \\
\end{align}
\]
</div>

where B is the sparse matrix,

<div>
\[
\begin{align}
B = \left( \begin{array}{ccccc}
        \mathbf{0} & \cdots & \delta_i & \cdots & \mathbf{0}
    \end{array}\right)
\end{align}.
\]
</div>

We can exploit this sparsity to further expand \\(U'\\) to

<div>
\[
\begin{align}
U'_{(i)} &= \left(S \, \delta_i \right) S_i^\top  + S_i \left( S \, \delta_i \right)^\top \\
         &= C_{(i)} + C_{(i)}^\top
\end{align}
\]

where \(C_{(i)} = S \, \delta_i \, S_i^\top \).
</div>

We can use this identity to expand \\(\text{Tr}[A]\\).

<div>
\[
\begin{align}
    \text{Tr}[A] &= \text{Tr}[V'_{(j)} U'_{(i)}] \\
          &= \text{Tr}[-U^{-1} U'_{(j)}U^{-1} U'_{(i)}] \\
          &= -\text{Tr}[U^{-1} \left( C_{(j)} + C_{(j)}^\top \right) U^{-1} \left( C_{(i)} + C_{(i)}^\top \right) ] \\
          &= -\text{Tr}[U^{-1} \left( C_{(j)} + C_{(j)}^\top \right) U^{-1} \left( C_{(i)} + C_{(i)}^\top \right) ] \\
          &= -\text{Tr}[\left( U^{-1}  C_{(j)} + U^{-1}C_{(j)}^\top \right) \left(U^{-1}  C_{(i)} + U^{-1}C_{(i)}^\top \right) ] \\
          &= -\text{Tr}\left [U^{-1}  C_{(j)} U^{-1}C_{(i)} + U^{-1}  C_{(j)} U^{-1}C_{(i)}^\top + U^{-1}C_{(j)}^\top U^{-1}C_{(i)} + U^{-1}C_{(j)}^\top U^{-1}C_{(i)} ^\top\right] \\
          &= -2 \text{Tr}\left [U^{-1}  C_{(j)} U^{-1}C_{(i)}\right]  - 2 \text{Tr}\left[U^{-1} C_{(j)} U^{-1}C_{(i)}^\top \right ] \\
          &= -2 \text{Tr}\left [U^{-1} \left( S \delta_j S_j^\top \right) U^{-1} \left ( S \delta_i S_i^\top \right)\right]  - 2 \text{Tr}\left[U^{-1} \left( S \delta_j S_j^\top \right) U^{-1}\left( S_i \delta_i^\top S^\top \right) \right ] \\
          &= -2 \text{Tr}\left [S_i^\top U^{-1} S \delta_j S_j^\top U^{-1} S \delta_i \right]  - 2 \text{Tr}\left[ \delta_i^\top S^\top U^{-1} S \delta_j S_j^\top U^{-1} S_i \right ] \\

\end{align}
\]

The last identity exploits the fact that Traces are invariant under cyclic permutations.  Note that both expressions inside the trace operator are scalar products, which makes the trace operator redundant.  

\[
\begin{align}
    \text{Tr}[A]
          &= -2 S_i^\top U^{-1} S \delta_j S_j^\top U^{-1} S \delta_i  - 2  \delta_i^\top S^\top U^{-1} S \delta_j S_j^\top U^{-1} S_i \\
          &= -2 \left( S_i^\top U^{-1} S \delta_j \right) \left(S_j^\top U^{-1} S \delta_i \right)  - 2  \left(\delta_i^\top S^\top U^{-1} S \delta_j \right) \left( S_j^\top U^{-1} S_i \right) \\
\end{align}
\]

Here, we've regrouped the dot-products in each term to be a product of two dot-products.  We can generalize this for the full hessian as follows:

\[
\begin{align}
    H_{2,A} &= -\left( S^\top U^{-1} S \Delta^\top \right)^\top \odot \left( S^\top U^{-1} S \Delta^\top \right)  - \left(\Delta S^\top U^{-1} S \Delta^\top\right) \odot \left(S^\top U^{-1} S \right) 
\end{align}
\]

</div>

Next is the second term, \\(\text{Tr}[B]\\).  

First lets derive \\(U''\\).

<div>
\begin{align}
U''_{(ij)} = \frac{\partial U_{(i)}'}{\partial x_j} &= 
            \frac{\partial}{\partial x_j} \left \{ 
            \left(S \, \delta_i \right) S_i^\top  +
            S_i \left( S \, \delta_i \right)^\top 
            \right \} \\
            &= \left(S \, \delta'_{(ij)} \right) S_i^\top  +
            S_i \left( S \, \delta'_{(ij)} \right)^\top  \\
            &= S \, 
            \left( \begin{array}{c} 0 \\ \cdots \\ \min(x_i, x_j) \\ \cdots \\ 0 \end{array}\right)
                    S_i^\top  + ... \\
            &= S_j \min(x_i, x_j) S_i^\top + S_i \min(x_i, x_j) S_j^\top \\
            &= \min(x_i, x_j) \left( S_i S_j^\top + S_j  S_i^\top \right)
\end{align}
</div>

Now we can derive \\(\text{Tr}[B]\\).
<div>
\[
\begin{align}
    \text{Tr}[B] &= \text{Tr}[U^{-1} U''_{(ij)}] \\
            &= \text{Tr}[U^{-1} \min(x_i, x_j) \left( S_i S_j^\top + S_j S_i^\top \right)] \\
            &= \min(x_i, x_j) \text{Tr}\left [ U^{-1} S_i  S_j^\top \right ] + \min(x_i, x_j) \text{Tr}\left [ U^{-1} S_j  S_i^\top \right ] \\
            &= \min(x_i, x_j) \left( S_j^\top U^{-1} S_i \right)  + ...  & \text{(Second term is the transpose of the first; is equivalent)}\\
            &= 2 \min(x_i, x_j) \left( S_j^\top U^{-1} S_i \right) \\
\end{align}
\]

</div>

This is for a single term of the Hessian.  We can rewrite it to compute the entire Hessian using matrix arithmetic:


<div>
\[
    H_{2,B} = M \odot S^\top U^{-1} S
\]
</div>

Here, M is defined as, \\(m_{ij} = \min(x_i, x_j)\\).  

We can put these three expresssions together to get the full Hessian matrix:

<div>
\[
 H = Z' \odot \left[ \Delta \, z \, (1 \, 1 \, ...) \right] + A \odot \left(z z^\top \right ) + \left[ z \, (1 \, 1 \, ...) \right] \odot \left[ \Delta \, Z' \right]
    +\left( S^\top U^{-1} S \Delta^\top \right)^\top \odot \left( S^\top U^{-1} S \Delta^\top \right)  - \left(\Delta S^\top U^{-1} S \Delta^\top\right) \odot \left(S^\top U^{-1} S \right)
    -  M \odot S^\top U^{-1} S
\]
</div>
