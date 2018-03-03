in array x.

![][y(i) = a*x(i-1) + b*x(i) + c*x(i+1)]

is a convolution of x and [a,b,c], for example y(i) = -x(i-1) + x(i) is a differential core of [-1, 1, 0].

when N = fft.size f_x = fft(x) and f_c = fft(c) , the fft(convolution(f,c)) == N * f_x * f_c.

so in aother of view. to convolution c, is change x's frequency function f_x by multiply N * f_c.

convolution c is some kind of changing frequency function of x.

so you want to approximately change f_x, you can apply some kind of c = [..., a, b, c, ...] to do the same effect, but without really do a fft and ifft.


[y(i) = a*x(i-1) + b*x(i) + c*x(i+1)]: #math
