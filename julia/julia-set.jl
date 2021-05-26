import Pkg
Pkg.add("PyPlot")
using PyPlot

max_iters = 100
width = 1000
height = 1000
inf = 4
z_start = complex(0.5)

x = range(-2, stop=2, length=width)
y = range(-2, stop=2, length=height)
x = repeat(x',width,1)
y = repeat(y,1,height)

function julia(X, Y)
    z = z_start
    c = complex(X,Y)
    for i in 0:max_iters
        z = z * z + c
        if abs(z) > inf
            return i
        end
    end
    return 0
end
z = julia.(x, y)

contour(x, y, z)
show()
